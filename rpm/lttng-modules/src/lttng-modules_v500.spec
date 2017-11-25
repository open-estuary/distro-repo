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

Summary:        Licensing information for package lttng-modules
License:        GPL-2.0 and LGPL-2.1 and MIT
Group:          System/Kernel
Name:           lttng-modules
Version:        2.10.3
Release:        0
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  kernel = 4.12.0 kernel-devel = 4.12.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

#%suse_kernel_module_package -p %{name}-preamble ec2 xen xenpae vmi um 

%description
This package provides licensing documentation for the lttng kmp packages.

%prep
%setup -q

%build
make

%install
mkdir -p %{buildroot}/usr/lib/modules/%{kernel_version}/armor/
install -m 511 lib/*.ko %{buildroot}/usr/lib/modules/%{kernel_version}/armor/
install -m 511 *.ko %{buildroot}/usr/lib/modules/%{kernel_version}/armor
install -m 511 probes/*.ko %{buildroot}/usr/lib/modules/%{kernel_version}/armor/


%files
%defattr(-,root,root)

/usr/lib/modules/%{kernel_version}/armor/*

%post
depmod -a

%changelog

