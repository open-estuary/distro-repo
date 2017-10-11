Name:           order
Version:   1.0
Release:        0
Summary:        order jar
License:        GPL-2.0
Source:         https://github.com/zhouxingchen1993/discovery.git/order-1.0.tar.gz
BuildRequires: maven-local

%description
clone code , build package, excute jar

%prep
%setup -q

%build
#%_configure
#make %{?_smp_mflags}

cd %{_sourcedir}/
tar -zxvf %{name}-%{version}.tar.gz
cd %{name}-%{version}/order-service
mvn clean package
cd ../../

%install
cd %{_sourcedir}
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile
tar -zcvf %{name}-%{version}-jar.tar.gz %{name}-%{version}/order-service/target
scp -r  %{_sourcedir}/%{name}-%{version}-jar.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile

%files
%defattr(-,root,root,-)
%{_bindir}/jarfile/*

%clean
rm -rf %{_sourcedir}/%{name}-%{version}.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}
rm -rf %{_sourcedir}/%{name}-%{version}-jar.tar.gz

%changelog
* Wed Oct 11 2017 zhouxingchen  <zhouxingchen@huawei.com> - 1.0-1
- create order service 1.0 rpm package                              
