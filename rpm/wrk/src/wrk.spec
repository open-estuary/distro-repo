Summary: a HTTP benchmarking tool
Name: wrk
Version: 4.0.2
Release: 1
URL: https://github.com/wg/wrk
License: Apache License 2.0
Source0: wrk-%{version}.tar.gz
Source1: LuaJIT-2.1.0-beta3.tar.gz
Patch0: aarch64_makefile.patch

BuildRequires: openssl-devel
BuildRequires: gcc

%description
wrk is a modern HTTP benchmarking tool capable of generating significant load when run on a single multi-core CPU. It combines a multithreaded design with scalable event notification systems such as epoll and kqueue.

%prep
%setup -q -n wrk-%{version}
%patch0 -p1
rm deps/LuaJIT*.tar.gz
cp %{SOURCE1} deps/
sed -i 's/luaL_reg/luaL_Reg/g' src/*.h
sed -i 's/luaL_reg/luaL_Reg/g' src/*.c
sed -i 's/luajit-2.0/luajit-2.1/g' src/*.h
sed -i 's/luaL_Register/luaL_register/g' src/*.c
sed -i 's/luaL_Register/luaL_register/g' src/*.h

%build
make 

%install
%{__rm} -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m755 wrk $RPM_BUILD_ROOT%{_bindir}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%{_bindir}/wrk

%changelog
* Tue Aug 1 2017 Open-Estuary <sjtuhjh@hotmail.com> 4.0.2
- Initial wrk package for ARM64 platform

