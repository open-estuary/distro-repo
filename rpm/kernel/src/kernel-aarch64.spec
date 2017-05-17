# We have to override the new %%install behavior because, well... the kernel is special.
%global __spec_install_pre %{___build_pre}

Summary: The Linux kernel

# %define buildid .1

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

%define rpmversion 4.9.20
%define pkgrelease 3.1.rc1

%define pkg_release %{pkgrelease}.estuary

# The kernel tarball/base version
%define rheltarball %{rpmversion}-%{pkgrelease}

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them.
#
# kernel
%define with_default   %{?_without_default:   0} %{?!_without_default:   1}
# kernel-debug
%define with_debug     %{?_without_debug:     0} %{?!_without_debug:     1}
# kernel-doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       1}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
# perf
%define with_perf      %{?_without_perf:      0} %{?!_without_perf:      1}
# tools
%define with_tools     %{?_without_tools:     0} %{?!_without_tools:     1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# kernel-abi-whitelists
%define with_kernel_abi_whitelists %{?_with_kernel_abi_whitelists: 0} %{?!_with_kernel_abi_whitelists: 1}
%define with_kernel_abi_whitelists 0

# Build the kernel-doc package, but don't fail the build if it botches.
# Here "true" means "continue" and "false" means "fail the build".
%if 0%{?released_kernel}
%define doc_build_fail false
%else
%define doc_build_fail true
%endif

%define rawhide_skip_docs 0
%if 0%{?rawhide_skip_docs}
%define with_doc 0
%define doc_build_fail true
%endif

# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# Only build the debug kernel (--with dbgonly):
%define with_dbgonly   %{?_with_dbgonly:      1} %{?!_with_dbgonly:      0}

# Control whether we perform a compat. check against published ABI.
# %define with_kabichk   %{?_without_kabichk:   0} %{?!_without_kabichk:   1}
%define with_kabichk   0

# should we do C=1 builds with sparse
%define with_sparse    %{?_with_sparse:       1} %{?!_with_sparse:       0}

# Cross compile requested?
%define with_cross    %{?_with_cross:         1} %{?!_with_cross:        0}

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 1

%define signmodules 0

%define make_target bzImage

%define KVERREL %{version}-%{release}.%{_target_cpu}
%define hdrarch %{_target_cpu}
%define asmarch %{_target_cpu}
%define cross_target %{_target_cpu}

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug

# if requested, only build base kernel
%if %{with_baseonly}
%define with_debug 0
%endif

# if requested, only build debug kernel
%if %{with_dbgonly}
%define with_default 0
%define with_tools 0
%define with_perf 0
%endif

# These arches install vdso/ directories.
# %define vdso_arches %{all_x86} x86_64 ppc ppc64 s390 s390x
%define vdso_arches aarch64

# Overrides for generic default options

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_doc 0
%define with_debug 0
%define with_default 0
%define with_headers 0
%define with_tools 0
%define with_perf 0
%define all_arch_configs kernel-%{version}-*.config
%endif

# Per-arch tweaks

%ifarch aarch64
%define asmarch arm64
%define hdrarch arm64
%define all_arch_configs kernel-%{version}-aarch64*.config
%define make_target Image.gz
%define kernel_image arch/arm64/boot/Image.gz
%define image_install_path boot
%define with_doc 0
%endif

# Should make listnewconfig fail if there's config options
# printed out?
%define listnewconfig_fail 1

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# Architectures we build tools/cpupower on
# %define cpupowerarchs x86_64 ppc64
%define cpupowerarchs aarch64

#
# Three sets of minimum package version requirements in the form of Conflicts:
# to versions below the minimum
#

#
# First the general kernel 2.6 required versions as per
# Documentation/Changes
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.0.7-12, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2, device-mapper-libs < 1.02.63-2, mdadm < 3.2.1-5

#
# Then a series of requirements that are distribution specific, either
# because we add patches for something, or the older versions have
# problems with the newer kernel or lack certain things that make
# integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, ipw2200-firmware < 2.4, iwl4965-firmware < 228.57.2, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0, wireless-tools < 29-3

# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  fileutils, module-init-tools >= 3.16-2, initscripts >= 8.11.1-1, grubby >= 8.28-2
%define initrd_prereq  dracut >= 001-7

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#	%%kernel_reqprovconf <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf \
Provides: kernel = %{rpmversion}-%{pkg_release}\
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:.%{1}}\
Provides: kernel-drm = 4.3.0\
Provides: kernel-drm-nouveau = 16\
Provides: kernel-modeset = 1\
Provides: kernel-uname-r = %{KVERREL}%{?1:.%{1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): linux-firmware >= 20100806-2\
Requires(post): %{_sbindir}/new-kernel-pkg\
Requires(preun): %{_sbindir}/new-kernel-pkg\
Conflicts: %{kernel_dot_org_conflicts}\
Conflicts: %{package_conflicts}\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}

Name: kernel-aarch64%{?variant}
Group: System Environment/Kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
ExclusiveArch: aarch64
ExclusiveOS: Linux

%kernel_reqprovconf

#
# List the packages used during the kernel build
#
BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildRequires: xz, findutils, gzip, m4, perl, make >= 3.78, diffutils, gawk
BuildRequires: gcc >= 3.4.2, binutils >= 2.12
BuildRequires: hostname, net-tools, bc
BuildRequires: xmlto, asciidoc, git
BuildRequires: openssl, openssl-devel
BuildRequires: hmaccalc
%ifarch x86_64
BuildRequires: pesign >= 0.109-4
%endif
%if %{with_sparse}
BuildRequires: sparse >= 0.4.1
%endif
%if %{with_perf}
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison
BuildRequires: audit-libs-devel
%endif
%if %{with_tools}
BuildRequires: pciutils-devel gettext
%endif
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
%define debuginfo_args --strict-build-id -r
%endif
%ifarch s390x
# required for zfcpdump
BuildRequires: glibc-static
%endif

#cross compile make
%if %{with_cross}
%define cross_opts CROSS_COMPILE=%{cross_target}-linux-gnu-
%endif

