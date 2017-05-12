#
# spec file for package nicstat
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

Summary:	Network traffic statics utility
Name:		nicstat
Version:	1.95
Release:	0
Group:		Productivity/Networking/Other
License:	GPL-2.0
URL:		http://sourceforge.net/projects/nicstat/
Source0:	http://sourceforge.net/projects/nicstat/files/nicstat-src-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description
Prints out network statistics for all network cards (NICs), including packets,
kilobytes per second, average packet sizes and more.

%prep

%setup -q -n nicstat-src-%{version}

%build
gcc %{optflags}  nicstat.c -o nicstat

%install

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

install -m0755 nicstat %{buildroot}%{_bindir}/
install -m0644 nicstat.1 %{buildroot}%{_mandir}/man1/

%files
%defattr(-,root,root,-)
%doc ChangeLog.txt LICENSE.txt README.txt
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog

