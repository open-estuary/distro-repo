# rpmbuild parameters:
# --define "binutils_target arm-linux-gnu" to create arm-linux-gnu-binutils.
# --with debug: Build without optimizations and without splitting the debuginfo.
# --without testsuite: Do not run the testsuite.  Default is to run it.
# --with testsuite: Run the testsuite.  Default --with debug is not to run it.

# For DTS-6 on RHEL-6 we only support x86 and x86_64.
# For DTS-6 on RHEL-7 we also support ppc64, ppc64le, s390x and aarch64
%define scl devtoolset-6
%global scl_prefix devtoolset-6

%{?scl:%{?scl_package:%scl_package binutils}}

%if 0%{!?binutils_target:1}
%define binutils_target %{_target_platform}
%define isnative 1
%define enable_shared 1
%else
%define cross %{binutils_target}-
%define isnative 0
%define enable_shared 0
%endif
# Disable deterministic archives by default.
# This is for package builders who do not want to have to change
# their build scripts to work with deterministic archives.
%define enable_deterministic_archives 0
# BZ 1342618: Enable support for GCC LTO compilation.
%define enable_lto 1
# Disable the default generation of compressed debug sections.
%define default_compress_debug 0

Summary: A GNU collection of binary utilities
Name: %{?scl_prefix}%{?cross}binutils%{?_with_debug:-debug}
Version: 2.27
Release: 10%{?dist}
License: GPLv3+
Group: Development/Tools
URL: http://sources.redhat.com/binutils

# Note - the Linux Kernel binutils releases are too unstable and contain too
# many controversial patches so we stick with the official FSF version
# instead.

Source: http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2

Source2: binutils-2.19.50.0.1-output-format.sed

Patch01: binutils-2.20.51.0.2-libtool-lib64.patch
Patch02: binutils-2.20.51.0.10-ppc64-pie.patch
Patch03: binutils-2.20.51.0.2-ia64-lib64.patch
Patch04: binutils-2.25-version.patch
Patch05: binutils-2.25-set-long-long.patch
Patch06: binutils-2.20.51.0.10-sec-merge-emit.patch
# Enable -zrelro by default: BZ #621983
Patch07: binutils-2.22.52.0.1-relro-on-by-default.patch
# Local patch - export demangle.h with the binutils-devel rpm.
Patch08: binutils-2.22.52.0.1-export-demangle.h.patch
# Disable checks that config.h has been included before system headers.  BZ #845084
Patch09: binutils-2.22.52.0.4-no-config-h-check.patch
# Fix addr2line to use the dynamic symbol table if it could not find any ordinary symbols.
Patch10: binutils-2.23.52.0.1-addr2line-dynsymtab.patch
# Fix detections little endian PPC shared libraries
Patch11: binutils-2.24-ldforcele.patch
# Import H.J.Lu's Kernel LTO patch.
Patch12: binutils-2.26-lto.patch
Patch13: binutils-2.23.51.0.3-Provide-std-tr1-hash.patch
Patch14: binutils-rh1038339.patch
Patch15: binutils-2.24-rh919508.patch
# Fix the computation of the value for the sh_info field of the .dynsym section.
Patch16: binutils-2.27-local-dynsym-count.patch
# Sort section headers according to increasing section offset.
Patch17: binutils-2.27-monotonic-section-offsets.patch
# Really enable -z relro by default for aarch64
Patch18: binutils-2.27-aarch64-relro-default.patch
# Add support for the Power9 architecture
Patch19: binutils-2.27-power9.patch

Provides: bundled(libiberty)

%define gold_arches %ix86 x86_64 %arm aarch64

%ifarch %gold_arches
%define build_gold	both
%else
%define build_gold	no
%endif

%define alternatives_cmd %{!?scl:%{_sbindir}}%{?scl:%{_root_sbindir}}/alternatives
%define alternatives_cmdline %{alternatives_cmd}%{?scl: --altdir %{_sysconfdir}/alternatives --admindir %{_scl_root}/var/lib/alternatives}

