Name:          bigdata
Version:       1.0 
Release:       1%{?dist}
Summary:       install hadoop

License:       Shareware


%description
autoinstall hadoop

%prep


%build


%install
cd %{_sourcedir}
install -d %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/bigdata 
#scp -r  %{_sourcedir}/* %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/bigdata 
cp -rf %{_sourcedir}/* %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}/bigdata

%files 
%defattr(-, root, root, -)
/bigdata/*


%post
cd /bigdata
echo "please input config file(properties and xml)"
echo "e.g.: config.properties config.xml"
exec 6<&0 0</dev/tty
read pro xml
exec 0<&6 6<&-

sh prepare.sh $pro $xml
sh install.sh install
sh install.sh startup


%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -d "/bigdata" ] ; then
 cd /bigdata 
 if [ -f "usrconf.properties" ] ; then
  sh install.sh stop
  sh install.sh uninstall
  rm -rf /bigdata
 else
  rm -rf /bigdata
 fi
fi



%changelog
