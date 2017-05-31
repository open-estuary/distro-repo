%global DATE 20160603
%global SVNREV 246806
%global gcc_version 5.4.1
%global gcc_major 5
%global nvptx_tools_gitrev c28050f60193b3b95a18866a96f03334e874e78f
%global nvptx_newlib_gitrev aadc8eb0ec43b7cd0dd2dfb484bae63c8b05ef24
%define binsuffix 5

# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 4.1
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
# Hardening slows the compiler way too much.
%undefine _hardened_build
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64
%global build_ada 1
%else
%global build_ada 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} %{mips}
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm}
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 ppc64 ppc64le
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 ppc64 ppc64le
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm}
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifarch %{ix86} x86_64
%global build_libmpx 1
%else
%global build_libmpx 0
%endif
%global build_isl 1
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch x86_64
%global build_offload_nvptx 1
%else
%global build_offload_nvptx 0
%endif
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64 ppc64p7
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc5
Version:   5.4.1
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-6-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
# The source for nvptx-tools package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone https://github.com/MentorEmbedded/nvptx-tools.git
# cd nvptx-tools
# git archive origin/master --prefix=nvptx-tools-%{nvptx_tools_gitrev}/ | bzip2 -9 > ../nvptx-tools-%{nvptx_tools_gitrev}.tar.bz2
# cd ..; rm -rf nvptx-tools
Source1: nvptx-tools-%{nvptx_tools_gitrev}.tar.bz2
# The source for nvptx-newlib package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone https://github.com/MentorEmbedded/nvptx-newlib.git
# cd nvptx-newlib
# git archive origin/master --prefix=nvptx-newlib-%{nvptx_newlib_gitrev}/ | bzip2 -9 > ../nvptx-newlib-%{nvptx_newlib_gitrev}.tar.bz2
# cd ..; rm -rf nvptx-newlib
Source2: nvptx-newlib-%{nvptx_newlib_gitrev}.tar.bz2
%global isl_version 0.16.1
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
BuildRequires: binutils >= 2.24
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
BuildRequires: python2-devel, python34-devel
%if %{build_go}
BuildRequires: hostname, procps
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}
%if 0%{?__isa_bits} == 64
Requires: libisl.so.15()(64bit)
%else
Requires: libisl.so.15
%endif
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
Requires: cpp%{binsuffix} = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
Requires: binutils >= 2.24
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc%{binsuffix} >= %{version}-%{release}
Requires: libgomp%{binsuffix} = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
%endif
Obsoletes: gcc-java < %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true
Provides: bundled(libiberty)
Provides: gcc(major) = %{gcc_major}

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc ppc64p7
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc ppc64p7
%global gcc_target_platform %{_target_platform}
%endif

%description
The gcc5 package contains the GNU Compiler Collection version 5.
You'll need this package in order to compile C code.

%package -n libgcc%{binsuffix}
Summary: GCC version 5 shared support library
Group: System Environment/Libraries
Autoreq: false
%if !%{build_ada}
Obsoletes: libgnat < %{version}-%{release}
%endif
Obsoletes: libmudflap
Obsoletes: libmudflap-devel
Obsoletes: libmudflap-static
Obsoletes: libgcj < %{version}-%{release}
Obsoletes: libgcj-devel < %{version}-%{release}
Obsoletes: libgcj-src < %{version}-%{release}

%description -n libgcc%{binsuffix}
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++%{binsuffix}
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc%{binsuffix} = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description c++%{binsuffix}
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++%{binsuffix}
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++%{binsuffix}
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++%{binsuffix}-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{?_isa}%{binsuffix} = %{version}-%{release}
Autoreq: true

%description -n libstdc++%{binsuffix}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static%{binsuffix}
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static%{binsuffix}
Static libraries for the GNU standard C++ library.

%package -n libstdc++%{binsuffix}-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++%{binsuffix}-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc%{binsuffix}
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc%{binsuffix} = %{version}-%{release}
Requires: libobjc%{binsuffix} = %{version}-%{release}
Autoreq: true

%description objc%{binsuffix}
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++%{binsuffix}
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++%{binsuffix} = %{version}-%{release}, gcc-objc%{binsuffix} = %{version}-%{release}
Autoreq: true

%description objc++%{binsuffix}
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc%{binsuffix}
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc%{binsuffix}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran%{binsuffix}
Summary: Fortran support
Group: Development/Languages
Requires: gcc%{binsuffix} = %{version}-%{release}
Requires: libgfortran%{binsuffix} = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath%{binsuffix} = %{version}-%{release}
Requires: libquadmath%{binsuffix}-devel = %{version}-%{release}
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gfortran%{binsuffix}
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran%{binsuffix}
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true
%if %{build_libquadmath}
Requires: libquadmath%{binsuffix} = %{version}-%{release}
%endif