Source0: kernel-%{rpmversion}-%{pkgrelease}.tar.gz

Source1: Makefile.common

Source10: sign-modules
%define modsign_cmd %{SOURCE10}
Source11: x509.genkey
Source12: extra_certificates
# Source13: redhatsecurebootca2.cer
# Source14: redhatsecureboot003.cer

Source15: merge.pl

# %if %{with_kabichk}
# Source18: check-kabi

# Source20: Module.kabi_x86_64
# Source21: Module.kabi_ppc64
# Source22: Module.kabi_s390x

# Source23: kabi_whitelist_ppc64
# Source24: kabi_whitelist_s390x
# Source25: kabi_whitelist_x86_64
# %endif

Source30: Makefile.config

# Source50: kernel-%{version}-x86_64.config
# Source51: kernel-%{version}-x86_64-debug.config

# Source60: kernel-%{version}-ppc64.config
# Source61: kernel-%{version}-ppc64-debug.config

# Source70: kernel-%{version}-s390x.config
# Source71: kernel-%{version}-s390x-debug.config
# Source72: kernel-%{version}-s390x-kdump.config

# Source80: kernel-%{version}-arm64.config
# Source81: kernel-%{version}-arm64-debug.config

# Sources for kernel-tools
Source2000: cpupower.service
Source2001: cpupower.config
Source51: config-arm-generic
Source52: config-local
Source53: config-arm64
Source54: config-nodebug
Source55: config-generic
Source56: config-debug

# Additional patches
#Patch1001: 0001-arm64-prefer-ACPI-by-default.patch
#Patch1002: 0001-net-mlx4_core-enable-enable_4k_uar-by-default.patch
#Patch1003: 0001-DISTROHACK-acpi-spcr-remove-baud-rate-handling.patch

# empty final patch to facilitate testing of kernel patches
Patch999999: linux-kernel-test.patch

BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package -n kernel-doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
%description -n kernel-doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.


%package -n kernel-headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers
%description -n kernel-headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package -n kernel-bootwrapper
Summary: Boot wrapper files for generating combined kernel + initrd images
Group: Development/System
Requires: gzip binutils
%description -n kernel-bootwrapper
Kernel-bootwrapper contains the wrapper code which makes bootable "zImage"
files combining both kernel and initial ramdisk.

%package -n kernel-debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by kernel-debuginfo packages
Group: Development/Debug
%description -n kernel-debuginfo-common-%{_target_cpu}
This package is required by kernel-debuginfo subpackages.
It provides the kernel source files common to all builds.

%if %{with_perf}
%package -n perf
Summary: Performance monitoring for the Linux kernel
Group: Development/System
License: GPLv2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n perf-debuginfo
Summary: Debug information for package perf
Group: Development/Debug
Requires: kernel-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|XXX' -o perf-debuginfo.list}

%package -n python-perf
Summary: Python bindings for apps which will manipulate perf events
Group: Development/Libraries
%description -n python-perf
The python-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%package -n python-perf-debuginfo
Summary: Debug information for package perf python bindings
Group: Development/Debug
Requires: kernel-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n python-perf-debuginfo
This package provides debug information for the perf python bindings.

# the python_sitearch macro should already be defined from above
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{python_sitearch}/perf.so(\.debug)?|XXX' -o python-perf-debuginfo.list}


%endif # with_perf

%if %{with_tools}

%package -n kernel-tools
Summary: Assortment of tools for the Linux kernel
Group: Development/System
License: GPLv2
# Provides:  cpupowerutils = 1:009-0.6.p1
# Obsoletes: cpupowerutils < 1:009-0.6.p1
# Provides:  cpufreq-utils = 1:009-0.6.p1
# Provides:  cpufrequtils = 1:009-0.6.p1
# Obsoletes: cpufreq-utils < 1:009-0.6.p1
# Obsoletes: cpufrequtils < 1:009-0.6.p1
# Obsoletes: cpuspeed < 1:1.5-16
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools
%description -n kernel-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package -n kernel-tools-libs
Summary: Libraries for the kernels-tools
Group: Development/System
License: GPLv2
Provides: kernel-tools-lib
%description -n kernel-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n kernel-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
Group: Development/System
License: GPLv2
Requires: kernel-tools = %{version}-%{release}
# Provides:  cpupowerutils-devel = 1:009-0.6.p1
# Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: kernel-tools-libs = %{version}-%{release}
Provides: kernel-tools-devel
%description -n kernel-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n kernel-tools-debuginfo
Summary: Debug information for package kernel-tools
Group: Development/Debug
Requires: kernel-debuginfo-common-%{_target_cpu} = %{version}-%{release}
Provides: kernel-tools-debuginfo
AutoReqProv: no
%description -n kernel-tools-debuginfo
This package provides debug information for package kernel-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|.*%%{_libdir}/libcpupower.*|.*%%{_bindir}/turbostat(\.debug)?|.*%%{_bindir}/x86_energy_perf_policy(\.debug)?|XXX' -o kernel-tools-debuginfo.list}

%endif # with_tools

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#	%%kernel_debuginfo_package <subpackage>
#
%define kernel_debuginfo_package() \
%package -n kernel-%{?1:%{1}-}debuginfo\
Summary: Debug information for package kernel%{?1:-%{1}}\
Group: Development/Debug\
Requires: kernel-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: kernel%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
AutoReqProv: no\
%description -n kernel-%{?1:%{1}-}debuginfo\
This package provides debug information for package kernel%{?1:-%{1}}.\
This is required to use SystemTap with kernel%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '/.*/%%{KVERREL}%{?1:\.%{1}}/.*|/.*%%{KVERREL}%{?1:\.%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#	%%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package -n kernel%{?1:-%{1}}-devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: kernel%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel-devel = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{?1:.%{1}}\
AutoReqProv: no\
Requires(pre): /usr/bin/find\
Requires: perl\
%description -n kernel%{?1:-%{1}}-devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package -n kernel-%1\
Summary: %{variant_summary}\
Group: System Environment/Kernel\
%kernel_reqprovconf\
%{expand:%%kernel_devel_package %1 %{!?-n:%1}%{?-n:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %1}\
%{nil}

