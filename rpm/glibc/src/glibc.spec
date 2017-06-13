%define scl devtoolset-4
%global scl_prefix devtoolset-4
%global MPI_HOME %{_libdir}

%{?scl:%scl_package glibc}
%{!?scl:
 %global pkg_name %{name}
 %global _root_prefix %{_prefix}
 %global _root_datadir %{_datadir}
 %global _root_bindir %{_bindir}
}

%define _unpackaged_files_terminate_build 0
%define glibcsrcdir  glibc-2.25-258-g25e39b4
%define glibcversion 2.25.90
%define glibcrelease 2%{?dist}
# Pre-release tarballs are pulled in from git using a command that is
# effectively:
#
# git archive HEAD --format=tar --prefix=$(git describe --match 'glibc-*')/ \
#	> $(git describe --match 'glibc-*').tar
# gzip -9 $(git describe --match 'glibc-*').tar
#
# glibc_release_url is only defined when we have a release tarball.
%{lua: if not string.match(rpm.expand("%glibcversion"), "%.*.90$") then
  rpm.define("glibc_release_url http://ftp.gnu.org/gnu/glibc/") end}
##############################################################################
# We support hte following options:
# --with/--without,
# * testsuite - Running the testsuite.
# * benchtests - Running and building benchmark subpackage.
# * bootstrap - Bootstrapping the package.
# * werror - Build with -Werror
# * docs - Build with documentation and the required dependencies.
# * valgrind - Run smoke tests with valgrind to verify dynamic loader.
#
# You must always run the testsuite for production builds.
# Default: Always run the testsuite.
%bcond_without testsuite
# Default: Always build the benchtests.
%bcond_without benchtests
# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Enable using -Werror
%bcond_without werror
# Default: Always build documentation.
%bcond_without docs
# Default: Always run valgrind tests
%bcond_without valgrind

# Run a valgrind smoke test to ensure that the release is compatible and
# doesn't any new feature that might cause valgrind to abort.
%if %{with valgrind}
%ifarch s390 ppc64 ppc64p7 %{mips}
# There is no valgrind support for 31-bit s390, nor for MIPS.
# The valgrind test does not work on ppc64, ppc64p7 (bug 1273103).
%undefine with_valgrind
%endif
%endif
%if %{with werror}
%ifarch s390 s390x
# The s390 and s390x builds are not -Werror clean yet.  For s390, the
# latest problem may be due to questionable code in test-string.h
# (upstream bug 19261, rhbz#1283184).
%undefine with_werror
%endif
%endif
%if %{with bootstrap}
# Disable benchtests, -Werror, docs, and valgrind if we're bootstrapping
%undefine with_benchtests
%undefine with_werror
%undefine with_docs
%undefine with_valgrind
%endif
##############################################################################
# Auxiliary arches are those arches that can be built in addition
# to the core supported arches. You either install an auxarch or
# you install the base arch, not both. You would do this in order
# to provide a more optimized version of the package for your arch.
%define auxarches athlon alphaev6
##############################################################################
# Enable lock elision support for these architectures
#
# At the moment lock elision is disabled on x86_64 until there's a CPU that
# would actually benefit from enabling it.  Intel released a microcode update
# to disable HLE and RTM at boot and the Fedora kernel now applies it early
# enough that keeping lock elision enabled should be harmless, but we have
# disabled it anyway as a conservative measure.
%define lock_elision_arches s390 s390x
##############################################################################
# We build a special package for Xen that includes TLS support with
# no negative segment offsets for use with Xen guests. This is
# purely an optimization for increased performance on those arches.
%define xenarches i686 athlon
%ifarch %{xenarches}
%define buildxen 1
%define xenpackage 0
%else
%define buildxen 0
%define xenpackage 0
%endif
##############################################################################
# We support only 64-bit POWER with the following runtimes:
# 64-bit BE:
# - Power 620 / 970 ISA (default runtime, compatile with POWER4 and newer)
#	- Provided for the large number of PowerPC G5 users.
#	- IFUNC support provides optimized core routines for POWER6,
#	  POWER7, and POWER8 transparently (if not using specific runtimes
#	  below)
# - POWER6 (has power6x symlink to power6, enabled via AT_PLATFORM)
#	- Legacy for old systems. Should be deprecated at some point soon.
# - POWER7 (enabled via AT_PLATFORM)
#	- Existing deployments.
# - POWER8 (enabled via AT_PLATFORM)
#	- Latest generation.
# 64-bit LE:
# - POWER8 LE (default)
#	- Latest generation.
#
# No 32-bit POWER support is provided.
#
# There are currently no plans for POWER9 enablement, but as hardware and
# upstream support become available this will be reviewed.
#
%ifarch ppc64
# Build the additional runtimes for 64-bit BE POWER.
%define buildpower6 1
%define buildpower7 1
%define buildpower8 1
%else
# No additional runtimes for ppc64le or ppc64p7, just the default.
%define buildpower6 0
%define buildpower7 0
%define buildpower8 0
%endif

##############################################################################
# Any architecture/kernel combination that supports running 32-bit and 64-bit
# code in userspace is considered a biarch arch.
%define biarcharches %{ix86} x86_64 %{power64} s390 s390x
##############################################################################
# If the debug information is split into two packages, the core debuginfo
# pacakge and the common debuginfo package then the arch should be listed
# here. If the arch is not listed here then a single core debuginfo package
# will be created for the architecture.
%define debuginfocommonarches %{biarcharches} alpha alphaev6
##############################################################################
# If the architecture has multiarch support in glibc then it should be listed
# here to enable support in the build. Multiarch support is a single library
# with implementations of certain functions for multiple architectures. The
# most optimal function is selected at runtime based on the hardware that is
# detected by glibc. The underlying support for function selection and
# execution is provided by STT_GNU_IFUNC.
%define multiarcharches %{power64} %{ix86} x86_64 %{sparc}
##############################################################################
# Add -s for a less verbose build output.
%define silentrules PARALLELMFLAGS=
##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: %{?scl_prefix}glibc
Version: %{glibcversion}
Release: %{glibcrelease}
# GPLv2+ is used in a bunch of programs, LGPLv2+ is used for libraries.
# Things that are linked directly into dynamically linked programs
# and shared libraries (e.g. crt files, lib*_nonshared.a) have an additional
# exception which allows linking it into any kind of programs or shared
# libraries without restrictions.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System Environment/Libraries
URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.gz
Source1: build-locale-archive.c
Source2: glibc_post_upgrade.c
Source4: nscd.conf
Source7: nsswitch.conf
Source8: power6emul.c
Source9: bench.mk
Source10: glibc-bench-compare
# A copt of localedata/SUPPORTED in the Source0 tarball.  The
# SUPPORTED file is used below to generate the list of locale
# packages.  See the language_list macro definition.
Source11: SUPPORTED

##############################################################################
# Start of glibc patches
##############################################################################
# 0000-0999 for patches which are unlikely to ever go upstream or which
# have not been analyzed to see if they ought to go upstream yet.
#
# 1000-2000 for patches that are already upstream.
#
# 2000-3000 for patches that are awaiting upstream approval
#
# Yes, I realize this means some gratutious changes as patches to from
# one bucket to another, but I find this scheme makes it easier to track
# the upstream divergence and patches needing approval.
#
# Note that we can still apply the patches in any order we see fit, so
# the changes from one bucket to another won't necessarily result in needing
# to twiddle the patch because of dependencies on prior patches and the like.


##############################################################################
#
# Patches that are unlikely to go upstream or not yet analyzed.
#
##############################################################################

# Configuration twiddle, not sure there's a good case to get upstream to
# change this.
Patch0001: glibc-fedora-nscd.patch

Patch0003: glibc-fedora-ldd.patch

Patch0004: glibc-fedora-ppc-unwind.patch

# Build info files in the source tree, then move to the build
# tree so that they're identical for multilib builds
Patch0005: glibc-rh825061.patch

# Horrible hack, never to be upstreamed.  Can go away once the world
# has been rebuilt to use the new ld.so path.
Patch0006: glibc-arm-hardfloat-3.patch

# Needs to be sent upstream
Patch0009: glibc-fedora-include-bits-ldbl.patch

# All these were from the glibc-fedora.patch mega-patch and need another
# round of reviewing.  Ideally they'll either be submitted upstream or
# dropped.
Patch0012: glibc-fedora-linux-tcsetattr.patch
Patch0014: glibc-fedora-nptl-linklibc.patch
Patch0015: glibc-fedora-localedef.patch
Patch0016: glibc-fedora-i386-tls-direct-seg-refs.patch
Patch0019: glibc-fedora-nis-rh188246.patch
Patch0020: glibc-fedora-manual-dircategory.patch
Patch0024: glibc-fedora-locarchive.patch
Patch0025: glibc-fedora-streams-rh436349.patch
Patch0028: glibc-fedora-localedata-rh61908.patch
Patch0031: glibc-fedora-__libc_multiple_libcs.patch
Patch0033: glibc-fedora-elf-ORIGIN.patch

# Needs to be sent upstream.
# Support mangling and demangling null pointers.
Patch0037: glibc-rh952799.patch

# ARM: Accept that some objects marked hard ABI are now not because of a
#      binutils bug.
Patch0044: glibc-rh1009145.patch

# Allow applications to call pthread_atfork without libpthread.so.
Patch0046: glibc-rh1013801.patch

Patch0047: glibc-nscd-sysconfig.patch

# confstr _CS_PATH should only return /usr/bin on Fedora since /bin is just a
# symlink to it.
Patch0053: glibc-cs-path.patch

# Add C.UTF-8 locale into /usr/lib/locale/
Patch0059: glibc-c-utf8-locale.patch

# Build libcrypt twice, with and without NSS.
Patch0060: glibc-rh1324623.patch

# Fix -Wstrict-overflow issues with gcc 7.0.
Patch0061: glibc-gcc-strict-overflow.patch

##############################################################################
#
# Patches from upstream
#
##############################################################################

##############################################################################
#
# Patches submitted, but not yet approved upstream.
#
##############################################################################
#
# Each should be associated with a BZ.
# Obviously we're not there right now, but that's the goal
#

# http://sourceware.org/ml/libc-alpha/2012-12/msg00103.html
Patch2007: glibc-rh697421.patch

Patch2013: glibc-rh741105.patch

# Upstream BZ 14247
Patch2023: glibc-rh827510.patch

# Upstream BZ 14185
Patch2027: glibc-rh819430.patch

Patch2031: glibc-rh1070416.patch

Patch2033: glibc-aarch64-tls-fixes.patch
Patch2034: glibc-aarch64-workaround-nzcv-clobber-in-tlsdesc.patch

Patch2036: glibc-gcc-PR69537.patch

# extend_alloca removal, BZ 18023
Patch2037: glibc-rh1315108.patch

# sln implemented by ldconfig, to conserve disk space.
Patch2112: glibc-rh1315476-2.patch

##############################################################################
# End of glibc patches.
##############################################################################

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: glibc-profile < 2.4
Provides: ldconfig

# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# This is a short term need until everything is rebuilt in the ARM world
# to use the new dynamic linker path
%ifarch armv7hl armv7hnl
Provides: ld-linux.so.3
Provides: ld-linux.so.3(GLIBC_2.4)
%endif

Requires: %{?scl_prefix}glibc-common = %{version}-%{release}

%if %{without bootstrap}
# Use the NSS-based cryptographic libraries by default.
Requires: %{?scl_prefix}libcrypt-nss%{_isa}
%endif

Requires(pre): basesystem

# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
BuildRequires: gd-devel libpng-devel zlib-devel
%if %{with docs}
# Removing texinfo will cause check-safety.sh test to fail because it seems to
# trigger documentation generation based on dependencies.  We need to fix this
# upstream in some way that doesn't depend on generating docs to validate the
# texinfo.  I expect it's simply the wrong dependency for that target.
BuildRequires: texinfo
%endif
%if %{without bootstrap}
BuildRequires: libselinux-devel >= 1.33.4-3
BuildRequires: nss-devel
%endif
BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
# We need procps-ng (/bin/ps), util-linux (/bin/kill), and gawk (/bin/awk),
# but it is more flexible to require the actual programs and let rpm infer
# the packages. However, until bug 1259054 is widely fixed we avoid the
# following:
# BuildRequires: /bin/ps, /bin/kill, /bin/awk
# And use instead (which should be reverted some time in the future):
BuildRequires: procps-ng, util-linux, gawk
BuildRequires: systemtap-sdt-devel

%if %{with valgrind}
# Require valgrind for smoke testing the dynamic loader to make sure we
# have not broken valgrind.
BuildRequires: /usr/bin/valgrind
%endif

# We use systemd rpm macros for nscd
BuildRequires: systemd

# We use python for the microbenchmarks
BuildRequires: python

