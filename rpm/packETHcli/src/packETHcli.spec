#
#spec file for package packETH
#
# Copyright (c) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           packETHcli
Version:   1.8
Release:        0
Summary:        Packet generator tool for ethernet
License:        GPL-3.0+
Group:          Productivity/Networking/Diagnostic
Url:            http://packeth.sourceforge.net/packeth/Home.html
Source0:        https://sourceforge.net/projects/packeth/files/packETHcli-%{version}.tar.gz
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build


%description
the command line version of packETH called packETHcli.
Type ./packETHcli -h  for more options.

%prep
%setup -q

%build
make

%install
mkdir -p %{buildroot}%{_bindir}
install -m 500 packETHcli %{buildroot}%{_bindir}


%files
%{_bindir}/packETHcli

%changelog

