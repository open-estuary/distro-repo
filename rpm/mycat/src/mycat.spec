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

Source0:        Mycat-server-%{version}-RELEASE-%{mycat_build_datetime}-linux.tar.gz
Source1:        wrapper-linux-aarch64-64

%description
mycat is a fast and lightweight proxy for mysql or other databases.

%prep
sudo rm -rf $RPM_BUILD_DIR/mycat
sudo tar -zxvf $RPM_SOURCE_DIR/Mycat-server-%{version}-RELEASE-%{mycat_build_datetime}-linux.tar.gz

%build

%install
cd mycat/bin
cp $RPM_SOURCE_DIR/wrapper-linux-aarch64-64 .

install -d %{_buildrootdir}//%{name}-%{version}-%{release}.%{_arch}/usr/local/mycat
cp -R $RPM_BUILD_DIR/mycat %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/usr/local/

%post

%preun
if [ -z "`ps aux | grep mycat | grep -v grep`" ];then
    ps -ef|grep mycat |grep -v grep|awk  '{print "kill -9 " $2}' |sh
    exit 0
fi

%files
%defattr(-, root, root,)
/usr/local/mycat

%changelog
* Thu Nov 9 2017 wy200885@163.com
- First version