# This is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: %{?scl_prefix}gcc >= 5.0
%define enablekernel 2.6.32
Conflicts: kernel < %{enablekernel}
%define target %{_target_cpu}-redhat-linux
%ifarch %{arm}
%define target %{_target_cpu}-redhat-linuxeabi
%endif
%ifarch %{power64}
%ifarch ppc64le
%define target ppc64le-redhat-linux
%else
%define target ppc64-redhat-linux
%endif
%endif

%ifarch %{multiarcharches}
# Need STT_IFUNC support
%ifarch %{power64}
BuildRequires: %{?scl_prefix}binutils >= 2.20.51.0.2
Conflicts: %{?scl_prefix}binutils < 2.20.51.0.2
%else
%ifarch s390 s390x
# Needed for STT_GNU_IFUNC support for s390/390x
BuildRequires: %{?scl_prefix}binutils >= 2.23.52.0.1-8
Conflicts: %{?scl_prefix}binutils < 2.23.52.0.1-8
%else
# Default to this version
BuildRequires: %{?scl_prefix}binutils >= 2.19.51.0.10
Conflicts: %{?scl_prefix}binutils < 2.19.51.0.10
%endif
%endif
# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2
%else
# Need AS_NEEDED directive
# Need --hash-style=* support
BuildRequires: %{?scl_prefix}binutils >= 2.17.50.0.2-5
%endif

BuildRequires: %{?scl_prefix}gcc >= 5.0
%ifarch s390 s390x
BuildRequires: %{?scl_prefix}gcc >= 4.1.0-0.17
%endif
%if 0%{?_enable_debug_packages}
BuildRequires: elfutils >= 0.72
BuildRequires: rpm >= 4.2-0.56
%endif

%if %{without boostrap}
%if %{with testsuite}
# The testsuite builds static C++ binaries that require a C++ compiler,
# static C++ runtime from libstdc++-static, and lastly static glibc.
BuildRequires: %{?scl_prefix}gcc-c++
BuildRequires: libstdc++-static
# A configure check tests for the ability to create static C++ binaries
# before glibc is built and therefore we need a glibc-static for that
# check to pass even if we aren't going to use any of those objects to
# build the tests.
BuildRequires: glibc-static
%endif
%endif

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1

# For language packs we have glibc require a virtual dependency
# "glibc-langpack" wich gives us at least one installed langpack.
# If no langpack providing 'glibc-langpack' was installed you'd
# get all of them, and that would make the transition from a
# system without langpacks smoother (you'd get all the locales
# installed). You would then trim that list, and the trimmed list
# is preserved. One problem is you can't have "no" locales installed,
# in that case we offer a "glibc-minimal-langpack" sub-pakcage for
# this purpose.
Requires: %{?scl_prefix}glibc-langpack = %{version}-%{release}
Requires: %{?scl_prefix}glibc-all-langpacks = %{version}-%{release}

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

##############################################################################
# glibc "xen" sub-package
##############################################################################
%if %{xenpackage}
%package xen
Summary: The GNU libc libraries (optimized for running under Xen)
Group: System Environment/Libraries
Requires: glibc = %{version}-%{release}, glibc-utils = %{version}-%{release}

%description xen
The standard glibc package is optimized for native kernels and does not
perform as well under the Xen hypervisor.  This package provides alternative
library binaries that will be selected instead when running under Xen.

Install glibc-xen if you might run your system under the Xen hypervisor.
%endif

######################################################################
# crypt subpackages
######################################################################

%package -n %{?scl_prefix}libcrypt
Summary: Password hashing library (non-NSS version)
Group: System Environment/Libraries
Requires: %{name}%{_isa} = %{version}-%{release}
Provides: %{?scl_prefix}libcrypt%{_isa}
Conflicts: %{?scl_prefix}libcrypt-nss

%description -n %{?scl_prefix}libcrypt
This package provides the crypt function, which implements password
hashing.  The glibc implementation of the cryptographic algorithms is
used by this package.

%post -n %{?scl_prefix}libcrypt
/sbin/ldconfig

%postun -n %{?scl_prefix}libcrypt
/sbin/ldconfig

%if %{without bootstrap}
%package -n %{?scl_prefix}libcrypt-nss
Summary: Password hashing library (NSS version)
Group: System Environment/Libraries
Requires: %{name}%{_isa} = %{version}-%{release}
Provides: %{?scl_prefix}libcrypt%{_isa}
Conflicts: %{?scl_prefix}libcrypt

%description -n %{?scl_prefix}libcrypt-nss
This package provides the crypt function, which implements password
hashing.  The cryptographic algorithm implementations are provided by
the low-level NSS libraries.

%post -n %{?scl_prefix}libcrypt-nss
/sbin/ldconfig

%postun -n %{?scl_prefix}libcrypt-nss
/sbin/ldconfig
%endif

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Group: Development/Libraries
Requires(pre): /sbin/install-info
Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: libgcc%{_isa}
Requires: %{?scl_prefix}libcrypt%{_isa}

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "static" sub-package
##############################################################################
%package static
Summary: C library static libraries for -static linking.
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

##############################################################################
# glibc "headers" sub-package
# - The headers package includes all common headers that are shared amongst
#   the multilib builds. It was created to reduce the download size, and
#   thus avoid downloading one header package per multilib. The package is
#   identical both in content and file list, any difference is an error.
#   Files like gnu/stubs.h which have gnu/stubs-32.h (i686) and gnu/stubs-64.h
#   are included in glibc-headers, but the -32 and -64 files are in their
#   respective i686 and x86_64 devel packages.
##############################################################################
%package headers
Summary: Header files for development using standard C libraries.
Group: Development/Libraries
Provides: %{name}-headers(%{_target_cpu})
%ifarch x86_64
# If both -m32 and -m64 is to be supported on AMD64, x86_64 glibc-headers
# have to be installed, not i586 ones.
Obsoletes: %{name}-headers(i586)
Obsoletes: %{name}-headers(i686)
%endif
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
BuildRequires: kernel-headers >= 2.6.22

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "common" sub-package
##############################################################################
%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a
Group: System Environment/Base

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

%package locale-source
Summary: The sources for the locales
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Group: System Environment/Base

%description locale-source
The sources for all locales provided in the language packs.
If you are building custom locales you will most likely use
these sources as the basis for your new locale.

# The glibc-all-langpacks provides the virtual glibc-langpack,
# and thus satisfies glibc's requirement for installed locales.
# Users can add one more other langauge packs and then eventually
# uninstall all-langpacks to save space.
%package all-langpacks
Summary: All language packs for %{name}.
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-langpack = %{version}-%{release}
%description all-langpacks

# No %files, this is an empty pacakge. The C/POSIX and
# C.UTF-8 files are already installed by glibc. We create
# minimal-langpack because the virtual provide of
# glibc-langpack needs at least one package installed
# to satisfy it. Given that no-locales installed is a valid
# use case we support it here with this package.
%package minimal-langpack
Summary: Minimal language packs for %{name}.
Group: System Environment/Base
Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description minimal-langpack
This is a Meta package that is used to install minimal language packs.
This package ensures you can use C, POSIX, or C.UTF-8 locales, but
nothing else. It is designed for assembling a minimal system.
%ifnarch %{auxarches}
%files minimal-langpack
%endif

##############################################################################
# glibc "nscd" sub-package
##############################################################################
%package -n %{?scl_prefix}nscd
Summary: A Name Service Caching Daemon (nscd).
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%if %{without bootstrap}
Requires: libselinux >= 1.17.10-1
%endif
Requires: audit-libs >= 1.1.3
Requires(pre): /usr/sbin/useradd, coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd, /usr/sbin/userdel

%description -n %{?scl_prefix}nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS+, and may help with DNS as well.

##############################################################################
# Subpackages for NSS modules except nss_files, nss_dns
##############################################################################

%package -n %{?scl_prefix}nss_db
Summary: Name Service Switch (NSS) module using hash-indexed files
Group: System Environment/Base
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n %{?scl_prefix}nss_db
The nss_db Name Service Switch module uses hash-indexed files in %{_localstatedir}/db
to speed up user, group, service, host name, and other NSS-based lookups.

%package -n %{?scl_prefix}nss_nis
Summary: Name Service Switch (NSS) module using NIS
Group: System Environment/Base
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n %{?scl_prefix}nss_nis
The nss_nis, nss_nisplus, and nss_compat Name Service Switch modules
uses the Network Information System (NIS) to obtain user, group, host
name, and other data.

%package -n %{?scl_prefix}nss_hesiod
Summary: Name Service Switch (NSS) module using Hesiod
Group: System Environment/Base
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n %{?scl_prefix}nss_hesiod
The nss_hesiod Name Service Switch module uses the Domain Name System
(DNS) as a source for user, group, and service information, following
the Hesiod convention of Project Athena.

%package nss-devel
Summary: Development files for directly linking NSS service modules
Group: Development/Libraries
Requires: %{?scl_prefix}nss_db%{_isa} = %{version}-%{release}
Requires: %{?scl_prefix}nss_nis%{_isa} = %{version}-%{release}
Requires: %{?scl_prefix}nss_hesiod%{_isa} = %{version}-%{release}

%description nss-devel
The glibc-nss-devel package contains the object files necessary to
compile applications and libraries which directly link against NSS
modules supplied by glibc.

This is a rare and special use case; regular development has to use
the glibc-devel package instead.

##############################################################################
# glibc "utils" sub-package
##############################################################################
%package utils
Summary: Development utilities from GNU C library
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

##############################################################################
# glibc core "debuginfo" sub-package
##############################################################################
%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%global __debug_package 1

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no
%ifarch %{debuginfocommonarches}
Requires: %{?scl_prefix}glibc-debuginfo-common = %{version}-%{release}
%else
%ifarch %{ix86} %{sparc}
Obsoletes: %{?scl_prefix}glibc-debuginfo-common
%endif
%endif

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

This package also contains static standard C libraries with
debugging information.  You need this only if you want to step into
C library routines during debugging programs statically linked against
one or more of the standard C libraries.
To use this debugging information, you need to link binaries
with -static -L%{_prefix}/lib/debug%{_libdir} compiler options.

##############################################################################
# glibc common "debuginfo-common" sub-package
##############################################################################
%ifarch %{debuginfocommonarches}

%package debuginfo-common
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no

%description debuginfo-common
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%endif # %{debuginfocommonarches}
%endif # 0%{?_enable_debug_packages}

%if %{with benchtests}
%package benchtests
Summary: Benchmarking binaries and scripts for %{name}
Group: Development/Debug
%description benchtests
This package provides built benchmark binaries and scripts to run
microbenchmark tests on the system.
%endif

##############################################################################
# Prepare for the build.
##############################################################################
%prep
%setup -q -n %{glibcsrcdir}

# Patch order matters.
%patch0001 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch2007 -p1
%patch0009 -p1
%patch0012 -p1
%patch2013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0019 -p1
%patch0020 -p1
%patch2023 -p1
%patch0024 -p1
%patch0025 -p1
%patch2027 -p1
%patch0028 -p1
%patch0031 -p1
%patch0033 -p1
%patch0037 -p1
%patch0044 -p1
%patch0046 -p1
%patch2031 -p1
%patch0047 -p1
%patch2033 -p1
%patch2034 -p1
%patch0053 -p1
%patch0059 -p1
%patch0060 -p1
%patch2036 -p1
%patch2037 -p1
%patch2112 -p1
%patch0061 -p1

