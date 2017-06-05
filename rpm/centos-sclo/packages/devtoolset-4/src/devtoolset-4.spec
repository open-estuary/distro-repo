%global scl devtoolset-4
%scl_package %scl
%global dfcommit 51560a33b6e3e429b807bcb3e4423415c43b5bb5
%global dfshortcommit %(c=%{dfcommit}; echo ${c:0:7})
%global dockerfiledir %{_datadir}/%{scl_prefix}dockerfiles

Summary: Package that installs %scl
Name: %scl_name
Version: 4.0
Release: 9%{?dist}
License: GPLv2+
Group: Applications/File
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/sclorg/rhscl-dockerfiles/archive/%{dfcommit}/rhscl-dockerfiles-%{dfshortcommit}.tar.gz
Source1: README

# The base package must require everything in the collection
Requires: %{scl_prefix}toolchain %{scl_prefix}ide %{scl_prefix}perftools
Obsoletes: %{name} < %{version}-%{release}

BuildRequires: scl-utils-build >= 20120927-11
BuildRequires: iso-codes
BuildRequires: help2man

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Group: Applications/File
Requires: scl-utils >= 20120927-11
Obsoletes: %{name}-runtime < %{version}-%{release}
Requires: libsemanage-static
Requires(post): libselinux policycoreutils-python
Requires(postun): libselinux policycoreutils-python
Requires(preun): libselinux policycoreutils-python

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: scl-utils-build >= 20120927-11
Obsoletes: %{name}-build < %{version}-%{release}
# Java stuff has build-time requirements on these SCLs,
# which are only available for x86_64 arch
%ifarch x86_64
Requires: rh-java-common-scldevel >= 1.1-12
Requires: maven30-scldevel >= 1.1-7
%endif

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package toolchain
Summary: Package shipping basic toolchain applications
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}gcc %{scl_prefix}gcc-c++ %{scl_prefix}gcc-gfortran
Requires: %{scl_prefix}binutils %{scl_prefix}gdb %{scl_prefix}strace
Requires: %{scl_prefix}dwz %{scl_prefix}elfutils %{scl_prefix}memstomp
Requires: %{scl_prefix}ltrace
Obsoletes: %{name}-toolchain < %{version}-%{release}

%description toolchain
Package shipping basic toolchain applications (compiler, debugger, ...)

%package ide
Summary: Package shipping Eclipse IDE
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}eclipse-cdt
Requires: %{scl_prefix}eclipse-cdt-docker
Requires: %{scl_prefix}eclipse-cdt-parsers
Requires: %{scl_prefix}eclipse-changelog
Requires: %{scl_prefix}eclipse-egit
Requires: %{scl_prefix}eclipse-egit-mylyn
Requires: %{scl_prefix}eclipse-emf-runtime
Requires: %{scl_prefix}eclipse-gcov
Requires: %{scl_prefix}eclipse-gef
Requires: %{scl_prefix}eclipse-gprof
Requires: %{scl_prefix}eclipse-jdt
Requires: %{scl_prefix}eclipse-jgit
Requires: %{scl_prefix}eclipse-linuxtools
Requires: %{scl_prefix}eclipse-linuxtools-docker
Requires: %{scl_prefix}eclipse-linuxtools-javadocs
Requires: %{scl_prefix}eclipse-linuxtools-libhover
Requires: %{scl_prefix}eclipse-manpage
Requires: %{scl_prefix}eclipse-mylyn
Requires: %{scl_prefix}eclipse-mylyn-builds
Requires: %{scl_prefix}eclipse-mylyn-builds-hudson
Requires: %{scl_prefix}eclipse-mylyn-context-cdt
Requires: %{scl_prefix}eclipse-mylyn-context-java
Requires: %{scl_prefix}eclipse-mylyn-context-pde
Requires: %{scl_prefix}eclipse-mylyn-docs-epub
Requires: %{scl_prefix}eclipse-mylyn-docs-wikitext
Requires: %{scl_prefix}eclipse-mylyn-tasks-bugzilla
Requires: %{scl_prefix}eclipse-mylyn-tasks-trac
Requires: %{scl_prefix}eclipse-mylyn-tasks-web
Requires: %{scl_prefix}eclipse-mylyn-versions
Requires: %{scl_prefix}eclipse-mylyn-versions-cvs
Requires: %{scl_prefix}eclipse-mylyn-versions-git
Requires: %{scl_prefix}eclipse-oprofile
Requires: %{scl_prefix}eclipse-p2-discovery
Requires: %{scl_prefix}eclipse-pde
Requires: %{scl_prefix}eclipse-perf
Requires: %{scl_prefix}eclipse-platform
Requires: %{scl_prefix}eclipse-ptp
Requires: %{scl_prefix}eclipse-ptp-master
Requires: %{scl_prefix}eclipse-ptp-rm-contrib
Requires: %{scl_prefix}eclipse-ptp-sci
Requires: %{scl_prefix}eclipse-ptp-sdm
Requires: %{scl_prefix}eclipse-pydev
Requires: %{scl_prefix}eclipse-pydev-mylyn
Requires: %{scl_prefix}eclipse-remote
Requires: %{scl_prefix}eclipse-rpm-editor
Requires: %{scl_prefix}eclipse-rse
Requires: %{scl_prefix}eclipse-rse-server
Requires: %{scl_prefix}eclipse-systemtap
Requires: %{scl_prefix}eclipse-tm-terminal
Requires: %{scl_prefix}eclipse-valgrind
Obsoletes: %{name}-ide < %{version}-%{release}

