#
# spec file for package open-lldp
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define libname liblldp_clif1
Name:           open-lldp
Summary:        Link Layer Discovery Protocol (LLDP) Agent
License:        GPL-2.0
Group:          System/Daemons
Version:        0.9.46
Release:        0
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  libconfig-devel
BuildRequires:  libnl3-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  readline-devel
Url:            http://open-lldp.org/
Source:         %{name}-%{version}.tar.gz
#Source:        http://ftp-osl.osuosl.org/pub/%{name}/%{name}-%{version}.tar.gz
#Patch0:         %{name}-git-update.patch.bz2
#Patch1:         0001-l2_linux_packet-correctly-process-return-value-of-ge.patch
#Patch2:         0002-lldpad-Only-set-Tx-adminStatus-if-interface-is-not-m.patch
#Patch3:         open-lldp-gcc5.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       dcbd = %{version}
Obsoletes:      dcbd < %{version}
Provides:       lldpad = %{version}
Obsoletes:      lldpad < %{version}
BuildRequires:  systemd
%systemd_requires

%description
This package contains the Link Layer Discovery Protocol (LLDP) Agent
with Data Center Bridging (DCB) for Intel(R) Network Connections
'lldpad' plus the configuration tools 'dcbtool' and 'lldptool'.

%package -n %{libname}
Summary:        Link Layer Discovery Protocol (LLDP) libraries
Group:          System/Libraries

%description -n %{libname}
This package contains the Link Layer Discovery Protocol (LLDP) libraries

%package devel
Summary:        Link Layer Discovery Protocol (LLDP) Agent
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{version}
Requires:       %{name} = %{version}
Provides:       dcbd-devel = %{version}
Obsoletes:      dcbd-devel < %{version}
Provides:       lldpad-devel = %{version}
Obsoletes:      lldpad-devel < %{version}

%description devel
This package contains the Link Layer Discovery Protocol (LLDP) Agent
with Data Center Bridging (DCB) for Intel(R) Network Connections
'lldpad' plus the configuration tools 'dcbtool' and 'lldptool'.

%prep
%setup
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1

%build
autoreconf -vi
%configure \
	--disable-static
make %{?_smp_mflags}

%check
make check %{?_smp_mflags}

%install
mkdir -p %{buildroot}/var/lib/lldpad
%makeinstall
# remove la archives
rm -rf %{buildroot}/%{_libdir}/*.la
ln -s service %{buildroot}%{_sbindir}/rclldpad

%post
%{fillup_only -n -i lldpad}
%service_add_post lldpad.service

%pre
%service_add_pre lldpad.service

%preun
%service_del_preun lldpad.service

%postun
%service_del_postun lldpad.service

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%dir /var/lib/lldpad
%{_unitdir}/*
%{_sbindir}/*
%{_mandir}/man3/*
%{_mandir}/man8/*
%config /etc/bash_completion.d/*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog

