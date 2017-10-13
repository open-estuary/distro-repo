Name:           micro-service
Version:   1.0
Release:        0
Summary:        micro-service jar
License:        GPL-2.0
Source:         https://github.com/open-estuary/packages.git/micro-service-1.0.tar.gz
BuildRequires: maven-local
Group:          jar

%package api
Group: jar
Summary: api jar

%description api

%package discovery
Group: jar
Summary: discovery jar

%description discovery

%package cart
Group: jar
Summary: cart jar

%description cart

%package order
Group: jar
Summary: order jar

%description order

%package search
Group: jar
Summary: search jar

%description search


%description
clone code , build package, excute jar

%prep
%setup -q

%build
#%_configure
#make %{?_smp_mflags}

pushd %{_sourcedir} > /dev/null
tar -zxvf %{name}-%{version}.tar.gz

pushd %{name}-%{version}/apigateway-service > /dev/null
mvn clean package
tar -zcvf %{name}-%{version}-api.tar.gz target
mv %{name}-%{version}-api.tar.gz ../../%{name}-%{version}-api.tar.gz
popd > /dev/null

pushd %{name}-%{version}/discovery-service > /dev/null
mvn clean package
tar -zcvf %{name}-%{version}-discovery.tar.gz target
mv %{name}-%{version}-discovery.tar.gz ../../%{name}-%{version}-discovery.tar.gz
popd > /dev/null

pushd %{name}-%{version}/cart-service > /dev/null
mvn clean package
tar -zcvf %{name}-%{version}-cart.tar.gz target
mv %{name}-%{version}-cart.tar.gz ../../%{name}-%{version}-cart.tar.gz
popd > /dev/null

pushd %{name}-%{version}/order-service > /dev/null
mvn clean package
tar -zcvf %{name}-%{version}-order.tar.gz target
mv %{name}-%{version}-order.tar.gz ../../%{name}-%{version}-order.tar.gz
popd > /dev/null

pushd %{name}-%{version}/search-service > /dev/null
mvn clean package
tar -zcvf %{name}-%{version}-search.tar.gz target
mv %{name}-%{version}-search.tar.gz ../../%{name}-%{version}-search.tar.gz
popd > /dev/null


%install
pushd %{_sourcedir} > /dev/null
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/api
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/discovery
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/cart
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/order
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/search

scp -r  %{name}-%{version}-api.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/api
scp -r  %{name}-%{version}-discovery.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/discovery
scp -r  %{name}-%{version}-cart.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/cart
scp -r  %{name}-%{version}-order.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/order
scp -r  %{name}-%{version}-search.tar.gz %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/%{_bindir}/jarfile/search

%files api
%defattr(-,root,root,-)
%{_bindir}/jarfile/api/*

%files discovery
%defattr(-,root,root,-)
%{_bindir}/jarfile/discovery/*

%files cart
%defattr(-,root,root,-)
%{_bindir}/jarfile/cart/*

%files order
%defattr(-,root,root,-)
%{_bindir}/jarfile/order/*

%files search
%defattr(-,root,root,-)
%{_bindir}/jarfile/search/*

%clean
#rm -rf %{_sourcedir}/%{name}-%{version}.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}
rm -rf %{_sourcedir}/%{name}-%{version}-api.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}-discovery.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}-cart.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}-order.tar.gz
rm -rf %{_sourcedir}/%{name}-%{version}-search.tar.gz
rm -rf %{_sourcedir}/package

%changelog
* Wed Oct 11 2017 zhouxingchen  <zhouxingchen@huawei.com> - 1.0-1
- create 5 service 1.0 rpm package