%description ide
Package shipping Eclipse IDE

%package perftools
Summary: Package shipping performance tools
Group: Applications/File
Requires: %{scl_prefix}runtime
Requires: %{scl_prefix}oprofile %{scl_prefix}systemtap %{scl_prefix}valgrind
Requires: %{scl_prefix}dyninst
Obsoletes: %{name}-perftools < %{version}-%{release}

%description perftools
Package shipping performance tools (systemtap, oprofile)

%package dockerfiles
Summary: Package shipping Dockerfiles for Developer Toolset
Group: Applications/File

%description dockerfiles
This package provides a set of example Dockerfiles that can be used
with Red Hat Developer Toolset.  Use these examples to stand up
test environments using the Docker container engine.

%prep
%setup -c

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat <<'EOF' | tee README
%{expand:%(cat %{SOURCE1})}
EOF

%build

# Temporary helper script used by help2man.
cat <<\EOF | tee h2m_helper
#!/bin/sh
if [ "$1" = "--version" ]; then
  printf '%%s' "%{?scl_name} %{version} Software Collection"
else
  cat README
fi
EOF
chmod a+x h2m_helper
# Generate the man page.
help2man -N --section 7 ./h2m_helper -o %{?scl_name}.7

# Enable collection script
# ========================
cat <<EOF >enable
# The IDE part of this collection has a runtime dependency on
# the java-common collection, so enable it if present
if test -e /opt/rh/rh-java-common/enable ; then
  . scl_source enable rh-java-common
fi

# General environment variables
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export INFOPATH=%{_infodir}\${INFOPATH:+:\${INFOPATH}}

# Needed by Java Packages Tools to locate java.conf
export JAVACONFDIRS="%{_sysconfdir}/java:\${JAVACONFDIRS:-/etc/java}"

# Required by XMvn to locate its configuration files
export XDG_CONFIG_DIRS="%{_sysconfdir}/xdg:\${XDG_CONFIG_DIRS:-/etc/xdg}"
export XDG_DATA_DIRS="%{_datadir}:\${XDG_DATA_DIRS:+\${XDG_DATADIRS}:}/usr/local/share:/usr/share"

export PCP_DIR=%{_scl_root}
# Some perl Ext::MakeMaker versions install things under /usr/lib/perl5
# even though the system otherwise would go to /usr/lib64/perl5.
export PERL5LIB=%{_scl_root}/%{perl_vendorarch}:%{_scl_root}/usr/lib/perl5:%{_scl_root}/%{perl_vendorlib}\${PERL5LIB:+:\${PERL5LIB}}
# bz847911 workaround:
# we need to evaluate rpm's installed run-time % { _libdir }, not rpmbuild time
# or else /etc/ld.so.conf.d files?
rpmlibdir=\$(rpm --eval "%%{_libdir}")
# bz1017604: On 64-bit hosts, we should include also the 32-bit library path.
if [ "\$rpmlibdir" != "\${rpmlibdir/lib64/}" ]; then
  rpmlibdir32=":%{_scl_root}\${rpmlibdir/lib64/lib}"
fi
export LD_LIBRARY_PATH=%{_scl_root}\$rpmlibdir\$rpmlibdir32\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
# duplicate python site.py logic for sitepackages
pythonvers=`python -c 'import sys; print sys.version[:3]'`
export PYTHONPATH=%{_prefix}/lib64/python\$pythonvers/site-packages:%{_prefix}/lib/python\$pythonvers/site-packages\${PYTHONPATH:+:\${PYTHONPATH}}
EOF

