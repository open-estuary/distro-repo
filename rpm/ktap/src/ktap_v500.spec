#
# spec file for package lttng-modules
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

# needssslcertforbuild
%define kernel_version 4.12.0-estuary.2.aarch64

Summary:        A New Scripting Dynamic Tracing Tool For Linux 
License:        GPL-2.0 
Group:          System/Kernel
Name:           ktap
Version:   0.4
Release:        0
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  elfutils-libelf-devel kernel = 4.12.0 kernel-devel = 4.12.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
ktap is a new scripting dynamic tracing tool for Linux, it uses 
a scripting language and lets users trace the Linux kernel dynamically. 
ktap is designed to give operational insights with interoperability 
that allows users to tune, troubleshoot and extend the kernel and applications. 
It's similar to Linux Systemtap and Solaris Dtrace.

%prep
%setup -q

%build
make

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/modules/%{kernel_version}/armor/
mkdir -p %{buildroot}/test_scripts
install -m 511 ktap %{buildroot}/usr/bin
install -m 511 ktapvm.ko %{buildroot}/usr/lib/modules/%{kernel_version}/armor
install -m 511 samples/helloworld.kp  %{buildroot}/test_scripts


%files
%defattr(-,root,root)
/usr/bin/ktap
/usr/lib/modules/%{kernel_version}/armor/ktapvm.ko
/test_scripts/helloworld.kp

%post
depmod -a

%changelog

