%if 0%{?fedora}
%global with_devel 1
%global with_bundled 0
%global with_debug 1
# Some tests fails and it takes a lot of time to investigate
# what is wrong
%global with_check 0
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

#%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
#%endif

%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            etcd
# https://github.com/coreos/etcd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          0f4a535c2fb7a2920e13e2e19b9eaf6b2e9285e5
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:		%{repo}
Version:	3.1.9
Release:	1%{?dist}
Summary:	A highly-available key value store for shared configuration
License:	ASL 2.0
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.conf
Patch2:         change-import-path.patch
Patch3:         run-etcd-on-ppc64le-by-default.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 ppc64le s390x
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
#BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:   devtoolset-4-golang

%if ! 0%{?with_bundled}
BuildRequires: golang(github.com/bgentry/speakeasy)
BuildRequires: golang(github.com/boltdb/bolt)
BuildRequires: golang(github.com/cheggaaa/pb)
BuildRequires: golang(github.com/cockroachdb/cmux)
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/coreos/go-systemd/daemon)
BuildRequires: golang(github.com/coreos/go-systemd/util)
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/dustin/go-humanize)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/google/btree)
BuildRequires: golang(github.com/grpc-ecosystem/go-grpc-prometheus)
BuildRequires: golang(github.com/grpc-ecosystem/grpc-gateway/runtime)
BuildRequires: golang(github.com/grpc-ecosystem/grpc-gateway/utilities)
BuildRequires: golang(github.com/jonboulle/clockwork)
BuildRequires: golang(github.com/karlseguin/ccache)
BuildRequires: golang(github.com/kr/pty)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/ugorji/go/codec)
BuildRequires: golang(github.com/urfave/cli)
BuildRequires: golang(github.com/xiang90/probing)
BuildRequires: golang(golang.org/x/crypto/bcrypt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/http2)
BuildRequires: golang(golang.org/x/time/rate)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/credentials)
BuildRequires: golang(google.golang.org/grpc/grpclog)
BuildRequires: golang(google.golang.org/grpc/metadata)
BuildRequires: golang(google.golang.org/grpc/naming)
BuildRequires: golang(google.golang.org/grpc/transport)
%endif

BuildRequires:	systemd

Requires(pre):	shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A highly-available key value store for shared configuration.

%if 0%{?with_devel}
%package devel
Summary:        etcd golang devel libraries
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires: golang(github.com/bgentry/speakeasy)
BuildRequires: golang(github.com/boltdb/bolt)
BuildRequires: golang(github.com/cheggaaa/pb)
BuildRequires: golang(github.com/cockroachdb/cmux)
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/coreos/go-systemd/daemon)
BuildRequires: golang(github.com/coreos/go-systemd/util)
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/dustin/go-humanize)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/google/btree)
BuildRequires: golang(github.com/grpc-ecosystem/go-grpc-prometheus)
BuildRequires: golang(github.com/grpc-ecosystem/grpc-gateway/runtime)
BuildRequires: golang(github.com/grpc-ecosystem/grpc-gateway/utilities)
BuildRequires: golang(github.com/jonboulle/clockwork)
BuildRequires: golang(github.com/karlseguin/ccache)
BuildRequires: golang(github.com/kr/pty)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/pflag)
BuildRequires: golang(github.com/ugorji/go/codec)
BuildRequires: golang(github.com/urfave/cli)
BuildRequires: golang(github.com/xiang90/probing)
BuildRequires: golang(golang.org/x/crypto/bcrypt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/http2)
BuildRequires: golang(golang.org/x/time/rate)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/credentials)
BuildRequires: golang(google.golang.org/grpc/grpclog)
BuildRequires: golang(google.golang.org/grpc/metadata)
BuildRequires: golang(google.golang.org/grpc/naming)
%endif