##############################################################################
# %%prep - Additional prep required...
##############################################################################
# Make benchmark scripts executable
chmod +x benchtests/scripts/*.py scripts/pylint

# Remove all files generated from patching.
find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
touch locale/programs/*-kw.h

# Verify that our copy of localedata/SUPPORTED matches the glibc
# version.
#
# The separate file copy is used by the language_list macro above.
# Patches or new upstream versions may change the list of locales,
# which changes the set of langpacks we need to build.  Verify the
# differences then update the copy of SUPPORTED.  This approach has
# two purposes: (a) avoid spurious changes to the set of langpacks,
# and (b) the language_list macro can use a fully patched-up version
# of the localedata/SUPPORTED file.
diff -u %{SOURCE11} localedata/SUPPORTED

##############################################################################
# Build glibc...
##############################################################################
%build
# Log system information
uname -a
cat /proc/cpuinfo
cat /proc/meminfo
df

# We build using the native system compilers.
GCC=gcc
GXX=g++

##############################################################################
# %%build - x86 options.
##############################################################################
# On x86 we build for the specific target cpu rpm is using.
%ifarch %{ix86}
BuildFlags="-march=%{_target_cpu} -mtune=generic"
%endif
# We don't support building for i386. The generic i386 architecture lacks the
# atomic primitives required for NPTL support. However, when a user asks to
# build for i386 we interpret that as "for whatever works on x86" and we
# select i686. Thus we treat i386 as an alias for i686.
%ifarch i386 i686
BuildFlags="-march=i686 -mtune=generic"
%endif
%ifarch i486 i586
BuildFlags="$BuildFlags -mno-tls-direct-seg-refs"
%endif
%ifarch x86_64
BuildFlags="-mtune=generic"
%endif

##############################################################################
# %%build - s390 options.
##############################################################################
%ifarch s390 s390x
# The default is to turne for z13 (newer hardware), but build for zEC12.
BuildFlags="-march=zEC12 -mtune=z13"
%endif

##############################################################################
# %%build - SPARC options.
##############################################################################
%ifarch sparc
BuildFlags="-fcall-used-g6"
GCC="$GCC -m32"
GXX="$GXX -m32"
%endif
%ifarch sparcv9
BuildFlags="-mcpu=ultrasparc -fcall-used-g6"
GCC="$GCC -m32"
GXX="$GXX -m32"
%endif
%ifarch sparcv9v
BuildFlags="-mcpu=niagara -fcall-used-g6"
GCC="$GCC -m32"
GXX="$GXX -m32"
%endif
%ifarch sparc64
BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g6"
GCC="$GCC -m64"
GXX="$GXX -m64"
%endif
%ifarch sparc64v
BuildFlags="-mcpu=niagara -mvis -fcall-used-g6"
GCC="$GCC -m64"
GXX="$GXX -m64"
%endif

##############################################################################
# %%build - POWER options.
##############################################################################
%ifarch %{power64}
BuildFlags=""
GCC="$GCC -m64"
GXX="$GXX -m64"
%ifarch ppc64p7
GCC="$GCC -mcpu=power7 -mtune=power7"
GXX="$GXX -mcpu=power7 -mtune=power7"
core_with_options="--with-cpu=power7"
%endif
%ifarch ppc64le
GCC="$GCC -mcpu=power8 -mtune=power8"
GXX="$GXX -mcpu=power8 -mtune=power8"
core_with_options="--with-cpu=power8"
%endif
%endif

##############################################################################
# %%build - MIPS options.
##############################################################################
%ifarch mips mipsel
BuildFlags="-march=mips32r2 -mfpxx"
%endif
%ifarch mips64 mips64el
# Without -mrelax-pic-calls ld.so segfaults when built with -O3
BuildFlags="-march=mips64r2 -mabi=64 -mrelax-pic-calls"
%endif

##############################################################################
# %%build - Generic options.
##############################################################################
BuildFlags="$BuildFlags -fasynchronous-unwind-tables"
EnableKernel="--enable-kernel=%{enablekernel}"
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc
AddOns=`echo */configure | sed -e 's!/configure!!g;s!\(nptl\|powerpc-cpu\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`

#if [ -z "$(grep '^libdir = $(exec_prefix)/lib64' Makeconfig)" ] ; then
#    sed -i 's/^libdir\ =\ $(exec_prefix)\/lib/libdir\ =\ $(exec_prefix)\/lib64/g' Makeconfig
#fi

#if [ -z "$(grep '^slibdir = $(exec_prefix)/lib64' Makeconfig)" ] ; then
#    sed -i 's/^slibdir\ =\ $(exec_prefix)\/lib/slibdir\ =\ $(exec_prefix)\/lib64/g' Makeconfig
#fi
##############################################################################
# build()
#	Build glibc in `build-%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, add-ons, kernel
#	version, multiarch support, system tap support, etc.
##############################################################################
#
#		--prefix=%{_prefix} \
build()
{
	builddir=build-%{target}${1:+-$1}
	${1+shift}
	rm -rf $builddir
	mkdir $builddir
	pushd $builddir
	build_CFLAGS="$BuildFlags -g -O3 $*"
	# Some configure checks can spuriously fail for some architectures if
	# unwind info is present
	configure_CFLAGS="$build_CFLAGS -fno-asynchronous-unwind-tables"
	../configure CC="$GCC" CXX="$GXX" CFLAGS="$configure_CFLAGS" \
		--enable-add-ons=$AddOns \
		--prefix=%{_prefix} \
                --libdir=%{_prefix}/%{_lib} \
		--with-headers=/usr/include/ $EnableKernel --enable-bind-now \
		--build=%{target} \
%ifarch %{multiarcharches}
		--enable-multi-arch \
%endif
		--enable-stack-protector=strong \
		--enable-tunables \
		--enable-obsolete-rpc \
		--enable-obsolete-nsl \
		--enable-systemtap \
		${core_with_options} \
%ifarch %{lock_elision_arches}
		--enable-lock-elision \
%endif
%if %{without werror}
		--disable-werror \
%endif
		--disable-profile \
%if %{with bootstrap}
		--without-selinux \
		--disable-nss-crypt ||
%else
		--enable-nss-crypt ||
%endif
		{ cat config.log; false; }

	make %{?_smp_mflags} -r CFLAGS="$build_CFLAGS" %{silentrules}
	popd
}

##############################################################################
# Build glibc for the default set of options.
##############################################################################
build

##############################################################################
# Build glibc for xen:
# If we support xen build glibc again for xen support.
##############################################################################
%if %{buildxen}
build nosegneg -mno-tls-direct-seg-refs
%endif

##############################################################################
# Build glibc for power6:
# If we support building a power6 alternate runtime then built glibc again for
# power6.
# XXX: We build in a sub-shell for no apparent reason.
##############################################################################
%if %{buildpower6}
(
	platform=`LD_SHOW_AUXV=1 /bin/true | sed -n 's/^AT_PLATFORM:[[:blank:]]*//p'`
	if [ "$platform" != power6 ]; then
		mkdir -p power6emul/{lib,lib64}
		$GCC -shared -O2 -fpic -o power6emul/%{_lib}/power6emul.so %{SOURCE8} -Wl,-z,initfirst
%ifarch ppc64
		gcc -shared -nostdlib -O2 -fpic -m32 -o power6emul/%{_lib}/power6emul.so -xc - < /dev/null
%endif
		export LD_PRELOAD=`pwd`/power6emul/\$LIB/power6emul.so
	fi
	GCC="$GCC -mcpu=power6"
	GXX="$GXX -mcpu=power6"
	core_with_options="--with-cpu=power6"
	build power6
)
%endif # %{buildpower6}

%if %{buildpower7}
(
  GCC="$GCC -mcpu=power7 -mtune=power7"
  GXX="$GXX -mcpu=power7 -mtune=power7"
  core_with_options="--with-cpu=power7"
  build power7
)
%endif

%if %{buildpower8}
(
  GCC="$GCC -mcpu=power8 -mtune=power8"
  GXX="$GXX -mcpu=power8 -mtune=power8"
  core_with_options="--with-cpu=power8"
  build power8
)
%endif

# Build libcrypt with glibc cryptographic implementations.
%if %{without bootstrap}
make %{?_smpflags} -C build-%{target} subdirs=crypt-glibc \
    CFLAGS="$build_CFLAGS" %{silentrules}
%endif

##############################################################################
# Build the glibc post-upgrade program:
# We only build one of these with the default set of options. This program
# must be able to run on all hardware for the lowest common denomintor since
# we only build it once.
##############################################################################
pushd build-%{target}
$GCC -static -L. -Os -g %{SOURCE2} \
	-o glibc_post_upgrade.%{_target_cpu} \
	'-DLIBTLS="/%{_lib}/tls/"' \
	'-DGCONV_MODULES_DIR="%{_libdir}/gconv"' \
	'-DLD_SO_CONF="%{_sysconfdir}/ld.so.conf"' \
	'-DICONVCONFIG="%{_sbindir}/iconvconfig.%{_target_cpu}"'
popd

##############################################################################
# Install glibc...
##############################################################################
%install

# Ensure the permissions of errlist.c do not change.  When the file is
# regenerated the Makefile sets the permissions to 444. We set it to 644
# to match what comes out of git. The tarball of the git archive won't have
# correct permissions because git doesn't track all of the permissions
# accurately (see git-cache-meta if you need that). We also set it to 644 to
# match pre-existing rpms. We do this *after* the build because the build
# might regenerate the file and set the permissions to 444.
chmod 644 sysdeps/gnu/errlist.c

# Reload compiler and build options that were used during %%build.
GCC=`cat Gcc`

# Cleanup any previous installs...
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make -j1 install_root=$RPM_BUILD_ROOT \
	install -C build-%{target} %{silentrules}
# If we are not building an auxiliary arch then install all of the supported
# locales.
%ifnarch %{auxarches}
pushd build-%{target}
make %{?_smp_mflags} install_root=$RPM_BUILD_ROOT \
	install-locales -C ../localedata objdir=`pwd`
popd
%endif

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename $RPM_BUILD_ROOT%{_prefix}/%{_lib}/${libbase}-*.so)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
		dlib=$libdestdir/$(basename $RPM_BUILD_ROOT%{_prefix}/%{_lib}/${libbase}.so.*)
		ln -sf $libbaseso $dlib
	done
}

#############################################################################
# Install libcrypt
#############################################################################

%if %{without bootstrap}
# Move the NSS-based implementation out of the way.
libcrypt_found=false
for libcrypt in ${RPM_BUILD_ROOT}%{_prefix}/lib/libcrypt-*.so ; do
  if $libcrypt_found; then
     Multiple libcrypt files
     ls -l ${RPM_BUILD_ROOT}/lib/libcrypt-*.so
     exit 1
  fi
  mv "$libcrypt" "$(echo "$libcrypt" | sed s/libcrypt-/libcrypt-nss-/)"
done

# Install the non-NSS implementation in the original path.
install -m 755 build-%{target}/crypt-glibc/libcrypt.so "$libcrypt"

unset libcrypt libcrypt_found
%endif

# This symbolic link will be generated by ldconfig.
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libcrypt.so.1

##############################################################################
# Install the xen build files.
##############################################################################
%if %{buildxen}
%define nosegneg_subdir_base i686
%define nosegneg_subdir i686/nosegneg
%define nosegneg_subdir_up ../..
pushd build-%{target}-nosegneg
destdir=$RPM_BUILD_ROOT%{_prefix}/%{_lib}
install_different "$destdir" "%{nosegneg_subdir}" "%{nosegneg_subdir_up}"
popd
%endif # %{buildxen}

