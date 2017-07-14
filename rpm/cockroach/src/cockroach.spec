%global provider        github
%global provider_tld    com
%global project         cockroachdb
%global repo            cockroach
# https://github.com/cockroachdb/cockroach
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          b692a7cc7acc57022d1441034b93b85d860b7e86
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Version:        1.0.3
Release:        1.0.3
Summary:        !!!!FILL!!!!
License:        !!!!FILL!!!!
URL:            https://%{provider_prefix}
Source0:        cockroach-v%{version}.src.tgz

BuildRequires: gcc-c++
BuildRequires: devtoolset-4-golang >= 1.5.1
BuildRequires: git

%description
CockroachDB is a distributed SQL database built on a transactional and strongly-consistent key-value store. It scales horizontally; survives disk, machine, rack, and even datacenter failures with minimal latency disruption and no manual intervention; supports strongly-consistent ACID transactions; and provides a familiar SQL API for structuring, manipulating, and querying data.

%package debug
Summary:        Debug files for %{name}
Requires:       %{name} = %{version}-%{release}

%description debug
CockroachDB is a distributed SQL database built on a transactional and strongly-consistent key-value store. It scales horizontally; survives disk, machine, rack, and even datacenter failures with minimal latency disruption and no manual intervention; supports strongly-consistent ACID transactions; and provides a familiar SQL API for structuring, manipulating, and querying data.

%prep
%setup -q -n %{repo}-v%{version}
sed -i 's/\/usr\/local/\/usr/g' Makefile

%build
#export GOPATH=$(pwd)/_build:%{buildroot}%{gopath}:/opt/rh/devtoolset-4/root%{gopath}
#export PATH=${GOPATH}/bin:${PATH}

#go get -d github.com/cockroachdb/cockroach

#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/pkg/build.type=release"
#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildTag=%{shell git describe --dirty --tags}"
#export LDFLAGS=$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildTag=%{TAG}
#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildTime=$(shell date -u '+%Y/%m/%d %H:%M:%S')"
#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildDeps=$(shell GOPATH=${GOPATH} build/depvers.sh)"

#export TAGS="release"
#export GOFLAGS=" -installsuffix release-gnu"

#go build  -ldflags $LDFLAGS $GOFLAGS -i -o cockroach
#go build -tags $TAGS $GOFLAGS -i -o cockroach
#go build -tags $TAGS $GOFLAGS -ldflags $LDFLAGS -i -o cockroach

make build

%install
#mkdir -p $RPM_BUILD_ROOT%{_bindir}/
DESTDIR=$RPM_BUILD_ROOT make install
#install -pm 0755 cockroach $RPM_BUILD_ROOT%{_bindir}/

%files
%{_bindir}/cockroach
%{_usr}/lib/*
#%{_defaultdocdir}/*

%files debug
%{_usrsrc}/debug/*

#%doc README.md LICENSE

%changelog
* Mon Jul 10 2017 Huang Jinhua <sjtuhjh@hotmail.com> 1.0.3
- Open Estuary ARM64 release

* Tue Dec 29 2015 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0-0.1.gita724578
- First package for Fedora
