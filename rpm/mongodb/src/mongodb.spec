%global _hardened_build 1
# for better compatibility with SCL spec file
%global pkg_name mongodb
# mongod daemon
%global daemon mongod
# mongos daemon
%global daemonshard mongos
# Arches officially supported by MongoDB upstream
%global upstream_arches x86_64 ppc64le aarch64 s390x

# Regression tests may take a long time (many cores recommended), skip them by
# passing --nocheck to rpmbuild or by setting runselftest to 0 if defining
# --nocheck is not possible (e.g. in koji build)
%{!?runselftest:%global runselftest 1}

# Do we want to package tests
%bcond_without tests
# Do we want to package unit_tests
%bcond_with unit_tests

# MozJS version
%global mozjsVersion 45

Name:           mongodb
Version:        3.4.3
Release:        1%{?dist}
Summary:        High-performance, schema-free document-oriented database
Group:          Applications/Databases
License:        AGPLv3 and zlib and ASL 2.0
# util/md5 is under the zlib license
# manpages and bson are under ASL 2.0
# everything else is AGPLv3
URL:            http://www.mongodb.org

Source0:        http://fastdl.mongodb.org/src/mongodb-src-r%{version}.tar.gz
Source1:        %{pkg_name}-tmpfile
Source2:        %{pkg_name}.logrotate
Source3:        %{daemon}.conf
Source4:        %{daemon}.init
Source5:        %{daemon}.service
Source6:        %{daemon}.sysconf
Source7:        %{daemonshard}.conf
Source8:        %{daemonshard}.init
Source9:        %{daemonshard}.service
Source10:       %{daemonshard}.sysconf
Source11:       README

# Fix build system to allow building with system version of libraries (mozjs, icu and asio)
# - needed for building additional architectures
# https://jira.mongodb.org/browse/SERVER-21353
Patch0:         system-libs.patch
# Required for building with system icu (and that is required by
# system mozjs45 on some architectures).
# https://jira.mongodb.org/browse/SERVER-21353
#Patch1:         system-icu.patch

# Update bundled https://github.com/chriskohlhoff/asio/ to latest master (to support openssl 1.1.0)
# revision: 14db6371b338339383aacaed29b0fa352259645a
# ASIO_STANDALONE and ASIO_SEPARATE_COMPILATION needs to be defined for proper build
# Upstream would like to update bundled version but assio upstream does not release new versions
# https://github.com/chriskohlhoff/asio/issues/84#issuecomment-271927267
Patch2:         asio-master.patch
# Fix using timer from updated asio (changed in new asio version)
Patch3:         asio-new.patch
# Add support for openssl >= 1.1.0
# https://jira.mongodb.org/browse/SERVER-26781 - fixed in 3.5.3
Patch4:         openssl-1.1.0.patch

# Fix for boost 1.62+ (thanks to Gentoo)
# https://jira.mongodb.org/browse/SERVER-26756
Patch5:		mongodb-3.4.2-boost-1.63-fix.patch

# Fedora specific - adding support for rest of Fedora architectures
# Upstream does not support it at this time
#
# https://jira.mongodb.org/browse/SERVER-27833
# Enable ppc64 big endian support
Patch20:         ppc64.patch
# Add support also for 32bit platforms
Patch21:         32bit-support.patch

#Use devtoolset gcc5 to build mongodb
Patch22:         centos_gcc5_sconstruct.patch

BuildRequires:  devtoolset-4-gcc >= 5.3
BuildRequires:  devtoolset-4-boost-devel >= 1.56
BuildRequires:  gperftools-libs
#BuildRequires:  tcmalloc
BuildRequires:  gperftools-devel
BuildRequires:  libpcap-devel
BuildRequires:  libstemmer-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  scons
BuildRequires:  snappy-devel
BuildRequires:  devtoolset-4-yaml-cpp-devel
BuildRequires:  zlib-devel
BuildRequires:  asio-devel
%ifnarch %{upstream_arches}
BuildRequires:  mozjs%{mozjsVersion}-devel
%endif
BuildRequires:  valgrind-devel
BuildRequires:  libicu-devel
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
BuildRequires:  systemd
%endif
# Required by test suite
%if %runselftest
BuildRequires:  python-pymongo
BuildRequires:  PyYAML
%endif
Requires:       devtoolset-4-runtime
Requires:       devtoolset-4-boost-devel

# Mongodb must run on a 64-bit CPU (see bug #630898)
ExcludeArch:    ppc %{sparc} s390

%description
Mongo (from "humongous") is a high-performance, open source, schema-free
document-oriented database. MongoDB is written in C++ and offers the following
features:
    * Collection oriented storage: easy storage of object/JSON-style data
    * Dynamic queries
    * Full index support, including on inner objects and embedded arrays
    * Query profiling
    * Replication and fail-over support
    * Efficient storage of binary data including large objects (e.g. photos
    and videos)
    * Auto-sharding for cloud-level scalability (currently in early alpha)
    * Commercial Support Available

A key goal of MongoDB is to bridge the gap between key/value stores (which are
fast and highly scalable) and traditional RDBMS systems (which are deep in
functionality).


%package server
Summary:        MongoDB server, sharding server and support scripts
Group:          Applications/Databases
Requires:       devtoolset-4-boost-devel
Requires:       devtoolset-4-runtime
Requires(pre):  shadow-utils
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): initscripts
%endif