%if 0%{?_with_debug:1}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%define run_testsuite 0%{?_with_testsuite:1}
%else
%define run_testsuite 0%{!?_without_testsuite:1}
%endif

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel
# BZ 920545: We need pod2man in order to build the manual pages.
BuildRequires: /usr/bin/pod2man
# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{run_testsuite}
# relro_test.sh uses dc which is part of the bc rpm, hence its inclusion here.
BuildRequires: dejagnu, zlib-static, glibc-static, sharutils, bc
%if "%{build_gold}" == "both"
# The GOLD testsuite needs a static libc++
%if 0%{?rhel} >= 7
BuildRequires: libstdc++-static
%endif
%endif
%endif
Conflicts: gcc-c++ < 4.0.0
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%ifarch ia64
Obsoletes: gnupro <= 1117-1
%endif
%{?scl:Requires:%scl_runtime}

# The higher of these two numbers determines the default ld.
%{!?ld_bfd_priority: %global ld_bfd_priority	50}
%{!?ld_gold_priority:%global ld_gold_priority	30}

%if "%{build_gold}" == "both"
Requires(post): coreutils
Requires(post): %{alternatives_cmd}
Requires(preun): %{alternatives_cmd}
%endif

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

%package devel
Summary: BFD and opcodes static and dynamic libraries and header files
Group: System Environment/Libraries
Provides: binutils-static = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: %{?scl_prefix}binutils = %{version}-%{release}
Requires: zlib-devel
# BZ 1215242: We need touch...
Requires: coreutils

%description devel
This package contains BFD and opcodes static and dynamic libraries.

The dynamic libraries are in this package, rather than a seperate
base package because they are actually linker scripts that force
the use of the static libraries.  This is because the API of the
BFD library is too unstable to be used dynamically.

The static libraries are here because they are now needed by the
dynamic libraries.

Developers starting new projects are strongly encouraged to consider
using libelf instead of BFD.

%prep
%setup -q -n binutils-%{version}
%patch01 -p1 -b .libtool-lib64~
%patch02 -p1 -b .ppc64-pie~
%ifarch ia64
%if "%{_lib}" == "lib64"
%patch03 -p1 -b .ia64-lib64~
%endif
%endif
%patch04 -p1 -b .version~
%patch05 -p1 -b .set-long-long~
%patch06 -p1 -b .sec-merge-emit~
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch07 -p1 -b .relro~
%endif
%patch08 -p1 -b .export-demangle-h~
%patch09 -p1 -b .no-config-h-check~
%patch10 -p1 -b .addr2line~
%ifarch ppc64le
%patch11 -p1 -b .ldforcele~
%endif
%patch12 -p1 -b .kernel-lto~
%patch13 -p1 -b .provide-hash~
%patch14 -p1 -b .manpage~
%patch15 -p1 
%patch16 -p1 
%patch17 -p1 
%patch18 -p1 
%patch19 -p1 

# We cannot run autotools as there is an exact requirement of autoconf-2.59.

# On ppc64 and aarch64, we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c
sed -i -e '/common_pagesize/s/4 /64 /' gold/powerpc.cc
sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc
# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi
# $PACKAGE is used for the gettext catalog name.
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{?cross}/' */configure
# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done
touch */configure

%ifarch %{power64}
%define _target_platform %{_arch}-%{_vendor}-%{_host_os}
%endif

%build
echo target is %{binutils_target}
%ifarch %{power64}
#CFLAGS=`echo $RPM_OPT_FLAGS | sed -e -s "s/-Werror//g"`
#export CFLAGS
export CFLAGS="$RPM_OPT_FLAGS -Wno-error"
%else
export CFLAGS="$RPM_OPT_FLAGS"
%endif
CARGS=

case %{binutils_target} in i?86*|sparc*|ppc*|s390*|sh*|arm*|aarch64*)
  CARGS="$CARGS --enable-64-bit-bfd"
  ;;
esac

case %{binutils_target} in ia64*)
  CARGS="$CARGS --enable-targets=i386-linux"
  ;;
esac

case %{binutils_target} in ppc*|ppc64*)
  CARGS="$CARGS --enable-targets=spu"
  ;;
esac

case %{binutils_target} in ppc64-*)
  CARGS="$CARGS --enable-targets=powerpc64le-linux"
  ;;
esac

case %{binutils_target} in  ppc64le*)
    CARGS="$CARGS --enable-targets=powerpc-linux"
    ;;
esac

%if 0%{?_with_debug:1}
CFLAGS="$CFLAGS -O0 -ggdb2 -Wno-error -D_FORTIFY_SOURCE=0"
%define enable_shared 0
%endif

