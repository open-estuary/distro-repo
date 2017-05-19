%global oname redis
Name:          redis-protocol
Version:       0.7
Release:       4%{?dist}
Summary:       Java client and server implementation of Redis
License:       ASL 2.0
URL:           http://github.com/spullara/redis-protocol
Source0:       https://github.com/spullara/redis-protocol/archive/%{oname}-%{version}.tar.gz
# https://github.com/spullara/redis-protocol/issues/45
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

Patch0:        redis_protocol_pom_aarch64.patch

BuildRequires: maven-local
BuildRequires: mvn(com.github.spullara.cli-parser:cli-parser)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(junit:junit)

BuildArch:     noarch

%description
A very fast Redis client for the JVM.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{oname}-%{version}
%patch0 -p1

find . -name "*.jar" -print -delete
find . -name "*.class" -print -delete

cp -p %{SOURCE1} LICENSE
sed -i 's/\r//' LICENSE

# These modules use com.github.spullara.java:concurrent6
%pom_disable_module netty
# https://bugzilla.redhat.com/show_bug.cgi?id=849496
# org.webbitserver:webbit::test
%pom_disable_module netty-client
# io.netty:netty-all:4.0.0.CR3
%pom_disable_module netty4
%pom_disable_module netty4-client
%pom_disable_module netty4-server

# com.github.spullara.mustache.java:compiler:0.8.9
%pom_disable_module redisgen

%pom_remove_plugin :maven-assembly-plugin benchmark

%build
mvn install -DskipTests 
mvn rpm:rpm

# use web connection
%mvn_build -f 

%install
%mvn_install

%files -f .mfiles
%doc README
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 gil cattaneo <puntogil@libero.it> 0.7-1
- initial rpm
