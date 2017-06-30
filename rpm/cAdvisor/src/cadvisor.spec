%if 0%{?fedora} || 0%{?rhel} >= 6
%global with_devel 1
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         google
%global repo            cadvisor
# https://github.com/google/cadvisor
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          546a3771589bdb356777c646c6eca24914fdd48b
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Version:        0.26.1
Release:        2%{?dist}
Summary:        Analyzes resource usage and performance characteristics of running containers
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/v%{version}.tar.gz
Source1:        cadvisor
Source2:        cadvisor.service

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
# arm does not have zfs-fuse
ExclusiveArch:  %{ix86} x86_64 aarch64 ppc64le
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires: git
BuildRequires: systemd
BuildRequires: glibc-static

#%if ! 0%{?with_bundled}
%if 0
#BuildRequires: docker-io-pkg-devel
#BuildRequires: docker-io-devel
# indirect deps of docker
#BuildRequires:  golang(github.com/Sirupsen/logrus)

BuildRequires: golang(github.com/SeanDolphin/bqschema)
BuildRequires: golang(github.com/Shopify/sarama)
BuildRequires: golang(github.com/abbot/go-http-auth)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/ec2metadata)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/session)
BuildRequires: golang(github.com/docker/docker/pkg/mount)
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/fsouza/go-dockerclient)
BuildRequires: golang(github.com/garyburd/redigo/redis)
BuildRequires: golang(github.com/golang/glog)
BuildRequires: golang(github.com/influxdb/influxdb/client)
BuildRequires: golang(github.com/mistifyio/go-zfs)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/cgroups)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/cgroups/fs)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/configs)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/stretchr/testify/mock)
BuildRequires: golang(golang.org/x/exp/inotify)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/jwt)
BuildRequires: golang(google.golang.org/api/bigquery/v2)
BuildRequires: golang(google.golang.org/cloud/compute/metadata)
BuildRequires: golang(gopkg.in/olivere/elastic.v2)
%endif

%description
%{summary}

cAdvisor (Container Advisor) provides container users an understanding of the
resource usage and performance characteristics of their running containers.
It is a running daemon that collects, aggregates, processes, and exports
information about running containers. Specifically, for each container it keeps
resource isolation parameters, historical resource usage, histograms of
complete historical resource usage and network statistics. This data is
exported by container and machine-wide.

cAdvisor currently supports lmctfy containers as well as Docker containers
(those that use the default libcontainer execdriver). Other container backends
can also be added. cAdvisor's container abstraction is based on lmctfy's
so containers are inherently nested hierarchically.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0
#%if 0%{?with_check}
#BuildRequires: docker-io-pkg-devel
BuildRequires: golang(github.com/Shopify/sarama)
BuildRequires: golang(github.com/abbot/go-http-auth)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/ec2metadata)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/session)
BuildRequires: golang(github.com/docker/docker/pkg/mount)
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/fsouza/go-dockerclient)
BuildRequires: golang(github.com/garyburd/redigo/redis)
BuildRequires: golang(github.com/golang/glog)
BuildRequires: golang(github.com/influxdb/influxdb/client)
BuildRequires: golang(github.com/mistifyio/go-zfs)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/cgroups)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/cgroups/fs)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/configs)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/stretchr/testify/mock)
BuildRequires: golang(golang.org/x/exp/inotify)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/jwt)
BuildRequires: golang(google.golang.org/api/bigquery/v2)
BuildRequires: golang(google.golang.org/cloud/compute/metadata)
BuildRequires: golang(gopkg.in/olivere/elastic.v2)
%endif

