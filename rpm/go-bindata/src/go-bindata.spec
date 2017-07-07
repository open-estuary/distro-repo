%if 0%{?fedora}
%global with_devel 1
%global with_bundled 1
%global with_debug 1
# Some tests fails and it takes a lot of time to investigate
# what is wrong
%global with_check 0
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

#%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
#%endif

%global provider        github
%global provider_tld    com
%global project         jteeuwen
%global repo            go-bindata
# https://github.com/jteeuwen/go-bindata
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          a0ff2567cfb70903282db057e799fd826784d41d
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           go-bindata
Version:        3.0.7
Release:        8.git%{shortcommit}%{?dist}
Summary:        A small utility which generates Go code from any file
License:        MIT
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

This tool converts any file into managable Go source code. Useful for
embedding binary data into a go program. The file data is optionally gzip
compressed before being converted to a raw byte slice.

%prep
%setup -n go-bindata-%{commit}

%build
mkdir -p src/github.com/jteeuwen/
ln -s ../../../ src/github.com/jteeuwen/go-bindata

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gobuild -o bin/go-bindata %{import_path}/go-bindata

%install
install -d -p %{buildroot}%{_bindir}
install -m 755 bin/go-bindata %{buildroot}%{_bindir}/go-bindata

%files
%doc LICENSE README.md
%{_bindir}/go-bindata

%changelog
* Tue Nov 01 2016 jchaloup <jchaloup@redhat.com> - 3.0.7-8.gita0ff256
- restore supported architectures
  related: #1390114

* Mon Oct 31 2016 jchaloup <jchaloup@redhat.com> - 3.0.7-7.gita0ff256
- Bump to upstream a0ff2567cfb70903282db057e799fd826784d41d
  resolves: #1390114

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-6.gitf94581b
- https://fedoraproject.org/wiki/Changes/golang1.7

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-5.gitf94581b
- https://fedoraproject.org/wiki/Changes/golang1.6

* Thu Feb  4 2016 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.7-4.gitf94581b
- Use golang arches macro

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-3.gitf94581b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.7-2.gitf94581b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.git79847ab
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.git79847ab
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com>  0-0.4.git79847ab
- buildrequires golang

* Mon Oct 14 2013 Lokesh Mandvekar <lsm5@redhat.com>  0-0.3.git79847ab
- package name change to go-bindata

* Mon Oct 14 2013 Lokesh Mandvekar <lsm5@redhat.com>  0-0.2.git79847ab
- defattr removed
- only go-bindata installed, no devel package

* Sat Oct 12 2013 Lokesh Mandvekar <lsm5@redhat.com>  0-0.1.git79847ab
- Initial fedora package
