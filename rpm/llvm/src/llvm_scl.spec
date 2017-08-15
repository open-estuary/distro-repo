%define scl devtoolset-4
%global scl_prefix devtoolset-4
%global MPI_HOME %{_libdir}

%{?scl:%scl_package llvm}
%{!?scl:
 %global pkg_name %{name}
 %global _root_prefix %{_prefix}
 %global _root_datadir %{_datadir}
 %global _root_bindir %{_bindir}
}

# Components enabled if supported by target architecture:
%ifarch %ix86 x86_64
  %bcond_without gold
%else
  %bcond_with gold
%endif

%global llvm_bindir %{_libdir}/%{name}

Name:		%{?scl_prefix}llvm
Version:	4.0.1
Release:	1%{?dist}
Summary:	The Low Level Virtual Machine

License:	NCSA
URL:		http://llvm.org
Source0:	http://llvm.org/releases/%{version}/llvm-%{version}.src.tar.xz

# recognize s390 as SystemZ when configuring build
Patch0:		llvm-3.7.1-cmake-s390.patch
Patch2:		rust-lang-llvm-pr67.patch
Patch3:		0001-CMake-Split-static-library-exports-into-their-own-ex.patch
Patch4:		0001-Revert-Revert-CMake-Move-sphinx-detection-into-AddSp.patch
Patch5:		0001-CMake-Fix-docs-llvm-man-target-when-clang-llvm-is-in.patch
Patch6:		0001-CMake-Add-LLVM_UTILS_INSTALL_DIR-option.patch

BuildRequires:	cmake3
BuildRequires:	zlib-devel
BuildRequires:  libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	python-sphinx
BuildRequires:	multilib-rpm-config
%if %{with gold}
BuildRequires:  binutils-devel
%endif
BuildRequires:  libstdc++-static

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

%package devel
Summary:	Libraries and header files for LLVM
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires(post): /usr/sbin/alternatives
Requires(postun): /usr/sbin/alternatives

%description devel
This package contains library and header files needed to develop new native
programs that use the LLVM infrastructure.

%package doc
Summary:	Documentation for LLVM
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for the LLVM compiler infrastructure.

%package libs
Summary:	LLVM shared libraries

%description libs
Shared libraries for the LLVM compiler infrastructure.

%package static
Summary:	LLVM static libraries

%description static
Static libraries for the LLVM compiler infrastructure.

%prep
%autosetup -n llvm-%{version}.src -p1

%ifarch armv7hl

# These tests are marked as XFAIL, but they still run and hang on ARM.
for f in `grep -Rl 'XFAIL.\+arm' test/ExecutionEngine `; do  rm $f; done

%endif

%build
mkdir -p _build
cd _build

%ifarch s390
# Decrease debuginfo verbosity to reduce memory consumption during final library linking
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

# force off shared libs as cmake macros turns it on.
%cmake3 .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_SHARED_LINKER_FLAGS="-Wl,-Bsymbolic -static-libstdc++" \
%ifarch s390
	-DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -DNDEBUG" \
%endif
%if 0%{?__isa_bits} == 64
	-DLLVM_LIBDIR_SUFFIX=64 \
%else
	-DLLVM_LIBDIR_SUFFIX= \
%endif
	\
	-DLLVM_TARGETS_TO_BUILD="X86;AMDGPU;PowerPC;NVPTX;SystemZ;AArch64;ARM;Mips;BPF" \
	-DLLVM_ENABLE_LIBCXX:BOOL=OFF \
	-DLLVM_ENABLE_ZLIB:BOOL=ON \
	-DLLVM_ENABLE_FFI:BOOL=ON \
	-DLLVM_ENABLE_RTTI:BOOL=ON \
%if %{with gold}
	-DLLVM_BINUTILS_INCDIR=%{_includedir} \
