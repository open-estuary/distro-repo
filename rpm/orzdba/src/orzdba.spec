%define INSTALL_DIR              /etc/orzdba
%define EXECUTE_DIR              /usr/local/bin

Name:           orzdba
Version:        1.0
Release:        0
Summary:        mysql monitor
License:        taobao
Source:         http://code.taobao.org/svn/orzdba/trunk/orzdba-1.0.tar.gz
Requires:       perl-Time-HiRes
Requires:       perl-ExtUtils-CBuilder
Group:          mysql

%description
it can be used to monitor mysql performance

%prep
%setup -q

%build
#%_configure
#make %{?_smp_mflags}


%install
pushd %{_sourcedir} > /dev/null
install -d -m 755 %{buildroot}%{INSTALL_DIR}
install -d -m 755 %{buildroot}%{EXECUTE_DIR}

tar -zxvf %{name}-%{version}.tar.gz
cd %{name}-%{version}
tar -zxvf orzdba_rt_depend_perl_module.tar.gz
cd Perl_Module
tar -zxvf version-0.99.tar.gz
tar -zxvf Class-Data-Inheritable-0.08.tar.gz
tar -zxvf File-Lockfile-v1.0.5.tar.gz
tar -zxvf Module-Build-0.31.tar.gz

cp ../../Test-Simple-1.302113.tar.gz ./
cp ../../File-Fu-v0.0.8.tar.gz ./
cp ../../Class-Accessor-Classy-v0.9.1.tar.gz ./
tar -zxvf Test-Simple-1.302113.tar.gz
tar -zxvf File-Fu-v0.0.8.tar.gz
tar -zxvf Class-Accessor-Classy-v0.9.1.tar.gz

cd ../..

#cp Fu.pm %{name}-%{version}/Perl_Module/Module-Build-0.31/lib/Module/Build/

cp -rf  %{name}-%{version}/* %{buildroot}%{INSTALL_DIR}
cp -f orzdba %{buildroot}%{EXECUTE_DIR}/

popd > /dev/null

%files
%defattr(-,root,root,-)
%{INSTALL_DIR}/*
%{EXECUTE_DIR}/orzdba

%post
pushd %{INSTALL_DIR}/Perl_Module > /dev/null

cd version-0.99
perl Makefile.PL
make
make test
make install
cd ../
cd Class-Data-Inheritable-0.08
perl Makefile.PL
make
make test
make install
cd ../
cd File-Lockfile-v1.0.5
perl Build.PL
perl ./Build
perl ./Build test
perl ./Build install
cd ../
cd Module-Build-0.31
perl Build.PL
perl ./Build
perl ./Build test
perl ./Build install
cd ../
cd File-Fu-v0.0.8
perl Build.PL
perl ./Build
perl ./Build test
perl ./Build install
cd ../
cd Test-Simple-1.302113
perl Makefile.PL
make
make test
make install
cd ../
cd Class-Accessor-Classy-v0.9.1
perl Build.PL
perl ./Build
perl ./Build test
perl ./Build install
cd ../

chmod 755 %{EXECUTE_DIR}/orzdba

popd > /dev/null

%clean
#rm -rf %{_sourcedir}/%{name}-%{version}
#rm -rf %{_sourcedir}/%{name}-%{version}.tar.gz

%changelog
* Fri Nov 24 2017 zhouxingchen  <zhouxingchen@huawei.com> - 1.0-1
- first version orzdba
