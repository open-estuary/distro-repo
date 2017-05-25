Name:           AliSQL
Version:   5.6.32
Release:        5%{?dist}
Summary:        AliSQL

Group:          Applications/Databases
License:        GPL
URL:            https://github.com/alibaba/AliSQL
Source0:        %{name}-%{version}-5.tar.gz
Source1:        mysql-systemd-start
Source2:        mysqld.service
Source3:        mysql.conf
Source4:        my_config.h
Source5:        my.cnf

Patch0:         alisql_epoll_sub_aarch64.patch
Patch1:         alisql_innodb_memcache_handler_api_aarch64.patch

BuildRequires:  gcc gcc-c++
BuildRequires:  cmake
BuildRequires:  libaio-devel
BuildRequires:  numactl-devel
BuildRequires:  systemd
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
Requires:       ncurses-devel 
Requires:       bison 
Requires:       perl
Requires:       openssl-devel

%define MYSQL_USER mysql
%define MYSQL_GROUP mysql
%define mysqldatadir /var/lib/mysql

%global ssl_option -DWITH_SSL=yes
%global systemd     1
%global nodebuginfo 1
%global src_dir     %{name}-%{name}-%{version}-5

%description   
AliSQL is a MySQL branch originated from Alibaba Group. It is based on the MySQL official release and has many feature and performance enhancements. AliSQL has proven to be very stable and efficient in production environment. It can be used as a free, fully compatible, enhanced and open source drop-in replacement for MySQL.
The %{name}-devel package contains libraries and header files for developing applications that use %{name}.

%package        server
Summary:        AliSQL database server
Group:          Applications/Databases
Requires:       coreutils
Requires:       grep
Requires:       procps
Requires:       net-tools
Requires:       perl
Obsoletes:      MySQL-community-server
Obsoletes:      mariadb-server
Obsoletes:      mariadb-galera-server
Provides:       AliSQL-server = %{version}-%{release}
Requires:       AliSQL-client = %{version}-%{release}
Requires:       AliSQL-common = %{version}-%{release}
Obsoletes:      AliSQL-server < %{version}-%{release}
Obsoletes:      AliSQL-client < %{version}-%{release}
Conflicts:      otherproviders(mysqld)
Conflicts:      otherproviders(mysql)
Conflicts:      otherproviders(mysql-debug)

%description    server
AliSQL is a MySQL branch originated from Alibaba Group. It is based on the MySQL official release and has many feature and performance enhancements. AliSQL has proven to be very stable and efficient in production environment. It can be used as a free, fully compatible, enhanced and open source drop-in replacement for MySQL.
The %{name}-devel package contains libraries and header files for developing applications that use %{name}.

%package        client
Summary:        MySQL database client applications and tools
Group:          Applications/Databases
Provides:       AliSQL-client = %{version}-%{release}
Obsoletes:      AliSQL-client < %{version}-%{release}
Requires:       AliSQL-libs = %{version}-%{release}
Obsoletes:      MySQL-client-advanced
Obsoletes:      mysql-community-client
Obsoletes:      mariadb
Conflicts:      otherproviders(mysql-client)

%description    client
This package contains the standard MySQL clients and administration
tools.

%package        common
Summary:        AliSQL database common files for server and client libs
Group:          Applications/Databases
Provides:       AliSQL-common = %{version}-%{release}
Obsoletes:      AliSQL-common < %{version}-%{release}
Obsoletes:      mysql-common

%description    common
This packages contains common files needed by MySQL client library, and MySQL database server.

%package        devel
Summary:        Development header files and libraries for MySQL database client applications
Group:          Applications/Databases
Provides:       AliSQL-devel = %{version}-%{release}
Requires:       AliSQL-libs = %{version}-%{release}
Obsoletes:      AliSQL-devel < %{version}-%{release}
Obsoletes:      mysql-devel 
Obsoletes:      mariadb-devel
Obsoletes:      libmysqlclient-devel
Conflicts:      mysql-connector-c-devel < 6.2

