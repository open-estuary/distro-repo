#
# spec file for package ethtool
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           ethtool
Version:   4.8
Release:        0
Summary:        Examine and Tune Ethernet-Based Network Interfaces
License:        GPL-2.0
Group:          Productivity/Networking/Diagnostic
Url:            http://kernel.org/pub/software/network/ethtool/
#Git-Clone:	git://git.kernel.org/pub/scm/network/ethtool/ethtool
Source:         http://kernel.org/pub/software/network/ethtool/%{name}-%{version}.tar.gz
Patch0:         0001-ethtool-add-one-ethtool-option-to-set-relax-ordering.patch 
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  automake, autoconf

%description
Ethtool is a small utility for examining and tuning ethernet-based
network interfaces.  See the man page for more details.

%prep
%setup -q
%patch0 -p1

%build
#export CFLAGS="%{optflags} -W -Wall -Wstrict-prototypes -Wformat-security -Wpointer-arith"
%_configure
make %{?_smp_mflags}

%install
make install DESTDIR="%buildroot" INSTALL='install -p' install
mkdir -p %{buildroot}/sbin
ln -sf /usr/local/sbin/ethtool %{buildroot}/sbin/

%files
%defattr(-,root,root)
#UsrMerge
/sbin/ethtool
#EndUserMerge
/usr/local/sbin/ethtool
/usr/local/share/man/man8/ethtool.8*
%doc AUTHORS COPYING NEWS

%changelog
                              