##############################################################################
# Install the power6 build files.
##############################################################################
%if %{buildpower6}
%define power6_subdir power6
%define power6_subdir_up ..
%define power6_legacy power6x
%define power6_legacy_up ..
pushd build-%{target}-power6
destdir=$RPM_BUILD_ROOT%{_prefix}/%{_lib}
install_different "$destdir" "%{power6_subdir}" "%{power6_subdir_up}"
# Make a legacy /usr/lib[64]/power6x directory that is a symlink to the
# power6 runtime.
# XXX: When can we remove this? What is the history behind this?
mkdir -p ${destdir}/%{power6_legacy}
pushd ${destdir}/%{power6_legacy}
ln -sf %{power6_legacy_up}/%{power6_subdir}/*.so .
cp -a %{power6_legacy_up}/%{power6_subdir}/*.so.* .
popd
popd
%endif # %{buildpower6}

%if %{buildpower7}
%define power7_subdir power7
%define power7_subdir_up ..
pushd build-%{target}-power7
destdir=$RPM_BUILD_ROOT%{_prefix}/%{_lib}
install_different "$destdir" "%{power7_subdir}" "%{power7_subdir_up}"
popd
%endif

%if %{buildpower8}
%define power8_subdir power8
%define power8_subdir_up ..
pushd build-%{target}-power8
destdir=$RPM_BUILD_ROOT%{_prefix}/%{_lib}
install_different "$destdir" "%{power8_subdir}" "%{power8_subdir_up}"
popd
%endif

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f $RPM_BUILD_ROOT%{_libdir}/libNoVersion*
rm -f $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libNoVersion*

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# Remove the old nss modules.
rm -f ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/libnss-*.so.1

##############################################################################
# Install info files
##############################################################################

%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_infodir}
  mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

%else
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_infodir}/libc.info*
%endif

##############################################################################
# Create locale sub-package file lists
##############################################################################

%ifnarch %{auxarches}
olddir=`pwd`
pushd ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/locale
rm -f locale-archive
# Intentionally we do not pass --alias-file=, aliases will be added
# by build-locale-archive.
$olddir/build-%{target}/elf/ld.so \
        --library-path $olddir/build-%{target}/ \
        $olddir/build-%{target}/locale/localedef \
        --prefix ${RPM_BUILD_ROOT} --add-to-archive \
        *_*
# Setup the locale-archive template for use by glibc-all-langpacks.
mv locale-archive{,.tmpl}
# Create the file lists for the language specific sub-packages:
for i in eo *_*
do
    lang=${i%%_*}
    if [ ! -e langpack-${lang}.filelist ]; then
        echo "%dir %{_prefix}/%{_lib}/locale" >> langpack-${lang}.filelist
    fi
    echo "%dir  %{_prefix}/%{_lib}/locale/$i" >> langpack-${lang}.filelist
    echo "%{_prefix}/${_lib}/locale/$i/*" >> langpack-${lang}.filelist
done
popd
pushd ${RPM_BUILD_ROOT}%{_prefix}/share/locale
for i in */LC_MESSAGES/libc.mo
do
    locale=${i%%%%/*}
    lang=${locale%%%%_*}
    echo "%lang($lang) %{_prefix}/share/locale/${i}" \
         >> ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/locale/langpack-${lang}.filelist
done
popd
mv  ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/locale/*.filelist .
%endif

##############################################################################
# Install configuration files for services
##############################################################################
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/nsswitch.conf

%ifnarch %{auxarches}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/default
install -p -m 644 nis/nss $RPM_BUILD_ROOT%{_sysconfdir}/default/nss

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/..%{_tmpfilesdir}
install -m 644 %{SOURCE4} %{buildroot}%{_prefix}/..%{_tmpfilesdir}
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}/
sed -i "s#/etc#%{_scl_root}/etc#g" nscd/nscd.service
sed -i "s#/usr#%{_scl_root}/usr#g" nscd/nscd.service
sed -i "s#/run#%{_scl_root}/run#g" nscd/nscd.service
mv nscd/nscd.service nscd/%{scl_prefix}nscd.service
mv nscd/nscd.socket nscd/%{scl_prefix}nscd.socket
install -m 644 nscd/%{scl_prefix}nscd.service nscd/%{scl_prefix}nscd.socket $RPM_BUILD_ROOT%{_unitdir}/
%endif

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
truncate -s 0 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.cache
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
%ifnarch %{auxarches}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
truncate -s 0 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nscd
truncate -s 0 $RPM_BUILD_ROOT%{_sysconfdir}/gai.conf
%endif

# Include %{_libdir}/gconv/gconv-modules.cache
truncate -s 0 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache

##############################################################################
# Misc...
##############################################################################

# Install the upgrade program
install -m 700 build-%{target}/glibc_post_upgrade.%{_target_cpu} \
  $RPM_BUILD_ROOT%{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

# Strip all of the installed object files.
strip -g $RPM_BUILD_ROOT%{_libdir}/*.o

# XXX: Ugly hack for buggy rpm. What bug? BZ? Is this fixed?
ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

##############################################################################
# Install debug copies of unstripped static libraries
# - This step must be last in order to capture any additional static
#   archives we might have added.
##############################################################################

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}
cp -a $RPM_BUILD_ROOT%{_libdir}/*.a \
	$RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/*_p.a
%endif

##############################################################################
# Build the file lists used for describing the package and subpackages.
##############################################################################
# There are several main file lists (and many more for
# the langpack sub-packages (langpack-${lang}.filelist)):
# * rpm.fileslist
#	- Master file list. Eventually, after removing files from this list
#	  we are left with the list of files for the glibc package.
# * common.filelist
#	- Contains the list of flies for the common subpackage.
# * utils.filelist
#	- Contains the list of files for the utils subpackage.
# * nscd.filelist
#	- Contains the list of files for the nscd subpackage.
# * devel.filelist
#	- Contains the list of files for the devel subpackage.
# * headers.filelist
#	- Contains the list of files for the headers subpackage.
# * static.filelist
#	- Contains the list of files for the static subpackage.
# * nosegneg.filelist
#	- Contains the list of files for the xen subpackage.
# * libcrypt.filelist, libcrypt-nss.filelist
#       - Contains the list of files for the crypt-related subpackages
# * nss_db.filelist, nss_nis.filelist, nss_hesiod.filelist
#       - File lists for nss_* NSS module subpackages.
# * nss-devel.filelist
#       - File list with the .so symbolic links for NSS packages.
# * debuginfo.filelist
#	- Contains the list of files for the glibc debuginfo package.
# * debuginfocommon.filelist
#	- Contains the list of files for the glibc common debuginfo package.
#

{
  find $RPM_BUILD_ROOT \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  # Print all directories with a %%dir prefix.  We omit the info directory and
  # all directories in (and including) /usr/share/locale.
  find $RPM_BUILD_ROOT -type d \
       \( -path '*%{_prefix}/share/locale' -prune -o \
       \( -path '*%{_prefix}/share/*' \
%if %{with docs}
	! -path '*%{_infodir}' -o \
%endif
	  -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n" \)
} | {

  # primary filelist

  # Also remove the *.mo entries.  We will add them to the
  # language specific sub-packages.
  # libnss_ files go into subpackages related to NSS modules.
  # and .*/share/i18n/charmaps/.*), they go into the sub-package
  # "locale-source":
  sed -e '\,.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo,d' \
      -e '\,.*/share/i18n/locales/.*,d' \
      -e '\,.*/share/i18n/charmaps/.*,d' \
      -e '\,%{_sysconfdir}/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,/lib/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > rpm.filelist

touch common.filelist

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_prefix}/lib/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_libdir}

# The xtrace and memusage scripts have hard-coded paths that need to be
# translated to a correct set of paths using the $LIB token which is
# dynamically translated by ld.so as the default lib directory.
for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
  sed -e 's~=/lib/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=/lib/libmemusage.so~=%{_libdir}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

%if %{with docs}
# Put the info files into the devel file list.
grep '%{_infodir}' < rpm.filelist | grep -v '%{_infodir}/dir' > devel.filelist
%endif

# The glibc-headers package includes only common files which are identical
# across all multilib packages. We must keep gnu/stubs.h and gnu/lib-names.h
# in the glibc-headers package, but the -32, -64, -64-v1, and -64-v2 versions
# go into the development packages.
grep '%{_prefix}/include/gnu/stubs-.*\.h$' < rpm.filelist >> devel.filelist || :
grep '%{_prefix}/include/gnu/lib-names-.*\.h$' < rpm.filelist >> devel.filelist || :
# Put the include files into headers file list.
grep '%{_prefix}/include' < rpm.filelist \
  | egrep -v '%{_prefix}/include/gnu/stubs-.*\.h$' \
  | egrep -v '%{_prefix}/include/gnu/lib-names-.*\.h$' \
  > headers.filelist

# Remove partial (lib*_p.a) static libraries, include files, and info files from
# the core glibc package.
sed -i -e '\|%{_libdir}/lib.*_p.a|d' \
       -e '\|%{_prefix}/include|d' \
       -e '\|%{_infodir}|d' \
	rpm.filelist

# Put some static files into the devel package.
grep '%{_libdir}/lib.*\.a' < rpm.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  >> devel.filelist

# Put the rest of the static files into the static package.
grep '%{_libdir}/lib.*\.a' < rpm.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  > static.filelist

# Put all of the object files and *.so (not the versioned ones) into the
# devel package.
grep '%{_libdir}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < rpm.filelist >> devel.filelist

# Remove all of the static, object, unversioned DSOs, and nscd from the core
# glibc package.
sed -i -e '\|%{_libdir}/lib.*\.a|d' \
       -e '\|%{_libdir}/.*\.o|d' \
       -e '\|%{_libdir}/lib.*\.so|d' \
       -e '\|nscd|d' rpm.filelist

# All of the bin and certain sbin files go into the common package.
# We explicitly exclude certain sbin files that need to go into
# the core glibc package for use during upgrades.
grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
# All of the files under share go into the common package since
# they should be multilib-independent.
grep '%{_prefix}/share' < rpm.filelist | \
  grep -v -e '%{_prefix}/share/zoneinfo' -e '%%dir %{prefix}/share' \
       >> common.filelist

# Remove the bin, locale, some sbin, and share from the
# core glibc package. We cheat a bit and use the slightly dangerous
# /usr/sbin/[^gi] to match the inverse of the search that put the
# files into common.filelist. It's dangerous in that additional files
# that start with g, or i would get put into common.filelist and
# rpm.filelist.
sed -i -e '\|%{_prefix}/bin|d' \
       -e '\|%{_prefix}/%{_lib}/locale|d' \
       -e '\|%{_prefix}/sbin/[^gi]|d' \
       -e '\|%{_prefix}/share|d' rpm.filelist

##############################################################################
# Build the xen package file list (nosegneg.filelist)
##############################################################################
truncate -s 0 nosegneg.filelist
%if %{xenpackage}
grep '/%{_lib}/%{nosegneg_subdir}' < rpm.filelist >> nosegneg.filelist
sed -i -e '\|/%{_lib}/%{nosegneg_subdir}|d' rpm.filelist
# TODO: There are files in the nosegneg list which should be in the devel
#	pacakge, but we leave them instead in the xen subpackage. We may
#	wish to clean that up at some point.
%endif

# Add the binary to build locales to the common subpackage.
echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist

# The nscd binary must go into the nscd subpackage.
echo '%{_prefix}/sbin/nscd' > nscd.filelist

# The memusage and pcprofile libraries are put back into the core
# glibc package even though they are only used by utils package
# scripts..
cat >> rpm.filelist <<EOF
%{_libdir}/libmemusage.so
%{_libdir}/libpcprofile.so
EOF

# Add the utils scripts and programs to the utils subpackage.
cat > utils.filelist <<EOF
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%if %{without bootstrap}
%{_prefix}/bin/mtrace
%endif
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

# Move the NSS-related files to the NSS subpackages.  Be careful not
# to pick up .debug files, and the -devel symbolic links.
for module in db nis nisplus compat hesiod files dns; do
  grep -E "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
    rpm.filelist > nss_$module.filelist
done

# nis includes nisplus and compat
cat nss_nisplus.filelist nss_compat.filelist >> nss_nis.filelist
# Symlinks go into the nss-devel package (instead of the main devel
# package).
grep '/libnss_[a-z]*\.so$' devel.filelist > nss-devel.filelist

# Fix db/Makefile installtion
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/db
mv $RPM_BUILD_ROOT%{_prefix}/var/db/Makefile $RPM_BUILD_ROOT%{_localstatedir}/db/Makefile
sed -i 's/\/usr\/var\/db/\/var\/db/g' rpm.filelist

# %{_localstatedir}/db/Makefile goes into nss_hesiod, remove the other files from
# the main and devel file list.
sed -i -e '\,/libnss_.*\.so[0-9.]*$,d' \
    -e '\,%{_localstatedir}/db/Makefile,d' \
    rpm.filelist devel.filelist
# Restore the built-in NSS modules.
cat nss_files.filelist nss_dns.filelist >> rpm.filelist

# Prepare the libcrypt-related file lists.
grep '/libcrypt-[0-9.]*.so$' rpm.filelist > libcrypt.filelist

test $(wc -l < libcrypt.filelist) -eq 1
%if %{without bootstrap}
sed s/libcrypt/libcrypt-nss/ < libcrypt.filelist > libcrypt-nss.filelist
%endif
sed -i -e '\,/libcrypt,d' rpm.filelist

# Remove the zoneinfo files
# XXX: Why isn't this don't earlier when we are removing files?
#      Won't this impact what is shipped?
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent.  The choice of using
# glibc_post_upgrade.c is arbitrary.
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf
touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT%{_sysconfdir}/rpc

# We allow undefined symbols in shared libraries because the libraries
# referenced at link time here, particularly ld.so, may be different than
# the one used at runtime.  This is really only needed during the ARM
# transition from ld-linux.so.3 to ld-linux-armhf.so.3.
pushd build-%{target}
$GCC -Os -g -static -o build-locale-archive %{SOURCE1} \
	../build-%{target}/locale/locarchive.o \
	../build-%{target}/locale/md5.o \
	-I. -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
	-L../build-%{target} \
	-Wl,--allow-shlib-undefined \
	-B../build-%{target}/csu/ -lc -lc_nonshared
install -m 700 build-locale-archive $RPM_BUILD_ROOT%{_prefix}/sbin/build-locale-archive
popd

# Lastly copy some additional documentation for the packages.
rm -rf documentation
mkdir documentation
cp crypt/README.ufc-crypt documentation/README.ufc-crypt
cp timezone/README documentation/README.timezone
cp posix/gai.conf documentation/

%ifarch s390x
# Compatibility symlink
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/ld64.so.1
%endif

# Leave a compatibility symlink for the dynamic loader on armhfp targets,
# at least until the world gets rebuilt
%ifarch armv7hl armv7hnl
ln -sf %{_prefix}/%{_lib}/ld-linux-armhf.so.3 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/ld-linux.so.3
%endif

%if %{with benchtests}
# Build benchmark binaries.  Ignore the output of the benchmark runs.
pushd build-%{target}
make BENCH_DURATION=1 bench-build
popd

# Copy over benchmark binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests
cp $(find build-%{target}/benchtests -type f -executable) $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/

find build-%{target}/benchtests -type f -executable | while read b; do
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)"
done >> benchtests.filelist

# ... and the makefile.
for b in %{SOURCE9} %{SOURCE10}; do
	cp $b $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)" >> benchtests.filelist
done

# .. and finally, the comparison scripts.
cp benchtests/scripts/benchout.schema.json $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/compare_bench.py $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/import_bench.py $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/validate_benchout.py $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/