%description    devel
AliSQL development package which contains the development header files and libraries necessary
to develop AliSQL client applications.

%package        bench
Summary:        MySQL benchmark suite
Group:          Applications/Databases
Requires:       AliSQL-server = %{version}-%{release}
Obsoletes:      mariadb-bench
Obsoletes:      community-mysql-bench
Obsoletes:      mysql-bench 
Provides:       AliSQL-bench = %{version}-%{release}
Obsoletes:      AliSQL-bench < %{version}-%{release}
Conflicts:      mysql-community-bench 

%description    bench
AliSQL benchmakr suites which contains the MySQL Benchmark Suite for MySQL database
server.

%package        libs
Summary:        Shared libraries for MySQL database client applications
Group:          Applications/Databases
Provides:       AliSQL-libs = %{version}-%{release}
Requires:       AliSQL-common = %{version}-%{release}
Obsoletes:      AliSQL-libs < %{version}-%{release}
Obsoletes:      mysql-community-libs 
Obsoletes:      mariadb-libs
Obsoletes:      libmysqlclient18 < %{version}-%{release}
Obsoletes:      libmysqlclient_r18 < %{version}-%{release}
Provides:       libmysqlclient18 = %{version}-%{release}
Provides:       libmysqlclient_r18 = %{version}-%{release}
Conflicts:      mysql-connector-c-shared < 6.2
Conflicts:      mysql-community-libs
Conflicts:      mariadb-libs

%description    libs
AliSQL libs which contains the shared libraries for MySQL client applications.

%prep
%setup -q -n %{src_dir}
%patch0 -p1
%patch1 -p1

%build
cd BUILD
sh autorun.sh
cd ..
mkdir build
cd build
cmake .. -DBUILD_CONFIG=mysql_release \
         -DINSTALL_LAYOUT=RPM \
         -DCMAKE_BUILD_TYPE=RelWithDebInfo \
         -DINSTALL_LIBDIR="%{_lib}/mysql" \
         -DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
         -DINSTALL_SQLBENCHDIR=share \
         -DMYSQL_UNIX_ADDR="%{mysqldatadir}/mysql.sock" \
         %{ssl_option} \
         -DDEFAULT_CHARSET=utf8   \
         -DDEFAULT_COLLATION=utf8_general_ci \
         -DWITH_INNOBASE_STORAGE_ENGINE=1 \
         -DWITH_ARCHIVE_STORAGE_ENGINE=1 \
         -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
         -DWITH_INNODB_MEMCACHED=1 \
         -DWITH_EMBEDDED_SERVER=0 \
         -DMYSQL_TCP_PORT=3306 \

echo BEGIN_NORMAL_CONFIG ; egrep '^#define' include/config.h ; echo END_NORMAL_CONFIG
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# Ensure that needed directories exists
install -d -m 0755 %{buildroot}/var/lib/mysql
install -d -m 0755 %{buildroot}/var/run/mysqld
install -d -m 0755 %{buildroot}/var/tmp/mysql
install -d -m 0750 %{buildroot}/var/log/mysql

MBD=$RPM_BUILD_DIR/%{src_dir}
cd build
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

install -D -m 0644 $MBD/build/support-files/mysql-log-rotate %{buildroot}%{_sysconfdir}/logrotate.d/mysql
install -D -m 0644 $MBD/build/packaging/rpm-oel/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
install -d %{buildroot}%{_sysconfdir}/my.cnf.d
install -d -m 0755 %{buildroot}%{_datadir}/mysql/SELinux/RHEL4
install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/mysql-systemd-start
install -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/mysqld.service
install -D -m 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/tmpfiles.d/mysql.conf
install -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}

install -d -m 0755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/mysql" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/mysql-%{_arch}.conf

