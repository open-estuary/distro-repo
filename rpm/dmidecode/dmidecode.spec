#
# spec file for package dmidecode
#
# Copyright (c) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

Name:           dmidecode
Version:        3.0
Release:        0
Summary:        DMI table decoder
License:        GPL-2.0+
Group:          System/Console
Url:            http://www.nongnu.org/dmidecode/
Source0:        %{name}-%{version}.tar.gz
# would be, but tarball is signed by someone else without signatures.
# https://savannah.nongnu.org/project/memberlist-gpgkeys.php?group=dmidecode
# Source2:        %{name}.keyring
#Patch1:         dmidecode-01-add-no-sysfs-option-description-to-h-output.patch
#Patch2:         dmidecode-02-fix-no-smbios-nor-dmi-entry-point-found-on-smbios3.patch
#Patch3:         dmidecode-03-let-read_file-return-the-actual-data-size.patch
#Patch4:         dmidecode-04-use-read_file-to-read-the-dmi-table-from-sysfs.patch
#Patch5:         dmidecode-05-use-dword-for-structure-table-maximum-size-in-smbios3.patch
#Patch6:         dmidecode-06-hide-irrelevant-fixup-message.patch
#Patch7:         dmidecode-07-only-decode-one-dmi-table.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildRequires:  automake autoconf
ExclusiveArch:  %ix86 ia64 x86_64 %arm aarch64

%description
Dmidecode reports information about your system's hardware as described
in your system BIOS according to the SMBIOS/DMI standard. This
information typically includes system manufacturer, model name, serial
number, BIOS version, asset tag as well as a lot of other details of
varying level of interest and reliability depending on the
manufacturer. This will often include usage status for the CPU sockets,
expansion slots (e.g. AGP, PCI, ISA) and memory module slots, and the
list of I/O ports (e.g. serial, parallel, USB).

Beware that DMI data have proven to be too unreliable to be blindly
trusted. Dmidecode does not scan your hardware, it only reports what
the BIOS told it to.

%prep
%setup -q
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1

%build
make CFLAGS="%{optflags}" %{?_smp_mflags}

%install
install -dm 755 %{buildroot}%{_sbindir}
install -dm 755 %{buildroot}%{_mandir}/man8
install -dm 755 %{buildroot}%{_docdir}/%{name}
%ifarch ia64 %arm aarch64
for i in dmidecode ; do
%else
for i in dmidecode vpddecode ownership biosdecode ; do
%endif
install -m 755 $i %{buildroot}%{_sbindir}/
install -m 644 man/$i.8 %{buildroot}%{_mandir}/man8/
install -m 644 AUTHORS CHANGELOG LICENSE README %{buildroot}%{_docdir}/%{name}/
done

%files
%defattr(-,root,root)
%{_sbindir}/*
%doc %{_docdir}/%{name}
%{_mandir}/man8/*

%changelog