%package -n kernel
Summary: The Linux Kernel
Group: System Environment/Kernel
%kernel_reqprovconf
%description -n kernel
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

# First the auxiliary packages of the main kernel package.
%kernel_devel_package
%kernel_debuginfo_package


# Now, each variant package.

%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description -n kernel-debug
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.

%prep
# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_default}
echo "Cannot build --with baseonly, default kernel build is disabled"
exit 1
%endif
%endif

# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='patch -p1 -F1 -s'
ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  if ! grep -E "^Patch[0-9]+: $patch\$" %{_specdir}/${RPM_PACKAGE_NAME%%%%%{?variant}}.spec ; then
    if [ "${patch:0:8}" != "patch-3." ] ; then
      echo "ERROR: Patch  $patch  not listed as a source patch in specfile"
      exit 1
    fi
  fi 2>/dev/null
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# don't apply patch if it's empty
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}

if [ ! -d kernel-%{rheltarball}/vanilla-%{rheltarball}/ ]; then
	rm -f pax_global_header;
%setup -q -n kernel-%{rheltarball} -c
	mv kernel-%{rheltarball} vanilla-%{rheltarball};
else
	cd kernel-%{rheltarball}/;
fi

if [ -d kernel-%{KVERREL} ]; then
	# Just in case we ctrl-c'd a prep already
	rm -rf deleteme.%{_target_cpu}
	# Move away the stale away, and delete in background.
	mv kernel-%{KVERREL} deleteme.%{_target_cpu}
	rm -rf deleteme.%{_target_cpu} &
fi

cp -rl vanilla-%{rheltarball} kernel-%{KVERREL}
cd kernel-%{KVERREL}

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/config-* .
cp %{SOURCE15} .

# Dynamically generate kernel .config files from config-* files
make -f %{SOURCE30} VERSION=%{version} configs

ApplyOptionalPatch linux-kernel-test.patch

if [ ! -d .git ]; then
    git init
    git config user.email "noreply@centos.org"
    git config user.name "AltArch Kernel"
    git config gc.auto 0
    git add .
    git commit -a -q -m "baseline"
fi

# Apply patches
#git am %{PATCH1001}
#git am %{PATCH1002}
#git am %{PATCH1003}

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl

# This Prevents scripts/setlocalversion from mucking with our version numbers.
touch .scmversion

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

mkdir configs

# Remove configs not for the buildarch
for cfg in kernel-%{version}-*.config; do
  if [ `echo %{all_arch_configs} | grep -c $cfg` -eq 0 ]; then
    rm -f $cfg
  fi
done

%if !%{debugbuildsenabled}
rm -f kernel-%{version}-*debug.config
%endif

%define make make %{?cross_opts}

# now run oldconfig over all the config files
for i in *.config
do
  mv $i .config
  #perl merge.pl config-centos-sig $i > .config
  Arch=`head -1 .config | cut -b 3-`
  %{make} ARCH=$Arch listnewconfig | grep -E '^CONFIG_' >.newoptions || true
#%if %{listnewconfig_fail}
#  if [ -s .newoptions ]; then
#    cat .newoptions
#    exit 1
#  fi
#%endif
  rm -f .newoptions
  %{make} ARCH=$Arch oldnoconfig
  echo "# $Arch" > configs/$i
  cat .config >> configs/$i
done
# end of kernel config
%endif

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null

# remove unnecessary SCM files
find . -name .gitignore -exec rm -f {} \; >/dev/null

cd ..

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

%if %{with_debuginfo}
# This override tweaks the kernel makefiles so that we run debugedit on an
# object before embedding it.  When we later run find-debuginfo.sh, it will
# run debugedit again.  The edits it does change the build ID bits embedded
# in the stripped object, but repeating debugedit is a no-op.  We do it
# beforehand to get the proper final build ID bits into the embedded image.
# This affects the vDSO images in vmlinux, and the vmlinux image in bzImage.
export AFTER_LINK=\
'sh -xc "/usr/lib/rpm/debugedit -b $$RPM_BUILD_DIR -d /usr/src/debug \
    				-i $@ > $@.id"'
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$3
    InstallName=${4:-vmlinuz}

    # Pick the right config file for the kernel we're building
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flavour:+.${Flavour}}

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flavour:+.${Flavour}}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    %if 0%{?stable_update}
    # make sure SUBLEVEL is incremented on a stable release.  Sigh 3.x.
    perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{?stablerev}/" Makefile
    %endif

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}${Flavour:+.${Flavour}}/" Makefile

    # if pre-rc1 devel kernel, must fix up PATCHLEVEL for our versioning scheme
    %if !0%{?rcrev}
    %if 0%{?gitrev}
    perl -p -i -e 's/^PATCHLEVEL.*/PATCHLEVEL = %{upstream_sublevel}/' Makefile
    %endif
    %endif

    # and now to start the build process

    %{make} -s mrproper

    cp %{SOURCE11} .	# x509.genkey
    cp %{SOURCE12} .	# extra_certificates

    cp configs/$Config .config

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    %{make} -s ARCH=$Arch oldnoconfig >/dev/null
    %{make} -s ARCH=$Arch V=1 %{?_smp_mflags} $MakeTarget %{?sparse_mflags}
    %{make} -s ARCH=$Arch V=1 %{?_smp_mflags} modules %{?sparse_mflags} || exit 1

    # from f20 kernel.spec for aarch64; build dtb for now...
%ifarch aarch64
    %{make} -s ARCH=$Arch V=1 dtbs
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    install -m 644 arch/$Arch/boot/dts/*/*.dtb $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer/
    rm -f arch/$Arch/boot/dts/*/*.dtb
%endif

    # Start installing the results
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer

    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
    fi
# EFI SecureBoot signing, x86_64-only
%ifarch x86_64
    %pesign -s -i $KernelImage -o $KernelImage.signed -a %{SOURCE13} -c %{SOURCE14} -n redhatsecureboot003
    mv $KernelImage.signed $KernelImage