# multiarch support
mv %{buildroot}/%{_includedir}/mysql/my_config.h \
   %{buildroot}/%{_includedir}/mysql/my_config_%{_arch}.h
install -p -m 0644 %{SOURCE4} %{buildroot}/%{_includedir}/mysql/my_config.h
install -p -m 0755 %{SOURCE5} %{buildroot}/%{_bindir}/mysql_config

# Install SELinux files in datadir
install -m 0644 $MBD/support-files/RHEL4-SElinux/mysql.{fc,te} \
    %{buildroot}%{_datadir}/mysql/SELinux/RHEL4

# Remove files pages we explicitly do not want to package
rm -rf %{buildroot}%{_infodir}/mysql.info*
rm -rf %{buildroot}%{_datadir}/mysql/binary-configure
rm -rf %{buildroot}%{_datadir}/mysql/mysql.server
rm -rf %{buildroot}%{_datadir}/mysql/mysqld_multi.server
rm -rf %{buildroot}%{_sysconfdir}/init.d/mysql
rm -rf %{buildroot}%{_bindir}/mysql_embedded
rm -rf %{buildroot}%{_bindir}/mysql_setpermission
rm -rf %{buildroot}%{_mandir}/man1/mysql_setpermission.1*
rm -f %{buildroot}%{_datadir}/mysql/win_install_firewall.sql

rm -fr %{buildroot}/usr/share/mysql-test
rm -fr %{buildroot}/usr/bin/mysql_client_test

# rcmysql symlink
#install -d %{buildroot}%{_sbindir}
#ln -sf %{_sbindir}/service %{buildroot}%{_sbindir}/rcmysql

%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd  -M %{!?el5:-N} -g mysql -o -r -d /var/lib/mysql -s /bin/bash \
    -c "AliSQL Server" -u 27 mysql >/dev/null 2>&1 || :

#%clean server
#rm -rf $RPM_BUILD_ROOT

%post server
datadir=$(/usr/bin/my_print_defaults server mysqld | grep '^--datadir=' | sed -n 's/--datadir=//p' | tail -n 1)
/bin/chmod 0755 "$datadir" > /dev/null 2&1 || :
/bin/touch /var/log/mysql/mysqld.log > /dev/null 2&1 || :
/bin/chown mysql:mysql /var/log/mysql/mysqld.log >/dev/null 2>&1 || :
%systemd_post mysqld.service
#/usr/bin/systemd-tmpfiles --create %{_tmpfilesdir}/mysql.conf >/dev/null 2>&1 || :
/bin/systemctl enable mysqld >/dev/null 2>&1 || :
/sbin/ldconfig

%preun server
%systemd_preun mysqld.service

%postun 
%systemd_postun_with_restart mysqld.service
/sbin/ldconfig

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files server
%defattr(-, root, root, -)
#%doc %{?license_files_server} %{src_dir}/Docs/ChangeLog
%doc build/Docs/INFO_SRC*
%doc build/Docs/INFO_BIN*
%doc build/support-files/my-default.cnf

%attr(644, root, root) %{_mandir}/man1/mysqlman.1.gz

