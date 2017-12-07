# for better compatibility with SCL spec file
%global pkg_name mongo-cxx-driver

Name:           mongo-cxx-driver
Version:        1.1.2
Release:        10%{?dist}
Summary:        A legacy C++ Driver for MongoDB
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/mongodb/mongo-cxx-driver/wiki
Source0:        https://github.com/mongodb/%{pkg_name}/archive/legacy-%{version}.tar.gz

BuildRequires:  boost-devel >= 1.49
BuildRequires:  compat-openssl10-devel
BuildRequires:  scons
BuildRequires:  cyrus-sasl-devel
# Tests requirements
#BuildRequires:  python-virtualenv
#BuildRequires:  mongodb-server
#BuildRequires:  git

Provides: libmongodb = 2.6.0-%{release}
Provides: libmongodb%{?_isa} = 2.6.0-%{release}
Obsoletes: libmongodb <= 2.4.9-8

%description
This package provides the shared library for the MongoDB legacy C++ Driver.


%package devel
Summary:        MongoDB header files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

Provides: libmongodb-devel = 2.6.0-%{release}
Provides: libmongodb-devel%{?_isa} = 2.6.0-%{release}
Obsoletes: libmongodb-devel <= 2.4.9-8

Provides:       mongodb-devel = 2.6.0-%{release}
Obsoletes:      mongodb-devel < 2.4

%description devel
This package provides the header files for MongoDB legacy C++ driver.


%prep
# -n the name of the directory to cd after unpacking
%setup -q -n %{name}-legacy-%{version}

# CRLF -> LF
sed -i 's/\r//' README.md

# use _lib
sed -i -e "s@\$INSTALL_DIR/lib@\$INSTALL_DIR/%{_lib}@g" src/SConscript.client

# versioned client library
(pre='EnsureSConsVersion(2, 3, 0)'
post='sharedLibEnv.AppendUnique(SHLIBVERSION="%{version}")'
sed -i -r \
  -e "s|([[:space:]]*)(sharedLibEnv *= *libEnv.Clone.*)|\1$pre\n\1\2\n\1$post|" \
  -e "s|(sharedLibEnv.)Install *\(|\1InstallVersionedLib(|" \
  src/SConscript.client)

# use optflags
(opt=$(echo "%{optflags}" | sed -r -e 's| |","|g' )
sed -i -r -e "s|(if nix:)|\1\n\n    env.Append( CCFLAGS=[\"$opt\"] )\n\n|" SConstruct)

# fix one unit test which uses gnu++11 code (c++11 is used)
sed -i 's|ASSERT_PARSES(double, "0xabcab.defdefP-10", 0xabcab.defdefP-10);||' src/mongo/base/parse_number_test.cpp

# Fix boost:ref usage in examples
sed -i -r -e "s|boost::ref|std::ref|g" src/mongo/client/examples/connect.cpp


%build
# see 'scons -h' for options
scons \
        %{?_smp_mflags} \
        --sharedclient \
        --ssl \
        --c++11 \
        --disable-warnings-as-errors \
        --opt=off \
        --use-sasl-client


%install
# NOTE: If install flags are not the same as in %%build,
#   it will be built twice!
scons install \
        %{?_smp_mflags} \
        --sharedclient \
        --ssl \
        --c++11 \
        --disable-warnings-as-errors \
        --opt=off \
        --use-sasl-client \
        --prefix=%{buildroot}%{_prefix}

# There is no option to build without static library
rm -f %{buildroot}%{_libdir}/libmongoclient.a

%check
### Koji and Brew do not allow internet connection during build,
### so skipping integration tests and building examples

## Install mongo-orchestration into virtualenvironment
#virtualenv ./orchestration
#source ./orchestration/bin/activate
#pip install git+git://github.com/mongodb/mongo-orchestration@master

## Tests need running mongo-orchestration
#mongo-orchestration start

# Run tests
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH \
scons unit \
        %{?_smp_mflags} \
        --sharedclient \
        --ssl \
        --c++11 \
        --disable-warnings-as-errors \
        --opt=off \
        --use-sasl-client \
        --gtest-filter=-SASL* \
        --propagate-shell-environment

#mongo-orchestration stop

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md APACHE-2.0.txt
%{_libdir}/libmongoclient.so.*

%files devel
%{_includedir}/*
%{_libdir}/libmongoclient.so

%changelog
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 1.1.2-8
- Rebuilt for s390x binutils bug

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 1.1.2-7
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue Feb 28 2017 Marek Skalický <mskalick@redhat.com> - 1.1.2-5
- Temporary disable optimizations (some tests are failing with it)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.2-3
- Remove ExclusiveArch. While a MongoDB instance is little endian only, this is a client
- Build with openssl 1.0

* Tue Aug 02 2016 Marek Skalický <mskalick@redhat.com> - 1.1.2-2
- Enabled sasl support
- Unit tests added in check section

* Wed Jun 22 2016 Marek Skalicky <mskalick@redhat.com> - 1.1.2-1
- Upgrade to version 1.1.2

* Tue May 17 2016 Jonathan Wakely <jwakely@redhat.com> - 1.1.0-4
- Rebuilt for linker errors in boost (#1331983)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Jonathan Wakely <jwakely@redhat.com> - 1.1.0-2
- Rebuilt for Boost 1.60

* Thu Dec 10 2015 Marek Skalicky <mskalick@redhat.com> - 1.1.0-1
- Upgrade to version 1.1.0

* Fri Nov 20 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.7-1
- Upgrade to version 1.0.7

* Thu Oct 22 2015 Tim Niemueller <tim@niemueller.de> - 1.0.6-1
- Upgrade to version 1.0.6
- Add --c++11 flag

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.0.5-2
- Rebuilt for Boost 1.59

* Wed Aug 19 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.5-1
- Upgrade to version 1.0.5

* Mon Aug 17 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.4-1
- Upgrade to version 1.0.4

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.0.2-3
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.2-1
- Upgrade to version 1.0.2

* Tue Apr 14 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.1-1
- Upgrade to version 1.0.1

* Tue Feb 10 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.0-3
- Disabled -Werror (dont't build with gcc 5.0)

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 1.0.0-2
- Bump for rebuild.

* Thu Jan 29 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.0-1
- Upgrade to stable version 1.0.0

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.0.0-0.8.rc3
- Rebuild for boost 1.57.0

* Fri Jan 02 2015 Marek Skalicky <mskalick@redhat.com> - 1.0.0-0.7.rc3
- Upgrade to rc3

* Tue Nov 18 2014 Marek Skalický <mskalick@redhat.com> - 1.0.0-0.6.rc2
- Upgrade to rc2
- Changed scons target to build only driver

* Mon Oct 27 2014 Marek Skalický <mskalick@redhat.com> - 1.0.0-0.5.rc1
- Upgrade to rc1
- Added mongo-cxx-driver-devel requires (openssl-devel, boost-devel)

* Sat Oct 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-0.4.rc1
- Don't reset the Release until 1.0.0 GA

* Fri Oct 24 2014 Marek Skalický <mskalick@redhat.com> - 1.0.0-0.1.rc1
- Upgrade to rc1

* Thu Oct 9 2014 Marek Skalický <mskalick@redhat.com> - 1.0.0-0.3.rc0
- Added Provides: mongodb-devel = 2.6.0-1 provided by libmongo-devel

* Thu Oct 9 2014 Marek Skalický <mskalick@redhat.com> - 1.0.0-0.2.rc0
- Added Provides: libmongodb%{?_isa} packages

* Tue Sep 30 2014 Marek Skalický <mskalick@redhat.com> - 1.0.0-0.1.rc0
- initial port
