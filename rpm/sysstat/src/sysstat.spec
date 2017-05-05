Summary: Collection of performance monitoring tools for Linux
Name: sysstat
Version:   11.5.5
Release: 1%{?dist}
License: GPLv2+
Group: Applications/System
URL: http://sebastien.godard.pagesperso-orange.fr/
Source: http://pagesperso-orange.fr/sebastien.godard/%{name}-%{version}.tar.gz

# Use colors in sysstat output
Source10: colorsysstat.csh
Source11: colorsysstat.sh

BuildRequires: gettext, lm_sensors-devel, systemd

Requires: findutils, gz
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The sysstat package contains the sar, sadf, mpstat, iostat, tapestat,
pidstat, cifsiostat and sa tools for Linux.
The sar command collects and reports system activity information.
The information collected by sar can be saved in a file in a binary
format for future inspection. The statistics reported by sar concern
I/O transfer rates, paging activity, process-related activities,
interrupts, network activity, memory and swap space utilization, CPU
utilization, kernel activities and TTY statistics, among others. Both
UP and SMP machines are fully supported.
The sadf command may  be used to display data collected by sar in
various formats (CSV, XML, etc.).
The iostat command reports CPU utilization and I/O statistics for disks.
The tapestat command reports statistics for tapes connected to the system.
The mpstat command reports global and per-processor statistics.
The pidstat command reports statistics for Linux tasks (processes).
The cifsiostat command reports I/O statistics for CIFS file systems.

%define _unpackaged_files_terminate_build 0

%prep
%setup -q
cp %_topdir/SOURCES/colorsysstat.csh %{SOURCE10}
cp %_topdir/SOURCES/colorsysstat.sh %{SOURCE11}

%build
%configure \
    --enable-install-cron \
    --enable-copy-only \
    --disable-file-attr \
    --disable-stripping \
    --docdir=%{_pkgdocdir} \
    sadc_options='-S DISK' \
    history=28 \
    compressafter=31
make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}

# Colored sysstat output
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/profile.d
install -p -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/profile.d

%post
%systemd_post sysstat.service sysstat-collect.timer sysstat-summary.timer

%preun
%systemd_preun sysstat.service sysstat-collect.timer sysstat-summary.timer
if [[ $1 -eq 0 ]]; then
    # Remove sa logs if removing sysstat completely
    rm -rf %{_localstatedir}/log/sa/*
fi

%postun
%systemd_postun sysstat.service sysstat-collect.timer sysstat-summary.timer

%files -f %{name}.lang
%doc CHANGES COPYING CREDITS FAQ.md README.md %{name}-%{version}.lsm
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat.ioconf
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_libdir}/sa
%{_unitdir}/sysstat*
%{_mandir}/man*/*
%{_localstatedir}/log/sa

%changelog
* Tue Mar 28 2017 Peter Schiffer <pschiffe@redhat.com> - 11.5.5-1
- resolves: #1427351
  updated to 11.5.5

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Peter Schiffer <pschiffe@redhat.com> - 11.5.4-1
- resolves: #1413365
  updated to 11.5.4

* Tue Jan  3 2017 Peter Schiffer <pschiffe@redhat.com> - 11.5.3-1
- resolves: #1402178
  updated to 11.5.3

* Mon Nov 28 2016 Peter Schiffer <pschiffe@redhat.com> - 11.5.2-1
- resolves: #1392729
  updated to 11.5.2

* Tue Sep 27 2016 Peter Schiffer <pschiffe@redhat.com> - 11.5.1-1
- updated to 11.5.1

* Thu Sep  1 2016 Peter Schiffer <pschiffe@redhat.com> - 11.4.0-1
- resolves: #1370820
  updated to 11.4.0

* Thu Jun 30 2016 Peter Schiffer <pschiffe@redhat.com> - 11.3.5-1
- updated to 11.3.5

* Tue May 24 2016 Peter Schiffer <pschiffe@redhat.com> - 11.3.4-1
- resolves: #1336188
  updated to 11.3.4

* Sat Apr 30 2016 Peter Schiffer <pschiffe@redhat.com> - 11.3.3-1
- updated to 11.3.3

* Thu Mar 31 2016 Peter Schiffer <pschiffe@redhat.com> - 11.3.2-1
- resolves: #1317717
  updated to 11.3.2

* Mon Feb 29 2016 Peter Schiffer <pschiffe@redhat.com> - 11.3.1-1
- resolves: #1310920
  updated to 11.3.1

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Schiffer <pschiffe@redhat.com> - 11.2.0-1
- resolves: #1296762
  updated to 11.2.0

* Mon Nov  2 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.8-1
- resolves: #1274940
  updated to 11.1.8

* Fri Oct  2 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.7-1
- resolves: #1264895
  updated to 11.1.7
