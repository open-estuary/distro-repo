%bcond_with local_clang_static
#lua jit not available for some architectures
%ifarch ppc64 aarch64 ppc64le
%{!?with_lua: %global with_lua 0}
%else
%{!?with_lua: %global with_lua 1}
%endif
%define debug_package %{nil}

Name:           bcc
Version:   0.3
Release:        1
Summary:        BPF Compiler Collection (BCC)

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/iovisor/bcc
Source0:        bcc-0.3.tar.gz
Patch0:         disable_asm_for_clang.patch 

ExclusiveArch: x86_64 ppc64 aarch64 ppc64le
BuildRequires: bison cmake >= 2.8.7 flex make
BuildRequires: gcc gcc-c++ python2-devel elfutils-libelf-devel-static
%if %{with_lua}
BuildRequires: luajit luajit-devel
%endif
%if %{without local_clang_static}
BuildRequires: devtoolset-4-llvm-devel devtoolset-4-llvm-static
BuildRequires: devtoolset-4-clang-devel
%endif
BuildRequires: pkgconfig ncurses-devel

%description
Python bindings for BPF Compiler Collection (BCC). Control a BPF program from
userspace.

%if %{with_lua}
%global lua_include `pkg-config --variable=includedir luajit`
%global lua_libs `pkg-config --variable=libdir luajit`/lib`pkg-config --variable=libname luajit`.so
%global lua_config -DLUAJIT_INCLUDE_DIR=%{lua_include} -DLUAJIT_LIBRARIES=%{lua_libs}
%endif

%prep
%setup -q 
%patch0 -p1

%build
source /opt/rh/devtoolset-4/enable
ln -sv /opt/rh/devtoolset-4/root/usr/bin/llvm-config-64 /opt/rh/devtoolset-4/root/usr/bin/llvm-config
mkdir build
pushd build
cmake .. -DREVISION_LAST=%{version} -DREVISION=%{version} \
      -DCMAKE_INSTALL_PREFIX=/usr \
      %{?lua_config}
make %{?_smp_mflags}
popd

%install
pushd build
make install/strip DESTDIR=%{buildroot}

%package -n libbcc
Summary: Shared Library for BPF Compiler Collection (BCC)
Requires: elfutils-libelf kernel = 4.9.20 kernel-headers = 4.9.20 kernel-devel = 4.9.20 
%description -n libbcc
Shared Library for BPF Compiler Collection (BCC)

%package -n python-bcc
Summary: Python bindings for BPF Compiler Collection (BCC)
Requires: libbcc = %{version}-%{release} kernel = 4.9.20 kernel-headers = 4.9.20 kernel-devel = 4.9.20
%description -n python-bcc
Python bindings for BPF Compiler Collection (BCC)

%if %{with_lua}
%package -n bcc-lua
Summary: Standalone tool to run BCC tracers written in Lua
Requires: libbcc = %{version}-%{release} kernel = 4.9.20 kernel-headers = 4.9.20 kernel-devel = 4.9.20
%description -n bcc-lua
Standalone tool to run BCC tracers written in Lua
%endif

%package -n libbcc-examples
Summary: Examples for BPF Compiler Collection (BCC)
Requires: python-bcc = %{version}-%{release} kernel = 4.9.20 kernel-headers = 4.9.20 kernel-devel = 4.9.20
%if %{with_lua}
Requires: bcc-lua = %{version}-%{release}
%endif
%description -n libbcc-examples
Examples for BPF Compiler Collection (BCC)

%package -n bcc-tools
Summary: Command line tools for BPF Compiler Collection (BCC)
Requires: python-bcc = %{version}-%{release} kernel = 4.9.20 kernel-headers = 4.9.20 kernel-devel = 4.9.20 
%description -n bcc-tools
Command line tools for BPF Compiler Collection (BCC)

%files -n libbcc
/usr/lib64/*
/usr/include/bcc/*

%files -n python-bcc
%{python_sitelib}/bcc*

%if %{with_lua}
%files -n bcc-lua
/usr/bin/bcc-lua
%endif

%files -n libbcc-examples
/usr/share/bcc/examples/*
%exclude /usr/share/bcc/examples/*.pyc
%exclude /usr/share/bcc/examples/*.pyo
%exclude /usr/share/bcc/examples/*/*.pyc
%exclude /usr/share/bcc/examples/*/*.pyo
%exclude /usr/share/bcc/examples/*/*/*.pyc
%exclude /usr/share/bcc/examples/*/*/*.pyo

%files -n bcc-tools
/usr/share/bcc/tools/*
/usr/share/bcc/man/*

%post -n libbcc -p /sbin/ldconfig

%post -n bcc-tools 
mv /lib/modules/4.9.20-3.1.rc1.estuary.aarch64 /lib/modules/4.9.20

%postun -n libbcc -p /sbin/ldconfig

%changelog
* Mon Nov 21 2016 William Cohen <wcohen@redhat.com> - 0.2.0-1
- Revise bcc.spec to address rpmlint issues and build properly in Fedora koji.

* Mon Apr 04 2016 Vicent Marti <vicent@github.com> - 0.1.4-1
- Add bcc-lua package

* Sun Nov 29 2015 Brenden Blanco <bblanco@plumgrid.com> - 0.1.3-1
- Add bcc-tools package

* Mon Oct 12 2015 Brenden Blanco <bblanco@plumgrid.com> - 0.1.2-1
- Add better version numbering into libbcc.so

* Fri Jul 03 2015 Brenden Blanco <bblanco@plumgrid.com> - 0.1.1-2
- Initial RPM Release