#Requires: docker-io-pkg-devel
Requires: golang(github.com/Shopify/sarama)
Requires: golang(github.com/abbot/go-http-auth)
Requires: golang(github.com/aws/aws-sdk-go/aws)
Requires: golang(github.com/aws/aws-sdk-go/aws/ec2metadata)
Requires: golang(github.com/aws/aws-sdk-go/aws/session)
Requires: golang(github.com/docker/docker/pkg/mount)
Requires: golang(github.com/docker/go-units)
Requires: golang(github.com/fsouza/go-dockerclient)
Requires: golang(github.com/garyburd/redigo/redis)
Requires: golang(github.com/golang/glog)
Requires: golang(github.com/influxdb/influxdb/client)
Requires: golang(github.com/mistifyio/go-zfs)
Requires: golang(github.com/opencontainers/runc/libcontainer)
Requires: golang(github.com/opencontainers/runc/libcontainer/cgroups)
Requires: golang(github.com/opencontainers/runc/libcontainer/cgroups/fs)
Requires: golang(github.com/opencontainers/runc/libcontainer/configs)
Requires: golang(github.com/prometheus/client_golang/prometheus)
Requires: golang(github.com/stretchr/testify/assert)
Requires: golang(github.com/stretchr/testify/mock)
Requires: golang(golang.org/x/exp/inotify)
Requires: golang(golang.org/x/oauth2)
Requires: golang(golang.org/x/oauth2/jwt)
Requires: golang(google.golang.org/api/bigquery/v2)
Requires: golang(google.golang.org/cloud/compute/metadata)
Requires: golang(gopkg.in/olivere/elastic.v2)

Provides: golang(%{import_path}/api) = %{version}-%{release}
Provides: golang(%{import_path}/cache) = %{version}-%{release}
Provides: golang(%{import_path}/cache/memory) = %{version}-%{release}
Provides: golang(%{import_path}/client) = %{version}-%{release}
Provides: golang(%{import_path}/client/v2) = %{version}-%{release}
Provides: golang(%{import_path}/collector) = %{version}-%{release}
Provides: golang(%{import_path}/container) = %{version}-%{release}
Provides: golang(%{import_path}/container/docker) = %{version}-%{release}
Provides: golang(%{import_path}/container/libcontainer) = %{version}-%{release}
Provides: golang(%{import_path}/container/raw) = %{version}-%{release}
Provides: golang(%{import_path}/events) = %{version}-%{release}
Provides: golang(%{import_path}/fs) = %{version}-%{release}
Provides: golang(%{import_path}/healthz) = %{version}-%{release}
Provides: golang(%{import_path}/http) = %{version}-%{release}
Provides: golang(%{import_path}/http/mux) = %{version}-%{release}
Provides: golang(%{import_path}/info/v1) = %{version}-%{release}
Provides: golang(%{import_path}/info/v1/test) = %{version}-%{release}
Provides: golang(%{import_path}/info/v2) = %{version}-%{release}
Provides: golang(%{import_path}/integration/framework) = %{version}-%{release}
Provides: golang(%{import_path}/integration/tests/api) = %{version}-%{release}
Provides: golang(%{import_path}/integration/tests/healthz) = %{version}-%{release}
Provides: golang(%{import_path}/manager) = %{version}-%{release}
Provides: golang(%{import_path}/metrics) = %{version}-%{release}
Provides: golang(%{import_path}/pages) = %{version}-%{release}
Provides: golang(%{import_path}/pages/static) = %{version}-%{release}
Provides: golang(%{import_path}/storage) = %{version}-%{release}
Provides: golang(%{import_path}/storage/bigquery) = %{version}-%{release}
Provides: golang(%{import_path}/storage/bigquery/client) = %{version}-%{release}
Provides: golang(%{import_path}/storage/elasticsearch) = %{version}-%{release}
Provides: golang(%{import_path}/storage/influxdb) = %{version}-%{release}
Provides: golang(%{import_path}/storage/kafka) = %{version}-%{release}
Provides: golang(%{import_path}/storage/redis) = %{version}-%{release}
Provides: golang(%{import_path}/storage/statsd) = %{version}-%{release}
Provides: golang(%{import_path}/storage/statsd/client) = %{version}-%{release}
Provides: golang(%{import_path}/storage/stdout) = %{version}-%{release}
Provides: golang(%{import_path}/storage/test) = %{version}-%{release}
Provides: golang(%{import_path}/summary) = %{version}-%{release}
Provides: golang(%{import_path}/utils) = %{version}-%{release}
Provides: golang(%{import_path}/utils/cloudinfo) = %{version}-%{release}
Provides: golang(%{import_path}/utils/container) = %{version}-%{release}
Provides: golang(%{import_path}/utils/cpuload) = %{version}-%{release}
Provides: golang(%{import_path}/utils/cpuload/netlink) = %{version}-%{release}
Provides: golang(%{import_path}/utils/machine) = %{version}-%{release}
Provides: golang(%{import_path}/utils/oomparser) = %{version}-%{release}
Provides: golang(%{import_path}/utils/procfs) = %{version}-%{release}
Provides: golang(%{import_path}/utils/sysfs) = %{version}-%{release}
Provides: golang(%{import_path}/utils/sysfs/fakesysfs) = %{version}-%{release}
Provides: golang(%{import_path}/utils/sysinfo) = %{version}-%{release}
Provides: golang(%{import_path}/validate) = %{version}-%{release}
Provides: golang(%{import_path}/version) = %{version}-%{release}