# Sudo script
# ===========
cat <<EOF >sudo
#! /bin/sh
# TODO: parse & pass-through sudo options from \$@
sudo_options="-E"

for arg in "\$@"
do
   case "\$arg" in
    *\'*)
      arg=`echo "\$arg" | sed "s/'/'\\\\\\\\''/g"` ;;
   esac
   cmd_options="\$cmd_options '\$arg'" 
done
exec /usr/bin/sudo \$sudo_options LD_LIBRARY_PATH=\$LD_LIBRARY_PATH PATH=\$PATH scl enable %{scl} "\$cmd_options"
EOF

# " (Fix vim syntax coloring.)

# Java configuration
# ==================
cat <<EOF >java.conf
JAVA_LIBDIR=%{_datadir}/java
JNI_LIBDIR=%{_prefix}/lib/java
JVM_ROOT=%{_prefix}/lib/jvm
EOF

# Ivy configuration
# =================
cat <<EOF >ivysettings.xml
<!-- Ivy configuration file for %{scl} software collection
     Artifact resolution order is:
      1. %{scl} collection
      2. java-common collection
      3. maven30 collection
      4. base operating system
-->
<ivysettings>
  <settings defaultResolver="default"/>
  <resolvers>
    <filesystem name="%{scl}-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="java-common-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="/opt/rh/rh-java-common/root/%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="maven30-public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="/opt/rh/maven30/root/%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <filesystem name="public">
      <ivy pattern="\${ivy.conf.dir}/lib/[module]/apache-ivy-[revision].xml" />
      <artifact pattern="%{_root_datadir}/java/\[artifact].[ext]" />
    </filesystem>
    <chain name="main" dual="true">
      <resolver ref="%{scl}-public"/>
      <resolver ref="java-common-public"/>
      <resolver ref="maven30-public"/>
      <resolver ref="public"/>
    </chain>
  </resolvers>
  <include url="\${ivy.default.settings.dir}/ivysettings-local.xml"/>
  <include url="\${ivy.default.settings.dir}/ivysettings-default-chain.xml"/>
</ivysettings>
EOF

# XMvn configuration
# =================
cat <<EOF >configuration.xml
<?xml version="1.0" encoding="US-ASCII"?>
<!-- XMvn configuration file for %{scl} software collection
     Artifact resolution order is:
      1. %{scl} collection
      2. java-common collection
      3. maven30 collection
      4. base operating system
-->
<configuration xmlns="http://fedorahosted.org/xmvn/CONFIG/2.0.0">
  <resolverSettings>
    <prefixes>
      <prefix>%{_scl_root}</prefix>
      <prefix>/</prefix>
    </prefixes>
    <metadataRepositories>
      <repository>%{_scl_root}/usr/share/maven-metadata</repository>
    </metadataRepositories>
  </resolverSettings>
  <installerSettings>
    <metadataDir>opt/rh/%{scl}/root/usr/share/maven-metadata</metadataDir>
  </installerSettings>
  <repositories>
    <repository>
      <id>resolve-%{scl}</id>
      <type>compound</type>
      <properties>
        <prefix>%{_scl_root}</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>resolve</id>
      <type>compound</type>
      <properties>
        <prefix>/</prefix>
      </properties>
      <configuration>
        <repositories>
	  <!-- Put resolvers in order you want to use them, from
	       highest to lowest preference. (resolve-local is
	       resolver that resolves from local Maven repository in
	       .xm2 in current directory.) -->
          <repository>resolve-local</repository>
          <repository>resolve-%{scl}</repository>
          <repository>resolve-java-common</repository>
          <repository>resolve-maven30</repository>
          <repository>base-resolve</repository>
        </repositories>
      </configuration>
    </repository>
    <repository>
      <id>install</id>
      <type>compound</type>
      <properties>
        <prefix>opt/rh/%{scl}/root</prefix>
        <namespace>%{scl}</namespace>
      </properties>
      <configuration>
        <repositories>
          <repository>base-install</repository>
        </repositories>
      </configuration>
    </repository>
  </repositories>
</configuration>
EOF

%install
(%{scl_install})

mkdir -p %{buildroot}%{_scl_root}/etc/alternatives %{buildroot}%{_scl_root}/var/lib/alternatives

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 enable %{buildroot}%{_scl_scripts}/

