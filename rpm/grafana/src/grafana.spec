%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         grafana
%global repo            grafana
# https://github.com/grafana/grafana
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          v4.4.1
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           grafana
Version:        4.4.1
Release:        2%{?dist}
Summary:        Grafana is an open source, feature rich metrics dashboard and graph editor
License:        ASL 2.0
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
#Source1:        grafana-4.4.1-app.js
#ExclusiveArch:  %{ix86} x86_64 %{arm}

BuildRequires:  devtoolset-4-golang >= 1.2.1-3
%if 0
BuildRequires:  golang(github.com/BurntSushi/toml)
BuildRequires:  golang(github.com/Unknwon/com)
BuildRequires:  golang(github.com/aws/aws-sdk-go/aws)
BuildRequires:  golang(github.com/bmizerany/assert)
BuildRequires:  golang(github.com/bradfitz/gomemcache)
BuildRequires:  golang(github.com/codegangsta/cli)
BuildRequires:  golang(github.com/davecgh/go-spew/spew)
BuildRequires:  golang(github.com/fatih/color)
BuildRequires:  golang(github.com/franela/goreq)
BuildRequires:  golang(github.com/go-ini/ini)
BuildRequires:  golang(github.com/go-ldap/ldap)
BuildRequires:  golang(github.com/Unknwon/macaron)
BuildRequires:  golang(github.com/macaron-contrib/binding)
BuildRequires:  golang(github.com/macaron-contrib/session)
BuildRequires:  golang(github.com/macaron-contrib/session/mysql)
BuildRequires:  golang(github.com/macaron-contrib/session/postgres)
BuildRequires:  golang(github.com/macaron-contrib/session/redis)
BuildRequires:  golang(github.com/go-sql-driver/mysql)
BuildRequires:  golang(github.com/go-xorm/core)
BuildRequires:  golang(github.com/go-xorm/xorm)
BuildRequires:  golang(github.com/gorilla/websocket)
BuildRequires:  golang(github.com/gosimple/slug)
BuildRequires:  golang(github.com/hashicorp/go-version)
BuildRequires:  golang(github.com/jmespath/go-jmespath)
BuildRequires:  golang(github.com/jtolds/gls)
BuildRequires:  golang(github.com/klauspost/compress)
BuildRequires:  golang(github.com/klauspost/cpuid)
BuildRequires:  golang(github.com/klauspost/crc32)
BuildRequires:  golang(github.com/kr/pretty)
BuildRequires:  golang(github.com/kr/text)
BuildRequires:  golang(github.com/lib/pq)
BuildRequires:  golang(github.com/lib/pq/oid)
BuildRequires:  golang(github.com/mattn/go-colorable)
BuildRequires:  golang(github.com/mattn/go-isatty)
BuildRequires:  golang(github.com/mattn/go-sqlite3)
BuildRequires:  golang(github.com/rainycape/unidecode)
BuildRequires:  golang(github.com/smartystreets/goconvey/convey)
BuildRequires:  golang(github.com/streadway/amqp)
BuildRequires:  golang(golang.org/x/net/context)
BuildRequires:  golang(golang.org/x/oauth2)
BuildRequires:  golang(gopkg.in/bufio.v1)
BuildRequires:  golang(gopkg.in/redis.v2)
%endif

# requires nodejs-less <= 1.7.5 for build
#BuildRequires:  nodejs-less
BuildRequires: systemd

# more node deps:
#BuildRequires: nodejs-grunt-cli
#BuildRequires: nodejs-grunt-angular-templates
#BuildRequires: nodejs-grunt-contrib-requirejs
#BuildRequires: nodejs-typescript
#BuildRequires: nodejs-grunt-contrib-cssmin
#BuildRequires: nodejs-grunt-contrib-clean
#BuildRequires: nodejs-grunt-contrib-concat



Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires:       golang >= 1.2.1-3
Requires:       phantomjs

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -n %{repo}-%{version}
#rm -rf Godeps
#rm -f package.json

#sed -i "s/'jshint/#'jshint/" tasks/build_task.js
#sed -i "s/'jscs/#'jscs/" tasks/build_task.js
#sed -i "s/'tslint/#'tslint/" tasks/build_task.js
#sed -i "s/'karma:/#'karma/" tasks/build_task.js
#sed -i "s/'phantom:/#'phantom/" tasks/build_task.js
#sed -i "s/'usemin:/#'usemin/" tasks/build_task.js

%build
#mkdir -p ./_build/src/github.com/grafana
#ln -s $(pwd) ./_build/src/github.com/grafana/grafana
#export GOPATH=$(pwd)/_build:%{gopath}
#go build -o ./bin/grafana-server main.go
#go build -o ./bin/build build.go

# required for grafana-3.0.0
# go run build.go build

#grunt --base=/usr/lib/node_modules
#grunt build

export GOPATH=$(pwd)
#go get -d github.com/grafana/grafana
mkdir -p src/github.com/grafana
git clone https://github.com/grafana/grafana src/github.com/grafana/grafana
cd  src/github.com/grafana/grafana
git checkout v%{version}
#git pull
go run build.go setup
go run build.go build

