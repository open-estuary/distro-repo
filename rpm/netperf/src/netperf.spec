#
# spec file for package netperf
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


Name:           netperf
Version:   2.7.0
Release:        8.1
Summary:        Network benchmarking tool
License:        SUSE-NonFree
Group:          System/Benchmark
Url:            http://www.netperf.org/
Source:         ftp://ftp.netperf.org/netperf/%{name}-%{version}.tar.bz2
# Patches from gentoo package
Patch0:         netperf-fix-scripts.patch
Patch1:         netperf-2.6.0-log-dir.patch
Patch2:         netperf-2.7.0-includes.patch
BuildRequires:  lksctp-tools-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%ifarch ix86 x86_64
BuildRequires:  libsmbios-devel
%endif

%description
Netperf is a benchmark that can be used to measure the performance of many different types of networking. It provides tests for both unidirecitonal throughput, and end-to-end latency. The environments currently measureable by netperf include:

    * TCP and UDP via BSD Sockets for both IPv4 and IPv6
    * DLPI
    * Unix Domain Sockets
    * SCTP for both IPv4 and IPv6

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="%{optflags} -fno-strict-aliasing"
%configure \
	--enable-unixdomain \
	--enable-dccp \
	--enable-sctp

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm doc/examples/Makefile*

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%preun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%files
%defattr(-, root, root,)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/netperf
%{_bindir}/netserver
%doc doc/examples
%{_mandir}/man1/*
%{_infodir}/%{name}.info.gz
%{_infodir}/dir

%changelog
* Thu Sep  3 2015 mpluskal@suse.com
- Update to 2.7.0
  * See ChangeLog for full list of changes
- Add patches from gentoo
  * netperf-fix-scripts.patch
  * netperf-2.6.0-log-dir.patch
  * netperf-2.7.0-includes.patch
* Tue May  5 2015 mpluskal@suse.com
- Make dependency on libsmbios conditional only to supported
  architectures
* Wed Apr  8 2015 mpluskal@suse.com
- Update license
* Mon Apr  6 2015 mpluskal@suse.com
- Initial package for openSUSE
