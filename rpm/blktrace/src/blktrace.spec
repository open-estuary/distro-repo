Summary: Utilities for performing block layer IO tracing in the linux kernel
Name:           blktrace
Version:   1.0.5
Release:        1%{?dist}
License:        GPLv2+
Group:          Development/System
Source: 	http://brick.kernel.dk/snaps/blktrace-%{version}.tar.gz
URL:            http://brick.kernel.dk/snaps

Requires: python
BuildRequires: libaio-devel python
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
blktrace is a block layer IO tracing mechanism which provides detailed information about request queue operations to user space. 
This package includes both blktrace, a utility which gathers event traces from the kernel;and blkparse, a utility which formats trace data collected by blktrace.

You should install the blktrace package if you need to gather detailed information about IO patterns.

%prep
%setup -q

%build
make CFLAGS="%{optflags}" all

%install
rm -rf %{buildroot}
make dest=%{buildroot} prefix=%{buildroot}/%{_prefix} mandir=%{buildroot}/usr/share/man install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COPYING
%{_bindir}/*
%attr(0644,root,root) /usr/share/man/man1/*
%attr(0644,root,root) /usr/share/man/man8/*

%changelog
