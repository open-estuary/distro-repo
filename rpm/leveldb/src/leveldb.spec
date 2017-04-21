Name:           leveldb
Version:   1.20
Release:        1%{?dist}
Summary:        A fast and lightweight key/value database library by Google
License:        BSD
URL:            https://github.com/google/leveldb
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# available in https://github.com/fusesource/leveldbjni/blob/leveldb.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  snappy-devel

%description
LevelDB is a fast key-value storage library written at Google that provides an
ordered mapping from string keys to string values.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1
cat > %{name}.pc << EOF
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version:   1.20
Libs: -l%{name}
EOF

%global configure() {                  \
  export OPT="-DNDEBUG"                \
  export CFLAGS="%{optflags}"          \
  export CXXFLAGS="%{optflags}"        \
  export LDFLAGS="%{__global_ldflags}" \
}

%build
%configure
%make_build

%install
mkdir -p %{buildroot}{%{_libdir}/pkgconfig,%{_includedir}}
cp -a out-shared/lib%{name}.so* %{buildroot}%{_libdir}/
cp -a out-static/lib%{name}.a* %{buildroot}%{_libdir}/
cp -a include/%{name}/ %{buildroot}%{_includedir}/
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%check
%configure
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}.a*

%files devel
%doc doc/ README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Mar 2 2017 Huang Jinhua <sjtuhjh@hotmail.com> - 1.20
- Initial package