%if 0
%attr(644, root, root) %{_mandir}/man1/innochecksum.1*
%attr(644, root, root) %{_mandir}/man1/my_print_defaults.1*
%attr(644, root, root) %{_mandir}/man1/myisam_ftdump.1*
%attr(644, root, root) %{_mandir}/man1/myisamchk.1*
%attr(644, root, root) %{_mandir}/man1/myisamlog.1*
%attr(644, root, root) %{_mandir}/man1/myisampack.1*
%attr(644, root, root) %{_mandir}/man1/mysql_convert_table_format.1*
%attr(644, root, root) %{_mandir}/man1/mysql_fix_extensions.1*
%attr(644, root, root) %{_mandir}/man8/mysqld.8*
%attr(644, root, root) %{_mandir}/man1/mysqld_multi.1*
%attr(644, root, root) %{_mandir}/man1/mysqld_safe.1*
%attr(644, root, root) %{_mandir}/man1/mysqldumpslow.1*
%attr(644, root, root) %{_mandir}/man1/mysql_install_db.1*
%attr(644, root, root) %{_mandir}/man1/mysql_plugin.1*
%attr(644, root, root) %{_mandir}/man1/mysql_secure_installation.1*
%attr(644, root, root) %{_mandir}/man1/mysql_upgrade.1*
%attr(644, root, root) %{_mandir}/man1/mysqlhotcopy.1*
%attr(644, root, root) %{_mandir}/man1/mysqlman.1*
%attr(644, root, root) %{_mandir}/man1/mysql.server.1*
%attr(644, root, root) %{_mandir}/man1/mysqltest.1*
%attr(644, root, root) %{_mandir}/man1/mysql_tzinfo_to_sql.1*
%attr(644, root, root) %{_mandir}/man1/mysql_zap.1*
%attr(644, root, root) %{_mandir}/man1/mysqlbug.1*
%attr(644, root, root) %{_mandir}/man1/perror.1*
%attr(644, root, root) %{_mandir}/man1/replace.1*
%attr(644, root, root) %{_mandir}/man1/resolve_stack_dump.1*
%attr(644, root, root) %{_mandir}/man1/resolveip.1*
%endif

%config(noreplace) %{_sysconfdir}/my.cnf
%dir %{_sysconfdir}/my.cnf.d

%attr(755, root, root) %{_bindir}/innochecksum
%attr(755, root, root) %{_bindir}/my_print_defaults
%attr(755, root, root) %{_bindir}/myisam_ftdump
%attr(755, root, root) %{_bindir}/myisamchk
%attr(755, root, root) %{_bindir}/myisamlog
%attr(755, root, root) %{_bindir}/myisampack
%attr(755, root, root) %{_bindir}/mysql_convert_table_format
%attr(755, root, root) %{_bindir}/mysql_fix_extensions
%attr(755, root, root) %{_bindir}/mysql_install_db
%attr(755, root, root) %{_bindir}/mysql_plugin
%attr(755, root, root) %{_bindir}/mysql_secure_installation
%attr(755, root, root) %{_bindir}/mysql_tzinfo_to_sql
%attr(755, root, root) %{_bindir}/mysql_upgrade
%attr(755, root, root) %{_bindir}/mysql_zap
%attr(755, root, root) %{_bindir}/mysqlbug
%attr(755, root, root) %{_bindir}/mysqld_multi
%attr(755, root, root) %{_bindir}/mysqld_safe
%attr(755, root, root) %{_bindir}/mysqldumpslow
%attr(755, root, root) %{_bindir}/mysqlhotcopy
%attr(755, root, root) %{_bindir}/mysqltest
%attr(755, root, root) %{_bindir}/perror
%attr(755, root, root) %{_bindir}/replace
%attr(755, root, root) %{_bindir}/resolve_stack_dump
%attr(755, root, root) %{_bindir}/resolveip
%attr(755, root, root) %{_bindir}/mysql-systemd-start
%attr(755, root, root) %{_sbindir}/mysqld
#%attr(755, root, root) %{_sbindir}/mysqld-debug
#%attr(755, root, root) %{_sbindir}/rcmysql