%endif
	\
	-DLLVM_BUILD_RUNTIME:BOOL=ON \
	\
	-DLLVM_INCLUDE_TOOLS:BOOL=ON \
	-DLLVM_BUILD_TOOLS:BOOL=ON \
	\
	-DLLVM_INCLUDE_TESTS:BOOL=ON \
	-DLLVM_BUILD_TESTS:BOOL=ON \
	\
	-DLLVM_INCLUDE_EXAMPLES:BOOL=ON \
	-DLLVM_BUILD_EXAMPLES:BOOL=OFF \
	\
	-DLLVM_INCLUDE_UTILS:BOOL=ON \
	-DLLVM_INSTALL_UTILS:BOOL=ON \
	-DLLVM_UTILS_INSTALL_DIR:PATH=%{llvm_bindir} \
	\
	-DLLVM_INCLUDE_DOCS:BOOL=ON \
	-DLLVM_BUILD_DOCS:BOOL=ON \
	-DLLVM_ENABLE_SPHINX:BOOL=ON \
	-DLLVM_ENABLE_DOXYGEN:BOOL=OFF \
	\
	-DLLVM_BUILD_LLVM_DYLIB:BOOL=ON \
	-DLLVM_DYLIB_EXPORT_ALL:BOOL=ON \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DLLVM_BUILD_EXTERNAL_COMPILER_RT:BOOL=ON \
	-DLLVM_INSTALL_TOOLCHAIN_ONLY:BOOL=OFF \
	\
	-DSPHINX_WARNINGS_AS_ERRORS=OFF \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build

make %{?_smp_mflags}

%install
cd _build
make install DESTDIR=%{buildroot}

# fix multi-lib
mv -v %{buildroot}%{_bindir}/llvm-config{,-%{__isa_bits}}

%multilib_fix_c_header --file %{_includedir}/llvm/Config/llvm-config.h

%check
cd _build
make check-all || :

%post
mv %{_libdir}/devtoolset-4-llvm %{_libdir}/llvm
%postun
rm -rf %{_libdir}/llvm

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post devel
ln -s %{_bindir}/llvm-config-%{__isa_bits} %{_bindir}/llvm-config 
#/usr/sbin/update-alternatives --install %{_bindir}/llvm-config llvm-config %{_bindir}/llvm-config-%{__isa_bits} %{__isa_bits}

%postun devel
rm %{_bindir}/llvm-config
#if [ $1 -eq 0 ]; then
#  /usr/sbin/update-alternatives --remove llvm-config %{_bindir}/llvm-config-%{__isa_bits}
#fi