%endif
    $CopyKernel $KernelImage \
    		$RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer

    # hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;

    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/kernel
        # Override $(mod-fw) because we don't want it to install any firmware
        # we'll get it from the linux-firmware package and we don't want conflicts
        %{make} -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=
%ifarch %{vdso_arches}
    %{make} -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
    if [ ! -s ldconfig-kernel.conf ]; then
      echo > ldconfig-kernel.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-kernel.conf \
        $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
%endif

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi

%if %{with_kabichk}
    # create the kABI metadata for use in packaging
    # NOTENOTE: the name symvers is used by the rpm backend
    # NOTENOTE: to discover and run the /usr/lib/rpm/fileattrs/kabi.attr
    # NOTENOTE: script which dynamically adds exported kernel symbol
    # NOTENOTE: checksums to the rpm metadata provides list.
    # NOTENOTE: if you change the symvers name, update the backend too
    echo "**** GENERATING kernel ABI metadata ****"
    gzip -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz

    echo "**** kABI checking is enabled in kernel SPEC file. ****"
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        rm $RPM_BUILD_ROOT/Module.kabi # for now, don't keep it around.
    else
        echo "**** NOTE: Cannot find reference Module.kabi file. ****"
    fi
%endif %{with_kabichk}

    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
%ifarch ppc64
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
%ifarch aarch64
#    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/arm/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include

    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/autoconf.h
    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    if test -s vmlinux.id; then
      cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id
    else
	if test -s vmlinux; then
		vmlinux_id=$(file vmlinux   | awk -F '=|,' '{print $(NF-1)}')
		touch vmlinux.id
		echo ${vmlinux_id} > vmlinux.id
	else
	      echo >&2 "*** ERROR *** no vmlinux build ID! ***"
	      exit 1
	fi
    fi

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
      LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      if [ ! -z "$3" ]; then
        sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      fi
    }

    collect_modules_list networking \
    			 'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt2x00(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
			 'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size|ahci_platform_get_resources' 'pktcdvd.ko|dm-mod.ko'
    collect_modules_list drm \
    			 'drm_open|drm_init'
    collect_modules_list modesetting \
    			 'drm_crtc_init'

    # detect missing or incorrect license tags
    rm -f modinfo
    while read i
    do
      echo -n "${i#$RPM_BUILD_ROOT/lib/modules/$KernelVer/} " >> modinfo
      /sbin/modinfo -l $i >> modinfo
    done < modnames

    grep -E -v \
    	  'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' \
	  modinfo && exit 1

    rm -f modinfo modnames

    # Save off the .tmp_versions/ directory.  We'll use it in the
    # __debug_install_post macro below to sign the right things
    # Also save the signing keys so we actually sign the modules with the
    # right key.
%if %{signmodules}
    cp -r .tmp_versions .tmp_versions.sign${Flavour:+.${Flavour}}
    cp signing_key.priv signing_key.priv.sign${Flavour:+.${Flavour}}
    cp signing_key.x509 signing_key.x509.sign${Flavour:+.${Flavour}}
%endif

    # remove files that will be auto generated by depmod at rpm -i time
    for i in alias alias.bin builtin.bin ccwmap dep dep.bin ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols symbols.bin usbmap
    do
      rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$i
    done

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -exec rm -f {} \;
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd kernel-%{KVERREL}

%if %{with_default}
BuildKernel %make_target %kernel_image
%endif

%if %{with_debug}
BuildKernel %make_target %kernel_image debug
%endif

%global perf_make \
  make %{?_smp_mflags} -C tools/perf -s V=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_LIBNUMA=1 NO_STRLCPY=1 prefix=%{_prefix}
%if %{with_perf}
# perf
%{perf_make} all
%{perf_make} man || %{doc_build_fail}
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    make %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   make
   popd
   pushd tools/power/x86/turbostat
   make
   popd
%endif #turbostat/x86_energy_perf_policy
%endif
%endif

%if %{with_doc}
# Make the HTML and man pages.
make htmldocs mandocs || %{doc_build_fail}

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w
%endif

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke 'make modules_sign' and the mod-extra-sign.sh
# commands to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.
#
# Finally, pick a module at random and check that it's signed and fail the build
# if it isn't.

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
  if [ "%{with_debug}" -ne "0" ]; then \
    Arch=`head -1 configs/kernel-%{version}-%{_target_cpu}-debug.config | cut -b 3-` \
    rm -rf .tmp_versions $RPM_BUILD_ROOT/usr/share/perf-core/strace/groups/file \
    mv .tmp_versions.sign.debug .tmp_versions \
    mv signing_key.priv.sign.debug signing_key.priv \
    mv signing_key.x509.sign.debug signing_key.x509 \
    %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}.debug || exit 1 \
  fi \
    if [ "%{with_default}" -ne "0" ]; then \
    Arch=`head -1 configs/kernel-%{version}-%{_target_cpu}.config | cut -b 3-` \
    rm -rf .tmp_versions $RPM_BUILD_ROOT/usr/share/perf-core/strace/groups/file \
    mv .tmp_versions.sign .tmp_versions \
    mv signing_key.priv.sign signing_key.priv \
    mv signing_key.x509.sign signing_key.x509 \
    %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL} || exit 1 \
  fi \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%define __debug_install_post \
  /usr/lib/rpm/find-debuginfo.sh %{debuginfo_args} %{_builddir}/%{?buildsubdir}\
%{nil}

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list -n kernel-debuginfo-common-%{_target_cpu}
%defattr(-,root,root)
%endif

%endif

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd kernel-%{KVERREL}

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{rpmversion}
man9dir=$RPM_BUILD_ROOT%{_datadir}/man/man9

# copy the source over
mkdir -p $docdir
tar -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir

# Install man pages for the kernel API.
mkdir -p $man9dir
find Documentation/DocBook/man -name '*.9.gz' -print0 |
xargs -0 --no-run-if-empty %{__install} -m 444 -t $man9dir $m
ls $man9dir | grep -q '' || > $man9dir/BROKEN
%endif # with_doc

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
%{make} ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do headers_check but don't die if it fails.
%{make} ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check \
     > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   # exit 1