%dir %{_libdir}/mysql/plugin
%attr(755, root, root) %{_libdir}/mysql/plugin/adt_null.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth_socket.so
%attr(755, root, root) %{_libdir}/mysql/plugin/innodb_engine.so
%attr(755, root, root) %{_libdir}/mysql/plugin/libmemcached.so
%attr(755, root, root) %{_libdir}/mysql/plugin/mypluglib.so
%attr(755, root, root) %{_libdir}/mysql/plugin/mysql_no_login.so
#%attr(755, root, root) %{_libdir}/mysql/plugin/semisync_master.so
#%attr(755, root, root) %{_libdir}/mysql/plugin/semisync_slave.so
%attr(755, root, root) %{_libdir}/mysql/plugin/validate_password.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth.so
%attr(755, root, root) %{_libdir}/mysql/plugin/auth_test_plugin.so
%attr(755, root, root) %{_libdir}/mysql/plugin/daemon_example.ini
%attr(755, root, root) %{_libdir}/mysql/plugin/libdaemon_example.so
%attr(755, root, root) %{_libdir}/mysql/plugin/qa_auth_interface.so
%attr(755, root, root) %{_libdir}/mysql/plugin/qa_auth_server.so
%attr(755, root, root) %{_libdir}/mysql/plugin/qa_auth_client.so
%attr(755, root, root) %{_libdir}/mysql/plugin/test_udf_services.so

%if 0
%dir %{_libdir}/mysql/plugin/debug
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/adt_null.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/auth_socket.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/innodb_engine.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/libmemcached.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/mypluglib.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/mysql_no_login.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/semisync_master.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/semisync_slave.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/validate_password.so
%endif

%if 0%{?commercial}
%attr(755, root, root) %{_libdir}/mysql/plugin/audit_log.so
%attr(755, root, root) %{_libdir}/mysql/plugin/authentication_pam.so
%attr(755, root, root) %{_libdir}/mysql/plugin/thread_pool.so
%attr(755, root, root) %{_libdir}/mysql/plugin/openssl_udf.so
%attr(755, root, root) %{_libdir}/mysql/plugin/firewall.so
%attr(644, root, root) %{_datadir}/mysql/linux_install_firewall.sql
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/audit_log.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/authentication_pam.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/thread_pool.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/openssl_udf.so
%attr(755, root, root) %{_libdir}/mysql/plugin/debug/firewall.so
%endif
%attr(644, root, root) %{_datadir}/mysql/fill_help_tables.sql
%attr(644, root, root) %{_datadir}/mysql/mysql_system_tables.sql
%attr(644, root, root) %{_datadir}/mysql/mysql_system_tables_data.sql
%attr(644, root, root) %{_datadir}/mysql/mysql_test_data_timezone.sql
%attr(644, root, root) %{_datadir}/mysql/my-*.cnf
%attr(644, root, root) %{_datadir}/mysql/mysql-log-rotate
%attr(644, root, root) %{_datadir}/mysql/mysql_security_commands.sql
%attr(644, root, root) %{_datadir}/mysql/SELinux/RHEL4/mysql.fc
%attr(644, root, root) %{_datadir}/mysql/SELinux/RHEL4/mysql.te
%attr(644, root, root) %{_datadir}/mysql/dictionary.txt
%attr(644, root, root) %{_datadir}/mysql/innodb_memcached_config.sql
%attr(644, root, root) %{_datadir}/mysql/magic
%attr(644, root, root) %{_prefix}/lib/tmpfiles.d/mysql.conf
%attr(644, root, root) %{_unitdir}/mysqld.service
%attr(644, root, root) %config(noreplace,missingok) %{_sysconfdir}/logrotate.d/mysql
%dir %attr(755, mysql, mysql) /var/lib/mysql
%dir %attr(755, mysql, mysql) /var/run/mysqld
%dir %attr(750, mysql, mysql) /var/log/mysql

%files common
%defattr(-, root, root, -)
%doc %{?license_files_server}
%{_datadir}/mysql/charsets/
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/bulgarian/
%{_datadir}/mysql/czech/
%{_datadir}/mysql/danish/
%{_datadir}/mysql/dutch/
%{_datadir}/mysql/english/
%{_datadir}/mysql/estonian/
%{_datadir}/mysql/french/
%{_datadir}/mysql/german/
%{_datadir}/mysql/greek/
%{_datadir}/mysql/hungarian/
%{_datadir}/mysql/italian/
%{_datadir}/mysql/japanese/
%{_datadir}/mysql/korean/
%{_datadir}/mysql/norwegian-ny/
%{_datadir}/mysql/norwegian/
%{_datadir}/mysql/polish/
%{_datadir}/mysql/portuguese/
%{_datadir}/mysql/romanian/
%{_datadir}/mysql/russian/
%{_datadir}/mysql/serbian/
%{_datadir}/mysql/slovak/
%{_datadir}/mysql/spanish/
%{_datadir}/mysql/swedish/
%{_datadir}/mysql/ukrainian/

