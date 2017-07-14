%global provider        github
%global provider_tld    com
%global project         kubernetes
%global repo            kops
# https://github.com/kubernetes/kops
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          b692a7cc7acc57022d1441034b93b85d860b7e86
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Version:        1.6.2
Release:        1.6.2
Summary:        Kubernetes Operations 
License:        Apache License 2.0
URL:            https://%{provider_prefix}
Source0:        kops-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: devtoolset-4-golang >= 1.8
BuildRequires: git

%description
The easiest way to get a production grade Kubernetes cluster up and running.

%prep
%setup -q -n %{repo}-%{version}
#sed -i 's/\/usr\/local/\/usr/g' Makefile

%build

export GOPATH=$(pwd)
go get -d k8s.io/kops
cd ${GOPATH}/src/k8s.io/kops
rm -fr _vendor
git checkout %{version}
git checkout --f _vendor
make

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
#DESTDIR=$RPM_BUILD_ROOT make install
install -pm 0755 bin/kops $RPM_BUILD_ROOT%{_bindir}/

%files
%{_bindir}/kops
#%{_usr}/lib/*
#%{_defaultdocdir}/*

#%doc README.md LICENSE

%changelog
* Mon Jul 10 2017 Huang Jinhua <sjtuhjh@hotmail.com> 1.6.2
- Open Estuary ARM64 release

