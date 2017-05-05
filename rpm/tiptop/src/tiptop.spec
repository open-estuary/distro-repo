Name:           tiptop
Version:   2.3
Release:        3%{?dist}
Summary:        Performance monitoring tool based on hardware counters
License:        GPLv2

URL:            http://tiptop.gforge.inria.fr/
Source0:        http://tiptop.gforge.inria.fr/releases/tiptop-%{version}.tar.gz

# BZ 1141338
#Patch0:         tiptop-sigfpe.patch

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  hostname
BuildRequires:  libxml2-devel
BuildRequires:  ncurses-devel

%description
Hardware performance monitoring counters have recently received a lot of
attention. They have been used by diverse communities to understand and
improve the quality of computing systems: For example, architects use them to
extract application characteristics and propose new hardware mechanisms;
compiler writers study how generated code behaves on particular hardware;
software developers identify critical regions of their applications and
evaluate design choices to select the best performing implementation. We
propose that counters be used by all categories of users, in particular
non-experts, and we advocate that a few simple metrics derived from these
counters are relevant and useful. For example, a low IPC (number of executed
instructions per cycle) indicates that the hardware is not performing at its
best; a high cache miss ratio can suggest several causes, such as conflicts
between processes in a multicore environment.

Tiptop is a performance monitoring tool for Linux. It provides a dynamic
real-time view of the tasks running in the system. Tiptop is very similar to
the top utility, but most of the information displayed comes from hardware
counters.

%prep
%setup -q
#%patch0 -p1

%build
%configure
%make_build

%install
%make_install

%files
%doc AUTHORS README tiptoprc
%license COPYING
%{_bindir}/*tiptop
%{_mandir}/man1/*tiptop.1*

%changelog
* Sat Feb 11 2017 Dridi Boukelmoune <dridi@fedoraproject.org> - 2.3-3
- Patch for BZ 1141338

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 08 2015 Christopher Meng <rpm@cicku.me> - 2.3-1
- Update to 2.3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Oct  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.2-3
- Add patch to support aarch64

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Christopher Meng <rpm@cicku.me> - 2.2-1
- Update to 2.2

* Sat Nov 10 2012 Christopher Meng <rpm@cicku.me> - 2.1-1
- Initial Package.