# We could optimize the cross builds size by --enable-shared but the produced
# binaries may be less convenient in the embedded environment.
# The seemingly unncessary --with-sysroot argument is merely meant to enable
# sysroot capabilities in the resulting executables.  That allows customers
# to then use the sysroot capability to set up host-x-host build environments
# easier.
%configure \
  --build=%{_target_platform} --host=%{_target_platform} \
  --target=%{binutils_target} \
  --with-sysroot=/ \
%ifarch %gold_arches
%if "%{build_gold}" == "both"
  --enable-gold=default --enable-ld \
%else
  --enable-gold \
%endif
%endif
%if %{isnative}
  --with-sysroot=/ \
%else
  --enable-targets=%{_host} \
  --with-sysroot=%{_prefix}/%{binutils_target}/sys-root \
  --program-prefix=%{cross} \
%endif
%if %{enable_shared}
  --enable-shared \
%else
  --disable-shared \
%endif
%if %{enable_deterministic_archives}
  --enable-deterministic-archives \
%else    
  --enable-deterministic-archives=no \
%endif
%if %{enable_lto}
  --enable-lto \
%endif
%if %{default_compress_debug}
  --enable-compressed-debug-sections=all \
%else
  --enable-compressed-debug-sections=none \
%endif
  $CARGS \
  --enable-plugins \
  --with-bugurl=http://bugzilla.redhat.com/bugzilla/

make %{_smp_mflags} tooldir=%{_prefix} all
make %{_smp_mflags} tooldir=%{_prefix} info

# Do not use %%check as it is run after %%install where libbfd.so is rebuild
# with -fvisibility=hidden no longer being usable in its shared form.
%if !%{run_testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
make -k check < /dev/null || :
echo ====================TESTING=========================
cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
echo ====================TESTING END=====================
for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
do
  ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}.tar.bz2
rm -f binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%if %{isnative}
make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info

# Rebuild libiberty.a with -fPIC.
# Future: Remove it together with its header file, projects should bundle it.
make -C libiberty clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libiberty

# Rebuild libbfd.a with -fPIC.
# Without the hidden visibility the 3rd party shared libraries would export
# the bfd non-stable ABI.
make -C bfd clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS -fvisibility=hidden" -C bfd

# Rebuild libopcodes.a with -fPIC.
make -C opcodes clean
make CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C opcodes

install -m 644 bfd/libbfd.a %{buildroot}%{_libdir}
install -m 644 libiberty/libiberty.a %{buildroot}%{_libdir}
install -m 644 include/libiberty.h %{buildroot}%{_prefix}/include
install -m 644 opcodes/libopcodes.a %{buildroot}%{_libdir}
# Remove Windows/Novell only man pages
rm -f %{buildroot}%{_mandir}/man1/{dlltool,nlmconv,windmc,windres}*

%if %{enable_shared}
chmod +x %{buildroot}%{_libdir}/lib*.so*
%endif

# Prevent programs from linking against libbfd and libopcodes
# dynamically, as they are change far too often.
rm -f %{buildroot}%{_libdir}/lib{bfd,opcodes}.so

# Remove libtool files, which reference the .so libs
rm -f %{buildroot}%{_libdir}/lib{bfd,opcodes}.la

# Sanity check --enable-64-bit-bfd really works.
grep '^#define BFD_ARCH_SIZE 64$' %{buildroot}%{_prefix}/include/bfd.h
# Fix multilib conflicts of generated values by __WORDSIZE-based expressions.
%ifarch %{ix86} x86_64 ppc %{power64} s390 s390x sh3 sh4 sparc sparc64 arm
sed -i -e '/^#include "ansidecl.h"/{p;s~^.*$~#include <bits/wordsize.h>~;}' \
    -e 's/^#define BFD_DEFAULT_TARGET_SIZE \(32\|64\) *$/#define BFD_DEFAULT_TARGET_SIZE __WORDSIZE/' \
    -e 's/^#define BFD_HOST_64BIT_LONG [01] *$/#define BFD_HOST_64BIT_LONG (__WORDSIZE == 64)/' \
    -e 's/^#define BFD_HOST_64_BIT \(long \)\?long *$/#if __WORDSIZE == 32\
#define BFD_HOST_64_BIT long long\
#else\
#define BFD_HOST_64_BIT long\
#endif/' \
    -e 's/^#define BFD_HOST_U_64_BIT unsigned \(long \)\?long *$/#define BFD_HOST_U_64_BIT unsigned BFD_HOST_64_BIT/' \
    %{buildroot}%{_prefix}/include/bfd.h