Provides: bundled(wiredtiger) = 2.6.1
# MongoDB bundles development release of asio 1.11
# This is not in Fedora yet (only asio-1.10)
Provides: bundled(asio) = 1.11.0
%ifarch %{upstream_arches}
Provides: bundled(mozjs45) = 45.5.0
%endif

%description server
This package provides the mongo server software, mongo sharding server
software, default configuration files, and init scripts.


%if %{with tests}
%package test
Summary:          MongoDB test suite
Group:            Applications/Databases
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         python-pymongo
Requires:         PyYAML

%description test
This package contains the regression test suite distributed with
the MongoDB sources.
%endif

%prep
%setup -q -n mongodb-src-r%{version}
%patch0 -p1
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# Boost 1.62+ is in F26
%if 0%{?fedora} >= 26 || 0%{?rhel} >= 7
%patch5 -p1
%endif
# Patch only Fedora specific architectures
%ifnarch %{upstream_arches}
%patch20 -p1
%patch21 -p1
%endif
%patch22 -p1

# CRLF -> LF
sed -i 's/\r//' README

# disable propagation of $TERM env var into the Scons build system
sed -i -r "s|(for key in \('HOME'), 'TERM'(\):)|\1\2|" SConstruct

# Use system versions of header files (bundled does not differ)
sed -i -r "s|third_party/libstemmer_c/include/libstemmer.h|libstemmer.h|" src/mongo/db/fts/stemmer.h
sed -i -r "s|third_party/yaml-cpp-0.5.1/include/yaml-cpp/yaml.h|yaml-cpp/yaml.h|" src/mongo/util/options_parser/options_parser.cpp

# by default use system mongod, mongos and mongo binaries in resmoke.py
sed -i -r "s|os.curdir(, \"mongo\")|\"%{_bindir}\"\1|"   buildscripts/resmokelib/config.py
sed -i -r "s|os.curdir(, \"mongod\")|\"%{_bindir}\"\1|"   buildscripts/resmokelib/config.py
sed -i -r "s|os.curdir(, \"mongos\")|\"%{_bindir}\"\1|"   buildscripts/resmokelib/config.py

# set default data prefix in resmoke.py
sed -i -r "s|/data/db|%{_datadir}/%{pkg_name}-test/var|"   buildscripts/resmokelib/config.py

# Disable optimization for s2 library
# https://jira.mongodb.org/browse/SERVER-17511
sed -i -r "s|(env.Append\(CCFLAGS=\['-DDEBUG_MODE=false')(\]\))|\1,'-O0'\2|"  src/third_party/s2/SConscript

# fix one unit test which used gnu++11 code (c++11 is used)
sed -i 's|ASSERT_PARSES(double, "0xabcab.defdefP-10", 0xabcab.defdefP-10);||' src/mongo/base/parse_number_test.cpp

# set default storage engine for non 64-bit arches - RHBZ#1303846
%ifnarch %{upstream_arches} ppc64
sed -i 's|engine = "wiredTiger"|engine = "mmapv1"|' src/mongo/db/storage/storage_options.h
%endif


%build
# Prepare variables for building
cat > variables.list << EOF
CCFLAGS="%{?optflags}"
LINKFLAGS="%{?__global_ldflags} -Wl,-z,noexecstack -Wl,--reduce-memory-overheads,--no-keep-memory"
CPPDEFINES="ASIO_STANDALONE ASIO_SEPARATE_COMPILATION"
VERBOSE=1

%ifarch %{ix86}
# On i686 -ffloat-store is requred to round in GranularityRounderPreferredNumbers
# propeely, without this:
# -> build/opt/mongo/db/pipeline/granularity_rounder_test,
#    build/opt/mongo/db/pipeline/accumulator_test, build/opt/mongo/util/summation_test
#    and build/opt/mongo/db/pipeline/document_source_test unittests fail
CCFLAGS+=" -ffloat-store -std=c++11 -DBOOST_NO_CXX11_SCOPED_ENUMS"
%endif
%ifarch ppc64
# Needed for altivec instructions in mongo/db/fts/unicode/byte_vector_altivec.h
CCFLAGS+=" -mcpu=power8"
%endif
%ifarch aarch64
# Needed for CRC32 instructions in third_party/wiredtiger/src/checksum/arm64/crc32-arm64.c
CCFLAGS+=" -march=armv8-a+crc"
%endif
EOF
cat variables.list

# Define build options
cat > build-options << EOF
 %{?_smp_mflags} \
 --use-system-pcre \
 --use-system-boost \
 --use-system-snappy \
 --use-system-valgrind \
 --use-system-zlib \
 --use-system-stemmer \
 --use-system-tcmalloc \
 --use-system-yaml \
%ifarch s390x ppc64
 --mmapv1=off
%else
 --mmapv1=on \
%endif
%ifarch %{upstream_arches} ppc64
 --wiredtiger=on \
%else
 --wiredtiger=off \
%endif
%ifarch s390x
 --use-s390x-crc32=off \
%endif
%ifnarch %{upstream_arches}
 --use-system-mozjs \
 --js-engine=mozjs-%{mozjsVersion} \
%endif
 --ssl \
 --nostrip \
 --disable-warnings-as-errors \
 --variables-files=variables.list
EOF
# --use-system-asio \

# see output of "scons --help" for options
scons all $(cat build-options)


%install
scons install --prefix=%{buildroot}%{_prefix} $(cat build-options)