%files
%{_bindir}/*
%{llvm_bindir}
%{_mandir}/man1/*.1.*
%exclude %{_bindir}/llvm-config-%{__isa_bits}
%exclude %{_mandir}/man1/llvm-config.1.*

%files libs
%{_libdir}/BugpointPasses.so
%{_libdir}/LLVMHello.so
%if %{with gold}
%{_libdir}/LLVMgold.so
%endif
%{_libdir}/libLLVM-4.0*.so
%{_libdir}/libLTO.so*

%files devel
%{_bindir}/llvm-config-%{__isa_bits}
%{_mandir}/man1/llvm-config.1.*
%{_includedir}/llvm
%{_includedir}/llvm-c
%{_libdir}/libLLVM.so
%{_libdir}/cmake/llvm
%exclude %{_libdir}/cmake/llvm/LLVMStaticExports.cmake

%files doc
%doc %{_docdir}/llvm/html

%files static
%{_libdir}/*.a
%{_libdir}/cmake/llvm/LLVMStaticExports.cmake

%changelog
* Tue Aug 15  2017 Yu Lijie <sjtuhjh@hotmail.com> - 4.0.1-1
- Fix some bugs for clang building

* Tue Jul 4  2017 Huang Jinhua <sjtuhjh@hotmail.com> - 4.0.1-1
- Add to devtoolset-4 tools

* Wed Jun 21 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-1
- 4.0.1 Release

* Thu Jun 15 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-6
- Install llvm utils

* Thu Jun 08 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-5
- Fix docs-llvm-man target

* Mon May 01 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-4
- Make cmake files no longer depend on static libs (rhbz 1388200)

* Tue Apr 18 2017 Josh Stone <jistone@redhat.com> - 4.0.0-3
- Fix computeKnownBits for ARMISD::CMOV (rust-lang/llvm#67)

* Mon Apr 03 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-2
- Simplify spec with rpm macros.

* Thu Mar 23 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- LLVM 4.0.0 Final Release

* Wed Mar 22 2017 tstellar@redhat.com - 3.9.1-6
- Fix %postun sep for -devel package.

* Mon Mar 13 2017 Tom Stellard <tstellar@redhat.com> - 3.9.1-5
- Disable failing tests on ARM.

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 3.9.1-4
- Fix missing mask on relocation for aarch64 (rhbz 1429050)

* Wed Mar 01 2017 Dave Airlie <airlied@redhat.com> - 3.9.1-3
- revert upstream radeonsi breaking change.

* Thu Feb 23 2017 Josh Stone <jistone@redhat.com> - 3.9.1-2
- disable sphinx warnings-as-errors

* Fri Feb 10 2017 Orion Poplawski <orion@cora.nwra.com> - 3.9.1-1
- llvm 3.9.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Josh Stone <jistone@redhat.com> - 3.9.0-7
- Apply backports from rust-lang/llvm#55, #57

* Tue Nov 01 2016 Dave Airlie <airlied@gmail.com - 3.9.0-6
- rebuild for new arches

* Wed Oct 26 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-5
- apply the patch from -4

* Wed Oct 26 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-4
- add fix for lldb out-of-tree build

* Mon Oct 17 2016 Josh Stone <jistone@redhat.com> - 3.9.0-3
- Apply backports from rust-lang/llvm#47, #48, #53, #54

* Sat Oct 15 2016 Josh Stone <jistone@redhat.com> - 3.9.0-2
- Apply an InstCombine backport via rust-lang/llvm#51

* Wed Sep 07 2016 Dave Airlie <airlied@redhat.com> - 3.9.0-1
- llvm 3.9.0
- upstream moved where cmake files are packaged.
- upstream dropped CppBackend

* Wed Jul 13 2016 Adam Jackson <ajax@redhat.com> - 3.8.1-1
- llvm 3.8.1
- Add mips target
- Fix some shared library mispackaging

* Tue Jun 07 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 3.8.0-2
- fix color support detection on terminal

* Thu Mar 10 2016 Dave Airlie <airlied@redhat.com> 3.8.0-1
- llvm 3.8.0 release

* Wed Mar 09 2016 Dan Horák <dan[at][danny.cz> 3.8.0-0.3
- install back memory consumption workaround for s390

* Thu Mar 03 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.2
- llvm 3.8.0 rc3 release

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 3.8.0-0.1
- llvm 3.8.0 rc2 release

* Tue Feb 16 2016 Dan Horák <dan[at][danny.cz> 3.7.1-7
- recognize s390 as SystemZ when configuring build

* Sat Feb 13 2016 Dave Airlie <airlied@redhat.com> 3.7.1-6
- export C++ API for mesa.

* Sat Feb 13 2016 Dave Airlie <airlied@redhat.com> 3.7.1-5
- reintroduce llvm-static, clang needs it currently.

* Fri Feb 12 2016 Dave Airlie <airlied@redhat.com> 3.7.1-4
- jump back to single llvm library, the split libs aren't working very well.

* Fri Feb 05 2016 Dave Airlie <airlied@redhat.com> 3.7.1-3
- add missing obsoletes (#1303497)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.1-1
- new upstream release
- enable gold linker

* Wed Nov 04 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- fix Requires for subpackages on the main package

* Tue Oct 06 2015 Jan Vcelak <jvcelak@fedoraproject.org> 3.7.0-100
- initial version using cmake build system