%description -n libgfortran%{binsuffix}
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static%{binsuffix}
Summary: Static Fortran libraries
Group: Development/Libraries
Requires: libgfortran%{binsuffix} = %{version}-%{release}
Requires: gcc%{binsuffix} = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static%{binsuffix} = %{version}-%{release}
%endif

%description -n libgfortran-static%{binsuffix}
This package contains static Fortran libraries.

%package -n libgomp%{binsuffix}
Summary: GCC OpenMP v4.5 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp%{binsuffix}
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.

%package -n libgomp-offload-nvptx%{binsuffix}
Summary: GCC OpenMP v4.5 plugin for offloading to NVPTX
Group: System Environment/Libraries
Requires: libgomp%{binsuffix} = %{version}-%{release}

%description -n libgomp-offload-nvptx%{binsuffix}
This package contains libgomp plugin for offloading to NVidia
PTX.  The plugin needs libcuda.so.1 shared library that has to be
installed separately.

%package gdb-plugin%{binsuffix}
Summary: GCC plugin for GDB
Group: Development/Debuggers
Requires: gcc%{binsuffix} =  %{version}-%{release}

%description gdb-plugin%{binsuffix}
This package contains GCC plugin for GDB C expression evaluation.

%package -n libgccjit%{binsuffix}
Summary: Library for embedding GCC inside programs and libraries
Group: System Environment/Libraries
Requires: gcc%{binsuffix} =  %{version}-%{release}

%description -n libgccjit%{binsuffix}
This package contains shared library with GCC JIT front-end.

%package -n libgccjit%{binsuffix}-devel
Summary: Support for embedding GCC inside programs and libraries
Group: Development/Libraries
BuildRequires: python-sphinx
Requires: libgccjit%{binsuffix} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgccjit%{binsuffix}-devel
This package contains header files and documentation for GCC JIT front-end.

%package -n libquadmath%{binsuffix}
Summary: GCC __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libquadmath%{binsuffix}
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath%{binsuffix}-devel
Summary: GCC __float128 support
Group: Development/Libraries
Requires: libquadmath%{binsuffix} = %{version}-%{release}
Requires: gcc%{binsuffix} =  %{version}-%{release}

%description -n libquadmath%{binsuffix}-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static%{binsuffix}
Summary: Static libraries for __float128 support
Group: Development/Libraries
Requires: libquadmath%{binsuffix}-devel = %{version}-%{release}

%description -n libquadmath-static%{binsuffix}
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm%{binsuffix}
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm%{binsuffix}
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm%{binsuffix}-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libitm%{binsuffix} = %{version}-%{release}
Requires: gcc%{binsuffix} =  %{version}-%{release}

%description -n libitm%{binsuffix}-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static%{binsuffix}
Summary: The GNU Transactional Memory static library
Group: Development/Libraries
Requires: libitm%{binsuffix}-devel = %{version}-%{release}

%description -n libitm-static%{binsuffix}
This package contains GNU Transactional Memory static libraries.

%package -n libatomic%{binsuffix}
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic%{binsuffix}
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static%{binsuffix}
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic%{binsuffix} = %{version}-%{release}

%description -n libatomic-static%{binsuffix}
This package contains GNU Atomic static libraries.

%package -n libasan%{binsuffix}
Summary: The Address Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan%{binsuffix}
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static%{binsuffix}
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan%{binsuffix} = %{version}-%{release}

%description -n libasan-static%{binsuffix}
This package contains Address Sanitizer static runtime library.

%package -n libtsan%{binsuffix}
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan%{binsuffix}
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

#%package -n libtsan-static
#Summary: The Thread Sanitizer static library
#Group: Development/Libraries
#Requires: libtsan = %{version}-%{release}

#%description -n libtsan-static
#This package contains Thread Sanitizer static runtime library.

%package -n libubsan%{binsuffix}
Summary: The Undefined Behavior Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libubsan%{binsuffix}
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static%{binsuffix}
Summary: The Undefined Behavior Sanitizer static library
Group: Development/Libraries
Requires: libubsan%{binsuffix} = %{version}-%{release}

%description -n libubsan-static%{binsuffix}
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan%{binsuffix}
Summary: The Leak Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n liblsan%{binsuffix}
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static%{binsuffix}
Summary: The Leak Sanitizer static library
Group: Development/Libraries
Requires: liblsan%{binsuffix} = %{version}-%{release}

%description -n liblsan-static%{binsuffix}
This package contains Leak Sanitizer static runtime library.

%package -n libcilkrts%{binsuffix}
Summary: The Cilk+ runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libcilkrts%{binsuffix}
This package contains the Cilk+ runtime library.

%package -n libcilkrts-static%{binsuffix}
Summary: The Cilk+ static runtime library
Group: Development/Libraries
Requires: libcilkrts%{binsuffix} = %{version}-%{release}

%description -n libcilkrts-static%{binsuffix}
This package contains the Cilk+ static runtime library.

