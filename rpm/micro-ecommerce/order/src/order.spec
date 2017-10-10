Name:           order
Version:   1.0
Release:        0
Summary:        order jar
License:        GPL-2.0
Source:         https://github.com/zhouxingchen1993/discovery.git/order-1.0.tar.gz
#BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
clone code , build package, excute jar

%prep
#%setup -q

%build
#%_configure
#make %{?_smp_mflags}

%install
cd %{_sourcedir}
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile
scp -r  %{_sourcedir}/%{name}-%{version}.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile

%files
%defattr(-,root,root,-)
%{_bindir}/jarfile/*

%clean
rm -rf %{_sourcedir}/%{name}-%{version}.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}
%changelog
                              
