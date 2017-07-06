# dont' touch the bazel file!
%define debug_package %{nil}
%define __strip /bin/true

Summary: Build software of any size, quickly and reliably, just as engineers do at Google.
Name: bazel
Version: 0.4.5
Release: 1%{?dist}
License: APL2
Group: Development/Tools
URL: http://bazel.build/
Source:  https://github.com/bazelbuild/bazel/releases/download/0.4.5/bazel-0.4.5-dist.zip
Requires: java-1.8.0-openjdk
BuildRequires: java-1.8.0-openjdk-devel zlib-devel which findutils tar gzip zip unzip
BuildRequires: scl-utils devtoolset-4-gcc devtoolset-4-gcc-c++ devtoolset-4-binutils
# https://gist.github.com/truatpasteurdotfr/d541cd279b9f7bf38ce967aa3743dfcb

Patch0:   aarch64_cpu.patch

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%setup -c -n bazel-0.4.5
%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%build
# rebuilding as regular user needs a higher number process limit...
ulimit -u20480
echo 'bash ./compile.sh' | scl enable devtoolset-4 bash

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m755  output/bazel $RPM_BUILD_ROOT%{_bindir}/bazel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/bazel

%changelog
* Fri Mar 17 2017 Tru Huynh <tru@pasteur.fr> - 0.4.5
- initial build for CentOS-6 which can not use the binary installers at https://github.com/bazelbuild/bazel/releases
  /usr/local/bin/bazel: /lib64/libc.so.6: version `GLIBC_2.14' not found (required by /usr/local/bin/bazel)