%package -n libmpx%{binsuffix}
Summary: The Memory Protection Extensions runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libmpx%{binsuffix}
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package -n libmpx-static%{binsuffix}
Summary: The Memory Protection Extensions static libraries
Group: Development/Libraries
Requires: libmpx%{binsuffix} = %{version}-%{release}

%description -n libmpx-static%{binsuffix}
This package contains the Memory Protection Extensions static runtime libraries.

%package -n cpp%{binsuffix}
Summary: The C Preprocessor
Group: Development/Languages
Requires: filesystem >= 3
Provides: /lib/cpp
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description -n cpp%{binsuffix}
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat%{binsuffix}
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Group: Development/Languages
Requires: gcc%{binsuffix} =  %{version}-%{release}
Requires: libgnat%{binsuffix} = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gnat%{binsuffix}
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat%{binsuffix}
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat%{binsuffix}
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package -n libgnat%{binsuffix}-devel
Summary: GNU Ada 83, 95, 2005 and 2012 libraries
Group: Development/Languages
Autoreq: true

%description -n libgnat%{binsuffix}-devel
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
libraries, which are required to compile with the GNAT.

%package -n libgnat-static%{binsuffix}
Summary: GNU Ada 83, 95, 2005 and 2012 static libraries
Group: Development/Languages
Requires: libgnat%{binsuffix}-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static%{binsuffix}
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
static libraries.

%package go%{binsuffix}
Summary: Go support
Group: Development/Languages
Requires: gcc%{binsuffix} =  %{version}-%{release}
Requires: libgo%{binsuffix} = %{version}-%{release}
Requires: libgo%{binsuffix}-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Autoreq: true

%description go%{binsuffix}
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo%{binsuffix}
Summary: Go runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgo%{binsuffix}
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo%{binsuffix}-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo%{binsuffix} = %{version}-%{release}
Autoreq: true

%description -n libgo%{binsuffix}-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static%{binsuffix}
Summary: Static Go libraries
Group: Development/Libraries
Requires: libgo%{binsuffix} = %{version}-%{release}
Requires: gcc%{binsuffix} =  %{version}-%{release}

%description -n libgo-static%{binsuffix}
This package contains static Go libraries.

%package plugin%{binsuffix}-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: gcc%{binsuffix} =  %{version}-%{release}
Requires: gmp%{binsuffix}-devel >= 4.1.2-8, mpfr%{binsuffix}-devel >= 2.2.1, libmpc%{binsuffix}-devel >= 0.8.1

%description plugin%{binsuffix}-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package offload-nvptx%{binsuffix}
Summary: Offloading compiler to NVPTX
Group: Group: Development/Languages
Requires: gcc%{binsuffix} =  %{version}-%{release}
Requires: libgomp-offload-nvptx%{binsuffix} = %{version}-%{release}

%description offload-nvptx%{binsuffix}
The gcc-offload-nvptx package provides offloading support for
NVidia PTX.  OpenMP and OpenACC programs linked with -fopenmp will
by default add PTX code into the binaries, which can be offloaded
to NVidia PTX capable devices if available.

%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%global __debug_package 1
%global __debug_install_post \
   PATH=%{_builddir}/gcc-%{version}-%{DATE}/dwz-wrapper/:$PATH %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_dwz_opts} %{?_find_debuginfo_opts} "%{_builddir}/gcc-%{version}-%{DATE}"\
    %{_builddir}/gcc-%{version}-%{DATE}/split-debuginfo.sh\
%{nil}

%package debuginfo%{binsuffix}
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: gcc%{binsuffix}-base-debuginfo = %{version}-%{release}

%description debuginfo%{binsuffix}
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files debuginfo%{binsuffix} -f debugfiles.list

%package base-debuginfo
Summary: Debug information for libraries from package %{name}
Group: Development/Debug
AutoReqProv: 0

%description base-debuginfo
This package provides debug information for libgcc_s, libgomp and
libstdc++ libraries from package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files base-debuginfo -f debugfiles-base.list
%endif

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2

%if 0%{?_enable_debug_packages}
mkdir dwz-wrapper
if [ -f /usr/bin/dwz ]; then
cat > dwz-wrapper/dwz <<\EOF
#!/bin/bash
dwz_opts=
dwzm_opts=
dwz_files=
dwzm_files=
while [ $# -gt 0 ]; do
  case "$1" in
  -l|-L)
    dwz_opts="$dwz_opts $1 $2"; shift;;
  -m|-M)
    dwzm_opts="$dwzm_opts $1 $2"; shift;;
  -*)
    dwz_opts="$dwz_opts $1";;
  *)
    if [[ "$1" =~ (lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm|go\.so)|bin/gofmt.gcc.debug|bin/go.gcc.debug|/cgo.debug) ]]; then
      dwz_files="$dwz_files $1"
    else
      dwzm_files="$dwzm_files $1"
    fi;;
  esac
  shift