%files client
%defattr(-, root, root, -)
%doc %{?license_files_server}
%attr(755, root, root) %{_bindir}/msql2mysql
%attr(755, root, root) %{_bindir}/mysql
%attr(755, root, root) %{_bindir}/mysql_find_rows
%attr(755, root, root) %{_bindir}/mysql_waitpid
%attr(755, root, root) %{_bindir}/mysqlaccess
# XXX: This should be moved to %{_sysconfdir}
%attr(644, root, root) %{_bindir}/mysqlaccess.conf
%attr(755, root, root) %{_bindir}/mysqladmin
%attr(755, root, root) %{_bindir}/mysqlbinlog
%attr(755, root, root) %{_bindir}/mysqlcheck
%attr(755, root, root) %{_bindir}/mysqldump
%attr(755, root, root) %{_bindir}/mysqlimport
%attr(755, root, root) %{_bindir}/mysqlshow
%attr(755, root, root) %{_bindir}/mysqlslap
%attr(755, root, root) %{_bindir}/mysql_config_editor

%if 0
%attr(644, root, root) %{_mandir}/man1/msql2mysql.1*
%attr(644, root, root) %{_mandir}/man1/mysql.1*
%attr(644, root, root) %{_mandir}/man1/mysql_find_rows.1*
%attr(644, root, root) %{_mandir}/man1/mysql_waitpid.1*
%attr(644, root, root) %{_mandir}/man1/mysqlaccess.1*
%attr(644, root, root) %{_mandir}/man1/mysqladmin.1*
%attr(644, root, root) %{_mandir}/man1/mysqlbinlog.1*
%attr(644, root, root) %{_mandir}/man1/mysqlcheck.1*
%attr(644, root, root) %{_mandir}/man1/mysqldump.1*
%attr(644, root, root) %{_mandir}/man1/mysqlimport.1*
%attr(644, root, root) %{_mandir}/man1/mysqlshow.1*
%attr(644, root, root) %{_mandir}/man1/mysqlslap.1*
%attr(644, root, root) %{_mandir}/man1/mysql_config_editor.1*
%endif

%files devel
%defattr(-, root, root, -)
%doc %{?license_files_server}

%if 0
%attr(644, root, root) %{_mandir}/man1/comp_err.1*
%attr(644, root, root) %{_mandir}/man1/mysql_config.1*
%endif

%attr(755, root, root) %{_bindir}/mysql_config
%{_includedir}/mysql
%{_datadir}/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient.a
%{_libdir}/mysql/libmysqlclient_r.a
%{_libdir}/mysql/libmysqlservices.a
%{_libdir}/mysql/libmysqlclient_r.so
%{_libdir}/mysql/libmysqlclient.so

%files libs
%defattr(-, root, root, -)
%doc %{?license_files_server}
%dir %attr(755, root, root) %{_libdir}/mysql
%attr(644, root, root) %{_sysconfdir}/ld.so.conf.d/mysql-%{_arch}.conf
%{_libdir}/mysql/libmysqlclient.so.18*
%{_libdir}/mysql/libmysqlclient_r.so.18*

%files bench
%defattr(-, root, root, -)
%doc %{?license_files_server}
%{_datadir}/sql-bench

%changelog
* Wed May 24 2017 Huang Jinhau <sjtuhjh@hotmail.com> 5.6.32-5
- Initial Estuary AliSQL package

