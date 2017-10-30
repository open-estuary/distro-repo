#%define __\_os\_install_post %{nil}
%define __jar_repack 0
%define service_installdir        /etc/systemd/system
%define api_installdir            /etc/micro-services/api-gateway
%define discovery_installdir      /etc/micro-services/discovery
%define order_installdir          /etc/e-commerce/order
%define cart_installdir           /etc/e-commerce/cart
%define search_installdir         /etc/e-commerce/search

%define apigateway_name           api-gateway-1.0.0.jar
%define discovery_name            eureka-server-0.0.1-SNAPSHOT.jar
%define order_name                order-0.0.1-SNAPSHOT.jar
%define cart_name                 cart-0.0.1-SNAPSHOT.jar
%define search_name               search-0.0.1-SNAPSHOT.jar

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

cd %{name}-%{version}/apigateway-service
mvn clean package
cd ../..

cd %{name}-%{version}/discovery-service
mvn clean package
cd ../..

cd %{name}-%{version}/cart-service
mvn clean package
cd ../..

cd %{name}-%{version}/order-service
mvn clean package
cd ../..

cd %{name}-%{version}/search-service > /dev/null
mvn clean package
cd ../..

%install
pushd %{_sourcedir} > /dev/null
install -d -m 755 %{buildroot}%{service_installdir}
install -d -m 755 %{buildroot}%{_bindir} 

install -d -m 755 %{buildroot}%{api_installdir}
install -d -m 755 %{buildroot}%{discovery_installdir}
install -d -m 755 %{buildroot}%{order_installdir}
install -d -m 755 %{buildroot}%{cart_installdir}
install -d -m 755 %{buildroot}%{search_installdir}

install -d -m 755 %{buildroot}/opt/micro-services
install -d -m 755 %{buildroot}/opt/e-commerce

cp -rf  %{name}-%{version}/apigateway-service/target/%{apigateway_name} %{buildroot}%{api_installdir}
cp -f microservice-zuul %{buildroot}%{_bindir}
cp -f microservice-zuul.service %{buildroot}%{service_installdir}

cp -rf  %{name}-%{version}/discovery-service/target/%{discovery_name} %{buildroot}%{discovery_installdir}
cp -f microservice-eureka %{buildroot}%{_bindir}
cp -f microservice-eureka.service %{buildroot}%{service_installdir}

cp -rf  %{name}-%{version}/order-service/target/%{order_name} %{buildroot}%{order_installdir}
cp -f e-commerce-order %{buildroot}%{_bindir}
cp -f e-commerce-order.service %{buildroot}%{service_installdir}

cp -rf  %{name}-%{version}/cart-service/target/%{cart_name} %{buildroot}%{cart_installdir}
cp -f e-commerce-cart %{buildroot}%{_bindir}
cp -f e-commerce-cart.service %{buildroot}%{service_installdir}

cp -rf  %{name}-%{version}/search-service/target/%{search_name} %{buildroot}%{search_installdir}
cp -f e-commerce-search %{buildroot}%{_bindir}
cp -f e-commerce-search.service %{buildroot}%{service_installdir}

cd %{buildroot}%{api_installdir}
ln -s %{apigateway_name} micro-service-zuul.jar
cd ../discovery
ln -s %{discovery_name} micro-service-eureka.jar
cd ../../e-commerce/order
ln -s %{order_name} e-commerce-order.jar
cd ../cart
ln -s %{cart_name} e-commerce-cart.jar
cd ../search
ln -s %{search_name} e-commerce-search.jar

#ln -s %{buildroot}%{api_installdir}/%{apigateway_name} %{buildroot}%{api_installdir}/micro-service-zuul.jar
#ln -s %{buildroot}%{discovery_installdir}/%{discovery_name} %{buildroot}%{discovery_installdir}/micro-service-eureka.jar
#ln -s %{buildroot}%{order_installdir}/%{order_name} %{buildroot}%{order_installdir}/e-commerce-order.jar
#ln -s %{buildroot}%{cart_installdir}/%{cart_name} %{buildroot}%{cart_installdir}/e-commerce-cart.jar
#ln -s %{buildroot}%{search_installdir}/%{search_name} %{buildroot}%{search_installdir}/e-commerce-search.jar

#mkdir -p %{buildroot}/opt/micro-services
#mkdir -p %{buildroot}/opt/e-commerce

#ln -s %{buildroot}%{_bindir}/microservice-zuul %{buildroot}/opt/micro-services/microservice-zuul
#ln -s %{buildroot}%{_bindir}/microservice-eureka %{buildroot}/opt/micro-services/microservice-eureka
#ln -s %{buildroot}%{_bindir}/e-commerce-order %{buildroot}/opt/e-commerce/e-commerce-order
#ln -s %{buildroot}%{_bindir}/e-commerce-cart %{buildroot}/opt/e-commerce/e-commerce-cart
#ln -s %{buildroot}%{_bindir}/e-commerce-search %{buildroot}/opt/e-commerce/e-commerce-search

cd %{buildroot}/opt/micro-services
ln -s ../../usr/bin/microservice-zuul microservice-zuul
ln -s ../../usr/bin/microservice-eureka microservice-eureka

cd ../e-commerce
ln -s ../../usr/bin/e-commerce-order e-commerce-order
ln -s ../../usr/bin/e-commerce-cart e-commerce-cart
ln -s ../../usr/bin/e-commerce-search e-commerce-search

%files api
%defattr(-,root,root,-)
%{api_installdir}/*
%{service_installdir}/microservice-zuul.service
%{_bindir}/microservice-zuul
/opt/micro-services/microservice-zuul

%files discovery
%defattr(-,root,root,-)
%{discovery_installdir}/*
%{service_installdir}/microservice-eureka.service
%{_bindir}/microservice-eureka
/opt/micro-services/microservice-eureka

%files cart
%defattr(-,root,root,-)
%{cart_installdir}/*
%{service_installdir}/e-commerce-cart.service
%{_bindir}/e-commerce-cart
/opt/e-commerce/e-commerce-cart

%files order
%defattr(-,root,root,-)
%{order_installdir}/*
%{service_installdir}/e-commerce-order.service
%{_bindir}/e-commerce-order
/opt/e-commerce/e-commerce-order

%files search
%defattr(-,root,root,-)
%{search_installdir}/*
%{service_installdir}/e-commerce-search.service
%{_bindir}/e-commerce-search
/opt/e-commerce/e-commerce-search

%clean
rm -rf %{_sourcedir}/%{name}-%{version}
rm -rf %{_sourcedir}/%{name}-%{version}.tar.gz
rm -rf %{_sourcedir}/package

%changelog
* Fri Oct 27 2017 zhouxingchen  <zhouxingchen@huawei.com> - 1.0-2
- update 5 service 1.0 rpm package

* Wed Oct 11 2017 zhouxingchen  <zhouxingchen@huawei.com> - 1.0-1
- create 5 service 1.0 rpm package