done
if [ -f /usr/bin/dwz ]; then
  /usr/bin/dwz $dwz_opts $dwz_files
  /usr/bin/dwz $dwz_opts $dwzm_opts $dwzm_files
fi
EOF
chmod 755 dwz-wrapper/dwz
fi
cat > split-debuginfo.sh <<\EOF
#!/bin/sh
BUILDDIR="%{_builddir}/gcc-%{version}-%{DATE}"
if [ -f "${BUILDDIR}"/debugfiles.list \
     -a -f "${BUILDDIR}"/debuglinks.list ]; then
  > "${BUILDDIR}"/debugsources-base.list
  > "${BUILDDIR}"/debugfiles-base.list
  cd "${RPM_BUILD_ROOT}"
  for f in `find usr/lib/debug -name \*.debug \
	    | egrep 'lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm)'`; do
    echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
    if [ -f "$f" -a ! -L "$f" ]; then
      cp -a "$f" "${BUILDDIR}"/test.debug
      /usr/lib/rpm/debugedit -b "${RPM_BUILD_DIR}" -d /usr/src/debug \
			     -l "${BUILDDIR}"/debugsources-base.list \
			     "${BUILDDIR}"/test.debug
      rm -f "${BUILDDIR}"/test.debug
    fi
  done
  for f in `find usr/lib/debug/.build-id -type l`; do
    ls -l "$f" | egrep -q -- '->.*lib[0-9]*/lib(gcc[_.]|gomp|stdc|quadmath|itm)' \
      && echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
  done
  cp -a "${BUILDDIR}"/debugfiles-base.list "${BUILDDIR}"/debugfiles-remove.list
%if %{build_go}
  libgoso=`basename .%{_prefix}/%{_lib}/libgo.so.7.*`
  for f in %{_prefix}/bin/go.gcc \
	   %{_prefix}/bin/gofmt.gcc \
	   %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/cgo \
	   %{_prefix}/%{_lib}/$libgoso ; do
    eu-unstrip .$f usr/lib/debug$f.debug -o .$f.new
    chmod --reference=.$f .$f.new
    mv -f .$f.new .$f
    rm -f usr/lib/debug$f.debug
    echo "/usr/lib/debug$f.debug" >> "${BUILDDIR}"/debugfiles-remove.list
  done
  rm -f usr/lib/debug%{_prefix}/%{_lib}/libgo.so.7.debug
  echo "/usr/lib/debug%{_prefix}/%{_lib}/libgo.so.7.debug" >> "${BUILDDIR}"/debugfiles-remove.list
  for f in `find usr/lib/debug/.build-id -type l`; do
    if ls -l "$f" | egrep -q -- '->.*(/bin/go.gcc|/bin/gofmt.gcc|/cgo|lib[0-9]*/libgo\.so)'; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-remove.list
      rm -f "$f"
    fi
  done
%endif
  grep -v -f "${BUILDDIR}"/debugfiles-remove.list \
    "${BUILDDIR}"/debugfiles.list > "${BUILDDIR}"/debugfiles.list.new
  mv -f "${BUILDDIR}"/debugfiles.list.new "${BUILDDIR}"/debugfiles.list
  for f in `LC_ALL=C sort -z -u "${BUILDDIR}"/debugsources-base.list \
	    | grep -E -v -z '(<internal>|<built-in>)$' \
	    | xargs --no-run-if-empty -n 1 -0 echo \
	    | sed 's,^,usr/src/debug/,'`; do
    if [ -f "$f" ]; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
      echo "%%exclude /$f" >> "${BUILDDIR}"/debugfiles.list
    fi
  done
  mv -f "${BUILDDIR}"/debugfiles-base.list{,.old}
  echo "%%dir /usr/lib/debug" > "${BUILDDIR}"/debugfiles-base.list
  awk 'BEGIN{FS="/"}(NF>4&&$NF){d="%%dir /"$2"/"$3"/"$4;for(i=5;i<NF;i++){d=d"/"$i;if(!v[d]){v[d]=1;print d}}}' \
    "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  cat "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  rm -f "${BUILDDIR}"/debugfiles-base.list.old
fi
EOF
chmod 755 split-debuginfo.sh
%endif

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac

%if %{build_offload_nvptx}
mkdir obji
IROOT=`pwd`/obji
cd nvptx-tools-%{nvptx_tools_gitrev}
rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}
CC="$CC" CXX="$CXX" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
../configure --prefix=%{_prefix}
make %{?_smp_mflags}
make install prefix=${IROOT}%{_prefix}
cd ../..

ln -sf nvptx-newlib-%{nvptx_newlib_gitrev}/newlib newlib
rm -rf obj-offload-nvptx-none
mkdir obj-offload-nvptx-none