%if 0
# Generate CSS
lessc --include-path=./public/vendor/bootstrap/less:./public/less ./public/less/bootstrap.dark.less ./public/css/bootstrap.dark.min.css
lessc --include-path=./public/vendor/bootstrap/less:./public/less ./public/less/bootstrap.light.less ./public/css/bootstrap.light.min.css
lessc --include-path=./public/vendor/bootstrap/less:./public/less ./public/less/grafana-responsive.less ./public/css/bootstrap-responsive.min.css
cat public/vendor/css/normalize.min.css public/vendor/css/timepicker.css public/vendor/css/spectrum.css public/css/bootstrap.dark.min.css public/css/bootstrap-responsive.min.css public/vendor/css/font-awesome.min.css >> public/css/grafana.dark.min.css
cat public/vendor/css/normalize.min.css public/vendor/css/timepicker.css public/vendor/css/spectrum.css public/css/bootstrap.light.min.css public/css/bootstrap-responsive.min.css public/vendor/css/font-awesome.min.css >> public/css/grafana.light.min.css
#

#
#cat public/vendor/requirejs/require.js public/app/require_config.js > public/app/app.js

# compile typescript
find . -name *.ts -exec tsc -m amd -t ES5 --outDir public_gen/ --sourceMap -d --sourceRoot 'public/' --rootDir 'public/' --experimentalDecorators '{}' \;
## copy compiled files back

pushd public
cp -r ../public_gen/app .
cp -r ../public_gen/test .
popd
# place app.js
cp %{SOURCE1} public/app/app.js
%endif 
%install

%define src_prefix src/github.com/grafana/grafana
# install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/
# cp -rpav pkg public conf tests %{buildroot}/%{gopath}/src/%{import_path}/
install -d -p %{buildroot}%{_datadir}/%{name}
cp -pav %{src_prefix}/*.md %{buildroot}%{_datadir}/%{name}
# cp -rpav benchmarks %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav %{src_prefix}/docs %{buildroot}%{_datadir}/%{name}
cp -rpav %{src_prefix}/public %{buildroot}%{_datadir}/%{name}
cp -rpav %{src_prefix}/vendor %{buildroot}%{_datadir}/%{name}
install -d -p %{buildroot}%{_sbindir}
cp bin/%{name}-server %{buildroot}%{_sbindir}/
install -d -p %{buildroot}%{_sysconfdir}/%{name}
cp  %{src_prefix}/conf/sample.ini %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
cp -rpav %{src_prefix}/conf %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{src_prefix}/packaging/rpm/systemd/grafana-server.service %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{src_prefix}/packaging/rpm/sysconfig/grafana-server %{buildroot}%{_sysconfdir}/sysconfig
install -d -p %{buildroot}%{_sharedstatedir}/%{name}
install -d -p %{buildroot}/var/log/%{name}
#rm -f %{buildroot}%{_datadir}/%{name}/vendor/phantomjs/phantomjs
#ln -s /usr/bin/phantomjs %{buildroot}%{_datadir}/%{name}/vendor/phantomjs/phantomjs

%check
%if 0
mkdir -p ./_build/src/github.com/grafana
ln -s $(pwd) ./_build/src/github.com/grafana/grafana
export GOPATH=$(pwd)/_build:%{gopath}
go test ./pkg/api
go test ./pkg/bus
go test ./pkg/components/apikeygen
go test ./pkg/components/renderer
go test ./pkg/events
go test ./pkg/models
go test ./pkg/plugins
go test ./pkg/services/sqlstore
go test ./pkg/services/sqlstore/migrations
go test ./pkg/setting
go test ./pkg/util

%{!?_licensedir:%global license %doc}
%endif

%files
%defattr(-, grafana, grafana, -)
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/*.md
%exclude %{_datadir}/%{name}/docs
%doc %{_datadir}/%{name}/CHANGELOG.md
#%doc %{_datadir}/%{name}/CONTRIBUTING.md
%license %{_datadir}/%{name}/LICENSE.md
%doc %{_datadir}/%{name}/NOTICE.md
%doc %{_datadir}/%{name}/README.md
%doc %{_datadir}/%{name}/docs
%attr(0755, root, root) %{_sbindir}/%{name}-server
%{_sysconfdir}/%{name}/grafana.ini
%attr(-, root, root) %{_unitdir}/grafana-server.service
%attr(-, root, root) %{_sysconfdir}/sysconfig/grafana-server
%dir %{_sharedstatedir}/%{name}
%dir /var/log/%{name}

%pre
getent group grafana >/dev/null || groupadd -r grafana
getent passwd grafana >/dev/null || \
    useradd -r -g grafana -d /etc/grafana -s /sbin/nologin \
    -c "Grafana Dashboard" grafana
exit 0

%post
%systemd_post grafana.service

%preun
%systemd_preun grafana.service

%postun
%systemd_postun grafana.service

%changelog
* Wed Jul 12 2017 Huang Jinhua <sjtuhjh@hotmail.com> - 4.4.1
- Initial packages for Open-Estuary ARM64 platform

* Fri Jul 31 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-3
- Unbundled phantomjs from grafana

* Tue Jul 28 2015 Lon Hohberger <lon@redhat.com> - 2.0.2-2
- Change ownership for grafana-server to root

* Tue Apr 14 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-1
- First package for Fedora