%endif
touch -r bfd/bfd-in2.h %{buildroot}%{_prefix}/include/bfd.h

# Generate .so linker scripts for dependencies; imported from glibc/Makerules:

# This fragment of linker script gives the OUTPUT_FORMAT statement
# for the configuration we are building.
OUTPUT_FORMAT="\
/* Ensure this .so library will not be used by a link for a different format
   on a multi-architecture system.  */
$(gcc $CFLAGS $LDFLAGS -shared -x c /dev/null -o /dev/null -Wl,--verbose -v 2>&1 | sed -n -f "%{SOURCE2}")"

tee %{buildroot}%{_libdir}/libbfd.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

/* The libz dependency is unexpected by legacy build scripts.  */
/* The libdl dependency is for plugin support.  (BZ 889134)  */
INPUT ( %{_libdir}/libbfd.a -liberty -lz -ldl )
EOH

tee %{buildroot}%{_libdir}/libopcodes.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOH

%else # !%{isnative}
# For cross-binutils we drop the documentation.
rm -rf %{buildroot}%{_infodir}
# We keep these as one can have native + cross binutils of different versions.
#rm -rf %{buildroot}%{_prefix}/share/locale
#rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_libdir}/libiberty.a
%endif # !%{isnative}

# This one comes from gcc
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_prefix}/%{binutils_target}

%find_lang %{?cross}binutils
%find_lang %{?cross}opcodes
%find_lang %{?cross}bfd
%find_lang %{?cross}gas
%find_lang %{?cross}gprof
cat %{?cross}opcodes.lang >> %{?cross}binutils.lang
cat %{?cross}bfd.lang >> %{?cross}binutils.lang
cat %{?cross}gas.lang >> %{?cross}binutils.lang
cat %{?cross}gprof.lang >> %{?cross}binutils.lang

if [ -x ld/ld-new ]; then
  %find_lang %{?cross}ld
  cat %{?cross}ld.lang >> %{?cross}binutils.lang
fi
if [ -x gold/ld-new ]; then
  %find_lang %{?cross}gold
  cat %{?cross}gold.lang >> %{?cross}binutils.lang
fi

%clean
rm -rf %{buildroot}

%post
%if "%{build_gold}" == "both"
%__rm -f %{_bindir}/%{?cross}ld
%{alternatives_cmdline} --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.bfd %{ld_bfd_priority}
%{alternatives_cmdline} --install %{_bindir}/%{?cross}ld %{?cross}ld \
  %{_bindir}/%{?cross}ld.gold %{ld_gold_priority}
%{alternatives_cmdline} --auto %{?cross}ld
%endif
%if %{isnative}
/sbin/ldconfig
# For --excludedocs:
if [ -e %{_infodir}/binutils.info.gz ]
then
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/as.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/ld.info.gz
fi
%endif # %{isnative}
exit 0

%preun
%if "%{build_gold}" == "both"
if [ $1 = 0 ]; then
  %{alternatives_cmdline} --remove %{?cross}ld %{_bindir}/%{?cross}ld.bfd
  %{alternatives_cmdline} --remove %{?cross}ld %{_bindir}/%{?cross}ld.gold
fi
%endif
%if %{isnative}
if [ $1 = 0 ]; then
  if [ -e %{_infodir}/binutils.info.gz ]
  then
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/as.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/binutils.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gprof.info.gz
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/ld.info.gz
  fi
fi
%endif
exit 0

%if %{isnative}
%postun -p /sbin/ldconfig
%endif # %{isnative}

