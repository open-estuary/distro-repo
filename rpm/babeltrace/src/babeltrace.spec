#
# spec file for package babeltrace
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           babeltrace
Version:   1.2.4
Release:        0
Source:         http://www.efficios.com/files/babeltrace/%{name}-%{version}.tar.bz2
Summary:        Common Trace Format Babel Tower
License:        MIT and GPL-2.0
Group:          Development/Languages/C and C++
Url:            http://diamon.org/babeltrace
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
BuildRequires:  pkgconfig
BuildRequires:  popt-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  aarch64 %ix86 x86_64

%description
This project provides trace read and write libraries, as well as a trace
converter. A plugin can be created for any trace format to allow its conversion
to/from another trace format.

The main format expected to be converted to/from is the Common Trace
Format (CTF). The latest version of the CTF specification can be found at:

  git tree:   git://git.efficios.com/ctf.git
  gitweb:     http://git.efficios.com/?p=ctf.git

Mathieu Desnoyers, EfficiOS Inc.
September 2010

%package -n %{name}-devel

Summary:        Common Trace Format Babel Tower
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel

%description -n %{name}-devel
This project provides trace read and write libraries, as well as a trace
converter. A plugin can be created for any trace format to allow its conversion
to/from another trace format.

The main format expected to be converted to/from is the Common Trace
Format (CTF). The latest version of the CTF specification can be found at:

  git tree:   git://git.efficios.com/ctf.git
  gitweb:     http://git.efficios.com/?p=ctf.git

Mathieu Desnoyers, EfficiOS Inc.
September 2010

%prep
%setup -q 

%build
%configure --docdir=%{_docdir}/%{name}
make

%install
make DESTDIR=%buildroot install
rm -vf %buildroot%{_libdir}/*.la
mkdir -p %buildroot%{_prefix}/include/babeltrace
cp -R include/babeltrace/* %buildroot%{_prefix}/include/babeltrace

%clean
rm -rf %buildroot

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/%{name}*
%{_libdir}/*.so.*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/*.txt
%{_mandir}/man1/*.1.gz

%files -n %{name}-devel
%defattr(-,root,root)
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-ctf.pc

%changelog