cd obj-offload-nvptx-none
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --disable-bootstrap --disable-sjlj-exceptions \
	--enable-newlib-io-long-long --with-build-time-tools=${IROOT}%{_prefix}/nvptx-none/bin \
	--target nvptx-none --enable-as-accelerator-for=%{gcc_target_platform} \
	--enable-languages=c,c++,fortran,lto \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-checking=release --with-system-zlib \
	--with-gcc-major-version-only --without-isl \
	--program-suffix=%{binsuffix} \
make %{?_smp_mflags}
cd ..
rm -f newlib
%endif

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

enablelgo=
enablelada=
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
CONFIGURE_OPTS="\
	--program-suffix=%{binsuffix} \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux \
%endif
%ifarch ppc64le %{mips}
	--disable-multilib \
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
%ifnarch %{mips}
	--with-linker-hash-style=gnu \
%endif
	--enable-plugin --enable-initfini-array \
%if %{build_isl}
	--with-isl \
%else
	--without-isl \
%endif
%if %{build_libmpx}
	--enable-libmpx \
%else
	--disable-libmpx \
%endif
%if %{build_offload_nvptx}
	--enable-offload-targets=nvptx-none \
	--without-cuda-driver \
%endif
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc64le
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
	--with-arch=z196 --with-tune=zEC12 --enable-decimal-float \
%else
%if 0%{?fedora} >= 26
	--with-arch=zEC12 --with-tune=z13 --enable-decimal-float \
%else
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%endif
%endif
%ifarch armv7hl
	--with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
	--with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
	--with-arch=mips64r2 --with-abi=64 \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform} \
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++,objc,obj-c++,fortran${enablelada}${enablelgo},lto \
	$CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}.%{gcc_release}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}

for i in {gcc,gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -rf %{buildroot}

%if %{build_offload_nvptx}
cd nvptx-tools-%{nvptx_tools_gitrev}
cd obj-%{gcc_target_platform}
make install prefix=%{buildroot}%{_prefix}
cd ../..

ln -sf nvptx-newlib-%{nvptx_newlib_gitrev}/newlib newlib
cd obj-offload-nvptx-none
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
rm -rf %{buildroot}%{_prefix}/libexec/gcc/nvptx-none/%{gcc_major}/install-tools
rm -rf %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none/{install-tools,plugin,cc1,cc1plus,f951}
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_mandir}/man7 %{buildroot}%{_prefix}/share/locale
rm -rf %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/{install-tools,plugin}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none/{install-tools,plugin,include-fixed}
rm -rf %{buildroot}%{_prefix}/%{_lib}/libc[cp]1*
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/mgomp/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none/mgomp/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/mgomp/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none/mgomp/
find %{buildroot}%{_prefix}/lib/gcc/nvptx-none %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none \
     %{buildroot}%{_prefix}/nvptx-none/lib -name \*.la | xargs rm
cd ..
rm -f newlib
%endif

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}

# fix some things
ln -sf gcc${binsuffix} %{buildroot}%{_prefix}/bin/cc%{binsuffix}
rm -f %{buildroot}%{_prefix}/lib/cpp%{binsuffix}
ln -sf ../bin/cpp%{binsuffix} %{buildroot}/%{_prefix}/lib/cpp%{binsuffix}
ln -sf gfortran%{binsuffix} %{buildroot}%{_prefix}/bin/f95%{binsuffix}
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc%{binsuffix} %{buildroot}%{_prefix}/bin/gnatgcc%{binsuffix}
mkdir -p %{buildroot}%{_fmoddir}

%if %{build_go}
mv %{buildroot}%{_prefix}/bin/go{,.gcc}%{binsuffix}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}%{binsuffix}
ln -sf /etc/alternatives/go%{binsuffix} %{buildroot}%{_prefix}/bin/go%{binsuffix}
ln -sf /etc/alternatives/gofmt%{binsuffix} %{buildroot}%{_prefix}/bin/gofmt%{binsuffix}
%endif

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/

%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64 ppc64p7
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

FULLLSUBDIR=
%ifarch sparcv9 ppc
FULLLSUBDIR=lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLSUBDIR=lib64
%endif
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif
%if %{build_libcilkrts}
mv %{buildroot}%{_prefix}/%{_lib}/libcilkrts.spec $FULLPATH/
%endif
%if %{build_libmpx}
mv %{buildroot}%{_prefix}/%{_lib}/libmpx.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64 ppc64p7
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif
%ifarch %{arm}
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-littlearm)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}.%{gcc_release}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}.%{gcc_release}/python/ \
	       %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
  %{__python3} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python3} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
done

