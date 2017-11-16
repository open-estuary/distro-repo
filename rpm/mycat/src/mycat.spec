#
# spec file for package mycat
#

# Please submit bugfixes or comments via http://www.mycat.io/
#

%define mycat_version 1.6
%define mycat_build_datetime 20161028204710

Name:           mycat
Version:        1.6
Release:        1
Summary:        MySQL or other databases proxy
License:        SUSE-NonFree
Group:          System Environment/Libraries
Url:            http://www.mycat.io/
#Source:         https://github.com/MyCATApache/Mycat-download/raw/master/%{version}-RELEASE/

Source0:        http://dl.mycat.io/1.6-RELEASE/Mycat-server-%{version}-RELEASE-%{mycat_build_datetime}-linux.tar.gz
Source1:        https://sourceforge.net/projects/wrapper/files/wrapper_src/Wrapper_3.5.34_20170927/wrapper_3.5.34_src.tar.gz

#BuildRequires: ant
BuildRequires: CUnit-devel

%description
mycat is a fast and lightweight proxy for mysql or other databases.

%prep
rm -rf $RPM_BUILD_DIR/mycat
tar -zxvf $RPM_SOURCE_DIR/Mycat-server-%{version}-RELEASE-%{mycat_build_datetime}-linux.tar.gz
tar -zxvf $RPM_SOURCE_DIR/wrapper_3.5.34_src.tar.gz
cp $RPM_SOURCE_DIR/Makefile-linux-aarch64-64.make $RPM_BUILD_DIR/wrapper_3.5.34_src/src/c/

%build
cd $RPM_BUILD_DIR/wrapper_3.5.34_src/
chmod 777 *
sh build64.sh

%install
rm -rf mycat/bin/wrapper-linux-ppc-64
rm -rf mycat/bin/wrapper-linux-x86-64
rm -rf mycat/bin/wrapper-linux-x86-32
rm -rf mycat/lib/libwrapper-linux-ppc-64.so
rm -rf mycat/lib/libwrapper-linux-x86-32.so
rm -rf mycat/lib/libwrapper-linux-x86-64.so

cd mycat/bin
cp /bin/wrapper .
#cd ../lib
#rm -rf wrapper-linux-ppc-64.so wrapper-linux-x86-64.so wrapper-linux-x86-32.so


install -d %{_buildrootdir}//%{name}-%{version}-%{release}.%{_arch}/usr/share/mycat
cp -R $RPM_BUILD_DIR/mycat %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/usr/share/

%post

%preun
if [ -z "`ps aux | grep mycat | grep -v grep`" ];then
    ps -ef|grep mycat |grep -v grep|awk  '{print "kill -9 " $2}' |sh
    exit 0
fi

%files
%defattr(-, root, root,)
/usr/share/mycat

%changelog
* Thu Nov 9 2017 wy200885@163.com
- First version
