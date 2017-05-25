# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
%global soversion 10

# Number of threads to spawn when testing some threading fixes.
%global thread_test_threads %{?threads:%{threads}}%{!?threads:1}

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%global multilib_arches %{ix86} ia64 %{mips} ppc %{power64} s390 s390x sparcv9 sparc64 x86_64 aarch64

%global _performance_build 1

Summary: Compatibility version of the OpenSSL library
Name: compat-openssl10
Version: 1.0.2j
Release: 6%{?dist}
Epoch: 1
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: openssl-%{version}-hobbled.tar.xz
Source1: hobble-openssl
Source2: Makefile.certificate
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source8: openssl-thread-test.c
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
Source11: README.FIPS
Source12: ec_curve.c
Source13: ectest.c
# Build changes
Patch1: openssl-1.0.2e-rpmbuild.patch
Patch2: openssl-1.0.2a-defaults.patch
Patch4: openssl-1.0.2i-enginesdir.patch
Patch5: openssl-1.0.2a-no-rpath.patch
Patch6: openssl-1.0.2a-test-use-localhost.patch
Patch7: openssl-1.0.0-timezone.patch
Patch8: openssl-1.0.1c-perlfind.patch
Patch9: openssl-1.0.1c-aliasing.patch
# Bug fixes
Patch23: openssl-1.0.2c-default-paths.patch
Patch24: openssl-1.0.2a-issuer-hash.patch
# Functionality changes
Patch33: openssl-1.0.0-beta4-ca-dir.patch
Patch34: openssl-1.0.2a-x509.patch
Patch35: openssl-1.0.2a-version-add-engines.patch
Patch39: openssl-1.0.2a-ipv6-apps.patch
Patch40: openssl-1.0.2i-fips.patch
Patch45: openssl-1.0.2a-env-zlib.patch
Patch47: openssl-1.0.2a-readme-warning.patch
Patch49: openssl-1.0.1i-algo-doc.patch
Patch50: openssl-1.0.2a-dtls1-abi.patch
Patch51: openssl-1.0.2a-version.patch
Patch56: openssl-1.0.2a-rsa-x931.patch
Patch58: openssl-1.0.2a-fips-md5-allow.patch
Patch60: openssl-1.0.2a-apps-dgst.patch
Patch63: openssl-1.0.2a-xmpp-starttls.patch
Patch65: openssl-1.0.2i-chil-fixes.patch
Patch66: openssl-1.0.2h-pkgconfig.patch
Patch68: openssl-1.0.2i-secure-getenv.patch
Patch70: openssl-1.0.2a-fips-ec.patch
Patch71: openssl-1.0.2g-manfix.patch
Patch72: openssl-1.0.2a-fips-ctor.patch
Patch73: openssl-1.0.2c-ecc-suiteb.patch
Patch74: openssl-1.0.2a-no-md5-verify.patch
Patch75: openssl-1.0.2a-compat-symbols.patch
Patch76: openssl-1.0.2i-new-fips-reqs.patch
Patch78: openssl-1.0.2a-cc-reqs.patch
Patch90: openssl-1.0.2i-enc-fail.patch
Patch92: openssl-1.0.2a-system-cipherlist.patch
Patch93: openssl-1.0.2g-disable-sslv2v3.patch
Patch94: openssl-1.0.2d-secp256k1.patch
Patch95: openssl-1.0.2e-remove-nistp224.patch
Patch96: openssl-1.0.2e-speed-doc.patch
Patch97: openssl-1.0.2j-nokrb5-abi.patch
# Backported fixes including security fixes
Patch80: openssl-1.0.2e-wrap-pad.patch
Patch81: openssl-1.0.2a-padlock64.patch
Patch82: openssl-1.0.2i-trusted-first-doc.patch

License: OpenSSL
Group: System Environment/Libraries
URL: http://www.openssl.org/
BuildRequires: coreutils, perl, perl-generators, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
Requires: coreutils, make
Requires: crypto-policies
Conflicts: openssl < 1:1.1.0, openssl-libs < 1:1.1.0

%description
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
and is provided for compatibility with previous releases and software
that does not support compilation with OpenSSL-1.1.

%package devel
Summary: Files for development of applications which have to use OpenSSL-1.0.2
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: pkgconfig
# The devel subpackage intentionally conflicts with main openssl-devel
# as simultaneous use of both openssl package cannot be encouraged.
# Making the packages non-conflicting would also require further
# changes in the dependent packages.
Conflicts: openssl-devel

%description devel
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
and is provided for compatibility with previous releases and software
that does not support compilation with OpenSSL-1.1. This package
contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%prep
%setup -q -n openssl-%{version}