%description devel
%{summary}

cAdvisor (Container Advisor) provides container users an understanding of the
resource usage and performance characteristics of their running containers.
It is a running daemon that collects, aggregates, processes, and exports
information about running containers. Specifically, for each container it keeps
resource isolation parameters, historical resource usage, histograms of
complete historical resource usage and network statistics. This data is
exported by container and machine-wide.

cAdvisor currently supports lmctfy containers as well as Docker containers
(those that use the default libcontainer execdriver). Other container backends
can also be added. cAdvisor's container abstraction is based on lmctfy's
so containers are inherently nested hierarchically.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test
Summary:         Unit tests for %{name} package
# If gccgo_arches does not fit or is not defined fall through to golang

%if 0
#%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
BuildRequires:   golang(github.com/kr/pretty)
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}
Requires:        golang(github.com/kr/pretty)

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%autosetup -Sgit -n  cadvisor-%{version}

%build
mkdir -p src/github.com/google
ln -s ../../../ src/github.com/google/cadvisor

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

cd src/github.com/google/cadvisor

#Fix one bug
sed -i 's/tags/always/g' build/build.sh

make build
#%gobuild -o bin/cadvisor %{import_path}

%install
# main package binary
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 src/github.com/google/cadvisor/cadvisor %{buildroot}%{_bindir}

# install systemd/sysconfig 
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 0660 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go" | grep -v "./Godeps") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done