#TODO - create man page for mongobridge
install -p -D -m 755 build/*/mongo/tools/mongobridge %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_sharedstatedir}/%{pkg_name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{pkg_name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{pkg_name}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
install -p -D -m 644 "%{SOURCE1}"  %{buildroot}%{_tmpfilesdir}/%{pkg_name}.conf
install -p -D -m 644 "%{SOURCE5}"  %{buildroot}%{_unitdir}/%{daemon}.service
install -p -D -m 644 "%{SOURCE9}"  %{buildroot}%{_unitdir}/%{daemonshard}.service
%else
install -p -D -m 755 "%{SOURCE4}"  %{buildroot}%{_root_initddir}/%{daemon}
install -p -D -m 755 "%{SOURCE8}"  %{buildroot}%{_root_initddir}/%{daemonshard}
%endif
install -p -D -m 644 "%{SOURCE2}"  %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}
install -p -D -m 644 "%{SOURCE3}"  %{buildroot}%{_sysconfdir}/%{daemon}.conf
install -p -D -m 644 "%{SOURCE7}"  %{buildroot}%{_sysconfdir}/%{daemonshard}.conf
install -p -D -m 644 "%{SOURCE6}"  %{buildroot}%{_sysconfdir}/sysconfig/%{daemon}
install -p -D -m 644 "%{SOURCE10}" %{buildroot}%{_sysconfdir}/sysconfig/%{daemonshard}
# Enable WiredTiger for 64-bit architectures by default
%ifarch %{upstream_arches} ppc64
sed -i -r "s|(engine: )mmapv1|\1wiredTiger|" %{buildroot}%{_sysconfdir}/%{daemon}.conf
%endif

install -d -m 755                     %{buildroot}%{_mandir}/man1
install -p -m 644 debian/mongo.1      %{buildroot}%{_mandir}/man1/
install -p -m 644 debian/mongoperf.1  %{buildroot}%{_mandir}/man1/
install -p -m 644 debian/mongod.1     %{buildroot}%{_mandir}/man1/
install -p -m 644 debian/mongos.1     %{buildroot}%{_mandir}/man1/

%if %{with tests}
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/var
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts
install -p -D -m 755 buildscripts/resmoke.py   %{buildroot}%{_datadir}/%{pkg_name}-test/
install -p -D -m 444 buildscripts/__init__.py  %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/

cp -R     buildscripts/resmokeconfig     %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/
cp -R     buildscripts/resmokelib        %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/
cp -R     jstests                        %{buildroot}%{_datadir}/%{pkg_name}-test/
# Remove executable flag from JS tests
for file in `find %{buildroot}%{_datadir}/%{pkg_name}-test/jstests -type f`; do
  chmod a-x $file
done

install -p -D -m 444 "%{SOURCE11}"       %{buildroot}%{_datadir}/%{pkg_name}-test/
%endif
%if %{with unit_tests}
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/unittests
while read unittest
do
    install -p -D $unittest %{buildroot}%{_datadir}/%{pkg_name}-test/unittests/
done < ./build/unittests.txt
%endif

binlist=("mongo" "mongoperf" "mongobridge")
for bin in ${binlist[@]}
do
    mv %{buildroot}%{_bindir}/${bin} %{buildroot}%{_bindir}/${bin}_internal
    touch %{buildroot}%{_bindir}/${bin}
    echo '#!/bin/bash' > %{buildroot}%{_bindir}/${bin}
    echo 'source /opt/rh/devtoolset-4/enable' >> %{buildroot}%{_bindir}/${bin}
    echo "/usr/bin/${bin}"'_internal $@' >> %{buildroot}%{_bindir}/${bin}
    chmod 755 %{buildroot}%{_bindir}/${bin}
done

%check
%if %runselftest
# More info about testing:
# http://www.mongodb.org/about/contributors/tutorial/test-the-mongodb-server/
cd %{_builddir}/%{pkg_name}-src-r%{version}
mkdir ./var

# Run old-style heavy unit tests (dbtest binary)
#mkdir ./var/dbtest
#./dbtest --dbpath `pwd`/var/dbtest

# Fedora icu provides more/different langueges than bundled icu
sed -i "/collator_factory_icu_test/d" build/unittests.txt
#TODO
%ifarch %{ix86} %{arm}
sed -i "/service_entry_point_mock_test/d" build/unittests.txt
# Crashing on armv7hl due to optimizations
sed -i "/chunk_diff_test/d" build/unittests.txt
%endif
# Run new-style unit tests (*_test files)
source /opt/rh/devtoolset-4/enable && ./buildscripts/resmoke.py --dbpathPrefix `pwd`/var --continueOnFailure --mongo=%{buildroot}%{_bindir}/mongo_internal --mongod=%{buildroot}%{_bindir}/%{daemon} --mongos=%{buildroot}%{_bindir}/%{daemonshard} --nopreallocj --suites unittests \
%ifarch %{upstream_arches} ppc64
--storageEngine=wiredTiger
%else
--storageEngine=mmapv1
%endif

#Disable jsHeapLimit test so far 
rm -f ./jstests/core/jsHeapLimit.js

# Run JavaScript integration tests
source /opt/rh/devtoolset-4/enable && ./buildscripts/resmoke.py --dbpathPrefix `pwd`/var --continueOnFailure --mongo=%{buildroot}%{_bindir}/mongo_internal --mongod=%{buildroot}%{_bindir}/%{daemon} --mongos=%{buildroot}%{_bindir}/%{daemonshard} --nopreallocj --suites core \
%ifarch %{upstream_arches} ppc64
--storageEngine=wiredTiger
%else
--storageEngine=mmapv1
%endif

rm -Rf ./var
%endif

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%pre server
getent group  %{pkg_name} >/dev/null || groupadd -f -g 184 -r %{pkg_name}
if ! getent passwd %{pkg_name} >/dev/null ; then
    if ! getent passwd 184 >/dev/null ; then
      useradd -r -u 184 -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name} \
      -s /sbin/nologin -c "MongoDB Database Server" %{pkg_name}
    else
      useradd -r -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name} \
      -s /sbin/nologin -c "MongoDB Database Server" %{pkg_name}
    fi
fi
exit 0


%post server
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
  # https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
  # daemon-reload
  %systemd_postun
%else
  /sbin/chkconfig --add %{daemon}
  /sbin/chkconfig --add %{daemonshard}
%endif

%preun server
if [ "$1" = 0 ]; then
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
  # --no-reload disable; stop
  %systemd_preun %{daemon}.service
  %systemd_preun %{daemonshard}.service
%else
  /sbin/service %{daemon}       stop >/dev/null 2>&1
  /sbin/service %{daemonshard}  stop >/dev/null 2>&1
  /sbin/chkconfig --del %{daemon}
  /sbin/chkconfig --del %{daemonshard}
%endif
fi


%postun server
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
  # daemon-reload
  %systemd_postun
%endif
if [ "$1" -ge 1 ] ; then
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
  # try-restart
  %systemd_postun_with_restart %{daemon}.service
  %systemd_postun_with_restart %{daemonshard}.service
%else
  /sbin/service %{daemon}       condrestart >/dev/null 2>&1 || :
  /sbin/service %{daemonshard}  condrestart >/dev/null 2>&1 || :
%endif
fi


# Make rename of config files transparent and effortless
%triggerpostun server -- %{name}-server < 2.6.7-3
if [ -f %{_sysconfdir}/sysconfig/%{daemon}.rpmnew ]; then
  if [ -f %{_sysconfdir}/%{pkg_name}.conf.rpmsave ]; then
    mv %{_sysconfdir}/%{daemon}.conf            %{_sysconfdir}/%{daemon}.conf.rpmnew
    mv %{_sysconfdir}/%{pkg_name}.conf.rpmsave  %{_sysconfdir}/%{pkg_name}.conf
  else
    mv %{_sysconfdir}/%{daemon}.conf            %{_sysconfdir}/%{pkg_name}.conf
  fi
else
  if [ -f %{_sysconfdir}/%{pkg_name}.conf.rpmsave ]; then
    mv %{_sysconfdir}/%{daemon}.conf            %{_sysconfdir}/%{daemon}.conf.rpmnew
    mv %{_sysconfdir}/%{pkg_name}.conf.rpmsave  %{_sysconfdir}/%{daemon}.conf
  fi
fi

if [ -f %{_sysconfdir}/sysconfig/%{daemonshard}.rpmnew ]; then
  if [ -f %{_sysconfdir}/%{pkg_name}-shard.conf.rpmsave ]; then
    mv %{_sysconfdir}/%{daemonshard}.conf            %{_sysconfdir}/%{daemonshard}.conf.rpmnew
    mv %{_sysconfdir}/%{pkg_name}-shard.conf.rpmsave  %{_sysconfdir}/%{pkg_name}-shard.conf
  else
    mv %{_sysconfdir}/%{daemonshard}.conf            %{_sysconfdir}/%{pkg_name}-shard.conf
  fi
else
  if [ -f %{_sysconfdir}/%{pkg_name}-shard.conf.rpmsave ]; then
    mv %{_sysconfdir}/%{daemonshard}.conf            %{_sysconfdir}/%{daemonshard}.conf.rpmnew
    mv %{_sysconfdir}/%{pkg_name}-shard.conf.rpmsave  %{_sysconfdir}/%{daemonshard}.conf
  fi
fi


%files
%{!?_licensedir:%global license %%doc}
%license GNU-AGPL-3.0.txt APACHE-2.0.txt
%doc README
%{_bindir}/mongo
%{_bindir}/mongoperf
%{_bindir}/mongobridge
%{_bindir}/mongo_internal
%{_bindir}/mongoperf_internal
%{_bindir}/mongobridge_internal

%{_mandir}/man1/mongo.1*
%{_mandir}/man1/mongoperf.1*


%files server
%{_bindir}/mongod
%{_bindir}/mongos
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongos.1*
%dir %attr(0755, %{pkg_name}, root) %{_sharedstatedir}/%{pkg_name}
%dir %attr(0750, %{pkg_name}, root) %{_localstatedir}/log/%{pkg_name}
%dir %attr(0755, %{pkg_name}, root) %{_localstatedir}/run/%{pkg_name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{pkg_name}
%config(noreplace) %{_sysconfdir}/%{daemon}.conf
%config(noreplace) %{_sysconfdir}/%{daemonshard}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemon}
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemonshard}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%{_tmpfilesdir}/%{pkg_name}.conf
%{_unitdir}/*.service
%else
%{_initddir}/%{daemon}
%{_initddir}/%{daemonshard}
%endif


%if %{with tests}
%files test
%doc %{_datadir}/%{pkg_name}-test/README
%defattr(-,%{pkg_name},root)
%dir %attr(0755, %{pkg_name}, root) %{_datadir}/%{pkg_name}-test
%dir %attr(0755, %{pkg_name}, root) %{_datadir}/%{pkg_name}-test/var
%{_datadir}/%{pkg_name}-test/jstests
%{_datadir}/%{pkg_name}-test/buildscripts
%{_datadir}/%{pkg_name}-test/resmoke.*
%if %{with unit_tests}
%{_datadir}/%{pkg_name}-test/unittests
%endif
%endif


%changelog
* Wed Mar 29 2017 Huang Jinhua <sjtuhjh@hotmail.com> - 3.4.3-1
- Estuary initial package for ARM64 

* Wed Mar 29 2017 Marek Skalický <mskalick@redhat.com> - 3.4.3-1
- Update to latest versions 3.4.3

* Mon Mar 13 2017 Marek Skalický <mskalick@redhat.com> - 3.4.2-4
- Update patches and separate Fedora specific
- Enable tcmalloc for s390x

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 3.4.2-3
- Re-enable tests on ppc64le

* Wed Feb  8 2017 Tom Callaway <spot@fedoraproject.org> - 3.4.2-2
- temporarily disable test running for ppc64le

* Wed Feb  8 2017 Tom Callaway <spot@fedoraproject.org> - 3.4.2-1
- update to 3.4.2

* Thu Jan 12 2017 Marek Skalický <mskalick@redhat.com> - 3.4.1-3
- Disable CRC32 instructions for s390x
- Fix assio patch to have changes from MongoDB upstream

* Fri Jan 06 2017 Marek Skalický <mskalick@redhat.com> - 3.4.1-2
- Enable WiredTiger for aarch64, ppc64le and s390x and make it default
- Enable building for x390x and ppc64

* Wed Dec 21 2016 Marek Skalický <mskalick@redhat.com> - 3.4.1-1
- Update to latest minor release

* Fri Dec 16 2016 Marek Skalický <mskalick@redhat.com> - 3.4.0-2
- Fix setting default storage engine for non-64b architectures

* Thu Dec 01 2016 Marek Skalický <mskalick@redhat.com> - 3.4.0-1
- Update to MongoDB 3.4.0
- Updated bundled asio to latest master revision to support openssl 1.1.0
- Temporarily use bundled version of mozjs45 for 64 platforms
- Install unittests to own directory

* Thu Oct 06 2016 Marek Skalický <mskalick@redhat.com> - 3.2.10-1
- Upgrade to latest minor version

* Mon Sep 19 2016 Marek Skalický <mskalick@redhat.com> - 3.2.8-3
- Security fix for CVE-2016-6494
  (fix world-readable .dbshell history file)

* Tue Aug 23 2016 Richard Shaw <hobbes1069@gmail.com> - 3.2.8-2
- Rebuild for updated yaml-cpp

* Thu Aug 04 2016 Marek Skalický <mskalick@redhat.com> - 3.2.8-1
- Upgrade to MongoDB 3.2.8

* Tue Jun 14 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.7-1
- Upgrade to MongoDB 3.2.7

* Fri May 20 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.6-4
- Fixed server %pre to comply guidelines
- Using reserved GID for newly added group

* Mon May 16 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.6-3
- Disabled executable stack (since MongoDB 3.2.5)
- Added mongobridge tool (used in test suites)

* Thu May 12 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.6-2
- Enable to build mmapv1 storage engine

* Fri May 6 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.6-1
- Upgrade to MongoDB 3.2.6

* Mon Apr 11 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.4-2
- Fixed permissions in test subpackage

* Wed Apr 6 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.4-1
- Upgrade to MongoDB 3.2.4

* Thu Mar 31 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.3-2
- Make mmapv1 default storage engine for non x86_64 archs

* Wed Mar 9 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.3-1
- Upgrade to MongoDB 3.2.3
- Added ability to have also C++ unit tests in test subpackage

* Tue Jan 26 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.1-4
- Specify, that mmapv1 is default for 32-bit systems

* Tue Jan 26 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.1-3
- Rebuild for boost 1.60

* Tue Jan 19 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.1-2
- Fixed permissions of test files

* Thu Jan 14 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.1-1
- Upgrade to versions 3.2.1

* Tue Jan 12 2016 Marek Skalicky <mskalick@redhat.com> - 3.2.0-2
- Configuration files updated
  (mongod and mongos also listen on ipv6 localhost by default)
- test subpackage contains resmoke.py tool instead of smoke.py

* Wed Dec 9 2015 Marek Skalicky <mskalick@redhat.com> - 3.2.0-1
- Upgrade to latest stable version 3.2.0

* Thu Dec 3 2015 Marek Skalicky <mskalick@redhat.com> - 3.2.0-0.rc6
- Upgrade to version 3.2.0-rc6

* Fri Nov 27 2015 Marek Skalicky <mskalick@redhat.com> - 3.2.0-0.rc4
- Upgrade to version 3.2.0-rc4

* Thu Oct 15 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.7-2
- Fixed using system version of header files (#1269391#c0)

* Thu Oct 15 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.7-1
- Upgrade to version 3.0.7

* Mon Oct 12 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.6-3
- Added patch to support boost 1.59

* Thu Oct 8 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.6-2
- Enable bundled WiredTiger
  (FPC ticket - https://fedorahosted.org/fpc/ticket/562,
   upstream discussion - https://groups.google.com/forum/#!topic/mongodb-dev/31FQSo4KVCI)

* Thu Sep 24 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.6-1
- Fixed systemd service PIDFile setting (#1231269)
- Temporarily disable WiredTiger (FPC request to bundle it)
- Enable c++11 (MongoDB requires it since 3.0.5)
- Upgrade to version 3.0.6

* Tue Sep 08 2015 Severin Gehwolf <sgehwolf@redhat.com> - 3.0.4-6
- Allow for tests to be enabled conditionally during build.

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 3.0.4-5
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 3.0.4-3
- rebuild for Boost 1.58

* Thu Jul 9 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.4-2
- Temporarily disable dbtest - see mongodb#SERVER-19309
- Add patch to support latest WiredTiger release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 17 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.4-1
- Upgrade to version 3.0.4

* Fri Jun 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.3-2
- All architectures have python-pymongo
- BuildReq cleanups

* Wed Jun 10 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.3-1
- Fixed dbtest argument passing
- Upgrade to version 3.0.3

* Tue May 19 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.2-3
- Change log settigs (logappend=true)
- Run dbtest suite in check section
- Use variables instead of changing SConstruct

* Sun May 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Apr 14 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.2-1
- Upgrade to version 3.0.2

* Wed Mar 4 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.0-1
- Upgrade to version 3.0.0

* Thu Feb 19 2015 Marek Skalicky <mskalick@redhat.com> - 2.6.7-5
- Enabled hardened build
- Fixed init scripts to respect LSB (#1075736)

* Mon Feb 16 2015 Marek Skalicky <mskalick@redhat.com> - 2.6.7-4
- Revert bind_ip change in configuration files from version 2.6.6-4

* Wed Feb 4 2015 Marek Skalicky <mskalick@redhat.com> - 2.6.7-3
- mongod.init won't exit before preallocating is done
- Disabled -Werror (dont't build with gcc 5.0)
- Changed permissions of mognodb-test/var directory to 755
- Changed names of configuration and log files

* Wed Jan 28 2015 Petr Machata <pmachata@redhat.com> - 2.6.7-2
- Rebuild for boost 1.57.0
- include <algorithm> in src/mongo/shell/linenoise_utf8.h
  (mongodb-2.6.7-swap.patch)

* Fri Jan 16 2015 Marek Skalicky <mskalick@redhat.com> 2.6.7-1
- Upgrade to 2.6.7
- Fix typo errors in mongodb-test README

* Thu Jan 15 2015 Marek Skalicky <mskalick@redhat.com> 2.6.6-4
- Changed unix socket location to /var/run/mongodb/ (#1047858)
- Revised default config files to correspond with --help options

* Wed Jan 7 2015 Marek Skalicky <mskalick@redhat.com> 2.6.6-3
- Added systemd TimeoutStartSec (#1040573)
- Reviewed patches and dependencies
- Added gcc requires to support built-in atomic operations
- Fix use of libstemmer and yaml-cpp system libraries

* Wed Dec 10 2014 Marek Skalicky <mskalick@redhat.com> 2.6.6-2
- Added check section and test subpackage

* Wed Dec 10 2014 Marek Skalicky <mskalick@redhat.com> 2.6.6-1
- Upgrade to version 2.6.6

* Thu Oct 9 2014 Marek Skalicky <mskalick@redhat.com> 2.6.5-2
- Corrected/Finished renaming services and pid files
- Changed default mongos ports

* Thu Oct 9 2014 Marek Skalicky <mskalick@redhat.com> 2.6.5-1
- Updated to version 2.6.5
- Renamed sysmted service files (to reflect mainstream names)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul  9 2014 Jan Pacner <jpacner@redhat.com> - 2.6.3-1
- Resolves: #1103163 new major release with major differences
- add sharding server daemon init/unit files (and rename existing)
- use ld library path from env
- spec cleanup/clarification
- Resolves: #1047858 (RFE: Turn on PrivateTmp and relocate unix socket file)
- Related: #963824 (bloated binaries; splitting according to latest upstream)

* Sat Jun  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.9-7
- aarch64 now has gperftools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 2.4.9-5
- Rebuild for boost 1.55.0

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 2.4.9-4
- rebuild for boost 1.55.0


* Fri Feb 14 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.4.9-3
- rebuild for icu-53 (via v8)

* Tue Feb 04 2014 Matthias Saou <matthias@saou.eu> 2.4.9-2
- Merge el6 branch changes (we shouldn't start diverging now).
- Re-introduce conditionals, but to still support EL6.
- Include run directory only for EL6.
- Don't own the /usr/include directory.
- Make libmongodb requirement arch specific (#1010535).
- Fix multiple_occurrences error from duplicate --quiet options (#1022476).
- Fix broken v8 version specific requirement (#1027157).

* Sun Jan 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.9-1
- Update to 2.4.9
- Drop old < F-15 conditionals
- Cleanup Spec
- Run ldconfig for the lib package, not binary package
- Don't make some directories world readable (RHBZ 857926)

* Mon Jan 06 2014 Jan Pacner <jpacner@redhat.com> - 2.4.6-3
- Resolves: #1027157 (mongo shell sefgaults when using arbitrary v8 version)

* Thu Nov 28 2013 Jan Pacner <jpacner@redhat.com> - 2.4.8-1
- new release
- Resolves: #1010712 (LimitNOFILE)
- make sysconf options being respected

* Wed Aug 21 2013 Troy Dawson <tdawson@redhat.com> - 2.4.6-1
- Updated to 2.4.6
- Added Requires: v8  (#971595)

* Sun Jul 28 2013 Petr Machata <pmachata@redhat.com> - 2.4.5-6
- Rebuild for boost 1.54.0

* Sat Jul 27 2013 pmachata@redhat.com - 2.4.5-5
- Rebuild for boost 1.54.0

* Fri Jul 12 2013 Troy Dawson <tdawson@redhat.com> - 2.4.5-4
- Added Provides: mongodb-devel to libmongodb-devel

* Fri Jul 12 2013 Troy Dawson <tdawson@redhat.com> - 2.4.5-3
- Removed hardening section.  Currently doesn't work with 2.4.x
  Wasn't really being applied when we thought it was.
- Cleaned up RHEL5 spec leftovers

* Thu Jul 11 2013 David Marlin <dmarlin@redhat.com> - 2.4.5-2
- Updated arm patches to work with 2.4.x

* Mon Jul 08 2013 Troy Dawson <tdawson@redhat.com> - 2.4.5-1
- Update to version 2.4.5 to fix CVE-2013-4650
- Patch3 fixed upstream - https://jira.mongodb.org/browse/SERVER-5575
- Patch4 fixed upstream - https://jira.mongodb.org/browse/SERVER-6514
- Put lib dir in correct place
- no longer have to remove duplicate headers

* Sun Jul 07 2013 Johan Hedin <johan.o.hedin@gmail.com> - 2.4.4-4
- Added patch to make mongodb compile with gcc 4.8

* Wed Jul 03 2013 Johan Hedin <johan.o.hedin@gmail.com> - 2.4.4-3
- Added missing daemon name to the preun script for the server
- Fixed init script so that it does not kill the server on shutdown
- Renamed mongodb-devel to libmongdb-devel
- Dependency cleanup between the sub packages
- Moved Requires for the server to the server sub package
- Using %%{_unitdir} macro for where to put systemd unit files
- Fixed rpmlint warnings regarding %% in comments and mixed tabs/spaces
- Run systemd-tmpfiles --create mongodb.conf in post server

* Mon Jul 01 2013 Troy Dawson <tdawson@redhat.com> - 2.4.4-2
- Turn on hardened build (#958014)
- Apply patch to accept env flags

* Sun Jun 30 2013 Johan Hedin <johan.o.hedin@gmail.com> - 2.4.4-1
- Bumped version up to 2.4.4
- Rebased the old 2.2 patches that are still needed to 2.4.4
- Added some new patches to build 2.4.4 properly

* Sat May 04 2013 David Marlin <dmarlin@redhat.com> - 2.2.4-2
- Updated patch to work on both ARMv5 and ARMv7 (#921226)

* Thu May 02 2013 Troy Dawson <tdawson@redhat.com> - 2.2.4-1
- Bumped version up to 2.2.4
- Refreshed all patches to 2.2.4

* Fri Apr 26 2013 David Marlin <dmarlin@redhat.com> - 2.2.3-5
- Patch to build on ARM (#921226)

* Wed Mar 27 2013 Troy Dawson <tdawson@redhat.com> - 2.2.3-4
- Fix for CVE-2013-1892

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 2.2.3-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 2.2.3-2
- Rebuild for Boost-1.53.0

* Tue Feb 05 2013 Troy Dawson <tdawson@redhat.com> - 2.2.3-1
- Update to version 2.2.3

* Mon Jan 07 2013 Troy Dawson <tdawson@redhat.com> - 2.2.2-2
- remove duplicate headers (#886064)

* Wed Dec 05 2012 Troy Dawson <tdawson@redhat.com> - 2.2.2-1
- Updated to version 2.2.2

* Tue Nov 27 2012 Troy Dawson <tdawson@redhat.com> - 2.2.1-3
- Add ssl build option
- Using the reserved mongod UID for the useradd
- mongod man page in server package (#880351)
- added optional MONGODB_OPTIONS to init script

* Wed Oct 31 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.2.1-2
- Make sure build and install flags are the same
- Actually remove the js patch file

* Wed Oct 31 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.2.1-1
- Remove fork fix patch (fixed upstream)
- Remove pcre patch (fixed upstream)
- Remove mozjs patch (now using v8 upstream)
- Update to 2.2.1

* Tue Oct 02 2012 Troy Dawson <tdawson@redhat.com> - 2.2.0-6
- full flag patch to get 32 bit builds to work

* Tue Oct 02 2012 Troy Dawson <tdawson@redhat.com> - 2.2.0-5
- shared libraries patch
- Fix up minor %%files issues

* Fri Sep 28 2012 Troy Dawson <tdawson@redhat.com> - 2.2.0-4
- Fix spec files problems

* Fri Sep 28 2012 Troy Dawson <tdawson@redhat.com> - 2.2.0-3
- Updated patch to use system libraries
- Update init script to use a pidfile

* Thu Sep 27 2012 Troy Dawson <tdawson@redhat.com> - 2.2.0-2
- Added patch to use system libraries

* Wed Sep 19 2012 Troy Dawson <tdawson@redhat.com> - 2.2.0-1
- Updated to 2.2.0
- Updated patches that were still needed
- use v8 instead of spider_monkey due to bundled library issues

* Tue Aug 21 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.7-1
- Update to 2.0.7
- Don't patch for boost-filesystem version 3 on EL6

* Mon Aug 13 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.6-3
- Remove EL5 support
- Add patch to use boost-filesystem version 3

* Wed Aug 01 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.6-2
- Don't apply fix-xtime patch on EL5

* Wed Aug 01 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.6-1
- Update to 2.0.6
- Update no-term patch
- Add fix-xtime patch for new boost

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.4-1
- Update to 2.0.4
- Remove oldpython patch (fixed upstream)
- Remove snappy patch (fixed upstream)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-10
- Rebuilt for c++ ABI breakage

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0.2-9
- Rebuild against PCRE 8.30

* Fri Feb 03 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-8
- Disable HTTP interface by default (#752331)

* Fri Feb 03 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-7
- Enable journaling by default (#656112)
- Remove BuildRequires on unittest (#755081)

* Fri Feb 03 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-6
- Clean up mongodb-src-r2.0.2-js.patch and fix #787246

* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-5
- Enable build using external snappy

* Tue Jan 17 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-4
- Patch buildsystem for building on older pythons (RHEL5)

* Mon Jan 16 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-3
- Merge the 2.0.2 spec file with EPEL
- Merge mongodb-sm-pkgconfig.patch into mongodb-src-r2.0.2-js.patch

* Mon Jan 16 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-2
- Add pkg-config enablement patch

* Sat Jan 14 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 2.0.2-1
- Update to 2.0.2
- Add new files (mongotop and bsondump manpage)
- Update mongodb-src-r1.8.2-js.patch => mongodb-src-r2.0.2-js.patch
- Update mongodb-fix-fork.patch
- Fix pcre linking

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Chris Lalancette <clalancette@gmail.com> - 1.8.2-10
- Rebuild for rawhide boost update

* Thu Sep 22 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-9
- Copy the right source file into place for tmpfiles.d

* Tue Sep 20 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-8
- Add a tmpfiles.d file to create the /var/run/mongodb subdirectory

* Mon Sep 12 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-7
- Add a patch to fix the forking to play nice with systemd
- Make the /var/run/mongodb directory owned by mongodb

* Thu Jul 28 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-6
- BZ 725601 - fix the javascript engine to not hang (thanks to Eduardo Habkost)

* Mon Jul 25 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-5
- Fixes to post server, preun server, and postun server to use systemd

* Thu Jul 21 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-4
- Update to use systemd init

* Thu Jul 21 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-3
- Rebuild for boost ABI break

* Wed Jul 13 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-2
- Make mongodb-devel require boost-devel (BZ 703184)

* Fri Jul 01 2011 Chris Lalancette <clalance@redhat.com> - 1.8.2-1
- Update to upstream 1.8.2
- Add patch to ignore TERM

* Fri Jul 01 2011 Chris Lalancette <clalance@redhat.com> - 1.8.0-3
- Bump release to build against new boost package

* Sat Mar 19 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-2
- Make mongod bind only to 127.0.0.1 by default

* Sat Mar 19 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.8.0-1
- Update to 1.8.0
- Remove upstreamed nonce patch

* Wed Feb 16 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-5
- Add nonce patch

* Sun Feb 13 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-4
- Manually define to use boost-fs v2

* Sat Feb 12 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-3
- Disable extra warnings

* Fri Feb 11 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-2
- Disable compilation errors on warnings

* Fri Feb 11 2011 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.7.5-1
- Update to 1.7.5
- Remove CPPFLAGS override
- Added libmongodb package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.4-3
- Add post/postun ldconfig... oops!

* Mon Dec 06 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.4-2
- Enable --sharedclient option, remove static lib

* Sat Dec 04 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.4-1
- New upstream release

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.3-4
- Put -fPIC onto both the build and install scons calls

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.3-3
- Define _initddir when it doesn't exist for el5 and others

* Fri Oct 08 2010 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.6.3-2
- Added -fPIC build option which was dropped by accident

* Thu Oct  7 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.3-1
- removed js Requires
- new upstream release
- added more excludearches: sparc s390, s390x and bugzilla pointer

* Tue Sep  7 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.2-2
- added ExcludeArch for ppc

* Fri Sep  3 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.2-1
- new upstream release 1.6.2
- send mongod the USR1 signal when doing logrotate
- use config options when starting the daemon from the initfile
- removed dbpath patch: rely on config
- added pid directory to config file and created the dir in the spec
- made the init script use options from the config file
- changed logpath in mongodb.conf

* Wed Sep  1 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.1-1
- new upstream release 1.6.1
- patched SConstruct to allow setting cppflags
- stopped using sed and chmod macros

* Fri Aug  6 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.6.0-1
- new upstream release: 1.6.0
- added -server package
- added new license file to %%docs
- fix spurious permissions and EOF encodings on some files

* Tue Jun 15 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.4.3-2
- added explicit js requirement
- changed some names

* Wed May 26 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.4.3-1
- updated to 1.4.3
- added zlib license for util/md5
- deleted upstream deb/rpm recipes
- made scons not strip binaries
- made naming more consistent in logfile, lockfiles, init scripts etc.
- included manpages and added corresponding license
- added mongodb.conf to sources

* Fri Oct  2 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-3
- fixed libpath issue for 64bit systems

* Thu Oct  1 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-2
- added virtual -static package

* Mon Aug 31 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.0-1
- Initial release.