Requires: golang(github.com/bgentry/speakeasy)
Requires: golang(github.com/boltdb/bolt)
Requires: golang(github.com/cheggaaa/pb)
Requires: golang(github.com/cockroachdb/cmux)
Requires: golang(github.com/coreos/go-semver/semver)
Requires: golang(github.com/coreos/go-systemd/daemon)
Requires: golang(github.com/coreos/go-systemd/util)
Requires: golang(github.com/coreos/pkg/capnslog)
Requires: golang(github.com/dustin/go-humanize)
Requires: golang(github.com/ghodss/yaml)
Requires: golang(github.com/gogo/protobuf/proto)
Requires: golang(github.com/golang/protobuf/proto)
Requires: golang(github.com/google/btree)
Requires: golang(github.com/grpc-ecosystem/go-grpc-prometheus)
Requires: golang(github.com/grpc-ecosystem/grpc-gateway/runtime)
Requires: golang(github.com/grpc-ecosystem/grpc-gateway/utilities)
Requires: golang(github.com/jonboulle/clockwork)
Requires: golang(github.com/karlseguin/ccache)
Requires: golang(github.com/kr/pty)
Requires: golang(github.com/olekukonko/tablewriter)
Requires: golang(github.com/prometheus/client_golang/prometheus)
Requires: golang(github.com/spf13/cobra)
Requires: golang(github.com/spf13/pflag)
Requires: golang(github.com/ugorji/go/codec)
Requires: golang(github.com/urfave/cli)
Requires: golang(github.com/xiang90/probing)
Requires: golang(golang.org/x/crypto/bcrypt)
Requires: golang(golang.org/x/net/context)
Requires: golang(golang.org/x/net/http2)
Requires: golang(golang.org/x/time/rate)
Requires: golang(google.golang.org/grpc)
Requires: golang(google.golang.org/grpc/codes)
Requires: golang(google.golang.org/grpc/credentials)
Requires: golang(google.golang.org/grpc/grpclog)
Requires: golang(google.golang.org/grpc/metadata)
Requires: golang(google.golang.org/grpc/naming)

Provides: golang(%{import_path}/alarm) = %{version}-%{release}
Provides: golang(%{import_path}/auth) = %{version}-%{release}
Provides: golang(%{import_path}/auth/authpb) = %{version}-%{release}
Provides: golang(%{import_path}/client) = %{version}-%{release}
Provides: golang(%{import_path}/client/integration) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/concurrency) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/integration) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/mirror) = %{version}-%{release}
Provides: golang(%{import_path}/clientv3/naming) = %{version}-%{release}
Provides: golang(%{import_path}/compactor) = %{version}-%{release}
Provides: golang(%{import_path}/contrib/recipes) = %{version}-%{release}
Provides: golang(%{import_path}/discovery) = %{version}-%{release}
Provides: golang(%{import_path}/e2e) = %{version}-%{release}
Provides: golang(%{import_path}/embed) = %{version}-%{release}
Provides: golang(%{import_path}/error) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv2) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv2/command) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv3) = %{version}-%{release}
Provides: golang(%{import_path}/etcdctl/ctlv3/command) = %{version}-%{release}
Provides: golang(%{import_path}/etcdmain) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v2http) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v2http/httptypes) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v3rpc) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/api/v3rpc/rpctypes) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/auth) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/etcdserverpb) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/membership) = %{version}-%{release}
Provides: golang(%{import_path}/etcdserver/stats) = %{version}-%{release}
Provides: golang(%{import_path}/integration) = %{version}-%{release}
Provides: golang(%{import_path}/lease) = %{version}-%{release}
Provides: golang(%{import_path}/lease/leasehttp) = %{version}-%{release}
Provides: golang(%{import_path}/lease/leasepb) = %{version}-%{release}
Provides: golang(%{import_path}/mvcc) = %{version}-%{release}
Provides: golang(%{import_path}/mvcc/backend) = %{version}-%{release}
Provides: golang(%{import_path}/mvcc/mvccpb) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/adt) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/contention) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cors) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/cpuutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/crc) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/expect) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/fileutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/flags) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/httputil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/idutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ioutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/logutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mock/mockstorage) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mock/mockstore) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/mock/mockwait) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/monotime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/netutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/osutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pathutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/pbutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/report) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/runtime) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/schedule) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/stringutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/testutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/tlsutil) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/transport) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/wait) = %{version}-%{release}
Provides: golang(%{import_path}/proxy/grpcproxy) = %{version}-%{release}
Provides: golang(%{import_path}/proxy/grpcproxy/cache) = %{version}-%{release}
Provides: golang(%{import_path}/proxy/httpproxy) = %{version}-%{release}
Provides: golang(%{import_path}/proxy/tcpproxy) = %{version}-%{release}
Provides: golang(%{import_path}/raft) = %{version}-%{release}
Provides: golang(%{import_path}/raft/raftpb) = %{version}-%{release}
Provides: golang(%{import_path}/raft/rafttest) = %{version}-%{release}
Provides: golang(%{import_path}/rafthttp) = %{version}-%{release}
Provides: golang(%{import_path}/snap) = %{version}-%{release}
Provides: golang(%{import_path}/snap/snappb) = %{version}-%{release}
Provides: golang(%{import_path}/store) = %{version}-%{release}
Provides: golang(%{import_path}/tools/benchmark/cmd) = %{version}-%{release}
Provides: golang(%{import_path}/tools/functional-tester/etcd-agent/client) = %{version}-%{release}
Provides: golang(%{import_path}/tools/functional-tester/etcd-runner/command) = %{version}-%{release}
Provides: golang(%{import_path}/version) = %{version}-%{release}
Provides: golang(%{import_path}/wal) = %{version}-%{release}
Provides: golang(%{import_path}/wal/walpb) = %{version}-%{release}