fi

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
     	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

%endif

%if %{with_kernel_abi_whitelists}
# kabi directory
INSTALL_KABI_PATH=$RPM_BUILD_ROOT/lib/modules/kabi-rhel70
mkdir -p $INSTALL_KABI_PATH

# install kabi whitelists
cp %{SOURCE23} %{SOURCE24} %{SOURCE25} $INSTALL_KABI_PATH
%endif  # with_kernel_abi_whitelists

%if %{with_perf}
# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-bin try-install-man
#remove the 'trace' symlink
rm -f %{buildroot}%{_bindir}/trace
# remove the perf-tips
rm -rf %{buildroot}%{_docdir}/perf-tip

# perf-python extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man || %{doc_build_fail}
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
make -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2000} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE2001} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   make DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   make DESTDIR=%{buildroot} install
   popd
%endif #turbostat/x86_energy_perf_policy
%endif

%endif

###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

%if %{with_tools}
%post -n kernel-tools
/sbin/ldconfig

%postun -n kernel-tools
/sbin/ldconfig
%endif

# This macro defines a %%posttrans script for a kernel package.
#	%%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans -n kernel%{?1:-%{1}}}\
%{_sbindir}/new-kernel-pkg --package kernel%{?-v:-%{-v*}} --mkinitrd --dracut --depmod --update %{KVERREL}%{?-v:.%{-v*}} || exit $?\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --rpmposttrans %{KVERREL}%{?1:.%{1}} || exit $?\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#	%%kernel_variant_post [-v <subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:) \
%{expand:%%kernel_variant_posttrans %{?-v*}}\
%{expand:%%post -n kernel%{?-v:-%{-v*}}}\
%{expand:\
%{_sbindir}/new-kernel-pkg --package kernel%{?-v:-%{-v*}} --install %{KVERREL}%{?-v:.%{-v*}} || exit $?\
}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#	%%kernel_variant_preun <subpackage>
#
%define kernel_variant_preun() \
%{expand:%%preun -n kernel%{?1:-%{1}}}\
%{_sbindir}/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}%{?1:.%{1}} || exit $?\
%{nil}

%kernel_variant_preun
%kernel_variant_post 

%kernel_variant_preun debug
%kernel_variant_post -v debug

if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

###
### file lists
###

