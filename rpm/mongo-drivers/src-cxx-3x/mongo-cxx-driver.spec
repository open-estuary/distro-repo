# for better compatibility with SCL spec file
%global pkg_name mongo-cxx-driver

Name:           mongo-cxx-driver
Version:        3.1.1
Release:        1%{?dist}
Summary:        A  C++ Driver for MongoDB
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/mongodb/mongo-cxx-driver/wiki
Source0:        https://github.com/mongodb/%{pkg_name}/archive/r%{version}.tar.gz
Patch0: aarch64_mock_hh.patch

BuildRequires:  boost-devel >= 1.49
#BuildRequires:  compat-openssl10-devel
BuildRequires:  cmake3
#BuildRequires:  scons
BuildRequires:  cyrus-sasl-devel
# Tests requirements
#BuildRequires:  python-virtualenv
#BuildRequires:  mongodb-server
#BuildRequires:  git

Provides: libmongodb = 2.6.0-%{release}
Provides: libmongodb%{?_isa} = 2.6.0-%{release}
Obsoletes: libmongodb <= 2.4.9-8

%description
This package provides the shared library for the MongoDB  C++ Driver.


%package devel
Summary:        MongoDB header files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

Provides: libmongodb-devel = 2.6.0-%{release}
Provides: libmongodb-devel%{?_isa} = 2.6.0-%{release}
Obsoletes: libmongodb-devel <= 2.4.9-8

Provides:       mongodb-devel = 2.6.0-%{release}
Obsoletes:      mongodb-devel < 2.4

%description devel
This package provides the header files for MongoDB  C++ driver.


%prep
# -n the name of the directory to cd after unpacking
%setup -q -n %{name}-r%{version}
%patch0 -p1

# CRLF -> LF
sed -i 's/\r//' README.md

%build
cd build
cmake3 -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DLIBMONGOC_DIR=/usr/ \
      -DCMAKE_INSTALl_LIBDIR=lib64 \
      ..

make %{?_smp_mflags}
#make %{?_smp_mflags} doc/man V=1

%install
cd build
make install DESTDIR=%{buildroot}

: install examples
for i in  ../examples/*/*.cpp; do
  install -Dpm 644 $i %{buildroot}%{_datadir}/doc/%{name}/$i
done

: Rename documentation to match subpackage name
mv %{buildroot}%{_datadir}/doc/%{name} \
   %{buildroot}%{_datadir}/doc/%{name}-devel

%check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%doc README.md 
%{_exec_prefix}/lib/libmongocxx.so.*
%{_exec_prefix}/lib/libbsoncxx.so.*
%{_exec_prefix}/lib/libmongocxx.a
%{_exec_prefix}/lib/libbsoncxx.a

%files devel
%{_includedir}/*
%{_exec_prefix}/lib/libmongocxx.so
%{_exec_prefix}/lib/libbsoncxx.so
%{_exec_prefix}/lib/pkgconfig/lib*.pc
%{_exec_prefix}/lib/cmake/libmongocxx*/*.cmake
%{_exec_prefix}/lib/cmake/libbsoncxx*/*.cmake

%{_datadir}/doc/*

%changelog
* Tue May 23 2017 Huang Jinhua <sjtuhjh@hotmail.com> 3.1.1
- Initial Estuary Pakcage for Mongo-CXX-Driver
%{_datadir}/doc/*

%changelog
* Tue May 23 2017 Huang Jinhua <sjtuhjh@hotmail.com> 3.1.1
- Initial Estuary Pakcage for Mongo-CXX-Driver