echo "%{_prefix}/libexec/glibc-benchtests/benchout.schema.json" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/compare_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/import_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/validate_benchout.py*" >> benchtests.filelist
%endif

###############################################################################
# Rebuild libpthread.a using --whole-archive to ensure all of libpthread
# is included in a static link. This prevents any problems when linking
# statically, using parts of libpthread, and other necessary parts not
# being included. Upstream has decided that this is the wrong approach to
# this problem and that the full set of dependencies should be resolved
# such that static linking works and produces the most minimally sized
# static application possible.
###############################################################################
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
$GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
popd
###############################################################################

%if 0%{?_enable_debug_packages}

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
pushd locale
ln -s programs/*.gperf .
popd
pushd iconv
ln -s ../locale/programs/charmap-kw.gperf .
popd

# Print some diagnostic information in the builds about the
# getconf binaries.
# XXX: Why do we do this?
ls -l $RPM_BUILD_ROOT%{_prefix}/bin/getconf
ls -l $RPM_BUILD_ROOT%{_prefix}/libexec/getconf
eu-readelf -hS $RPM_BUILD_ROOT%{_prefix}/bin/getconf \
	$RPM_BUILD_ROOT%{_prefix}/libexec/getconf/*

find_debuginfo_args='--strict-build-id -g'
%ifarch %{debuginfocommonarches}
find_debuginfo_args="$find_debuginfo_args \
	-l common.filelist \
	-l utils.filelist \
	-l nscd.filelist \
	-p '.*/(sbin|libexec)/.*' \
	-o debuginfocommon.filelist \
	-l nss_db.filelist -l nss_nis.filelist -l nss_hesiod.filelist \
	-l libcrypt.filelist \
%if %{without bootstrap}
	-l libcrypt-nss.filelist \
%endif
	-l rpm.filelist \
%if %{with benchtests}
	-l nosegneg.filelist -l benchtests.filelist"
%else
	-l nosegneg.filelist"
%endif
%endif
eval /usr/lib/rpm/find-debuginfo.sh \
	"$find_debuginfo_args" \
	-o debuginfo.filelist

# List all of the *.a archives in the debug directory.
list_debug_archives()
{
	local dir=%{_prefix}/lib/debug%{_libdir}
	find $RPM_BUILD_ROOT$dir -name "*.a" -printf "$dir/%%P\n"
}

%ifarch %{debuginfocommonarches}

# Remove the source files from the common package debuginfo.
sed -i '\#^%{_prefix}/src/debug/#d' debuginfocommon.filelist

# Create a list of all of the source files we copied to the debug directory.
find $RPM_BUILD_ROOT%{_prefix}/src/debug \
     \( -type d -printf '%%%%dir ' \) , \
     -printf '%{_prefix}/src/debug/%%P\n' > debuginfocommon.sources

%ifarch %{biarcharches}

# Add the source files to the core debuginfo package.
cat debuginfocommon.sources >> debuginfo.filelist

%else

%ifarch %{ix86}
%define basearch i686
%endif
%ifarch sparc sparcv9
%define basearch sparc
%endif

# The auxarches get only these few source files.
auxarches_debugsources=\
'/(generic|linux|%{basearch}|nptl(_db)?)/|/%{glibcsrcdir}/build|/dl-osinfo\.h'

# Place the source files into the core debuginfo pakcage.
egrep "$auxarches_debugsources" debuginfocommon.sources >> debuginfo.filelist

# Remove the source files from the common debuginfo package.
egrep -v "$auxarches_debugsources" \
  debuginfocommon.sources >> debuginfocommon.filelist

%endif # %{biarcharches}

# Add the list of *.a archives in the debug directory to
# the common debuginfo package.
list_debug_archives >> debuginfocommon.filelist

# It happens that find-debuginfo.sh produces duplicate entries even
# though the inputs are unique. Therefore we sort and unique the
# entries in the debug file lists. This avoids the following warnings:
# ~~~
# Processing files: glibc-debuginfo-common-2.17.90-10.fc20.x86_64
# warning: File listed twice: /usr/lib/debug/usr/sbin/build-locale-archive.debug
# warning: File listed twice: /usr/lib/debug/usr/sbin/nscd.debug
# warning: File listed twice: /usr/lib/debug/usr/sbin/zdump.debug
# warning: File listed twice: /usr/lib/debug/usr/sbin/zic.debug
# ~~~
sort -u debuginfocommon.filelist > debuginfocommon2.filelist
mv debuginfocommon2.filelist debuginfocommon.filelist

%endif # %{debuginfocommonarches}

# Remove any duplicates output by a buggy find-debuginfo.sh.
sort -u debuginfo.filelist > debuginfo2.filelist
mv debuginfo2.filelist debuginfo.filelist

# Remove some common directories from the common package debuginfo so that we
# don't end up owning them.
exclude_common_dirs()
{
	exclude_dirs="%{_prefix}/src/debug"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug{,/%{_lib},/bin,/sbin})"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug%{_prefix}{,/%{_lib},/libexec,/bin,/sbin})"

	for d in $(echo $exclude_dirs | sed 's/ /\n/g'); do
		sed -i "\|^%%dir $d/\?$|d" $1
	done
}

%ifarch %{debuginfocommonarches}
exclude_common_dirs debuginfocommon.filelist
%endif
exclude_common_dirs debuginfo.filelist

%endif # 0%{?_enable_debug_packages}

%if %{with docs}
# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%endif

%ifarch %{auxarches}

# Delete files that we do not intended to ship with the auxarch.
echo Cutting down the list of unpackaged files
sed -e '/%%dir/d;/%%config/d;/%%verify/d;s/%%lang([^)]*) //;s#^/*##' \
	common.filelist devel.filelist static.filelist headers.filelist \
	utils.filelist nscd.filelist \
%ifarch %{debuginfocommonarches}
	debuginfocommon.filelist \
%endif
	| (cd $RPM_BUILD_ROOT; xargs --no-run-if-empty rm -f 2> /dev/null || :)

%else

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/{db,run}/nscd
touch $RPM_BUILD_ROOT%{_localstatedir}/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT%{_localstatedir}/run/nscd/{socket,nscd.pid}

%endif # %{auxarches}

%ifnarch %{auxarches}
truncate -s 0 $RPM_BUILD_ROOT%{_prefix}/%{_lib}/locale/locale-archive
%endif

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/ldconfig
truncate -s 0 $RPM_BUILD_ROOT%{_localstatedir}/cache/ldconfig/aux-cache

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

# Run the glibc tests. If any tests fail to build we exit %check with an error
# of 1, otherwise we print the test failure list and the failed test output
# and exit with 0. In the future we want to compare against a baseline and
# exit with 1 if the results deviate from the baseline.
run_tests () {

        #Fix nptl test failurs when glibc is not installed into /usr directory 
        ln -s /usr/%{_lib}/libgcc_s.so.1 libgcc_s.so.1
        ln -s /usr/%{_lib}/libstdc++.so.6 libstdc++.so.6
        ln -s /usr/%{_lib}/libfreebl3.so libfreebl3.so

	truncate -s 0 check.log
	tail -f check.log &
	tailpid=$!
	# Run the make a sub-shell (to avoid %check failing if make fails)
	# but capture the status for use later. We use the normal sub-shell
	# trick of printing the status. The actual result of the sub-shell
	# is the successful execution of the echo.
	status=$(set +e
		 make %{?_smp_mflags} check %{silentrules} > check.log 2>&1
		 status=$?
		 echo $status)
	# Wait for the tail to catch up with the output and then kill it.
	sleep 10
	kill $tailpid
	# Print the header, so we can find it, but skip the error printing
	# if there aren't any failrues.
	echo ===================FAILED TESTS=====================
	if [ $status -ne 0 ]; then
		# We are not running with `-k`, therefore a test build failure
		# terminates the test run and that terminates %check with an
		# error which terminates the build. We want this behaviour to
		# ensure that all tests build, and all tests run.
		# If the test result summary is not present it means one of
		# tests failed to build.
		if ! grep 'Summary of test results:' check.log; then
			echo "FAIL: Some glibc tests failed to build."
			exit 1
		fi

		# Print out information about all of the failed tests.
		grep -e ^FAIL -e ^ERROR tests.sum \
			| awk '{print $2}' \
			| while read testcase;
		do
			echo "$testcase"
			cat $testcase.out
			echo -------------------------
		done
	fi

	# If the crypt-glibc test suite fails, something is completely
	# broken, so fail the build in this case.
	make %{?_smp_mflags} subdirs=crypt-glibc check %{silentrules}
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================
##############################################################################
# - Test the default runtime.
# 	- Power 620 / 970 ISA for 64-bit POWER BE.
#	- POWER8 for 64-bit POWER LE.
#	- ??? for 64-bit x86_64
#	- ??? for 32-bit x86
#	- ??? for 64-bit AArch64
#	- ??? for 32-bit ARM
#	- zEC12 for 64-bit s390x
#	- ??? for 32-bit s390
##############################################################################
pushd build-%{target}
run_tests
popd

%if %{buildxen}
echo ====================TESTING -mno-tls-direct-seg-refs=============
##############################################################################
# - Test the xen runtimes (nosegneg).
##############################################################################
pushd build-%{target}-nosegneg
run_tests
popd
%endif

%if %{buildpower6}
echo ====================TESTING -mcpu=power6=============
##############################################################################
# - Test the 64-bit POWER6 BE runtimes.
##############################################################################
pushd build-%{target}-power6
if [ -d ../power6emul ]; then
    export LD_PRELOAD=`cd ../power6emul; pwd`/\$LIB/power6emul.so
fi
run_tests
popd
%endif

%if %{buildpower7}
echo ====================TESTING -mcpu=power7=============
##############################################################################
# - Test the 64-bit POWER7 BE runtimes.
##############################################################################
pushd build-%{target}-power7
run_tests
popd
%endif

%if %{buildpower8}
echo ====================TESTING -mcpu=power8=============
##############################################################################
# - Test the 64-bit POWER8 BE runtimes.
##############################################################################
pushd build-%{target}-power8
run_tests
popd
%endif

echo ====================TESTING DETAILS=================
for i in `sed -n 's|^.*\*\*\* \[\([^]]*\.out\)\].*$|\1|p' build-*-linux*/check.log`; do
  echo =====$i=====
  cat $i || :
  echo ============
done
echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr $RPM_BUILD_ROOT%{_prefix}/lib/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr $RPM_BUILD_ROOT%{_prefix}/lib/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

%if %{with valgrind}
# Finally, check if valgrind runs with the new glibc.
# We want to fail building if valgrind is not able to run with this glibc so
# that we can then coordinate with valgrind to get it fixed before we update
# glibc.
pushd build-%{target}
elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/valgrind \
	elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/true
popd
%endif

%endif # %{run_glibc_tests}


%pre -p <lua>
-- Check that the running kernel is new enough
required = '%{enablekernel}'
rel = posix.uname("%r")
if rpm.vercmp(rel, required) < 0 then
  error("FATAL: kernel too old", 0)
end

%post -p %{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

%postun -p /sbin/ldconfig

%posttrans all-langpacks -e -p <lua>
-- If at the end of the transaction we are still installed
-- (have a template of non-zero size), then we rebuild the
-- locale cache (locale-archive) from the pre-populated
-- locale cache (locale-archive.tmpl) i.e. template.
if posix.stat("%{_prefix}/%{_lib}/locale/locale-archive.tmpl", "size") > 0 then
  pid = posix.fork()
  if pid == 0 then
    posix.exec("%{_prefix}/sbin/build-locale-archive", "--install-langs", "%%{_install_langs}")
  elseif pid > 0 then
    posix.wait(pid)
  end
end

%postun all-langpacks -p <lua>
-- In the postun we always remove the locale cache.
-- We are being uninstalled and if this is an upgrade
-- then the new packages template will be used to
-- recreate a new copy of the cache.
os.remove("%{_prefix}/%{_lib}/locale/locale-archive")

%if %{with docs}
%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
%endif

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%if %{with docs}
%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
fi
%endif

%post utils -p /sbin/ldconfig

%postun utils -p /sbin/ldconfig

%pre -n %{?scl_prefix}nscd
getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
getent passwd nscd >/dev/null ||
  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
		    -c "NSCD Daemon" -u 28 -g nscd nscd

%post -n %{?scl_prefix}nscd
%systemd_post %{scl_prefix}nscd.service

%preun -n %{?scl_prefix}nscd
%systemd_preun %{scl_prefix}nscd.service

%postun -n %{?scl_prefix}nscd
if test $1 = 0; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart %{scl_prefix}nscd.service

%if %{xenpackage}
%post xen -p /sbin/ldconfig
%postun xen -p /sbin/ldconfig
%endif

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

%files -f rpm.filelist
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/audit
%if %{buildxen} && !%{xenpackage}
%dir %{_prefix}/%{_lib}/%{nosegneg_subdir_base}
%dir %{_prefix}/%{_lib}/%{nosegneg_subdir}
%endif
%if %{buildpower6}
%dir %{_prefix}/%{_lib}/power6
%dir %{_prefix}/%{_lib}/power6x
%endif
%if %{buildpower7}
%dir %{_prefix}/%{_lib}/power7
%endif
%if %{buildpower8}
%dir %{_prefix}/%{_lib}/power8
%endif
%ifarch s390x
%{_prefix}/%{_lib}/ld64.so.1
%endif
%ifarch armv7hl armv7hnl
%{_prefix}/%{_lib}/ld-linux.so.3
%endif
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/rpc
%dir %{_sysconfdir}/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_libdir}/gconv
%dir %attr(0700,root,root) %{_localstatedir}/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_sysconfdir}/ld.so.cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_sysconfdir}/gai.conf
%doc README NEWS INSTALL BUGS CONFORMANCE elf/rtld-debugger-interface.txt
# If rpm doesn't support %license, then use %doc instead.
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB LICENSES

