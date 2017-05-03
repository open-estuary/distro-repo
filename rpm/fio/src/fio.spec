Name:		fio
Version:	2.19
Release:	2%{?dist}
Summary:	Multithreaded IO generation tool

Group:		Applications/System
License:	GPLv2
URL:		http://git.kernel.dk/?p=fio.git;a=summary
Source:		http://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libaio-devel
BuildRequires:	librdmacm-devel
%ifarch aarch64
BuildRequires:	librbd1-devel
%endif

%description
fio is an I/O tool that will spawn a number of threads or processes doing
a particular type of io action as specified by the user.  fio takes a
number of global parameters, each inherited by the thread unless
otherwise parameters given to them overriding that setting is given.
The typical use of fio is to write a job file matching the io load
one wants to simulate.

%prep
%setup -q

%build
EXTFLAGS="$RPM_OPT_FLAGS" make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{_prefix} mandir=%{_mandir} DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README REPORTING-BUGS COPYING HOWTO examples
%dir %{_datadir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}/*

%changelog
* Wed May 3 2017  Huang Jinhua <sjtuhjh@hotmail.com> 2.19
- Estuary initial package 

* Mon Dec 21 2015 Eric Sandeen <sandeen@redhat.com> 2.2.8-2
- Enable RDMA support

* Thu May 07 2015 Eric Sandeen <sandeen@redhat.com> 2.2.8-1
- New upstream version

* Wed Apr 15 2015 Eric Sandeen <sandeen@redhat.com> 2.2.7-1
- New upstream version
- Add librbd ioengine support

* Fri Apr 10 2015 Eric Sandeen <sandeen@redhat.com> 2.2.6-1
- New upstream version

* Tue Feb 17 2015 Eric Sandeen <sandeen@redhat.com> 2.2.5-1
- New upstream version

* Mon Jan 05 2015 Eric Sandeen <sandeen@redhat.com> 2.2.4-1
- New upstream version

* Fri Jan 02 2015 Eric Sandeen <sandeen@redhat.com> 2.2.3-1
- New upstream version

* Wed Nov 12 2014 Eric Sandeen <sandeen@redhat.com> 2.1.14-1
- New upstream version

* Wed Sep 17 2014 Eric Sandeen <sandeen@redhat.com> 2.1.12-1
- New upstream version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 17 2014 Eric Sandeen <sandeen@redhat.com> 2.1.11-1 
- New upstream version

* Mon Jun 16 2014 Eric Sandeen <sandeen@redhat.com> 2.1.10-1 
- New upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Eric Sandeen <sandeen@redhat.com> 2.1.9-1 
- New upstream version

* Mon Apr 14 2014 Eric Sandeen <sandeen@redhat.com> 2.1.8-1 
- New upstream version

* Mon Apr 07 2014 Eric Sandeen <sandeen@redhat.com> 2.1.7-1 
- New upstream version

* Wed Feb 12 2014 Eric Sandeen <sandeen@redhat.com> 2.1.5-1 
- New upstream version

* Wed Sep 25 2013 Eric Sandeen <sandeen@redhat.com> 2.1.3-1 
- New upstream version

* Thu Aug 08 2013 Eric Sandeen <sandeen@redhat.com> 2.1.2-1 
- New upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Eric Sandeen <sandeen@redhat.com> 2.1-1 
- New upstream version

* Wed Apr 17 2013 Eric Sandeen <sandeen@redhat.com> 2.0.15-1 
- New upstream version

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.13-1
- New upstream 2.0.13 release

* Tue Jan 01 2013 Dan Horák <dan[at]danny.cz> - 2.0.12.2-2
- fix build on arches without ARCH_HAVE_CPU_CLOCK (arm, s390)

* Fri Dec 21 2012 Eric Sandeen <sandeen@redhat.com> 2.0.12.2-1 
- New upstream version

* Sat Nov 24 2012 Eric Sandeen <sandeen@redhat.com> 2.0.11-1 
- New upstream version

* Thu Nov 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.10-2
- Merge latest from F16 to master, bump release

* Fri Oct 12 2012 Eric Sandeen <sandeen@redhat.com> 2.0.10-1 
- New upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Eric Sandeen <sandeen@redhat.com> 2.0.8-1
- New upstream version

* Fri Mar 23 2012 Eric Sandeen <sandeen@redhat.com> 2.0.6-1
- New upstream version

* Tue Feb 28 2012 Eric Sandeen <sandeen@redhat.com> 2.0.5-1
- New upstream version

* Mon Jan 23 2012 Eric Sandeen <sandeen@redhat.com> 2.0.1-1
- New upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Eric Sandeen <sandeen@redhat.com> 2.0-1
- New upstream version

* Fri Nov 11 2011 Eric Sandeen <sandeen@redhat.com> 1.99.12-1
- New upstream version

* Tue Sep 27 2011 Eric Sandeen <sandeen@redhat.com> 1.58-1
- New upstream version

* Thu Aug 11 2011 Eric Sandeen <sandeen@redhat.com> 1.57-1
- New upstream version

* Tue May 31 2011 Eric Sandeen <sandeen@redhat.com> 1.55-1
- New upstream version

* Mon May 09 2011 Eric Sandeen <sandeen@redhat.com> 1.53-1
- New upstream version

* Fri Apr 29 2011 Eric Sandeen <sandeen@redhat.com> 1.52-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Eric Sandeen <sandeen@redhat.com> 1.50.2-1
- New upstream version

* Wed Jan 26 2011 Eric Sandeen <sandeen@redhat.com> 1.50-1
- New upstream version

* Wed Dec 15 2010 Eric Sandeen <sandeen@redhat.com> 1.44.3-1
- New upstream version

* Fri Oct 22 2010 Eric Sandeen <sandeen@redhat.com> 1.44.1-1
- New upstream version

* Fri Oct 22 2010 Eric Sandeen <sandeen@redhat.com> 1.44-1
- New upstream version

* Thu Sep 23 2010 Eric Sandeen <sandeen@redhat.com> 1.43.2-1
- New upstream version

* Tue Jun 29 2010 Eric Sandeen <sandeen@redhat.com> 1.41.5-1
- New upstream version

* Tue Jun 22 2010 Eric Sandeen <sandeen@redhat.com> 1.41.3-1
- New upstream version

* Tue Jun 22 2010 Eric Sandeen <sandeen@redhat.com> 1.41-1
- New upstream version

* Fri Jun 18 2010 Eric Sandeen <sandeen@redhat.com> 1.40-1
- New upstream version

* Thu Jun 03 2010 Eric Sandeen <sandeen@redhat.com> 1.39-1
- New upstream version

* Tue Mar 23 2010 Eric Sandeen <sandeen@redhat.com> 1.38-1
- New upstream version

* Tue Feb 23 2010 Eric Sandeen <sandeen@redhat.com> 1.37-1
- New upstream version

* Tue Dec 15 2009 Eric Sandeen <sandeen@redhat.com> 1.36-1
- New upstream version

* Thu Nov 05 2009 Eric Sandeen <sandeen@redhat.com> 1.35-1
- New upstream version

* Mon Sep 14 2009 Eric Sandeen <sandeen@redhat.com> 1.34-1
- New upstream version

* Thu Sep 10 2009 Eric Sandeen <sandeen@redhat.com> 1.33.1-1
- New upstream version

* Tue Sep 08 2009 Eric Sandeen <sandeen@redhat.com> 1.33-1
- New upstream version

* Fri Jul 31 2009 Eric Sandeen <sandeen@redhat.com> 1.32-1
- New upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Eric Sandeen <sandeen@redhat.com> 1.31-1
- Much newer upstream version

* Fri Mar 06 2009 Eric Sandeen <sandeen@redhat.com> 1.24-1
- New upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Eric Sandeen <sandeen@redhat.com> 1.23-1
- New upstream version, several bugs fixed.

* Mon Oct 13 2008 Eric Sandeen <sandeen@redhat.com> 1.22-1
- New upstream version, several bugs fixed.

* Thu Jun 19 2008 Eric Sandeen <sandeen@redhat.com> 1.21-1
- New upstream version
- Build verbosely and with RPM cflags

* Fri Apr 25 2008 Eric Sandeen <sandeen@redhat.com> 1.20-1
- New upstream version

* Thu Apr 10 2008 Eric Sandeen <sandeen@redhat.com> 1.19-1
- New upstream version

* Wed Feb 13 2008 Eric Sandeen <sandeen@redhat.com> 1.18-1
- Initial build