%files -f %{?cross}binutils.lang
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{?cross}[!l]*
%if "%{build_gold}" == "both"
%{_bindir}/%{?cross}ld.*
%ghost %{_bindir}/%{?cross}ld
%else
%{_bindir}/%{?cross}ld*
%endif
%{_mandir}/man1/*
%if %{enable_shared}
%{_libdir}/lib*.so
%exclude %{_libdir}/libbfd.so
%exclude %{_libdir}/libopcodes.so
%endif

%if %{isnative}
%{_infodir}/[^b]*info*
%{_infodir}/binutils*info*

%files devel
%defattr(-,root,root,-)
%{_prefix}/include/*
%{_libdir}/lib*.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so
%{_infodir}/bfd*info*

%endif # %{isnative}

%changelog
* Wed Sep 28 2016 Nick Clifton  <nickc@redhat.com> 2.27-10
- Use correct default sysroot for native targets.
- Add Power9 ISA 3.0 support.

* Mon Sep 05 2016 Carlos O'Donell <carlos@redhat.com>  2.27-9
- Enable '--sysroot' option support for all configurations.

* Thu Sep 01 2016 Nick Clifton  <nickc@redhat.com> 2.27-8
- Properly disable the default generation of compressed debug sections.
  (#1366182)

* Thu Aug 18 2016 Nick Clifton  <nickc@redhat.com> 2.27-7
- Allow -z relro to be enabled by default for the AArch64 target.
  (#1367862)

* Wed Aug 17 2016 Nick Clifton  <nickc@redhat.com> 2.27-6
- Move .shstrtab section to end of section list so that the monotonic ordering of section offsets is restored.
  (#1366145)

* Fri Aug 12 2016 Nick Clifton  <nickc@redhat.com> 2.27-5
- Fix the computation of the sh_info field in the header of the .dynsym section.
  (#1366185)

* Thu Aug 04 2016 Nick Clifton  <nickc@redhat.com> 2.27-4
- Rebase on official FSF binutils 2.27 release.
  (#1358353)

* Thu Jul 21 2016 Nick Clifton  <nickc@redhat.com> 2.27-3
- Version bump so that the Brew build can be rerun, this time including ppc64 (big-endian)
  (#1358353)

* Wed Jul 20 2016 Nick Clifton  <nickc@redhat.com> 2.27-2
- Remove sim sources from tarball.
  (#1358353)

* Mon Jul 18 2016 Nick Clifton  <nickc@redhat.com> 2.27-1
- Rebase on FSF binutils 2.27 release. (#1356661)
- Retire: binutils-2.20.51.0.10-copy-osabi.patch
- Retire: binutils-2.23.2-aarch64-em.patch
- Retire: binutils-2.23.51.0.3-arm-ldralt.patch
- Retire: binutils-2.23.52.0.1-revert-pr15149.patch
- Retire: binutils-2.25.1-gold-testsuite-fixes.patch
- Retire: binutils-2.25-kernel-ld-r.bugfix.patch
- Retire: binutils-2.25-kernel-ld-r.patch
- Retire: binutils-2.25-only-keep-debug.patch
- Retire: binutils-2.25-x86_64-pie-relocs.patch
- Retire: binutils-pr18879.patch
- Retire: binutils-rh1224751.patch
- Retire: binutils-rh1309347.patch
- Retire: binutils-rh895241.patch

* Mon Apr 04 2016 Patsy Franklin <pfrankli@redhat.com> 2.25.1-10
- Fix a case where a string was being used after the memory
  containing the string had been freed.

* Wed Mar 02 2016 Nick Clifton <nickc@redhat.com> 2.25.1-9
- Bump release number by 2 in order to enable build.

* Wed Mar 02 2016 Nick Clifton <nickc@redhat.com> 2.25.1-7
- Fix GOLD testsuite failures.
  (#1312376)

* Thu Feb 25 2016 Nick Clifton <nickc@redhat.com> 2.25.1-6
- Change ar's default to be the creation of non-deterministic archives.

* Thu Feb 18 2016 Nick Clifton <nickc@redhat.com> 2.25.1-4
- Add support for Intel Memory Protection Key instructions.
  (#1309347)

* Thu Feb 04 2016 Nick Clifton <nickc@redhat.com> 2.25.1-2
- Import patch for FSF PR 18879
  (#1260034)

* Thu Jan 14 2016 Nick Clifton <nickc@redhat.com> 2.25.1-1
- Rebase on FSF binutils 2.25.1 release.
- Retire patch binutils-2.25-x86_64-pie-relocs.patch

* Tue Sep 22 2015 Nick Clifton <nickc@redhat.com> 2.25-10
- Improved patch to preserve the sh_link and sh_info fields in stripped ELF sections.
  (#1246390)

* Wed Aug 5 2015 Nick Clifton <nickc@redhat.com> 2.25-9
- Import patch from FSF to preserve the sh_link and sh_info fields in stripped ELF sections.
  (#1246390)

* Tue Aug 4 2015 Jeff Law <law@redhat.com> 2.25-8
- Backport Cary's patch to silence pedantic warning in gold
  (#895241)

* Thu Jun 4 2015 Jeff Law <law@redhat.com> 2.25-7
- Resync with Fedora (binutils-2.25)
  Reapply DTS specific patches
  Backport testsuite patch to fix gold testsuite failure
  