%if %{xenpackage}
%files -f nosegneg.filelist xen
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/%{nosegneg_subdir_base}
%dir ${_prefix}/%{_lib}/%{nosegneg_subdir}
%endif

%ifnarch %{auxarches}
%files -f common.filelist common
%defattr(-,root,root)
%dir %{_prefix}/%{_lib}/locale
%dir %{_prefix}/%{_lib}/locale/C.utf8
%{_prefix}/%{_lib}/locale/C.utf8/*
%dir %attr(755,root,root) %{_sysconfdir}/default
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/default/nss
%doc documentation/README.timezone
%doc documentation/gai.conf

%files all-langpacks
%attr(0644,root,root) %verify(not md5 size mtime) %{_prefix}/%{_lib}/locale/locale-archive.tmpl
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/locale/locale-archive

%files locale-source
%defattr(-,root,root)
%dir %{_prefix}/share/i18n/locales
%{_prefix}/share/i18n/locales/*
%dir %{_prefix}/share/i18n/charmaps
%{_prefix}/share/i18n/charmaps/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f static.filelist static
%defattr(-,root,root)

%files -f headers.filelist headers
%defattr(-,root,root)

%files -f utils.filelist utils
%defattr(-,root,root)

%files -f nscd.filelist -n %{?scl_prefix}nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%dir %attr(0755,root,root) %{_localstatedir}/run/nscd
%dir %attr(0755,root,root) %{_localstatedir}/db/nscd
/usr/lib/systemd/system/%{scl_prefix}nscd.service
/usr/lib/systemd/system/%{scl_prefix}nscd.socket
%{_prefix}/..%{_tmpfilesdir}/nscd.conf
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_localstatedir}/db/nscd/services
%ghost %config(missingok,noreplace) %{_sysconfdir}/sysconfig/nscd
%endif

%files -f nss_db.filelist -n %{?scl_prefix}nss_db
%files -f nss_nis.filelist -n %{?scl_prefix}nss_nis
%files -f nss_hesiod.filelist -n %{?scl_prefix}nss_hesiod
%{_localstatedir}/db/Makefile
%doc hesiod/README.hesiod
%files -f nss-devel.filelist nss-devel

%files -f libcrypt.filelist -n %{?scl_prefix}libcrypt
%doc documentation/README.ufc-crypt
%ghost /%{_lib}/libcrypt.so.1
%if %{without bootstrap}
%files -f libcrypt-nss.filelist -n %{?scl_prefix}libcrypt-nss
%ghost /%{_lib}/libcrypt.so.1
%endif

%if 0%{?_enable_debug_packages}
%files debuginfo -f debuginfo.filelist
%defattr(-,root,root)
%ifarch %{debuginfocommonarches}
%ifnarch %{auxarches}
%files debuginfo-common -f debuginfocommon.filelist
%defattr(-,root,root)
%endif
%endif
%endif

%if %{with benchtests}
%files benchtests -f benchtests.filelist
%defattr(-,root,root)
%endif

%changelog
* Fri May 5 2017 Huang Jinhua 2.25.90
- Estuary ARM64 initial package

* Mon May 01 2017 Carlos O'Donell <carlos@systemhalted.org> - 2.25.90-2
- Auto-sync with upstream master,
  commit 25e39b4229fb365a605dc4c8f5d6426a77bc08a6.
- logbl for POWER7 return incorrect results (swbz#21280)
- sys/socket.h uio.h namespace (swbz#21426)
- Support POSIX_SPAWN_SETSID (swbz#21340)
- Document how to provide a malloc replacement (swbz#20424)
- Verify that all internal sockets opened with SOCK_CLOEXEC (swbz#15722)
- Use AVX2 memcpy/memset on Skylake server (swbz#21396)
- unwind-dw2-fde deadlock when using AddressSanitizer (swbz#21357)
- resolv: Reduce advertised EDNS0 buffer size to guard against
  fragmentation attacks (swbz#21361)
- mmap64 silently truncates large offset values (swbz#21270)
- _dl_map_segments does not test for __mprotect failures consistently
  (swbz#20831)

* Thu Mar 02 2017 Florian Weimer <fweimer@redhat.com> - 2.25.90-1
- Switch back to upstream master branch.
- Drop Unicode 9 patch, merged upstream.
- Auto-sync with upstream master,
  commit a10e9c4e53fc652b79abf838f7f837589d2c84db, fixing:
- Build all DSOs with BIND_NOW (#1406731)

* Wed Mar  1 2017 Jakub Hrozek <jhrozek@redhat.com> - 2.25-3
- NSS: Prefer sss service for passwd, group databases (#1427646)

* Tue Feb 28 2017 Florian Weimer <fweimer@redhat.com> - 2.25-2
- Auto-sync with upstream release/2.25/master,
  commit 93cf93e06ce123439e41d3d62790601c313134cb, fixing:
- sunrpc: Improvements for UDP client timeout handling (#1346406)
- sunrpc: Avoid use-after-free read access in clntudp_call (swbz#21115)
- Fix getting tunable values on big-endian (swbz#21109)

* Wed Feb 08 2017 Carlos O'Donell <carlos@redhat.com> - 2.25-1
- Update to final released glibc 2.25.

* Wed Feb 08 2017 Carlos O'Donell <carlos@redhat.com> - 2.24.90-31
- Fix builds with GCC 7.0.

* Wed Feb 01 2017 Carlos O'Donell <carlos@redhat.com> - 2.24.90-30
- Optimize IBM z System builds for zEC12.

* Wed Jan 25 2017 Florian Weimer <fweimer@redhat.com> - 2.24.90-29
- Use vpath in crypt-glibc/Makefile to obtain the test input file.
- Auto-sync with upstream master,
  commit 5653ab12b4ae15b32d41de7c56b2a4626cd0437a, fixing:
- ARM fpu_control.h for assemblers requiring VFP insn names (swbz#21047)
- FAIL in test string/tst-xbzero-opt (swbz#21006)
- Make soft-float powerpc swapcontext restore the signal mask (swbz#21045)
- Clear list of acquired robust mutexes in the child after fork (swbz#19402)

* Thu Jan 12 2017 Carlos O'Donell <carlos@systemhalted.org> - 2.24.90-28
- Auto-sync with upstream master,
  commit 468e525c81a4af10f2e613289b6ff7c950773a9e:
- Drop rwlock related patches applied upstream.
- Fix i686 memchr for large input sizes (swbz#21014)
- Fix x86 strncat for large input sizes (swbz#19390)
- powerpc: Fix write-after-destroy in lock elision (swbz#20822)
- New pthread rwlock that is more scalable.
- Fix testsuite build for GCC 7 -Wformat-truncation.

* Mon Jan 02 2017 Florian Weimer <fweimer@redhat.com> - 2.24.90-27
- Auto-sync with upstream master,
  commit 73dfd088936b9237599e4ab737c7ae2ea7d710e1:
- Enable tunables.
- Drop condvar-related patches applied upstream.
- Update DNS RR type definitions (swbz#20593)
- CVE-2015-5180: resolv: Fix crash with internal QTYPE (#1249603)
- sunrpc: Always obtain AF_INET addresses from NSS (swbz#20964)


* Mon Dec 26 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-26
- Auto-sync with upstream master,
  commit cecbc7967f0bcac718b6f8f8942b58403c0e917c
- Enable stack protector for most of glibc (#1406731)

* Fri Dec 23 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.24.90-25
- Auto-sync with upstream master,
  commit 81e0662e5f2c342ffa413826b7b100d56677b613, fixing:
- Shared object unload assert when calling dlclose (#1398370, swbz#11941)
- Fix nss_nisplus build with mainline GCC (swbz#20978)
- Add Intel TSX blacklist for silicon with known errata.
- Add fmax, fmin, fmaxf, fminf microbenchmarks.
- Robust mutexes: Fix lost wake-up (swbz#20973).
- Add fmaxmag, fminmag, roundeven, roundevenf, roundevenl functions.

* Sun Dec 18 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-24
- Auto-sync with upstream master,
  commit e077349ce589466eecd47213db4fae6b80ec18c4, fixing:
- Warn about assignment in assertions (#1105335)
- powerpc64/power7 memchr for large input sizes (swbz#20971)
- fmax, fmin sNaN handling (swbz#20947)

* Mon Dec 12 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-23
- Auto-sync with upstream master,
  commit 92dcaa3e2f7bf0f7f1c04cd2fb6a317df1a4e225, fixing:
- Add getrandom, getentropy (#1172273)
- Add additional compiler barriers to backtrace tests (swbz#20956)

* Fri Dec 09 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-22
- Auto-sync with upstream master,
  commit 0abbe7cd700951082b314182a0958d65238297ef, changing:
- IN6_IS_ADDR_ does not require enabling non-standard extensions (#1138893)
- Install libm.a as linker script (swbz#20539)
- Fix writes past the allocated array bounds in execvpe (swbz#20847)
- Fix hypot sNaN handling (swbz#20940)
- Fix x86_64/x86 powl handling of sNaN arguments (swbz#20916)
- Fix sysdeps/ieee754 pow handling of sNaN arguments (swbz#20916)
- Fix pow (qNaN, 0) result with -lieee (swbz#20919)
- Fix --enable-nss-crypt failure of tst-linkall-static (swbz#20918)

* Fri Dec 02 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-21
- Auto-sync with upstream master,
  commit 01b23a30b42a90b1ebd882a0d81110a1542e504a, fixing:
- aarch64: Incorrect dynamic TLS resolution (#1400347)

* Wed Nov 30 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-20
- Auto-sync with upstream master,
  commit 9e78f6f6e7134a5f299cc8de77370218f8019237, fixing:
- stdio buffering with certain network file systems (#1400144)
- libpthread initialization breaks ld.so exceptions (#1393909)
- x86_64: Use of PLT and GOT in static archives (swbz#20750)
- localedata, iconvdata: 0x80->Euro sign mapping for GBK (swbz#20864)
- math: x86_64 -mfpmath=387 float_t, double_t (swbz#20787)

* Wed Nov 23 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-19
- Auto-sync with upstream master,
  commit 7a5e3d9d633c828d84a9535f26b202a6179978e7:
- Fix default float_t definition (swbz#20855)
- Fix writes past the allocated array bounds in execvpe (swbz#20847)

* Tue Nov 22 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-18
- Auto-sync with upstream master,
  commit 5ee1a4443a3eb0868cef1fe506ae6fb6af33d4ad.

* Wed Nov 16 2016 Carlos O'Donell <carlos@redhat.com> - 2.24.90-17
* Add new scalable implementation of POSIX read-write locks.

* Wed Nov 16 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-16
- Do not try to link libcrypt statically during tests

* Wed Nov 16 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-15
- Auto-sync with upstream master,
  commit 530862a63e0929128dc98fbbd463b120934434fb, fixing:
- Fix rpcgen buffer overrun (swbz#20790)
- Fix ppc64 build failure to swbz#20729 fix attempt

* Wed Nov  2 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-14
- Drop glibc-swbz20019.patch, applied upstream.
- dlerror returns NULL after dlsym (RTLD_NEXT) lookup failure (#1333945)
  (fixed by dropping the revert)
- Auto-sync with upstream master,
  commit 9032070deaa03431921315f973c548c2c403fecc, fixing:
- Correct clog10 documentation (swbz#19673)
- Fix building with -Os (swbz#20729)
- Properly initialize glob structure with GLOB_BRACE|GLOB_DOOFFS (swbz#20707)
- powerpc: Fix TOC stub on powerpc64 clone (swbz#20728)
- math: Make strtod raise "inexact" exceptions (swbz#19380)
- malloc: Remove malloc_get_state, malloc_set_state (swbz#19473)

* Sat Oct 22 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-13
- Auto-sync with upstream master,
  commit e37208ce86916af9510ffb9ce7b3c187986f07de, changing:
- Restore <math.h> compatbility with extern "C" wrappers

* Fri Oct 21 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-12
- Auto-sync with upstream master,
  commit b3918c44db615637b26d919ce599cd86592316b3, fixing:
- math: Turn iszero into a function template (#1387415)
- ARM: Use VSQRT instruction (swbz#20660)
- math: Stop powerpc copysignl raising "invalid" for sNaN (swbz#20718)
- x86: Fix FMA and AVX2 detection (swbz#20689)
- x86: Avoid assertion failure on older Intel CPus (swbz#20647)

* Mon Oct 17 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.24.90-11
- Add prototype support for detecting invalid IFUNC calls (swbz#20019).
- New POSIX thread condition variable implementation (swbz#13165).

* Fri Oct 07 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-10
- Auto-sync with upstream master,
  commit 5140d036f9c16585448b5908c3a219bd96842161, fixing:
- resolv: Remove RES_USEBSTRING and its implementation (swbz#20629)
- Refactor ifunc resolvers due to false debuginfo (swbz#20478)

* Tue Oct 04 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-9
- Auto-sync with upstream master,
  commit ff88ee7edfaa439e23c42fccaf3a36cd5f041894, fixing:
- LONG_WIDTH is incorrectly set to the 64 on 32-bit platforms (#1381582)
- libio: Multiple fixes for open_{w}memstream (swbz#18241, swbz#20181)
- Simplify and test _dl_addr_inside_object (swbz#20292)

* Thu Sep 22 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-8
- Add support for MIPS (#1377795)
- Drop glibc-rh1315476-1.patch (sln pre-processor cleanup), it was
  applied upstream.
- Auto-sync with upstream master,
  commit 17af5da98cd2c9ec958421ae2108f877e0945451, fixing the following bugs:
- Fix non-LE TLS in static programs (swbz#19826)
- resolv: Remove unsupported hook functions from the API (swbz#20016)
- Remove RR type classification macros (swbz#20592)
- Remove obsolete DNSSEC support (swbz#20591)
- manual: Clarify the documentation of strverscmp (swbz#20524)

* Tue Sep 20 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.24.90-7
- Auto-sync with upstream master.

* Thu Sep 01 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-6
- Auto-sync with upstream master,
  commit 4d728087ef8cc826b05bd21d0c74d4eca9b1a27d, fixing:
- Base <sys/quota.h> on Linux headers (#1360480)
- Simplify static malloc interposition (swbz#20432)

* Fri Aug 26 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-5
- Auto-sync with upstream master,
  commit 7e625f7e85b4e88f10dbde35a0641742af581806, fixing:
- lt_LT locale: use hyphens in d_fmt (swbz#20497)
- nptl test time reductions (swbz#19946)

* Sun Aug 21 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-4
- Auto-sync with upstream master,
  commit 66abf9bfbe24ac1e7207d26ccad725ed938dc52c, fixing:
- argp: Do not override GCC keywords with macros (#1366830)

* Wed Aug 17 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-3
- Auto-sync with upstream master,
  commit d9067fca40b8aac156d73cfa44d6875813555a6c, with these changes:
- Avoid duplicating object files already in libc.a (#1352625)
- CVE-2016-6323: Backtraces can hang on ARM EABI (32-bit) (swbz#20435)
- et_EE: locale has wrong {p,n}_cs_precedes value (swbz#20459

* Thu Aug 11 2016 Florian Weimer <fweimer@redhat.com> - 2.24.90-2
- Auto-sync with upstream master,
  commit f79211792127f38d5954419bb3784c8eb7f5e4e5

* Mon Aug 08 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.24.90-1
- Set version to 2.24.90 to match upstream development.

* Mon Aug 08 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.23.90-31
- Auto-sync with upstream master.

* Thu Jul 21 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-30
- Drop sendmsg/recvmsg compatibility patch (#1344830)
- glibc-devel depends on libgcc%%{_isa} (#1289356)
- Drop Requires(pre) on libgcc
- Introduce libcrypt and libcrypt-nss (#1324623)
- Do not try to install mtrace when bootstrapping

* Wed Jul 20 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-29
- Move NSS modules to subpackages (#1338889)

* Wed Jul 13 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-28
- Auto-sync with upstream master, commit
  f531f93056b34800383c5154280e7ba5112563c7.
- Add de_LI.UTF-8 locale.
- Make ldconfig and sln the same binary.  (#1315476)

* Fri Jul 08 2016 Mike FABIAN <mfabian@redhat.com> - 2.23.90-27
- Unicode 9.0.0 updates (ctype, charmap, transliteration) (#1351108)

* Tue Jul 05 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-26
- Auto-sync with upstream master, up to commit
  30e4cc5413f72c2c728a544389da0c48500d9904, fixing these bug:
- strcasecmp failure on ppc64le (#nscd breaks initgroups with nis (initgroups are empty) (#1294574)

* Fri Jun 24 2016 Carlos O'Donell <carlos@redhat.com> - 2.23.90-25
- Properly handle more invalid --install-langs arguments (#1349906).

* Tue Jun 21 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-24
- Auto-sync with upstream master, commit
  a3b473373ee43a292f5ec68a7fda6b9cfb26a9b0, fixing these bugs:
- Unnecessary mmap fallback in malloc (#1348620)
- pwritev system call passes incorrect offset to kernel (#1346070)

* Sat Jun 18 2016 Carlos O'Donell <carlos@redhat.com> - 2.23.90-23
- Use scriptlet expansion in all-langpacks posttrans script to expand
  _install_langes macro.

* Mon Jun 13 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-22
- Remove glibc-fedora-uname-getrlimit.patch.  This patch was
  introduced to fix bug rhbz#579086 (Preloading a replacement uname
  is causing environment to be cleaned if libpthread is loaded).
  UTS namespaces should now offer a cleaner way yo do this.
- Drop sendmmsg/recvmmsg compat symbols on 32-bit architectures (#1344830)
* Sat Jun 11 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-21
- First phase of sendmsg/recvmsg/sendmmsg/recvmmsg ABI revert:
  GLIBC_2.24 compatibility symbols (#1344830)
- Auto-sync with upstream master
  (commit 31d0a4fa646db8b8c97ce24e0ec0a7b73de4fca1),
  fixing the following bugs:
- Add eo locale
- Crash in the nss_db NSS service module during iteration (#1344480)

* Thu Jun 09 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-20
- Auto-sync with upstream master, fixing this bug:
- Emacs crashes on startup (#1342976)

* Wed Jun 01 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-19
- Auto-sync with upstream master.
- Adjust glibc-rh1315108.patch accordingly.
- Fix fork redirection in libpthread (#1326903)
- CVE-2016-4429: stack overflow in Sun RPC clntudp_call (#1337140)
- Do not disable assertions in release builds (#1338887)

* Wed May 11 2016 Carlos O'Donell <carlos@redhat.com> - 2.23.90-18
- Move support for building GCC 2.96 into compat-gcc-296.

* Wed May 11 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-17
- Temporily revert dlsym (RTLD_NEXT)/dlerror change, to unbreak
  ASAN until it is fixed (#1335011)

* Mon May  9 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-16
- Drop the “fix” for fork/vfork NULL symbols in libpthread.  It does
  not work because ld.so apparently supports some variant of direct
  binding.

* Mon May 09 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-15
- Auto-sync with upstream master.
- Drop glibc-nsswitch-Add-group-merging-support.patch, applied upstream.
- Drop glibc-rh1252570.patch, alternative fixes applied upstream.
- Adjust glibc-rh1315108.patch to minor upstream change.
- Update SUPPORTED file.
- Experimental fix for NULL fork/vfork symbols in libpthread (#1326903)

* Tue May 03 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.23.90-14
- Require libselinux for nscd in non-bootstrap configuration.

* Fri Apr 29 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.23.90-13
- Auto-sync with upstream master.

* Thu Apr 28 2016 Carlos O'Donell <carlos@redhat.com> - 2.23.90-12
- Move spec file system information logging to the build stage.

* Thu Apr 14 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-11
- Auto-sync with upstream master.
- Unbreak pread/pread64 on armhfp (#1327277)

* Thu Apr 14 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-10
- Auto-sync with upstream master.

* Thu Apr 14 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-9
- Auto-sync with upstream master.  Removes type union wait.
- Update SUPPORTED locales file.

* Fri Apr 08 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-8
- Auto-sync with upstream master.

* Tue Mar 29 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-7
- Auto-sync with upstream master.
- Adjust glibc-rh1252570.patch to partial upstream fix.
- Drop glibc-fix-an_ES.patch, now included upstream.

* Wed Mar 16 2016 Carlos O'Donell <carlos@redhat.com> - 2.23.90-6
- Use 'an' as language abbreviation for an_ES.

* Mon Mar 07 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.23.90-5
- Auto-sync with upstream master.

* Sun Mar  6 2016 Florian Weimer <fweimer@redhat.com> - 2.23.90-4
- Remove extend_alloca (#1315108)

* Mon Feb 29 2016 Carlos O'Donell <carlos@redhat.com> - 2.23.90-3
- Enhance support for upgrading from a non-language-pack system.

* Fri Feb 26 2016 Mike FABIAN <mfabian@redhat.com> - 2.23.90-2
- Create new language packages for all supported languages.
  Locales, translations, and locale sources are split into
  distinct sub-packages. A meta-package is created for users
  to install all languages. Transparent installation support
  is provided via dnf langpacks.

* Fri Feb 26 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.23.90-1
- Upstream development version is now 2.23.90.

* Thu Feb 25 2016 Carlos O'Donell <carlos@systemhalted.org> - 2.22.90-38
- Auto-sync with upstream master.

* Fri Feb 19 2016 Florian Weimer <fweimer@redhat.com> - 2.22.90-37
- Remove stray newline from Serbian locales (#1114591).

* Tue Feb 16 2016 CArlos O'Donell <carlos@redhat.com> - 2.22.90-36
- Fix CVE-2015-7547: getaddrinfo() stack-based buffer overflow (#1308943).

* Mon Feb 15 2016 Florian Weimer <fweimer@redhat.com> - 2.22.90-35
- Revert may_alias attribute for struct sockaddr (#1306511).
- Revert upstream commit 2212c1420c92a33b0e0bd9a34938c9814a56c0f7 (#1252570).

* Sat Feb 13 2016 Florian Weimer <fweimer@redhat.com> - 2.22.90-34
- Auto-sync with upstream master.
- Support aliasing with struct sockaddr pointers (#1306511).

* Tue Feb 09 2016 Carlos O'Donell <carlos@redhat.com> - 2.22.90-33
- Use --with-cpu=power8 for ppc64le default runtime (#1227361).

* Tue Feb 02 2016 Florian Weimer <fweimer@redhat.com> - 2.22.90-32
- Auto-sync with upstream master.
- Add glibc-isinf-cxx11.patch to improve C++11 compatibility.

* Thu Jan 28 2016 Florian Weimer <fweimer@redhat.com> - 2.22.90-31
- Add workaround for GCC PR69537.

* Thu Jan 28 2016 Florian Weimer <fweimer@redhat.com> - 2.22.90-30
- Auto-sync with upstream master.

* Wed Jan 13 2016 Carlos O'Donell <carlos@redhat.com> - 2.22.90-29
- New pthread_barrier algorithm with improved standards compliance.

* Wed Jan 13 2016 Carlos O'Donell <carlos@redhat.com> - 2.22.90-28
- Add group merging support for distributed management (#1146822).

* Tue Jan 12 2016 Carlos O'Donell <carlos@redhat.com> - 2.22.90-27
- Remove 32-bit POWER support.
- Add 64-bit POWER7 BE and 64-bit POWER8 BE optimized libraries.

* Mon Dec 21 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-26
- Auto-sync with upstream master.

* Wed Dec 16 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-25
- Auto-sync with upstream master.
- Includes fix for malloc assertion failure in get_free_list.  (#1281714)
- Drop Unicode 8.0 patches (now merged upstream).

* Sat Dec  5 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-24
- Put libmvec_nonshared.a into the -devel package.  (#1288738)

* Sat Dec 05 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-23
- Auto-sync with upstream master.

* Thu Nov 26 2015 Carlos O'Donell <carlos@redhat.com> - 2.22.90-22
- The generic hidden directive support is already used for
  preinit/init/fini-array symbols so we drop the Fedora-specific
  patch that does the same thing.
  Reported by Dmitry V. Levin <ldv@altlinux.org>

* Thu Nov 26 2015 DJ Delorie <dj@redhat.com> - 2.22.90-22
- Require glibc-static for C++ tests.
- Require gcc-c++, libstdc++-static, and glibc-static only when needed.
- Fix --without docs to not leave info files.

* Fri Nov 20 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-21
- Auto-sync with upstream master.

* Wed Nov 18 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-20
- Auto-sync with upstream master.

* Wed Nov 18 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-19
- Disable -Werror on s390 (#1283184).

* Mon Nov 16 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-18
- Auto-sync with upstream master.

* Mon Nov 16 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-17
- Revert temporary armhfp build fix.

* Mon Nov  9 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-16
- Apply temporary fix for armhfp build issue.

* Mon Nov 09 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-15
- Auto-sync with upstream master.

* Tue Nov  3 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-14
- Log uname, cpuinfo, meminfo during build (#1276636)

* Fri Oct 30 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-13
- Auto-sync with upstream master.

* Fri Oct 30 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-12
- Revert to upstream implementation of condition variables (#1229659)

* Wed Oct 28 2015 Florian Weimer <fweimer@redhat.com> - 2.22.90-11
- Disable valgrind test on ppc64p7, too.

* Mon Oct 26 2015 Carlos O'Donell <carlos@redhat.com> - 2.22.90-10
- Disable valgrind test for ppc64.

* Wed Oct 21 2015 Carlos O'Donell <carlos@redhat.com> - 2.22.90-9
- Sync with upstream master.
- Update new condvar implementation.

* Fri Oct  9 2015 Carlos O'Donell <carlos@redhat.com> - 2.22.90-8
- Remove libbsd.a (#1193168).

* Wed Sep 16 2015 Mike FABIAN <mfabian@redhat.com> - 2.22.90-7
- Add the C.UTF-8 locale (#902094).

* Wed Sep 16 2015 Carlos O'Donell <carlos@systemhalted.org> - 2.22.90-6
- Fix GCC 5 and -Werror related build failures.
- Fix --install-langs bug which causes SIGABRT (#1262040).

* Fri Aug 28 2015 Carlos O'Donell <carlos@systemhalted.org> - 2.22.90-5
- Auto-sync with upstream master.

* Thu Aug 27 2015 Carlos O'Donell <carlos@redhat.com> - 2.22.90-4
- Build require gcc-c++ for the C++ tests.
- Support --without testsuite option to disable testing after build.
- Support --without benchtests option to disable microbenchmarks.
- Update --with bootstrap to disable benchtests, valgrind, documentation,
  selinux, and nss-crypt during bootstrap.
- Support --without werror to disable building with -Werror.
- Support --without docs to disable build requirement on texinfo.
- Support --without valgrind to disable testing with valgrind.
- Remove c_stubs add-on and enable fuller support for static binaries.
- Remove librtkaio support (#1227855).

* Sun Aug 16 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.22.90-3
- Auto-sync with upstream master.

* Fri Aug 14 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.22.90-2
- Remove initgroups from the default nsswitch.conf (#751450).

* Fri Aug 14 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.22.90-1
- Sync with upstream master.

* Tue Jul 28 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-20
- Sync with upstream master.

* Thu Jul 23 2015 Mike FABIAN <mfabian@redhat.com> - 2.21.90-19
- some more additions to the translit_neutral file by Marko Myllynen

* Tue Jul 14 2015 Mike FABIAN <mfabian@redhat.com> - 2.21.90-18
- Unicode 8.0.0 updates, including the transliteration files (#1238412).

* Sun Jun 21 2015 Carlos O'Donell <carlos@redhat.com> - 2.21.90-17
- Remove all linuxthreads handling from glibc spec file.

* Wed Jun 17 2015 Carlos O'Donell <carlos@redhat.com> - 2.21.90-16
- Move split out architecture-dependent header files into devel package
  and keep generic variant in headers package, thus keeping headers package
  content and file list identical across multilib rpms.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.90-15.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun  3 2015 Carlos O'Donell <carlos@redhat.com> - 2.21.90-15
- Remove patch to increase DTV surplus which is no longer needed after
  upstream commit f8aeae347377f3dfa8cbadde057adf1827fb1d44.

* Sat May 30 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-14
- Fix build failure on aarch64 (#1226459).

* Mon May 18 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-13
- Sync with upstream master.
- Install new condvar implementation.

* Fri May 08 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-12
- Add benchmark comparison scripts.

* Thu May 07 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-11
- Auto-sync with upstream master.
- Revert arena threshold fix to work around #1209451.

* Tue Apr 07 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-10
- Revert last auto-sync (#1209451).

* Mon Apr 06 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-9
- Auto-sync with upstream master.

* Tue Mar 24 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-8
- Auto-sync with upstream master.

* Tue Mar 17 2015 Carlos O'Donell <carlos@redhat.com> - 2.21.90-7
- Use rpm.expand in scripts to reduce set of required RPM features.

* Thu Mar 12 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-6
- Auto-sync with upstream master.

* Tue Mar  3 2015 Mike Fabian <mfabian@redhat.com> - 2.21.90-5
- Support installing only those locales specified by the RPM macro
  %%_install_langs (#156477).

* Mon Feb 23 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21.90-4
- Auto-sync with upstream master.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.21.90-3.1
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 12 2015 Carlos O'Donell <carlos@systemhalted.org> - 2.21.90-3
- Fix missing clock_* IFUNCs in librtkaio.

* Thu Feb 12 2015 Carlos O'Donell <carlos@systemhalted.org> - 2.21.90-2
- Auto-sync with upstream master.

* Wed Feb 11 2015 Carlos O'Donell <carlos@systemhalted.org> - 2.21.90-1
- Add back x86 vDSO support.
- Fix rtkaio build to reference clock_* functions from libc.

* Wed Jan 21 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-20
- Sync with upstream master.
- Disable werror on s390x.
- Revert x86 vDSO support since it breaks i686 rtkaio build.

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.20.90-19
- Drop large ancient ChangeLogs (rhbz #1169546)

* Mon Jan 12 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-18
- Pass address of main_arena.mutex to mutex_lock/unlock.

* Thu Jan 08 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-17
- Define a __tls_get_addr macro to avoid a conflicting declaration.

* Wed Jan 07 2015 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 2.20.90-16
- Disable -Werror for s390 as well.

* Wed Jan 07 2015 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 2.20.90-14
- Sync with upstream master.
- Disable -Werror on powerpc and armv7hl.
- Temporarily disable valgrind test on ppc64.

* Sun Dec 28 2014 Dan Horák <dan[at]danny.cz>
- valgrind available only on selected arches (missing on s390)

* Wed Dec 10 2014 Kyle McMartin <kmcmarti@redhat.com>
- aarch64: Drop strchrnul.S revert, apply fix from Richard Earnshaw.

* Fri Dec 05 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-13
- Fix permission of debuginfo source files to allow multiarch
  debuginfo packages to be installed and upgraded.

* Fri Dec 05 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-12
- Remove LIB_LANG since we don't install locales in /usr/lib/locale anymore.
- Don't own any directories in /usr/share/locale (#1167445).
- Use the %%find_lang macro to get the *.mo files (#1167445).
- Add %%lang tags to language locale files in /usr/share/i18n/locale (#1169044).

* Wed Dec 03 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.20.90-11
- aarch64: revert optimized strchrnul.S implementation (rhbz#1167501)
  until it can be debugged.

* Fri Nov 28 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-10
- Auto-sync with upstream master.

* Wed Nov 19 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-9
- Sync with upstream master.

* Wed Nov 05 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-8
- Make getconf return only /usr/bin (#1138835).
- Sync with upstream master.

* Tue Nov 04 2014 Arjun Shankar <arjun.is@lostca.se> - 2.20.90-7
- Add patch that modifies several tests to use test-skeleton.c.
  The patch is accepted but not yet committed upstream.
  https://sourceware.org/ml/libc-alpha/2014-10/msg00744.html

* Tue Sep 30 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-6
- Sync with upstream master.
- Disable more Intel TSX usage in rwlocks (#1146967).
- Enable lock elision again on s390 and s390x.
- Enable Systemtap SDT probes for all architectures (#985109).

* Fri Sep 26 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-5
- Disable lock elision support for Intel hardware until microcode
  updates can be done in early bootup (#1146967).
- Fix building test tst-strtod-round for ARM.

* Tue Sep 23 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-4
- Sync with upstream master.
- Don't own the common debuginfo directories (#1144853).
- Run valgrind in the %%check section to ensure that it does not break.

* Tue Sep 16 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-3
- Sync with upstream master.
- Revert patch for #737223.

* Mon Sep 08 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-2
- Build build-locale-archive statically again.

* Mon Sep 08 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-1
- Sync with upstream master.

* Thu Sep  4 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-36
- Allow up to 32 dlopened modules to use static TLS (#1124987).
- Run glibc tests in %%check section of RPM spec file.
- Do not run tests with `-k` and fail if any test fails to build.

* Tue Aug 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-35
- Sync with upstream master.
- Use INTERNAL_SYSCALL in TLS_INIT_TP (#1133134).
- Remove gconv loadable module transliteration support (CVE-2014-5119, #1119128).

* Fri Aug 22 2014 Dennis Gilmore <dennis@ausil.us> - 2.19.90-34
- add back sss to nsswitch.conf we have added workarounds in the tools

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 2.19.90-33.1
- Rebuild for rpm bug 1131960

* Tue Aug 19 2014 Dennis Gilmore <dennis@ausil.us> - 2.19.90-33
- remove sss from default nsswitch.conf it causes issues with live image composing

* Wed Aug 13 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-32
- Auto-sync with upstream master.
- Revert to only defining __extern_always_inline for g++-4.3+.
- Fix build failure in compat-gcc-32 (#186410).

* Mon Jul 28 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-31
- Auto-sync with upstream master.

* Wed Jul 23 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-30
- Undo last master sync to fix up rawhide.

* Tue Jul 15 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-29
- Auto-sync with upstream master.

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.19.90-28
- fix license handling

* Mon Jul 07 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-27
- Auto-sync with upstream master.

* Fri Jul 04 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-26
- Sync with upstream roland/nptl branch.
- Improve testsuite failure outputs in build.log

* Thu Jul 03 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-25
- Sync with upstream roland/nptl branch.

* Wed Jul 02 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-24
- Sync with upstream master.

* Tue Jun 24 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-23
- Sync with upstream master.
- Add fix to unbreak i386 ABI breakage due to a change in scalbn.

* Fri Jun 20 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.19.90-22
- AArch64: Save & restore NZCV (flags) upon entry to _dl_tlsdesc_dynamic
  in order to work around GCC reordering compares across the TLS
  descriptor sequence (GCC PR61545.) Committing a (temporary) fix here
  allows us to avoid rebuilding the world with gcc 4.9.0-11.fc21.

* Mon Jun 16 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.19.90-21
- Auto-sync with upstream master.

* Thu Jun 12 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-20
- Auto-sync with upstream master.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.90-19.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-19
- Sync with upstream master.

* Mon May 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-18
- Sync with upstream master.
- Adjust rtkaio patches to build with upstream master.

* Wed May 21 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.19.90-17
- Backport some upstream-wards patches to fix TLS issues on AArch64.

* Wed May 21 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.19.90-16
- AArch64: Fix handling of nocancel syscall failures (#1098327)

* Thu May 15 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-15
- Sync with upstream master.

* Wed May 14 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-14
- Add support for displaying all test results in build logs.

* Wed May 14 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-13
- Add initial support for ppc64le.

* Tue Apr 29 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-12
- Auto-sync with upstream master.
- Remove ports addon.

* Fri Apr 18 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-11
- Sync with upstream master.

* Thu Apr 10 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-10
- Sync with upstream master.

* Thu Apr 03 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-9
- Sync with upstream master.

* Wed Mar 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-8
- Sync with upstream master.

* Wed Mar 19 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-7
- Sync with upstream master.
- Fix offset computation for append+ mode on switching from read (#1078355).

* Wed Mar 12 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-6
- Sync with upstream master.
- Use cleaner upstream solution for -ftree-loop-distribute-patterns (#911307).

* Tue Mar 04 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-5
- Sync with upstream master.

* Thu Feb 27 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-4
- Use nscd service files from glibc sources.
- Make nscd service forking in systemd service file.

* Tue Feb 25 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-3
- Sync with upstream master.
- Separate ftell from fseek logic and avoid modifying FILE data (#1069559).

* Mon Feb 24 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-2
- Fix build-locale-archive failure to open default template.

* Tue Feb 18 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-1
- Sync with upstream master.

* Tue Feb 04 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-27
- Sync with upstream master.

* Wed Jan 29 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-26
- Modify regular expressions to include powerpcle stubs-*.h (#1058258).

* Wed Jan 29 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-25
- Sync with upstream master.

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.18.90-24
- Own the %%{_prefix}/lib/locale dir.

* Thu Jan 23 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-23
- Sync with upstream master.

* Thu Jan 16 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-22
- Back out ftell test case (#1052846).

* Tue Jan 14 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-21
- Sync with upstream master.
- Fix infinite loop in ftell when writing wide char data (#1052846).

* Tue Jan  7 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-20
- Sync with upstream master.
- Enable systemtap probes on Power and S/390.