rm -f $FULLEPATH/libgccjit.so
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_prefix}/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.4 libobjc.so
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.7.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.2.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.0.* libubsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../libmpx.so.2.* libmpx.so
ln -sf ../../../libmpxwrappers.so.2.* libmpxwrappers.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.7.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.2.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.0.* libubsan.so
%endif
%if %{build_libcilkrts}
ln -sf ../../../../%{_lib}/libcilkrts.so.5.* libcilkrts.so
%endif
%if %{build_libmpx}
ln -sf ../../../../%{_lib}/libmpx.so.2.* libmpx.so
ln -sf ../../../../%{_lib}/libmpxwrappers.so.2.* libmpxwrappers.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../../%{_lib}/libtsan_preinit.o libtsan_preinit.o
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_libcilkrts}
mv -f %{buildroot}%{_prefix}/%{_lib}/libcilkrts.*a $FULLLPATH/
%endif
%if %{build_libmpx}
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpx.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-7.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-7.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-6.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-7.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-6.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-7.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.7.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.7.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.2.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.2.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > 64/libubsan.so
%endif
%if %{build_libcilkrts}
rm -f libcilkrts.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > libcilkrts.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > 64/libcilkrts.so
%endif
%if %{build_libmpx}
rm -f libmpx.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpx.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > 64/libmpx.so
rm -f libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > 64/libmpxwrappers.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
%endif
%if %{build_libubsan}
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf lib32/libcilkrts.a libcilkrts.a
ln -sf ../lib64/libcilkrts.a 64/libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf lib32/libmpx.a libmpx.a
ln -sf ../lib64/libmpx.a 64/libmpx.a
ln -sf lib32/libmpxwrappers.a libmpxwrappers.a
ln -sf ../lib64/libmpxwrappers.a 64/libmpxwrappers.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
ln -sf lib32/libgolibbegin.a libgolibbegin.a
ln -sf ../lib64/libgolibbegin.a 64/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.4 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.7.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.7.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.2.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.2.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libubsan.so.0.* | sed 's,^.*libu,libu,'`' )' > 32/libubsan.so
%endif
%if %{build_libcilkrts}
rm -f libcilkrts.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > libcilkrts.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libcilkrts.so.5.* | sed 's,^.*libc,libc,'`' )' > 32/libcilkrts.so
%endif
%if %{build_libmpx}
rm -f libmpx.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpx.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmpx.so.2.* | sed 's,^.*libm,libm,'`' )' > 32/libmpx.so
rm -f libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > libmpxwrappers.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmpxwrappers.so.2.* | sed 's,^.*libm,libm,'`' )' > 32/libmpxwrappers.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
%endif
%if %{build_libubsan}
ln -sf ../lib32/libubsan.a 32/libubsan.a
ln -sf lib64/libubsan.a libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf ../lib32/libcilkrts.a 32/libcilkrts.a
ln -sf lib64/libcilkrts.a libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf ../lib32/libmpx.a 32/libmpx.a
ln -sf lib64/libmpx.a libmpx.a
ln -sf ../lib32/libmpxwrappers.a 32/libmpxwrappers.a
ln -sf lib64/libmpxwrappers.a libmpxwrappers.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
ln -sf ../lib32/libgolibbegin.a 32/libgolibbegin.a
ln -sf lib64/libgolibbegin.a libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgfortran.a 32/libgfortran.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++fs.a 32/libstdc++fs.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libsupc++.a 32/libsupc++.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libasan.a 32/libasan.a
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libubsan.a 32/libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libcilkrts.a 32/libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libmpx.a 32/libmpx.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libmpxwrappers.a 32/libmpxwrappers.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgobegin.a 32/libgobegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgolibbegin.a 32/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adalib 32/adalib
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a -o -name libcilkrts.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libmpx.a -o -name libmpxwrappers.a \
		-o -name libobjc.a \
		-o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libsupc++.a \
	        -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/$d/
  done
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
		    -o -name libatomic.a -o -name libasan.a  \
		    -o -name libubsan.a -o -name liblsan.a -o -name libcilkrts.a \
		    -o -name libmpx.a -o -name libmpxwrappers.a -o -name libcc1.a \) \
		 -a -type f`
popd
#chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.2.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.0.*
%endif
%if %{build_libcilkrts}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcilkrts.so.5.*
%endif
%if %{build_libmpx}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpx.so.2.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.so.2.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.7.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89%{binsuffix} <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc%{binsuffix} $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99%{binsuffix} <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc%{binsuffix} $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9%{binsuffix}

cd ..
#%find_lang %{name}
%find_lang gcc
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a} || :
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/gappletviewer || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%endif

rm -f %{buildroot}%{mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%check
cd obj-%{gcc_target_platform}

# run the tests.
#make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
#%if 0%{?fedora} >= 20
#     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
#%else
#     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
#%endif
#echo ====================TESTING=========================
#( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
#echo ====================TESTING END=====================
#mkdir testlogs-%{_target_platform}-%{version}-%{release}
#for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
#  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
#done
#tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
#  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
#rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp%{binsuffix}
if [ -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%preun -n cpp%{binsuffix}
if [ $1 = 0 -a -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran%{binsuffix}
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran%{binsuffix}
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post gnat%{binsuffix}
if [ -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%preun gnat%{binsuffix}
if [ $1 = 0 -a -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%post go%{binsuffix}
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go%{binsuffix}
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc%{binsuffix} -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc%{binsuffix} -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%post -n libstdc++%{binsuffix} -p /sbin/ldconfig

%postun -n libstdc++%{binsuffix} -p /sbin/ldconfig

%post -n libobjc%{binsuffix} -p /sbin/ldconfig

%postun -n libobjc%{binsuffix} -p /sbin/ldconfig

%post -n libgfortran%{binsuffix} -p /sbin/ldconfig

%postun -n libgfortran%{binsuffix} -p /sbin/ldconfig

%post -n libgnat%{binsuffix} -p /sbin/ldconfig

%postun -n libgnat%{binsuffix} -p /sbin/ldconfig

%post -n libgomp%{binsuffix}
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp%{binsuffix}
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp%{binsuffix} -p /sbin/ldconfig

%post gdb-plugin%{binsuffix} -p /sbin/ldconfig

%postun gdb-plugin%{binsuffix} -p /sbin/ldconfig

%post -n libgccjit%{binsuffix} -p /sbin/ldconfig

%postun -n libgccjit%{binsuffix} -p /sbin/ldconfig

%post -n libgccjit%{binsuffix}-devel
if [ -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%preun -n libgccjit%{binsuffix}-devel
if [ $1 = 0 -a -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%post -n libquadmath%{binsuffix}
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath%{binsuffix}
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath%{binsuffix} -p /sbin/ldconfig

%post -n libitm%{binsuffix}
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libitm%{binsuffix}
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -n libitm%{binsuffix} -p /sbin/ldconfig

%post -n libatomic%{binsuffix} -p /sbin/ldconfig

%postun -n libatomic%{binsuffix} -p /sbin/ldconfig

%post -n libasan%{binsuffix} -p /sbin/ldconfig

%postun -n libasan%{binsuffix} -p /sbin/ldconfig

%post -n libubsan%{binsuffix} -p /sbin/ldconfig

%postun -n libubsan%{binsuffix} -p /sbin/ldconfig

%post -n libtsan%{binsuffix} -p /sbin/ldconfig

%postun -n libtsan%{binsuffix} -p /sbin/ldconfig

%post -n liblsan%{binsuffix} -p /sbin/ldconfig

%postun -n liblsan%{binsuffix} -p /sbin/ldconfig

%post -n libcilkrts%{binsuffix} -p /sbin/ldconfig

%postun -n libcilkrts%{binsuffix} -p /sbin/ldconfig

%post -n libmpx%{binsuffix} -p /sbin/ldconfig

%postun -n libmpx%{binsuffix} -p /sbin/ldconfig

%post -n libgo%{binsuffix} -p /sbin/ldconfig

%postun -n libgo%{binsuffix} -p /sbin/ldconfig

#%files -f %{name}.lang
%files -f gcc.lang
%{_prefix}/bin/cc%{binsuffix}
%{_prefix}/bin/c89%{binsuffix}
%{_prefix}/bin/c99%{binsuffix}
%{_prefix}/bin/gcc%{binsuffix}
%{_prefix}/bin/gcov%{binsuffix}
%{_prefix}/bin/gcov-tool%{binsuffix}
%{_prefix}/bin/gcc-ar%{binsuffix}
%{_prefix}/bin/gcc-nm%{binsuffix}
%{_prefix}/bin/gcc-ranlib%{binsuffix}
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64 ppc64p7
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc%{binsuffix}
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}.%{gcc_release}
%{_mandir}/man1/gcc*.1*
%{_mandir}/man1/gcov*.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/stdatomic.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/sgxintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/htmxlintrin.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_cmse.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_fp16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_acle.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/arm_fp16.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/vecintrin.h
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/cilk
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libcilkrts.spec
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpx.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libsanitizer.spec
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libmpxwrappers.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libmpxwrappers.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpxwrappers.so
%endif
%else
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpxwrappers.so
%endif
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libtsan_preinit.o
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/liblsan.so
%endif
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* 
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n cpp%{binsuffix} -f cpplib.lang
%{_prefix}/lib/cpp%{binsuffix}
%{_prefix}/bin/cpp%{binsuffix}
%{_mandir}/man1/cpp*.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/cc1

%files -n libgcc%{binsuffix}
/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files c++%{binsuffix}
%{_prefix}/bin/%{gcc_target_platform}-*++%{binsuffix}
%{_prefix}/bin/g++%{binsuffix}
%{_prefix}/bin/c++%{binsuffix}
%{_mandir}/man1/g++*.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++%{binsuffix}
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%dir %{_prefix}/share/gcc-%{gcc_major}.%{gcc_release}
%dir %{_prefix}/share/gcc-%{gcc_major}.%{gcc_release}/python
%{_prefix}/share/gcc-%{gcc_major}.%{gcc_release}/python/libstdcxx

%files -n libstdc++%{binsuffix}-devel
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libstdc++.so
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libstdc++fs.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libstdc++fs.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libstdc++fs.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++%{binsuffix}-docs
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++%{binsuffix}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/cc1objplus

%files -n libobjc%{binsuffix}
%{_prefix}/%{_lib}/libobjc.so.4*

%files gfortran%{binsuffix}
%{_prefix}/bin/gfortran%{binsuffix}
%{_prefix}/bin/f95%{binsuffix}
%{_mandir}/man1/gfortran*.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/finclude
%endif
%dir %{_fmoddir}
%doc rpm.doc/gfortran/*

%files -n libgfortran%{binsuffix}
%{_prefix}/%{_lib}/libgfortran.so.3*

%files -n libgfortran-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgfortran.a
%endif

%if %{build_ada}
%files gnat%{binsuffix}
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat%{binsuffix}
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat%{binsuffix}-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib/libgnarl.a
%endif

%files -n libgnat-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp%{binsuffix}
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_libquadmath}
%files -n libquadmath%{binsuffix}
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath%{binsuffix}-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libquadmath.a
%endif
%endif

%if %{build_libitm}
%files -n libitm%{binsuffix}
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm%{binsuffix}-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/itm.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libitm.a
%endif
%endif

%if %{build_libatomic}
%files -n libatomic%{binsuffix}
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan%{binsuffix}
%{_prefix}/%{_lib}/libasan.so.2*

%files -n libasan-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libasan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libasan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libasan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan%{binsuffix}
%{_prefix}/%{_lib}/libubsan.so.0*

%files -n libubsan-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libubsan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libubsan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libubsan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan%{binsuffix}
%{_prefix}/%{_lib}/libtsan.so*

#%files -n libtsan-static
#%dir %{_prefix}/lib/gcc
#%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
##%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libtsan.a
#%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
#%{!?_licensedir:%global license %%doc}
#%license libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan%{binsuffix}
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libcilkrts}
%files -n libcilkrts%{binsuffix}
%{_prefix}/%{_lib}/libcilkrts.so.5*

%files -n libcilkrts-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libcilkrts.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libcilkrts.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libcilkrts.a
%endif
%doc rpm.doc/changelogs/libcilkrts/ChangeLog* libcilkrts/README
%endif

%if %{build_libmpx}
%files -n libmpx%{binsuffix}
%{_prefix}/%{_lib}/libmpx.so.2*
%{_prefix}/%{_lib}/libmpxwrappers.so.2*

%files -n libmpx-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libmpxwrappers.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libmpxwrappers.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libmpxwrappers.a
%endif
%doc rpm.doc/changelogs/libmpx/ChangeLog*
%endif

%if %{build_go}
%files go%{binsuffix}
%ghost %{_prefix}/bin/go%{binsuffix}
%{_prefix}/bin/go.gcc%{binsuffix}
%{_prefix}/bin/gccgo%{binsuffix}
%ghost %{_prefix}/bin/gofmt%{binsuffix}
%{_prefix}/bin/gofmt.gcc%{binsuffix}
%{_mandir}/man1/gccgo*.1*
%{_mandir}/man1/go*.1*
%{_mandir}/man1/gofmt*.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/go1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/cgo
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/64/libgolibbegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/32/libgolibbegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgolibbegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo%{binsuffix}
%{_prefix}/%{_lib}/libgo.so.7*
%doc rpm.doc/libgo/*

%files -n libgo%{binsuffix}-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_major}
%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libgolibbegin.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libgolibbegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgo.so
%endif

%files -n libgo-static%{binsuffix}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/libgo.a
%endif
%endif

%files -n libgccjit%{binsuffix}
%{_prefix}/%{_lib}/libgccjit.so.*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n libgccjit%{binsuffix}-devel
%{_prefix}/%{_lib}/libgccjit.so
%{_prefix}/include/libgccjit*.h
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples

%files plugin%{binsuffix}-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin

%files gdb-plugin%{binsuffix}
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin/libcc1plugin.so*
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%if %{build_offload_nvptx}
%files offload-nvptx%{binsuffix}
%{_prefix}/bin/nvptx-none-*
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-gcc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel
%{_prefix}/lib/gcc/nvptx-none
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}.%{gcc_release}/accel/nvptx-none
%dir %{_prefix}/nvptx-none
%{_prefix}/nvptx-none/bin
%{_prefix}/nvptx-none/include

%files -n libgomp-offload-nvptx%{binsuffix}
%{_prefix}/%{_lib}/libgomp-plugin-nvptx.so.*
%endif

%changelog
* Sat Apr 22 2017 Huang Jinhua <sjtuhjh@hotmail.com> 5.4.1
- initial package for Open-Estuary