install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 sudo %{buildroot}%{_bindir}/

install -d -m 755 %{buildroot}%{_sysconfdir}/java
install -p -m 644 java.conf %{buildroot}%{_sysconfdir}/java/

install -d -m 755 %{buildroot}%{_sysconfdir}/ivy
install -p -m 644 ivysettings.xml %{buildroot}%{_sysconfdir}/ivy/

install -d -m 755 %{buildroot}%{_sysconfdir}/xdg/xmvn
install -p -m 644 configuration.xml %{buildroot}%{_sysconfdir}/xdg/xmvn/

%if 0%{?rhel} >= 7
install -d %{buildroot}%{dockerfiledir}

collections="devtoolset-4 devtoolset-4-toolchain devtoolset-4-dyninst \
             devtoolset-4-elfutils devtoolset-4-oprofile devtoolset-4-systemtap \
             devtoolset-4-valgrind"
install -d -p -m 755 %{buildroot}%{dockerfiledir}/rhel{6,7}
for d in $collections; do
  install -d -p -m 755 %{buildroot}%{dockerfiledir}/rhel{6,7}/$d
  cp -a rhscl-dockerfiles-%{dfcommit}/rhel7.$d/* %{buildroot}%{dockerfiledir}/rhel7/$d
  cp -a rhscl-dockerfiles-%{dfcommit}/rhel6.$d/* %{buildroot}%{dockerfiledir}/rhel6/$d
done

# BZ#1194557: Don't ship systemtap container for RHEL6.
rm -rf %{buildroot}%{dockerfiledir}/rhel6/devtoolset-4-systemtap
%endif

# Install generated man page.
install -d -m 755 %{buildroot}%{_mandir}/man7
install -p -m 644 %{?scl_name}.7 %{buildroot}%{_mandir}/man7/

%files
%doc README
%{_mandir}/man7/%{?scl_name}.*

%files runtime
%scl_files
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_sysconfdir}/selinux-equiv.created
%{_sysconfdir}/ivy
%{_sysconfdir}/java
%dir %{_scl_root}/etc/alternatives

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}*

%files toolchain

%files ide

%files perftools

%if 0%{?rhel} >= 7
%files dockerfiles
%{dockerfiledir}
%endif

%post runtime
if [ ! -f %{_sysconfdir}/selinux-equiv.created ]; then
  /usr/sbin/semanage fcontext -a -e / %{_scl_root}
  restorecon -R %{_scl_root}
  touch %{_sysconfdir}/selinux-equiv.created
fi

%preun runtime
[ $1 = 0 ] && rm -f %{_sysconfdir}/selinux-equiv.created || :

%postun runtime
if [ $1 = 0 ]; then
  /usr/sbin/semanage fcontext -d %{_scl_root}
  [ -d %{_scl_root} ] && restorecon -R %{_scl_root} || :
fi

%changelog
* Mon Oct 26 2015 Marek Polacek <polacek@redhat.com> - 4.0-9
- Ship RHEL6 Dockerfiles on RHEL7 (#1265118)

* Wed Sep 23 2015 Marek Polacek <polacek@redhat.com> - 4.0-8
- Update rhscl-dockerfiles from git (#1265118)

* Tue Sep 22 2015 Marek Polacek <polacek@redhat.com> - 4.0-7
- Update rhscl-dockerfiles from git (#1265236)

* Mon Sep 21 2015 Marek Polacek <polacek@redhat.com> - 4.0-6
- Add man page (#1264277)

* Tue Sep 01 2015 Marek Polacek <polacek@redhat.com> - 4.0-5
- Update rhscl-dockerfiles from git (#1223302)

* Mon Jul 20 2015 Mat Booth <mat.booth@redhat.com> - 4.0-4
- Rebuild for all arches

* Mon Jul 20 2015 Mat Booth <mat.booth@redhat.com> - 4.0-3
- Update IDE requires to include new packages

* Wed Jun 10 2015 Mat Booth <mat.booth@redhat.com> - 4.0-2
- Drop unnecessary Rs on eclipse sdk packages.

* Wed Jun 10 2015 Mat Booth <mat.booth@redhat.com> - 4.0-1
- Initial build for devtoolset-4.

* Thu May 07 2015 Marek Polacek <polacek@redhat.com> - 3.1-12
- Update rhscl-dockerfiles from git (#1194663)

* Wed May 06 2015 Mat Booth <mat.booth@redhat.com> - 3.1-11
- Resolves: rhbz#1218605 - Avoid BR on javapackages-tools

* Wed Apr 15 2015 Marek Polacek <polacek@redhat.com> - 3.1-10
- Bump Release to mollify #1211655

* Wed Apr 8 2015 Marek Polacek <polacek@redhat.com> - 3.1-9
- Add Obsoletes (#1208867)

* Mon Feb 23 2015 Marek Polacek <polacek@redhat.com> - 3.1-8
- Don't ship devtoolset-3-dockerfiles subpackage on RHEL6 (#1194558)

* Fri Feb 20 2015 Marek Polacek <polacek@redhat.com> - 3.1-7
- Don't ship systemtap container for RHEL6 (#1194557)

* Wed Feb 11 2015 Marek Polacek <polacek@redhat.com> - 3.1-6
- Add devtoolset-3-{dyninst,elfutils,valgrind,oprofile,systemtap}
  dockerfiles (#1180659)

* Tue Feb 10 2015 Marek Polacek <polacek@redhat.com> - 3.1-5
- Add devtoolset-3-dockerfiles (#1180657)

* Fri Jan 23 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1-4
- Include root /usr/share and /usr/local/share to prevent gsettings crash.

* Tue Jan 13 2015 Mat Booth <mat.booth@redhat.com> - 3.1-3
- Resolves: rhbz#1178915 - Rebuild to get correct disttag
- Add BR to Fix unexpanded java dir macros in java.conf
- Don't enable maven30 SCL, as recommended by maven30 maintainer

* Wed Jan 07 2015 Mat Booth <mat.booth@redhat.com> - 3.1-2
- Resolves: rhbz#1178915
- Add missing xmvn resolver setting for metadata repo.
- Make package archful to make sure lib64 dirs are owned.
- Only require java-common and maven30 SCLs when on x86_64.

* Thu Dec 18 2014 Mat Booth <mat.booth@redhat.com> - 3.1-1
- Resolves: rhbz#1178915 - Initial build for DTS 3.1
- Add build-time deps on java-common and mvn30 SCLs
- Update xmvn and ivy config for latest javapackages/xmvn
- Fix file listed twice warning for xmvn/config.xml

* Fri Jun 20 2014 Roland Grunberg <rgrunber@redhat.com> - 3.0-16
- Add macro for enablement of osgi auto-{provides,requires}.

* Wed Jun 04 2014 Marek Polacek <polacek@redhat.com> 3.0-15
- Drop the -vc subpackage (#1104342)

* Tue Jun 03 2014 Mat Booth <mat.booth@redhat.com> - 3.0-14
- Prevent premature command substitution (#1102796)

* Tue Jun 03 2014 Marek Polacek <polacek@redhat.com> 3.0-13
- Create alternatives directories (#1101246)

* Tue Jun 03 2014 Mat Booth <mat.booth@redhat.com> - 3.0-12
- Fix MANPATH variable (#1102741)

* Fri May 30 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-11
- Re enable mylyn-docs-epub.

* Tue May 27 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-10
- Comment mylyn-epub as the new version has huge dependency chain.

* Tue May 27 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-9
- Drop eclipse-xsd as it's no longer part of emf.
- Drop eclipse-rpmstubby as it's merged into rpm-editor.

* Wed May 21 2014 Mat Booth <mat.booth@redhat.com> - 3.0-8
- Revert ant_home fix temporarily

* Mon May 19 2014 Marek Polacek <polacek@redhat.com> 3.0-7
- Require ltrace (#1098247, #1098249)
- Properly set ANT_HOME (#1087654)

* Fri May 16 2014 Mat Booth <mat.booth@redhat.com> - 3.0-6
- Drop maven30 collection bits (we can use base OS maven on rhel7)

* Fri May 16 2014 Mat Booth <mat.booth@redhat.com> - 3.0-5
- Require newest version of scl-utils

* Fri May 16 2014 Mat Booth <mat.booth@redhat.com> - 3.0-4
- Conditionally enable maven30 collection
- Add maven scl macros for other packages to use

* Thu May 15 2014 Mat Booth <mat.booth@redhat.com> - 3.0-3
- Add collection-specific maven, java, ivy configuration

* Thu May 15 2014 Alexander Kurtakov <akurtako@redhat.com> 3.0-2
- Build subpackage should R: scl-utils.

* Tue Mar 4 2014 Marek Polacek <polacek@redhat.com> 3.0-1
- Initial package
