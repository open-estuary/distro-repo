# remirepo/fedora spec file for mongo-c-driver
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   mongo-c-driver
%global libname      libmongoc
%global libver       1.0
#global prever       rc2
%global bsonver      1.8

%ifarch x86_64
# Temporarily disabled
%global with_tests   0%{?_with_tests:1}
%else
# See https://jira.mongodb.org/browse/CDRIVER-1186
# 32-bit MongoDB support was officially deprecated
# in MongoDB 3.2, and support is being removed in 3.4.
%global with_tests   0%{?_with_tests:1}
%endif

Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   1.8.2
Release:   1%{?dist}
License:   ASL 2.0
Group:     System Environment/Libraries
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz

# RPM specific changes
# 1. Ignore check for libbson version = libmongoc version
# 2. Use bundled libbson documentation
#    https://jira.mongodb.org/browse/CDRIVER-2078
# 3. Don't install COPYING file which is not doc but license
Patch0:    %{name}-rpm.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libbson-1.0) > %{bsonver}
BuildRequires: pkgconfig(libsasl2)
BuildRequires: pkgconfig(zlib)
%if 0%{?fedora} >= 26
# pkgconfig file introduce in 1.1.4
BuildRequires: pkgconfig(snappy)
%else
BuildRequires: snappy-devel
%endif
%if %{with_tests}
BuildRequires: mongodb-server
BuildRequires: openssl
%endif
BuildRequires: perl-interpreter
# From man pages
BuildRequires: python
BuildRequires: /usr/bin/sphinx-build

Requires:   %{name}-libs%{?_isa} = %{version}-%{release}
# Sub package removed
Obsoletes:  %{name}-tools         < 1.3.0
Provides:   %{name}-tools         = %{version}
Provides:   %{name}-tools%{?_isa} = %{version}


%description
%{name} is a client library written in C for MongoDB.


%package libs
Summary:    Shared libraries for %{name}
Group:      Development/Libraries

%description libs
This package contains the shared libraries for %{name}.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}.

Documentation: http://api.mongodb.org/c/%{version}/


%prep
%setup -q -n %{gh_project}-%{version}%{?prever:-dev}
%patch0 -p1 -b .rpm

: Generate build scripts from sources
autoreconf --force --install --verbose -I build/autotools

: delete bundled libbson sources
rm -r src/libbson


%build
export LIBS=-lpthread

%configure \
  --enable-debug-symbols \
  --enable-shm-counters \
  --disable-automatic-init-and-cleanup \
  --enable-crypto-system-profile \
%if %{with_tests}
  --enable-tests \
%else
  --disable-tests \
%endif
  --enable-sasl \
  --enable-ssl \
  --with-libbson=system \
  --with-snappy=system \
  --with-zlib=system \
  --disable-html-docs \
  --enable-examples \
  --enable-man-pages

rm -r src/zlib-*

make %{?_smp_mflags} all V=1

# Explicit man target is needed for generating manual pages
make %{?_smp_mflags} doc/man V=1


%install
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*la

: install examples
for i in examples/*.c examples/*/*.c; do
  install -Dpm 644 $i %{buildroot}%{_datadir}/doc/%{name}/$i
done

: Rename documentation to match subpackage name
mv %{buildroot}%{_datadir}/doc/%{name} \
   %{buildroot}%{_datadir}/doc/%{name}-devel


%check
%if %{with_tests}
: Run a server
mkdir dbtest
mongod \
  --journal \
  --ipv6 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
ret=0
export MONGOC_TEST_OFFLINE=on
#export MONGOC_TEST_SKIP_SLOW=on

make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

exit $ret
%endif


%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%{_bindir}/mongoc-stat

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%license THIRD_PARTY_NOTICES
%{_libdir}/%{libname}-%{libver}.so.*

%files devel
%{_docdir}/%{name}-devel
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.so
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_libdir}/cmake/%{libname}-%{libver}
%{_mandir}/man3/mongoc*


%changelog
* Fri Nov 17 2017 Remi Collet <remi@fedoraproject.org> - 1.8.2-1
- update to 1.8.2

* Thu Oct 12 2017 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- update to 1.8.1

* Fri Sep 15 2017 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- update to 1.8.0

* Thu Aug 10 2017 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0
- disable test suite in rawhide (mongodb-server is broken)

* Tue Aug  8 2017 Remi Collet <remi@fedoraproject.org> - 1.7.0-0.1.rc2
- update to 1.7.0-rc2
- add --with-snappy and --with-zlib build options

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 24 2017 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.2

* Tue Mar 28 2017 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Wed Mar  8 2017 Remi Collet <remi@fedoraproject.org> - 1.6.1-2
- rebuild with new upstream tarball
- add examples in devel documentation
- use patch instead of sed hacks for rpm specific changes

* Tue Mar  7 2017 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1
- open https://jira.mongodb.org/browse/CDRIVER-2078
  can't build man pages

* Thu Feb  9 2017 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- add fix for https://jira.mongodb.org/browse/CDRIVER-2042
  from https://github.com/mongodb/mongo-c-driver/pull/421

* Thu Jan 12 2017 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- update to 1.5.3

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- update to 1.5.2
- run server on both IPv4 and IPv6
- open https://jira.mongodb.org/browse/CDRIVER-1988 - Failed test
- revert IPv6 commit

* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- update to 1.5.1

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Fri Nov 18 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.5.rc6
- update to 1.5.0-rc6

* Fri Nov  4 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.4.rc4
- update to 1.5.0-rc4

* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.3.rc3
- update to 1.5.0-rc3
- drop patches merged upstream

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.2.rc2
- open https://jira.mongodb.org/browse/CDRIVER-1703 missing files
- open https://jira.mongodb.org/browse/CDRIVER-1702 broken test
- enable test suite

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.1.rc2
- update to 1.5.0-rc2
- drop crypto patch merged upstream
- drop the private library
- disable test suite

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 1.3.5-6
- Rebuild against libbson-1.4.0 (bug #1361166)

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-5
- add BR on perl, FTBFS from Koschei

* Mon Jun 13 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-4
- add workaround to abicheck failure
  see https://bugzilla.redhat.com/1345868

* Mon May 16 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-2
- add patch to enforce system crypto policies

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- update to 1.3.5
- use --disable-automatic-init-and-cleanup build option
- ignore check for libbson version = libmongoc version

* Sat Mar 19 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- build with MONGOC_NO_AUTOMATIC_GLOBALS

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- update to 1.3.4
- drop patch merged upstream

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- cleanup for review
- move libraries in "libs" sub-package
- add patch to skip online tests
  open https://github.com/mongodb/mongo-c-driver/pull/314
- temporarily disable test suite on arm  (#1303864)
- temporarily disable test suite on i686/F24+ (#1313018)

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- move tools in devel package

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- open https://jira.mongodb.org/browse/CDRIVER-1040 - ABI breaks

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.6.rc0
- Update to 1.2.0-rc0

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.5.20150903git3eaf73e
- add patch to export library verson in the API
  open https://github.com/mongodb/mongo-c-driver/pull/265

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.4.20150903git3eaf73e
- update to version 1.2.0beta1 from git snapshot
- https://jira.mongodb.org/browse/CDRIVER-828 missing tests/json

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.3.beta
- more upstream patch (for EL-6)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.beta
- Upstream version 1.2.0beta

* Wed May 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Upstream version 1.1.6

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Upstream version 1.1.5

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-3
- test build for upstream patch

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- cleanup build dependencies and options

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Initial package
- open https://jira.mongodb.org/browse/CDRIVER-624 - gcc 5
