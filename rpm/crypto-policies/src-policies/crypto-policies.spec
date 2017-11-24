%global git_date 20171115
%global git_commit_hash 921600e
%global aname crypto-policies

Name:           crypto-policies
Version:        %{git_date}
Release:        1.git%{git_commit_hash}%{?dist}
Summary:        Crypto policies package for Fedora

License:        LGPLv2+
URL:            https://github.com/nmav/fedora-crypto-policies

# This is a tarball of the git repository without the .git/
# directory.
Source0:        crypto-policies-git%{git_commit_hash}.tar.gz
Source1:	config

BuildArch: noarch
BuildRequires: asciidoc
BuildRequires: libxslt
BuildRequires: openssl
BuildRequires: gnutls-utils
BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: bind
BuildRequires: perl
BuildRequires: perl-generators
BuildRequires: perl(File::pushd), perl(File::Temp), perl(File::Copy)

# used by crypto-update-policies
Requires: coreutils
Requires: grep
Requires: sed
Requires(post): coreutils
Requires(post): grep
Requires(post): sed

%description
This package provides update-crypto-policies, which is a tool that sets
the policy applicable for the various cryptographic back-ends, such as
SSL/TLS libraries. The policy set by the tool will be the default policy
used by these back-ends unless the application user configures them otherwise.
https://fedoraproject.org/wiki/Changes/CryptoPolicy


%prep
%setup -q -n %{aname}


%build
make %{?_smp_mflags} update-crypto-policies.8

%install
mkdir -p -m 755 %{buildroot}%{_datarootdir}/crypto-policies/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/local.d/
mkdir -p -m 755 %{buildroot}%{_mandir}/man8
mkdir -p -m 755 %{buildroot}%{_bindir}

make DESTDIR=%{buildroot} DIR=%{_datarootdir}/crypto-policies MANDIR=%{_mandir}/man8 %{?_smp_mflags} install
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/crypto-policies/config

%check
#make check %{?_smp_mflags}

%post
%{_bindir}/update-crypto-policies --no-check >/dev/null


%files
%defattr(-,root,root,-)

%dir %{_sysconfdir}/crypto-policies/
%dir %{_sysconfdir}/crypto-policies/back-ends/
%dir %{_sysconfdir}/crypto-policies/local.d/
%dir %{_datarootdir}/crypto-policies/

%config(noreplace) %{_sysconfdir}/crypto-policies/config

%ghost %{_sysconfdir}/crypto-policies/back-ends/gnutls.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/gnutls28.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openssl.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openssh.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/nss.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/bind.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/java.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/krb5.config
%ghost %{_sysconfdir}/crypto-policies/back-ends/openjdk.config

%{_bindir}/update-crypto-policies
%{_mandir}/man8/update-crypto-policies.8.gz
%{_datarootdir}/crypto-policies/LEGACY/*
%{_datarootdir}/crypto-policies/DEFAULT/*
%{_datarootdir}/crypto-policies/FUTURE/*
%{_datarootdir}/crypto-policies/EMPTY/*
%{_datarootdir}/crypto-policies/default-config
%{_datarootdir}/crypto-policies/reload-cmds.sh

%{!?_licensedir:%global license %%doc}
%license COPYING.LESSER

%changelog
* Sat Apr 01 2017 Björn Esser <besser82@fedoraproject.org> - 20170330-3.git55b66da
- Add Requires for update-crypto-policies in %%post

* Fri Mar 31 2017 Petr Šabata <contyk@redhat.com> - 20170330-2.git55b66da
- update-crypto-policies uses gred and sed, require them

* Thu Mar 30 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170330-1-git55b66da
- GnuTLS policies include RC4 in legacy mode (#1437213)

* Fri Feb 17 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160214-2-gitf3018dd
- Added openssh file

* Tue Feb 14 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160214-1-gitf3018dd
- Updated policies for BIND to address #1421875

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161111-2.gita2363ce
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20161111-1-gita2363ce
- Include OpenJDK documentation.

* Tue Sep 27 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160926-2-git08b5501
- Improved messages on error.

* Mon Sep 26 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160926-1-git08b5501
- Added support for openssh client policy

* Wed Sep 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160921-1-git75b9b04
- Updated with latest upstream.

* Thu Jul 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-2-gitdb5ca59
- Added support for administrator overrides in generated policies in local.d

* Thu Jul 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-1-git340cb69
- Fixed NSS policy generation to include allowed hash algorithms

* Wed Jul 20 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-1-gitcaa4a8d
- Updated to new version with auto-generated policies

* Mon May 16 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160516-1-git8f69c35
- Generate policies for NSS
- OpenJDK policies were updated for opendjk 8

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151104-2.gitf1cba5f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151104-1-gitcf1cba5f
- Generate policies for compat-gnutls28 (#1277790)

* Fri Oct 23 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151005-2-gitc8452f8
- Generated files are put in a %ghost directive

* Mon Oct  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151005-1-gitc8452f8
- Updated policies from upstream
- Added support for the generation of libkrb5 policy
- Added support for the generation of openjdk policy

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150518-2.gitffe885e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150518-1-gitffe885e
- Updated policies to remove SSL 3.0 and RC4 (#1220679)

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-3-git2eeb03b
- Added make check

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-2-git44afaa1
- Removed support for SECLEVEL (#1199274)

* Thu Mar  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-1-git098a8a6
- Include AEAD ciphersuites in gnutls (#1198979)

* Sun Jan 25 2015 Peter Robinson <pbrobinson@fedoraproject.org> 20150115-3-git9ef7493
- Bump release so lastest git snapshot is newer NVR

* Thu Jan 15 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150115-2-git9ef7493
- Updated to newest upstream version.
- Includes bind policies (#1179925)

* Tue Dec 16 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-2-gitd4aa178
- Corrected typo in gnutls' future policy (#1173886)

* Mon Nov 24 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-1-gitd4aa178
- re-enable SSL 3.0 (until its removal is coordinated with a Fedora change request)

* Thu Nov 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141120-1-git9a26a5b
- disable SSL 3.0 (doesn't work in openssl)

* Fri Sep 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140905-1-git4649b7d
- enforce the acceptable TLS versions in openssl

* Wed Aug 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140827-1-git4e06f1d
- fix issue with RC4 being disabled in DEFAULT settings for openssl

* Thu Aug 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140814-1-git80e1e98
- fix issue in post script run on upgrade (#1130074)

* Tue Aug 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140812-1-gitb914bfd
- updated crypto-policies from repository

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 20140708-2-git3a7ae3f
- fix license handling

* Tue Jul 08 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140708-1-git3a7ae3f
- updated crypto-policies from repository

* Fri Jun 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140620-1-gitdac1524
- updated crypto-policies from repository
- changed versioning

* Thu Jun 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-7-20140612gita2fa0c6
- updated crypto-policies from repository

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7.20140522gita50bad2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-6-20140522gita50bad2
- Require(post) coreutils (#1100335).

* Tue May 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-5-20140522gita50bad2
- Require coreutils.

* Thu May 22 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-4-20140522gita50bad2
- Install the default configuration file.

* Wed May 21 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-3-20140520git81364e4
- Run update-crypto-policies after installation.

* Tue May 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-2-20140520git81364e4
- Updated spec based on comments by Petr Lautrbach.

* Mon May 19 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-1-20140519gitf15621a
- Initial package build