%description devel
golang development libraries for etcd, a highly-available key value store for
shared configuration.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{name}-%{commit}
# move content of vendor under Godeps as has been so far
mkdir -p Godeps/_workspace/src
mv cmd/vendor/* Godeps/_workspace/src/.

%patch2 -p1
%patch3 -p1

%build
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/etcd

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

export LDFLAGS="-X %{import_path}/version.GitSHA=%{shortcommit}"
%gobuild -o bin/etcd %{import_path}/cmd/etcd
%gobuild -o bin/etcdctl %{import_path}/etcdctl

%install
install -D -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 bin/%{name}ctl %{buildroot}%{_bindir}/%{name}ctl
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} %{SOURCE2}

# And create /var/lib/etcd
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
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

install -dp %{buildroot}/%{gopath}/src/%{import_path}/integration/
cp -rpav integration/fixtures %{buildroot}/%{gopath}/src/%{import_path}/integration/.
echo "%%{gopath}/src/%%{import_path}/integration/fixtures" >> unit-test.file-list

install -dp %{buildroot}/%{gopath}/src/%{import_path}/etcdserver/api/v2http/testdata
cp -rpav etcdserver/api/v2http/testdata %{buildroot}/%{gopath}/src/%{import_path}/etcdserver/api/v2http/.
echo "%%{gopath}/src/%%{import_path}/etcdserver/api/v2http/testdata" >> unit-test.file-list
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

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%ifarch x86_64
RACE="--race"
%else
RACE=""
%endif

# unit-tests
# TODO(jchaloup): read all the envs from test file
export IGNORE_PKGS="(cmd|vendor|etcdserverpb|rafttest)"
export INTEGRATION_PKGS="(integration|e2e|contrib|functional-tester)"
export TEST_PKGS=`find . -name \*_test.go | while read a; do dirname $a; done | sort | uniq | egrep -v "$IGNORE_PKGS" | sed "s|\./||g"`
export TESTS=`echo "$TEST_PKGS" | egrep -v "$INTEGRATION_PKGS"`

for test in ${TESTS}; do
%gotest -timeout 3m -cover ${RACE} -cpu 1,2,4 -run=Test github.com/coreos/etcd/${test}
done

./test

%endif

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_sharedstatedir}/%{name} \
	-s /sbin/nologin -c "etcd user" %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc *.md
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc *.md
%doc glide.lock
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%license LICENSE
%doc *.md
%endif

%changelog
* Sun Jun 11 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.9-1
- Update to 3.1.9
  resolves: #1460496

* Mon Jun 05 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.8-1
  Update to 3.1.8
  resolves: #1458717

* Tue May 02 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.7-1
- Update to 3.1.7
  resolves: #1447232

* Thu Apr 20 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.6-1
- Update to 3.1.6
  resolves: #1444068

* Tue Mar 28 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.5-1
- Update to 3.1.5
  resolves: #1436452

* Mon Mar 27 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.4-1
- Update to 3.1.4
  resolves: #1435028

* Mon Mar 20 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.3-1
- Update to v3.1.3
  related: #1415341

* Tue Mar 14 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.1.0-1
- Update to v3.1.0
  related: #1415341

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Jan Chaloupka <jchaloup@redhat.com> - 3.0.17-1
- Update to v3.0.17
  etcd-top removed by upstream
  resolves: #1415622

* Fri Nov 18 2016 jchaloup <jchaloup@redhat.com> - 3.0.15-2
- Remove ppc64le architecture restriction
  resolves: #1396463

* Tue Nov 15 2016 jchaloup <jchaloup@redhat.com> - 3.0.15-1
- Update to v3.0.15
  related: #1382965

* Mon Nov 07 2016 jchaloup <jchaloup@redhat.com> - 3.0.14-1
- Update to v3.0.14
  related: #1382965

* Thu Oct 27 2016 jchaloup <jchaloup@redhat.com> - 3.0.13-1
- Update to v3.0.13
  related: #1382965

* Mon Oct 24 2016 jchaloup <jchaloup@redhat.com> - 3.0.12-2
- Extend supported architectures with s390x

* Thu Oct 13 2016 jchaloup <jchaloup@redhat.com> - 3.0.12-1
- Update to v3.0.12
  related: #1382965

* Fri Sep 16 2016 jchaloup <jchaloup@redhat.com> - 3.0.9-1
- Update to v3.0.9
  related: #1374880

* Wed Sep 14 2016 jchaloup <jchaloup@redhat.com> - 3.0.8-1
- Update to v3.0.8
  resolves: #1374880

* Fri Sep 09 2016 jchaloup <jchaloup@redhat.com> - 3.0.7-1
- Update to v3.0.7
  resolves: #1370678

* Tue Aug 16 2016 jchaloup <jchaloup@redhat.com> - 3.0.4-2
- Hack test to provide ability to run unit-tests and integration tests
  Still, keeping it disabled by default as it keeps failing
  related: #1351818

* Tue Aug 02 2016 jchaloup <jchaloup@redhat.com> - 3.0.4-1
- Update to 3.0.4
  related: #1351818

* Thu Jul 28 2016 jchaloup <jchaloup@redhat.com> - 3.0.2-1
- Update to 3.0.2
  resolves: #1351818

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.2.beta0
- https://fedoraproject.org/wiki/Changes/golang1.7

* Sun May 15 2016 jchaloup <jchaloup@redhat.com> - 3.0.0-0.1.beta0
- Update to v3.0.0-beta0 (build from bundled until new deps appear in dist-git)
  resolves: #1333988

* Sat Apr 30 2016 jchaloup <jchaloup@redhat.com> - 2.3.3-1
- Update to v2.3.3
  resolves: #1331896

* Fri Apr 22 2016 jchaloup <jchaloup@redhat.com> - 2.3.2-1
- Update to v2.3.2
  resolves: #1329438

* Sat Apr  9 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.1-3
- Enable aarch64

* Wed Apr 06 2016 jchaloup <jchaloup@redhat.com> - 2.3.1-2
- Don't apply patch (for tests only which are disabled atm)

* Mon Apr 04 2016 jchaloup <jchaloup@redhat.com> - 2.3.1-1
- Update to v.2.3.1
  resolves: #1323375

* Sun Mar 20 2016 jchaloup <jchaloup@redhat.com> - 2.3.0-1
- Update to v2.3.0
  resolves: #1314441

* Wed Mar 09 2016 jchaloup <jchaloup@redhat.com> - 2.2.5-4
- Only ppc64le is supported, ppc64 not
  related: #1315419

* Tue Mar 08 2016 jchaloup <jchaloup@redhat.com> - 2.2.5-3
- Extend archs to all supported
  resolves: #1315419

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- https://fedoraproject.org/wiki/Changes/golang1.6

* Thu Feb 18 2016 jchaloup <jchaloup@redhat.com> - 2.2.5-1
- Update to v2.2.5

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 jchaloup <jchaloup@redhat.com> - 2.2.4-1
- Update to v2.2.4
  resolves: #1300558

* Fri Jan 08 2016 jchaloup <jchaloup@redhat.com> - 2.2.3-1
- Update to v2.2.3
  resolves: #1296809

* Tue Dec 29 2015 jchaloup <jchaloup@redhat.com> - 2.2.2-2
- add missing options to etcd help (thanks to Joy Pu ypu@redhat.com)
- add more information when running etcd as a service

* Mon Dec 07 2015 jchaloup <jchaloup@redhat.com> - 2.2.2-1
- Update to v2.2.2

* Mon Nov 16 2015 jchaloup <jchaloup@redhat.com> - 2.2.1-4
- Update etcd.conf: add new options, fix current

* Fri Oct 30 2015 jchaloup <jchaloup@redhat.com> - 2.2.1-3
- Add After=network-online.target and Wants=network-online.target
  to etcd.service

* Tue Oct 20 2015 jchaloup <jchaloup@redhat.com> - 2.2.1-2
- Set Type=notify instead of simple in etcd.service (upstream #1576)
  related: #1272438

* Fri Oct 16 2015 jchaloup <jchaloup@redhat.com> - 2.2.1-1
- Update to v2.2.1
  resolves: #1272438

* Fri Sep 11 2015 jchaloup <jchaloup@redhat.com> - 2.2.0-1
- Update to v2.2.0 (etcd-migrate gone)
- Update to spec-2.1
  resolves: #1253864

* Mon Aug 31 2015 jchaloup <jchaloup@redhat.com> - 2.1.2-1
- Update to v2.1.2
  resolves: #1258599

* Thu Jul 30 2015 jchaloup <jchaloup@redhat.com> - 2.1.1-2
- Enable debug info again
  related: #1214958

* Mon Jul 20 2015 jchaloup <jchaloup@redhat.com> - 2.1.1-1
- fix definition of GOPATH for go1.5
- fix definition of gobuild function for non-debug way
- Update to v2.1.1
  resolves: #1214958

* Fri Jul 10 2015 jchaloup <jchaloup@redhat.com> - 2.0.13-3
- set GOMAXPROCS to use all processors available

* Mon Jun 29 2015 jchaloup <jchaloup@redhat.com> - 2.0.13-2
- Remove -s option from -ldflags string as it removes symbol table
  'go tool l6' gives explanation of all available options
  resolves: #1236320

* Fri Jun 26 2015 jchaloup <jchaloup@redhat.com> - 2.0.13-1
- Update to v2.0.13

* Thu Jun 25 2015 jchaloup <jchaloup@redhat.com> - 2.0.12-2
- Add restart policy and set LimitNOFILE to/in etcd.service file
- Update etcd.config file: add new flags and remove depricated
- Update 'go build' flags for GIT_SHA (used in build script)
- Don't use 4001 and 7001 ports in etcd.conf, they are replaced with 2379 and 2380

* Wed Jun 24 2015 jchaloup <jchaloup@redhat.com> - 2.0.12-1
- Update to v2.0.12
- Polish spec file

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 jchaloup <jchaloup@redhat.com> - 2.0.11-2
- ETCD_ADVERTISE_CLIENT_URLS has to be set if ETCD_LISTEN_CLIENT_URLS is
  related: #1222416

* Mon May 18 2015 jchaloup <jchaloup@redhat.com> - 2.0.11-1
- Update to v2.0.11
  resolves: #1222416

* Thu Apr 23 2015 jchaloup <jchaloup@redhat.com> - 2.0.10-1
- Update to v2.0.10
  resolves: #1214705

* Wed Apr 08 2015 jchaloup <jchaloup@redhat.com> - 2.0.9-1
- Update to v2.0.9
  resolves: #1209666

* Fri Apr 03 2015 jchaloup <jchaloup@redhat.com> - 2.0.8-0.2
- Update spec file to fit for rhel too (thanks to eparis)
  related: #1207881

* Wed Apr 01 2015 jchaloup <jchaloup@redhat.com> - 2.0.8-0.1
- Update to v2.0.8
  resolves: #1207881

* Tue Mar 31 2015 jchaloup <jchaloup@redhat.com> - 2.0.7-0.1
- Update to v2.0.7
  Add Godeps.json to doc
  related: #1191441

* Thu Mar 12 2015 jchaloup <jchaloup@redhat.com> - 2.0.5-0.1
- Bump to 9481945228b97c5d019596b921d8b03833964d9e (v2.0.5)

* Tue Mar 10 2015 Eric Paris <eparis@redhat.com> - 2.0.3-0.2
- Fix .service files to work if no config file

* Fri Feb 20 2015 jchaloup <jchaloup@redhat.com> - 2.0.3-0.1
- Bump to upstream 4d728cc8c488a545a8bdeafd054d9ccc2bfb6876

* Wed Feb 18 2015 jchaloup <jchaloup@redhat.com> - 2.0.1-0.2
- Update configuration and service file
  Fix depricated ErrWrongType after update of gogo/protobuf
  related: #1191441

* Wed Feb 11 2015 jchaloup <jchaloup@redhat.com> - 2.0.1-0.1
- Update to 2.0.1
  resolves: #1191441

* Mon Feb 09 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.5
- Add missing debug info to binaries (patch from Jan Kratochvil)
  resolves: #1184257

* Fri Jan 30 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.4
- Update to etcd-2.0.0
- use gopath as the last directory to search for source code
  related: #1176138

* Mon Jan 26 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.3.rc1
- default to /var/lib/etcd/default.etcd as 2.0 uses that default (f21 commit byt eparis)
  related: #1176138
  fix /etc/etcd/etcd.conf path

* Tue Jan 20 2015 jchaloup <jchaloup@redhat.com> - 2.0.0-0.2.rc1
- Update of BuildRequires/Requires, Provides and test
  Add BuildRequire on jonboulle/clockwork
  related: #1176138

* Tue Dec 23 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.0.0-0.1.rc1
- Resolves: rhbz#1176138 - update to v2.0.0-rc1
- do not redefine gopath
- use jonboulle/clockwork from within Godeps

* Fri Oct 17 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-7
- Add ExclusiveArch for go_arches

* Mon Oct 06 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-6
- related: #1047194
  Remove dependency on go.net

* Mon Oct 06 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-5
- Fix the .service file so it can launch!
  related: #1047194

* Mon Sep 22 2014 jchaloup <jchaloup@redhat.com> - 0.4.6-4
- resolves: #1047194
  Update to 0.4.6 from https://github.com/projectatomic/etcd-package

* Tue Aug 19 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.4.6-3
- Add devel sub-package

* Wed Aug 13 2014 Eric Paris <eparis@redhat.com> - 0.4.6-2
- Bump to 0.4.6
- run as etcd, not root

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 20 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-5
- goprotobuf library unbundled (see rhbz #1018477)
- go-log library unbundled (see rhbz #1018478)
- go-raft library unbundled (see rhbz #1018479)
- go-systemd library unbundled (see rhbz #1018480)
- kardianos library unbundled (see rhbz #1018481)

* Sun Oct 13 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-4
- go.net library unbundled (see rhbz #1018476)

* Sat Oct 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-3
- Prepare for packages unbundling
- Verbose build

* Sat Oct 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-2
- Fix typo in the etc.service file

* Sat Oct 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.1.2-1
- Ver. 0.1.2
- Integrate with systemd

* Mon Aug 26 2013 Luke Cypret <cypret@fedoraproject.org> - 0.1.1-1
- Initial creation