- added colors to sysstat output

* Mon Aug 31 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.6-1
- resolves: #1256784
  updated to 11.1.6

* Mon Jun 29 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.5-1
- resolves: #1231242
  updated to 11.1.5

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.4-1
- resolves: #1210532
  updated to 11.1.4

* Mon Mar 02 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.3-1
- resolves: #1193434
  updated to 11.1.3

* Thu Jan 22 2015 Dan Horák <dan[at]danny.cz> - 11.1.2-3
- fix 64-bit builds on non-x86 arches

* Thu Jan 15 2015 Peter Schiffer <pschiffe@redhat.com> - 11.1.2-2
- cleaned .spec file

* Mon Oct 20 2014 Peter Schiffer <pschiffe@redhat.com> - 11.1.2-1
- resolves: #1154601
  updated to 11.1.2

* Thu Sep  4 2014 Peter Schiffer <pschiffe@redhat.com> - 11.1.1-1
- resolves: #1138294
  updated to 11.1.1

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 11.0.0-3
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Peter Schiffer <pschiffe@redhat.com> - 11.0.0-1
- updated to 11.0.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Peter Schiffer <pschiffe@redhat.com> - 10.3.1-1
- resolves: #1077640
  updated to 10.3.1
  migrated to systemd timer units

* Mon Jan 27 2014 Peter Schiffer <pschiffe@redhat.com> - 10.2.1-1
- resolves: #1057547
  updated to 10.2.1

* Mon Nov 11 2013 Peter Schiffer <pschiffe@redhat.com> - 10.2.0-1
- resolves: #1026244
  updated to 10.2.0

* Fri Oct 25 2013 Peter Schiffer <pschiffe@redhat.com> - 10.1.7-1
- resolves: #1007794
  updated to 10.1.7

* Wed Aug 14 2013 Peter Schiffer <pschiffe@redhat.com> - 10.1.6-1
- resolves: #972508
  updated to 10.1.6
- resolves: #993394
  fixed FTBFS (added BR on systemd)
- install the docs in the new pkgdocdir
  (thanks to Mathieu Bridon <bochecha@fedoraproject.org> for the patch)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Peter Schiffer <pschiffe@redhat.com> - 10.1.5-1
- resolves: #919581
  updated to 10.1.5
- collect disk statistics by default

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Peter Schiffer <pschiffe@redhat.com> - 10.1.3-1
- resolves: #890425
  updated to 10.1.3

* Mon Dec  3 2012 Peter Schiffer <pschiffe@redhat.com> - 10.1.2-2
- added new -y option to iostat command to skip first since boot report if
  displaying multiple reports

* Tue Nov 13 2012 Peter Schiffer <pschiffe@redhat.com> - 10.1.2-1
- resolves: #863791
  updated to 10.1.2
- resolves: #850333
  migrated to the new systemd-rpm macros
- cleaned .spec file

* Wed Aug 01 2012 Peter Schiffer <pschiffe@redhat.com> - 10.1.1-1
- resolves: #844387
  update to 10.1.1
- keep log files for 28 days instead of 7
- collect all aditional statistics

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Peter Schiffer <pschiffe@redhat.com> - 10.0.5-1
- resolves: #822867
  update to 10.0.5

* Wed May 16 2012 Peter Schiffer <pschiffe@redhat.com> - 10.0.4-1
- resolves: #803032
  update to 10.0.4
- resolves: #820725
  enable sysstat service by default

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Peter Schiffer <pschiffe@redhat.com> - 10.0.3-1
- resolves: #757687
  update to 10.0.3

* Tue Sep 13 2011 Tom Callaway <spot@fedoraproject.org> - 10.0.2-2
- fix libdir pathing in systemd service file

* Mon Sep 12 2011 Tom Callaway <spot@fedoraproject.org> - 10.0.2-1
- update to 10.0.2
- convert to systemd

* Tue Jun  7 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.1-1
- update to 10.0.1
- remove useles patches

* Wed May  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-4
- close the file descriptor in a special situation in read_uoptime function
- fix the number on open files in cifsiostat output

* Mon May  2 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-3
- add -h optioon to iostat tool
  (-h   Make the disk stats report easier to read by a human.)

* Mon Apr  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-2
- remove unnecessary patch

* Mon Apr  4 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 10.0.0-1
- update to 10.0.0
  remove obsolete patches
  remove autoreconfiguration

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-13
- Resolves: #642280
  sar -u overflow problem - thanks Michal Srb

* Thu Oct  7 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-12
- improve sar thickless kernel support
  (fix the output per separate cpu "-P ALL" option )

* Mon Oct  4 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-11
- resolves: #635646
  test the output of localtime properly

* Wed Sep 29 2010 jkeating - 9.0.6.1-10
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-9
- add the mandir patch
- add the possibility to sed sadc cron options

