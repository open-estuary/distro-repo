Name:             weighttp
Summary:          Small tool to benchmark webservers
License:          MIT
URL:              http://redmine.lighttpd.net/projects/weighttp/

Version:          0.4
Release:          8%{?dist}

# Upstream doesn't release tarballs, so I created this one:
#     $ git clone git://git.lighttpd.net/weighttp && cd weighttp
#     $ git archive --format=tar --prefix=weighttp-0.3/ 1bdbe40 | xz -z > weighttp-0.3.tar.xz
#
# I use this specific git commit because it is the one for the 0.3 version.
# Unfortunately, upstream didn't tag it, even though they tagged v0.1 and v0.2
Source0:          %{name}-%{version}.tar.gz

BuildRequires:    libev-devel

# The build uses a bundled copy of waf, which requires python. If we ever
# start using the Fedora waf package instead, this will come in implictly.
BuildRequires:    python

%description
weighttp (pronounced weighty) is a lightweight and small benchmarking tool for
webservers.

It was designed to be very fast and easy to use and only supports a tiny
fraction of the HTTP protocol in order to be lean and simple.

weighttp supports multithreading to make good use of modern CPUs with multiple
cores as well as asynchronous i/o for concurrent requests within a single
thread.

For event handling, weighty relies on libev which fits the design perfectly,
being lightweight and fast itself. Thanks to that, weighty supports all modern
high-performance event interfaces like epoll or kqueue, that the major OSs
provide.


%prep
%setup -q -n %{name}-%{name}-%{version} 

%build
export CFLAGS="%{optflags}"

# The bundled waf script seems to be 1.5.9, and the wscript was written for
# this version. It doesn't work any more with the waf version packaged in
# Fedora, as it is much more recent and the waf API changed since then.
# Using the Fedora waf package would require significant changes to the
# upstream wscript, so we use the bundled one for now.
./waf configure --prefix=%{_prefix}
./waf build %{?_smp_mflags}


%install
./waf install --destdir=%{buildroot}


%files
%doc COPYING
%{_bindir}/%{name}


%changelog
* Mon Jul 31 2017 Open-Estuary <sjtuhjh@hotmail.com> 0.4
- Build 0.4 for ARM64 platform

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 0.3-6
- Drop our downstream patch, libev headers were moved back to where upstream
  intended them to be.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 0.3-3
- Add missing build requirement on Python.

* Mon Oct 15 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 0.3-2
- Added a comment to explain why we use the bundled waf, based on Eduardo's
  review feedback.

* Mon Oct 08 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 0.3-1
- Initial package for Fedora.