%if %{with_headers}
%files -n kernel-headers
%defattr(-,root,root)
/usr/include/*
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files -n kernel-doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}
%{_datadir}/man/man9/*
%endif

%if %{with_kernel_abi_whitelists}
%files -n kernel-abi-whitelists
%defattr(-,root,root,-)
/lib/modules/kabi-*
%endif

%if %{with_perf}
%files -n perf
%defattr(-,root,root)
%{_bindir}/perf
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_datadir}/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf

%files -n python-perf
%defattr(-,root,root)
%{python_sitearch}

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo
%defattr(-,root,root)

%files -f python-perf-debuginfo.list -n python-perf-debuginfo
%defattr(-,root,root)
%endif
%endif # with_perf

%if %{with_tools}
%files -n kernel-tools -f cpupower.lang
%defattr(-,root,root)
%ifarch %{cpupowerarchs}
%{_bindir}/cpupower
%ifarch x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_unitdir}/cpupower.service
%{_mandir}/man[1-8]/cpupower*
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%endif
%endif

%if %{with_debuginfo}
%files -f kernel-tools-debuginfo.list -n kernel-tools-debuginfo
%defattr(-,root,root)
%endif

%ifarch %{cpupowerarchs}
%files -n kernel-tools-libs
%defattr(-,root,root)
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.1

%files -n kernel-tools-libs-devel
%defattr(-,root,root)
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%endif

%endif # with_tools

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{1}\
%{expand:%%files -n %{2}}\
%defattr(-,root,root)\
/%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?3:.%{3}}\
/%{image_install_path}/.vmlinuz-%{KVERREL}%{?3:.%{3}}.hmac \
%ifarch aarch64\
/%{image_install_path}/dtb-%{KVERREL}%{?3:.%{3}} \
%endif\
%attr(600,root,root) /boot/System.map-%{KVERREL}%{?3:.%{3}}\
%if %{with_kabichk}\
/boot/symvers-%{KVERREL}%{?3:.%{3}}.gz\
%endif\
/boot/config-%{KVERREL}%{?3:.%{3}}\
%dir /lib/modules/%{KVERREL}%{?3:.%{3}}\
/lib/modules/%{KVERREL}%{?3:.%{3}}/kernel\
/lib/modules/%{KVERREL}%{?3:.%{3}}/build\
/lib/modules/%{KVERREL}%{?3:.%{3}}/source\
/lib/modules/%{KVERREL}%{?3:.%{3}}/extra\
/lib/modules/%{KVERREL}%{?3:.%{3}}/updates\
%ifarch %{vdso_arches}\
/lib/modules/%{KVERREL}%{?3:.%{3}}/vdso\
/etc/ld.so.conf.d/kernel-%{KVERREL}%{?3:.%{3}}.conf\
%endif\
/lib/modules/%{KVERREL}%{?3:.%{3}}/modules.*\
%ghost /boot/initramfs-%{KVERREL}%{?3:.%{3}}.img\
%{expand:%%files -n %{?2:%{2}-}devel}\
%defattr(-,root,root)\
/usr/src/kernels/%{KVERREL}%{?3:.%{3}}\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?3}.list -n %{?2:%{2}-}debuginfo}\
%defattr(-,root,root)\
%endif\
%endif\
%endif\
%{nil}

%kernel_variant_files %{with_default} kernel
%kernel_variant_files %{with_debug} kernel-debug debug

%changelog
* Mon May 09 2016 Christopher Covington <cov@codeaurora.org> [4.2.0-0.28.el7]
- Initial QDF2432 support

* Tue Mar 22 2016 Jim Perrin <jperrin@centos.org> [4.2.0-0.27.el7]
- Initial NXP support

* Thu Feb 25 2016 Jim Perrin <jperrin@centos.org> [4.2.0-0.26.el7]
- Add patches 1008-1012 for APM

* Wed Jan 20 2016 Jim Perrin <jperrin@centos.org [4.2.0-0.25.el7]
- Patch for CVE-2016-0728

* Tue Oct 06 2015 Mark Langsdorf <mlangsdo@redhat.com> [4.2.0-0.21.el7]
- irqchip, gicv3: Fix cpu hangs caused by IAR reader (Robert Richter) [1268381]

* Wed Sep 23 2015 Mark Langsdorf <mlangsdo@redhat.com> [4.2.0-0.20.el7]
- arm64: KVM: add kvm_register_device_ops() in acpi probing code (Wei Huang) [1259615]

* Tue Sep 01 2015 Mark Langsdorf <mlangsdo@redhat.com> [4.2.0-0.19.el7]
- [redhat] rebase to 4.2.0 (Mark Langsdorf)
- phylib: fix device deletion order in mdiobus_unregister() (Mark Langsdorf)
- net: sunrpc: fix tracepoint Warning: unknown op '->' (Pratyush Anand) [1252439]
- drivers: net: xgene: fix: Oops in linkwatch_fire_event (Dean Nelson) [1240785]
- tools lib traceevent: Add checks for returned EVENT_ERROR type (Dean Nelson) [1237310]
- pci: fix gicv2m MSI support (Mark Salter) [1185078]
- [redhat] disable 842 crypto accellerator emulation for ARM64 (Mark Langsdorf) [1254782]
- [redhat] kernel-4.2.0-0.rc5.18.el7 (Mark Langsdorf)
- net, thunder, bgx: Add support to get MAC address from ACPI. (David Daney) [1252569]
- arm64/pci/acpi: Call pcibios_assign_resources later. (David Daney) [1250263]
- [redhat] kernel-4.2.0-0.rc5.17.el7 (Mark Langsdorf)
- DO NOT UPSTREAM: pci, cavium: Fix thunder_pci_requester_id() (David Daney) [1250227]
- arm64:ftrace: add save_stack_trace_regs() (Pratyush Anand) [1247190]
- [redhat] Rebase to 4.2-rc5 (Mark Langsdorf)
- [redhat] kernel-4.2.0-0.rc3.16.el7 (Mark Langsdorf)
- [redhat] add Cavium ThunderX networking to configs (Mark Langsdorf)
- net: cavium: thunder_bgx/nic: Factor out DT specific code (Robert Richter) [1242981]
- net: thunderx: Add receive error stats reporting via ethtool (Robert Richter) [1242981]
- net: thunderx: Receive hashing HW offload support (Robert Richter) [1242981]
- net: thunderx: Fixes for nicvf_set_rxfh() (Robert Richter) [1242981]
- [redhat] DO NOT UPSTREAM: pci, cavium: Disable PEM support (Mark Langsdorf)
- Add Cavium Thunder PCI driver configs. (David Daney) [1242680]
- PCI: Add host drivers for Cavium ThunderX processors. (David Daney) [1242680]
- gic-its: Allow pci_requester_id to be overridden. (David Daney) [1242680]
- ARM64, ACPI, PCI, MSI: I/O Remapping Table (IORT) initial support. (David Daney) [1242995]
- irqchip: gicv3: its: probe ITS in ACPI way (David Daney) [1242995]
- irqchip/GICv3/ITS: refator ITS dt init code to prepare for ACPI (David Daney) [1242995]
- irqchip / GICv3 / ITS: mark its_init() as __init (David Daney) [1242995]
- irqchip / GICv3: remove gic root node in ITS (David Daney) [1242995]
- ACPI, GICV3+: Add support for GICv3+ initialization. (David Daney) [1242995]
- GICv3: Refactor gic_of_init() of GICv3 driver to allow for FDT and ACPI initialization. (David Daney) [1242995]
- arm64, acpi: Implement new "GIC version" field of MADT GIC entry. (David Daney) [1242995]
- arm64: gicv3: its: Add range check for number of allocated pages (David Daney) [1242984]
- irqchip, gicv3-its: Implement Cavium ThunderX errata 22375, 24313 (David Daney) [1242984]
- irqchip, gicv3: Implement Cavium ThunderX erratum 23154 (David Daney) [1242984]
- irqchip, gicv3: Add HW revision detection and configuration (David Daney) [1242984]
- irqchip, gicv3-its: Read typer register outside the loop (David Daney) [1242984]
- DO NOT UPSTREAM PCI: pci: xgene: Use default irq domain for MSI (Iyappan Subramanian) [1247716]
- arm64: Make all entry code as non-kprobe-able (Pratyush Anand) [1234589]
- arm64: Blacklist _mcount for kprobing (Pratyush Anand) [1234589]
- arm64: Add trampoline code for kretprobes (Pratyush Anand) [1234589]
- [redhat] kernel-4.2.0-0.rc3.15.el7 (Mark Langsdorf)
- arm64: Align regs name with latest upstream uapi headers (Pratyush Anand) [1243663]
- arm64: support initrd outside kernel linear map (Mark Salter) [1230869]
- mm: add utility for early copy from unmapped ram (Mark Salter) [1230869]
- arm64: don't panic on crash kernel alloc failure (Mark Salter) [1240381]
- arm64: select uprobe only if kprobe is selected (Pratyush Anand) [1210154]
- [redhat] kernel-4.2.0-0.rc3.14.el7 (Mark Langsdorf)
- crypto: ccp - Provide support to autoload CCP driver (Kim Naru)
- arm64: put cpu_reset in idmap (Mark Salter) [1243150]
- [redhat] rebase to 4.2-rc3 (Mark Langsdorf)
- arm64: perf fixes for 4.1 and 4.2 kernels (Mark Salter) [1243583]
- amd-xgbe-a0: Unify coherency checking logic (Mark Salter) [1243551]
- amd-xgbe-a0: add back CONFIG_AMD_XGBE_PHY (Mark Salter) [1243551]
- sata/xgene: support acpi probing (Mark Salter) [1144036, 1243551]
- [redhat] kernel-4.2.0-0.rc2.13.el7 (Mark Langsdorf)
- [redhat] Rebase to 4.2-rc1 (Mark Langsdorf)
- DO NOT UPSTREAM: move PL011 SBSA init later (Mark Salter)
- [redhat] kernel-4.1.0-0.12.el7 (Mark Langsdorf)
- [redhat] rebase to 4.1 (Mark Langsdorf)
- [redhat] set build targets to rhelsa-7.2-candidate (Mark Langsdorf)
- [redhat] don't build kernel docs - REMOVE ME IF ASKED (Mark Langsdorf)
- Update dynamic ftrace configs (Pratyush Anand) [1186517]
- KVM: Update RHMAINTAINERS (Andrew Jones)
- redhat: Update RHMAINTAINERS for APM (Iyappan Subramanian) [1230887]
- ahci_xgene: set ATA_HORKAGE_NOLPM for all attached disks (Kyle McMartin) [1229454]
- KVM: fix vgic_v2_acpi_probe (Andrew Jones) [1226348]
- crashkernel: Allocate 2G memory for auto reservation (Pratyush Anand)
- DONOTUPSTREAM: arm64: smp_send_stop: increase CPU stop IPI timeout to 60 seconds (Jon Masters) [1218374]
- arm64: move kdump memory init into arm64_memblock_init() (Mark Salter) [1219838]
- arm64: support ACPI tables outside of kernel RAM (Mark Salter) [1219838]
- tty/console: use SPCR table to define console (Torez Smith)
- Add CONFIG_KEXEC_AUTO_RESERVE into generic config (Pratyush Anand) [https://bugzilla.redhat.com/show_bug.cgi?id=1216287]
- crashkernel auto reservation code for ARM64 (Pratyush Anand) [https://bugzilla.redhat.com/show_bug.cgi?id=1216287]
- forward port crashkernel auto reservation code (Dave Young) [https://bugzilla.redhat.com/show_bug.cgi?id=1216287]
- arm64: KVM: Add CPU hyp mode re-initialization to complement KVM CPU reset (Wei Huang) [1169828]
- config: increase CONFIG_CMA_SIZE_MBYTES from 16 to 64MB (Jon Masters) [1201885]
- DO NOT UPSTREAM PCI: X-Gene1: Add ACPI MSI support (Jon Masters) [1201885]
- arm64: kexec: Fix relocate_new_kernel when CONFIG_DEBUG_RODATA is enabled (Pratyush Anand) [1215041]
- arm64: kexec: Remove arm64_kexec_dtb_addr refrences (Pratyush Anand) [1215036]
- arm64: default CPUMASK_OFFSTACK for SMP (Don Dutile)
- arm64: topology: Correct core_id calculation (Don Dutile)
- 	drivers: net: xgene: Add shutdown function (Mark Salter) [1203109]
- arm64: add smp spin-table cpu hotplug support for X-Gene platform (Mark Salter) [1209589]
- Add CRASH_DUMP into generic config (Pratyush Anand)
- arm64: use ioremap_cache in copy_oldmem_page (Pratyush Anand)
- arm64/kdump: Find free area for crash kernel memory (Pratyush Anand)
- arm: kvm: add stub implementation for kvm_cpu_reset() (Pratyush Anand)
- arm64: kvm: add cpu reset at module exit (Pratyush Anand)
- arm64: kvm: add cpu reset hook for cpu hotplug (Pratyush Anand)
- arm64: kvm: allow EL2 context to be reset on shutdown (Pratyush Anand)
- arm64: kvm: add a cpu tear-down function (Pratyush Anand)
- arm64: kdump: do not go into EL2 before starting a crash dump kernel (Pratyush Anand)
- arm64: add kdump support (Pratyush Anand)
- arm64: kdump: implement machine_crash_shutdown() (Pratyush Anand)
- arm64: kdump: reserve memory for crash dump kernel (Pratyush Anand)
- arm64/kexec: Add pr_devel output (Pratyush Anand)
- arm64/kexec: Add core kexec support (Pratyush Anand)
- arm64: Add EL2 switch to soft_restart (Pratyush Anand)
- arm64: Add new hcall HVC_CALL_FUNC (Pratyush Anand)
- arm64: Convert hcalls to use HVC immediate value (Pratyush Anand)
- arm64: Fold proc-macros.S into assembler.h (Pratyush Anand)
- [redhat] kernel-3.19.0-0.69.aa7a (Mark Langsdorf)
- Increase NR_CPUS from 8 to 4096 for RHELSA (Don Dutile) [1189951]
- uprobe: Add uprobe_pre/post_sstep_notifier to NOKPROBE_SYMBOL (Pratyush Anand) [963432]
- ARM64: Add symbols in NOKPROBE_SYMBOL (Pratyush Anand) [963432]
- ARM64: Add uprobe support (Pratyush Anand) [963432]
- ARM64: rename enum debug_el to enum debug_elx to fix "wrong kind of tag" (Pratyush Anand) [963432]
- ARM64: Handle TRAP_BRKPT for user mode as well (Pratyush Anand) [963432]
- ARM64: Handle TRAP_HWBRKPT for user mode as well (Pratyush Anand) [963432]
- ARM64: Re-factor flush_ptrace_access (Pratyush Anand) [963432]
- ARM64: Add helper for link pointer (Pratyush Anand) [963432]
- ARM64: include asm-generic/ptrace.h in asm/ptrace.h (Pratyush Anand) [963432]
- ARM64: fix kgdb_step_brk_fn to ignore other's exception (Pratyush Anand) [963432]
- ARM64: kprobe: Make prepare and handler function struct kprobe independent (Pratyush Anand) [963432]
- kprobes: Add arm64 case in kprobe example module (Pratyush Anand) [963432]
- arm64: Add kernel return probes support (kretprobes) (Pratyush Anand) [963432]
- arm64: Kprobes instruction simulation support (Pratyush Anand) [963432]
- arm64: Kprobes with single stepping support (Pratyush Anand) [963432]
- arm64: Add more test functions to insn.c (Pratyush Anand) [963432]
- arm64: Add HAVE_REGS_AND_STACK_ACCESS_API feature (Pratyush Anand) [963432]
- arm64: don't state topo is unsupported if !acpi (Don Dutile) [1186788]
- arm64: Change 'Call trace' to 'Call Trace' for dump tools (Don Dutile) [1189098]
- ARM64: gic: Do not allow bypass FIQ signals to reach to processor (Pratyush Anand) [1179954]
- kernel-aarch64.spec: disable noarch kernel-doc (Kyle McMartin)
- remove all uses of {name} in kernel-aarch64.spec.template (Mark Langsdorf) [1195790]
- [redhat] kernel-3.19.0-0.68.aa7a (Mark Langsdorf)
- update to 3.19 (Mark Langsdorf)
- kernel-aarch64.spec: implement seperate binary and src rpm names (Mark Langsdorf)
- Rename kernel.spec.template to kernel-aarch64.spec.template (Mark Langsdorf)
- Change extension to aa7a (Mark Langsdorf)
- remove legacy/non-server compile options for arm64 (Mark Langsdorf)
- [redhat] Add and modify redhat configs for 3.19 (Don Dutile)
- amd-xgbe-phy-a0: Add support for XGBE PHY on A0 (Tom Lendacky)
- amd-xgbe-a0: Add support for XGBE on A0 (Tom Lendacky)
- arm64: add smp parking protocol cpu hotplug support for X-Gene platform (Mark Langsdorf) [1175864]
- arm64: remove wfe in arm64 spinlock to workaround Xgene Ax silicon bug (Don Dutile) [1081562]
- xgene: add support for ACPI-probed serial port (Donald Dutile) [1144036]
- Change POWER_RESET_XGENE to POWER_RESET_SYSCON (Don Dutile) [1065469]
- arm64: Select reboot driver for X-Gene platform (Don Dutile) [1065469]
- power: reset: Add generic SYSCON register mapped reset (Mark Langsdorf) [1065469]
- virtio-mmio: add ACPI probing (Don Dutile) [1093352]
- net: smc91x: add ACPI probing support (Mark Langsdorf) [1093352]
- add support for ACPI identification to xhci-platform (Mark Langsdorf) [1080659]
- make xhci platform driver use 64 bit or 32 bit DMA (Mark Langsdorf) [1080659]
- DO NOT UPSTREAM: redhat: arm64: topology: Adjust sysfs topology (Don Dutile) [1056268 1127292]
- arm64: add sev to parking protocol (Mark Salter)
- arm64: add parking protocol support (Mark Salter)
- KVM/ACPI: Enable ACPI support for virt arch timer (Wei Huang) [1144036]
- Revert "arm64: kill flush_cache_all()" (Mark Langsdorf)
- arm/arm64: DT: Fix GICv2 CPU interface size (Don Dutile)
- arm: amba: of_platform_populate try deferred devices again (Andrew Jones) [963483]
- arm64: don't set READ_IMPLIES_EXEC for EM_AARCH64 ELF objects (Kyle McMartin) [1085528]
- pci: add support for setting DMA ops from ACPI info (Mark Salter)
- DO NOT UPSTREAM - pci/xgene: Provide fixup for ACPI MCFG support (Mark Salter) [1185078]
- DO NOT UPSTREAM - provide hook for MCFG fixups (Mark Salter) [1185078]
- arm64/pci/acpi: initial support for ACPI probing of PCI (Mark Salter) [1185078]
- pci, acpi: Share ACPI PCI config space accessors. (Mark Salter) [1185078]
- x86, acpi, pci: mmconfig_64.c becomes default implementation for arch agnostic low-level direct PCI config space accessors via MMCONFIG. (Mark Salter) [1185078]
- x86, acpi, pci: mmconfig_{32, 64}.c code refactoring - remove code duplication. (Mark Salter) [1185078]
- x86, acpi, pci: Move PCI config space accessors. (Mark Salter) [1185078]
- x86, acpi, pci: Move arch-agnostic MMCFG code out of arch/x86/ directory (Mark Langsdorf) [1185078]
- x86, acpi, pci: Reorder logic of pci_mmconfig_insert() function (Mark Salter) [1185078]
- DO NOT UPSTREAM YET: Clean up GIC irq domain for ACPI (Mark Langsdorf)
- DO NOT UPSTREAM YET: Introducing ACPI support for GICv2m (Mark Salter) [1185078]
- PCI/MSI: Drop domain field from msi_controller (Mark Salter) [1185078]
- PCI/MSI, xgene: Remove references to mchip.domain in pci-xgene-msi (Mark Langsdorf)
- irqchip: gicv3-its: Get rid of struct msi_controller (Marc Zyngier)
- irqchip: GICv2m: Get rid of struct msi_controller (Mark Salter) [1185078]
- PCI/MSI: Let pci_msi_get_domain use struct device's msi_domain (Mark Salter) [1185078]
- PCI/MSI: of: Allow msi_domain lookup using the PHB node (Mark Salter) [1185078]
- PCI/MSI: of: Add support for OF-provided msi_domain (Mark Salter) [1185078]
- PCI/MSI: Add hooks to populate the msi_domain field (Mark Salter) [1185078]
- device core: Introduce per-device MSI domain pointer (Mark Salter) [1185078]
- arm64/perf: add ACPI support (Mark Salter) [1152120]
- acpi: add utility to test for device dma coherency (Mark Salter) [1144036]
- crash: enable /dev/crash driver (Mark Langsdorf) [1077329]
- arm64/acpi: DO NOT UPSTREAM set ACPI enabled by default (Mark Langsdorf)
- acpi/arm64: remove EXPERT dependency (Mark Salter) [1163947]
- [debuginfo] enable generation (Donald Dutile)
- [redhat] Import redhat/ subdirectory (Mark Langsdorf)