* Tue Sep 21 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-8
- add necessary dependency (autoconf), necessary because of patch7

* Tue Sep 21 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-7
- remove needless DOCDIR setting
- remove needless INIT_DIR setting
- fix the problem with --disable-man-group option

* Wed Sep  8 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-6
- fix the sar output on tickless kernel

* Fri Aug 13 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-5
- remove bogus links description

* Mon Jul 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-4
- fix sar problem - sysstat can not monitor system status every second

* Mon Apr 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-3
- fix mpstat tool (when the cpu is switched off)

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-2
- fix the mpstat output on tickless kernel

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6.1-1
- update to 9.0.6.1

* Tue Feb 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6-3
- fix init script format

* Fri Dec 11 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.6-2
- fix the problem in get_nfs_mount_nr function
  ( iostat -n causes stack smashing)

* Wed Dec  2 2009 Ivana Hutarva Varekova <varekova@redhat.com> - 9.0.6-1
- update to 9.0.6

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-4
- fix init script

* Mon Sep 14 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-3
- fix init script - add INIT INFO flags (#522740)
  and add condrestart, try-restart and force-reload (#522743)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-1
- update to 9.0.4

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 9.0.3-1
- update to 9.0.3
- remove obsolete patches

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-6
- add /proc/diskstats reading patch

* Mon Sep 22 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-5
- Resolves: #463066 - Fix Patch0:/%%patch mismatch

* Wed Apr 23 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-4
- Resolves: #442801 mpstat shows one extra cpu
  thanks Chris Wright

* Thu Mar  6 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-3
- add nfs extended statistic to iostat command

* Thu Feb 28 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-2
- retry write functuon in sadc command - thanks Tomas Mraz

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-1
- updated to 8.0.4

* Mon Dec  3 2007 Ivana Varekova <varekova@redhat.com> - 8.0.3-1
- updated to 8.0.3

* Fri Nov  9 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-3
- used macros instead of var, etc

* Thu Nov  8 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-2
- change license tag
- remove sysstat.crond source (add -d)
- remove obsolete sysconfig file
- spec file cleanup

* Mon Nov  5 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-1
- update 8.0.2
- spec file cleanup

* Wed Oct 24 2007 Ivana Varekova <varekova@redhat.com> - 8.0.1-2
- remove useless patches

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 8.0.1-1
- update to 8.0.1
- remove useless patches
- spec file cleanup
- remove smp build flag (ar problem)
- add libdir flags

* Wed Aug 15 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-3
- fix cve-2007-3852 -
  sysstat insecure temporary file usage

* Fri Mar 23 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-2
- fix sa2 problem (sa2 works wrong when the /var/log/sa file is
  a link to another directory)

* Mon Feb 12 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-1
- update to 7.0.4
- spec file cleanup

* Tue Jan 30 2007 Ivana Varekova <varekova@redhat.com> - 7.0.3-3
- remove -s flag

* Mon Dec 18 2006 Ivana Varekova <varekova@redhat.com> - 7.0.3-1
- update to 7.0.3

* Tue Nov 21 2006 Ivana Varekova <varekova@redhat.com> - 7.0.2-3
- update NFS mount statistic patch

* Wed Nov  8 2006 Ivana Varekova <varekova@redhat.com> - 7.0.2-1
- update to 7.0.2

* Thu Oct 26 2006 Ivana Varekova <varekova@redhat.com> - 7.0.0-3
- move tmp file (#208433)

* Mon Oct  9 2006 Ivana Varekova <varekova@redhat.com> - 7.0.0-2
- add NFS mount statistic (#184321)

* Fri Jul 14 2006 Marcela Maslanova <mmaslano@redhat.com> - 7.0.0-1
- new version 7.0.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.2-2.1
- rebuild

* Mon Jun  5 2006 Jesse Keating <jkeating@redhat.com> 6.0.2-2
- Add missing BR of gettext

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> 6.0.2-1
- update to 6.0.2
- remove asm/page.h used sysconf command to get PAGE_SIZE

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.0.1-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.0.1-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct 11 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-3
- add FAQ to documentation (bug 170158)

* Mon Oct 10 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-2
- fix chkconfig problem

* Fri Oct  7 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-1
- version 6.0.1

* Thu Aug 18 2005 Florian La Roche <laroche@redhat.com>
- no need to kernel kernel 2.2 or newer anymore

* Tue May 10 2005 Ivana Varekova <varekova@redhat.com> 5.0.5-10.fc
- add debug files to debug_package

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 5.0.5-9.fc
- rebuilt (add gcc4fix, update lib64ini)

* Fri Mar  4 2005 Ivana Varekova <varekova@redhat.ccm> 5.0.5-7.fc
- rebuilt