# The hobble_openssl is called here redundantly, just to be sure.
# The tarball has already the sources removed.
%{SOURCE1} > /dev/null

cp %{SOURCE12} %{SOURCE13} crypto/ec/

%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .defaults
%patch4 -p1 -b .enginesdir %{?_rawbuild}
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .timezone
%patch8 -p1 -b .perlfind %{?_rawbuild}
%patch9 -p1 -b .aliasing

%patch23 -p1 -b .default-paths
%patch24 -p1 -b .issuer-hash

%patch33 -p1 -b .ca-dir
%patch34 -p1 -b .x509
%patch35 -p1 -b .version-add-engines
%patch39 -p1 -b .ipv6-apps
%patch40 -p1 -b .fips
%patch45 -p1 -b .env-zlib
%patch47 -p1 -b .warning
%patch49 -p1 -b .algo-doc
%patch50 -p1 -b .dtls1-abi
%patch51 -p1 -b .version
%patch56 -p1 -b .x931
%patch58 -p1 -b .md5-allow
%patch60 -p1 -b .dgst
%patch63 -p1 -b .starttls
%patch65 -p1 -b .chil
%patch66 -p1 -b .pkgconfig
%patch68 -p1 -b .secure-getenv
%patch70 -p1 -b .fips-ec
%patch71 -p1 -b .manfix
%patch72 -p1 -b .fips-ctor
%patch73 -p1 -b .suiteb
%patch74 -p1 -b .no-md5-verify
%patch75 -p1 -b .compat
%patch76 -p1 -b .fips-reqs
%patch78 -p1 -b .cc-reqs
%patch90 -p1 -b .enc-fail
%patch92 -p1 -b .system
%patch93 -p1 -b .v2v3
%patch94 -p1 -b .secp256k1
%patch95 -p1 -b .nistp224
%patch96 -p1 -b .speed-doc
%patch97 -p1 -b .nokrb5-abi

%patch80 -p1 -b .wrap
%patch81 -p1 -b .padlock64
%patch82 -p1 -b .trusted-first

sed -i 's/SHLIB_VERSION_NUMBER "1.0.0"/SHLIB_VERSION_NUMBER "%{version}"/' crypto/opensslv.h

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
    sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
    --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
    --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
    zlib sctp enable-camellia enable-seed enable-tlsext enable-rfc3779 \
    enable-cms enable-md2 enable-rc5 \
    no-mdc2 no-ec2m no-gost no-srp no-krb5 \
    --enginesdir=%{_libdir}/openssl/engines \
    shared  ${sslarch} %{?!nofips:fips}

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
make depend
make all

# Generate hashes for the included certs.
make rehash

# Overwrite FIPS README
cp -f %{SOURCE11} .

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

# We must revert patch33 before tests otherwise they will fail
patch -p1 -R < %{PATCH33}

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
make -C test apps tests
%{__cc} -o openssl-thread-test \
    -I./include \
    $RPM_OPT_FLAGS \
    %{SOURCE8} \
    -L. \
    -lssl -lcrypto \
    -lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{version}.hmac \
    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{soversion}.hmac \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs
mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT%{_libdir}/openssl
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
    chmod 755 ${lib}
    ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

# Delete static library
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a || :

# Rename man pages so that they don't conflict with other system man pages.
pushd $RPM_BUILD_ROOT%{_mandir}
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
popd

# Delete non-devel man pages in the compat package
rm -rf $RPM_BUILD_ROOT%{_mandir}/man[157]*

# Delete configuration files
rm -rf  $RPM_BUILD_ROOT%{_sysconfdir}/pki

# Remove binaries
rm -rf $RPM_BUILD_ROOT/%{_bindir}

# Remove engines
rm -rf $RPM_BUILD_ROOT/%{_libdir}/openssl

%files
%license LICENSE
%doc FAQ NEWS README README.FIPS

%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0644,root,root) %{_libdir}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac

%files devel
%doc doc/c-indentation.el doc/openssl.txt CHANGES
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_mandir}/man3*/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%postun -p /sbin/ldconfig

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.2j-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 20 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2j-5
- fix -devel subpackage conflict with man-pages package (#1387175)

* Fri Oct 14 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2j-4
- correct wrong Requires in -devel subpackage

* Fri Oct 14 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2j-3
- add back -devel subpackage as a stop-gap measure for software
  that cannot be ported to new API easily

* Fri Oct  7 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2j-2
- removed Buildroot and clean section
- added Conflicts with old openssl

* Thu Oct  6 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2j-1
- updated to 1.0.2j and modified Summary

* Thu Oct  6 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2i-3
- renamed to compat-openssl10, additional cleanups

* Fri Sep 23 2016 Tomáš Mráz <tmraz@redhat.com> 1.0.2i-2
- compat package created