for file in $(find . -iname "*.json" | grep -v "./Godeps") \
	./fs/test_resources/diskstats \
	./metrics/testdata/prometheus_metrics \
	./machine/testdata/cpuinfo \
	./utils/oomparser/*.txt; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if 0
%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/api
%gotest %{import_path}/cache/memory
%gotest %{import_path}/client
%gotest %{import_path}/client/v2
#%%gotest %{import_path}/collector
# undefined: FactoryForMockContainerHandler
#%%gotest %{import_path}/container
%gotest %{import_path}/container/raw
%gotest %{import_path}/events
%gotest %{import_path}/fs
%gotest %{import_path}/info/v1
# requires root
#%%gotest %%{import_path}/integration/tests/api
# mostly likely requires kubernetes running
#%%gotest %%{import_path}/integration/tests/healthz
#%%gotest %{import_path}/manager
%gotest %{import_path}/metrics
%gotest %{import_path}/storage/influxdb
%gotest %{import_path}/summary
%gotest %{import_path}/utils
%gotest %{import_path}/utils/machine
%gotest %{import_path}/utils/oomparser
%gotest %{import_path}/utils/sysinfo
%endif
%endif

%post
%systemd_post cadvisor.service

%preun
%systemd_preun cadvisor.service

%postun
%systemd_postun

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc CHANGELOG.md README.md CONTRIBUTING.md AUTHORS
%doc Godeps/Godeps.json
%{_bindir}/cadvisor
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc CHANGELOG.md README.md CONTRIBUTING.md AUTHORS
%doc Godeps/Godeps.json
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test -f unit-test.file-list
%license LICENSE
%doc CHANGELOG.md README.md CONTRIBUTING.md AUTHORS
%endif

%changelog
* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.2-2
- https://fedoraproject.org/wiki/Changes/golang1.7

* Mon Apr 11 2016 jchaloup <jchaloup@redhat.com> - 0.22.2-1
- Bump to upstream 546a3771589bdb356777c646c6eca24914fdd48b
  resolves: #1256978

* Sat Apr  9 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.16.0.2-4
- Package spec cleanups

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0.2-3
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 06 2015 jchaloup <jchaloup@redhat.com> - 0.16.0.2-1
- Update to 0.16.0.2
  related: #1256978

* Thu Aug 27 2015 jchaloup <jchaloup@redhat.com> - 0.16.0.1-1
- Update to 0.16.0.1
- Update spec file to spec-2.0
  resolves: #1256978

* Thu Jul 02 2015 jchaloup <jchaloup@redhat.com> - 0.16.0-1
- Bump to upstream ec240b60c547caf76c4cd9d73154ebb421fb9da1
  resolves: #1238481

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 jchaloup <jchaloup@redhat.com> - 0.15.1-1
- Update to 0.15.1
  related: #1219972

* Fri Jun 05 2015 jchaloup <jchaloup@redhat.com> - 0.14.0-1
- Update to 0.14.0
  related: #1219972

* Fri Jun 05 2015 jchaloup <jchaloup@redhat.com> - 0.13.0-2
- Build devel and debundled deps only for Fedora
  related: #1219972

* Fri May 08 2015 jchaloup <jchaloup@redhat.com> - 0.13.0-1
- Update to 0.13.0
- Add missing [B]Rs for devel subpackage
- Add Godeps.json to docs
  resolves: #1219972

* Thu Apr 09 2015 jchaloup <jchaloup@redhat.com> - 0.10.1-2
- Remove wrong option in cadvisor.service
  resolves: #1210336

* Mon Mar 30 2015 jchaloup <jchaloup@redhat.com> - 0.10.1-0.1.gitef7dddf
- Update to 0.10.1
- Add debug info
  related: #1141896

* Thu Mar 26 2015 jchaloup <jchaloup@redhat.com> - 0.6.2-0.3.git89088df
- Fix broken dependencies
- Convert int64 to float64 when calling HumanSize
  related: #1141896

* Fri Dec 12 2014 jchaloup <jchaloup@redhat.com> - 0.6.2-0.1.git89088df
- remove -q option from autosetup, it is not supported
  related: #1141896

* Fri Dec 05 2014 Eric Paris <eparis@redhat.com> - 0.6.2-0.0.git89088df
- Bump to upstream 89088df70eca64cf9d6b9a23a3d2bc21a30916d6

* Fri Nov 14 2014 Eric Paris <eparis@redhat.com> - 0.6.0-0.0.git1e98602
- update to 0.6.0

* Fri Nov 14 2014 Eric Paris <eparis@redhat.com> - 0.5.0-0.1.git8c4f650
- include fs/*.go

* Thu Nov 13 2014 Eric Paris <eparis@redhat.com> - 0.5.0-0.0.git8c4f650
- update to 0.5.0

* Sat Oct 18 2014 jchaloup <jchaloup@redhat.com> - 0.4.1-0.1.git6906a8c
- update to 0.4.1

* Thu Oct 09 2014 jchaloup <jchaloup@redhat.com> - 0.3.0-0.4.git9d158c3
- Move cadvisor.service and cadvisor config file from patch into repo
- Fix the build, thanks to Lokesh

* Fri Sep 19 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.0-0.3.git9d158c3
- own parent directory of <gopath</src/<import_path>
- preserve timestamps of copied files in -devel
- use _unitdir macro for systemd install path

* Fri Sep 12 2014 Eric Paris <eparis@redhat.com - 0.3.0-0.2.git9d158c3
- Log to stderr (and thus journal) by default

* Thu Sep 11 2014 Eric Paris <eparis@redhat.com - 0.3.0-0.1.git9d158c3
- Bump to upstream 9d158c3d66e8e6d14cfeb1d73695ab18dbc744e8

* Wed Aug 20 2014 Eric Paris <eparis@redhat.com - 0.2.0-2
- Bump to upstream 17b0ec576bcbeb321c133e4378dee1e500c9850d

* Thu Aug 07 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.2.0-1
- First package for Fedora
