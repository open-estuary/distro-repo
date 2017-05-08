# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2015, 2017, Oracle and/or its affiliates. All rights reserved.
#
# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?suse_version} && 0%{?suse_version} <= 1200
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?suse_version} == 1315
%global dist            .sles12
%endif

%if 0%{?suse_version} == 1110
%global dist            .sles11
%endif

%{?fedora: %global with_python3 1}

%global mysql_config    /usr/bin/mysql_config

%{?mysql_capi: %global with_mysql_capi %{mysql_capi}}
%{?mysql_capi: %global mysql_config %{mysql_capi}/bin/mysql_config}

%if 0%{?commercial}
%global license_type    Commercial
%global product_suffix  -commercial
%else
%global license_type    GPLv2
%endif

Summary:       Standardized MySQL database driver for Python
Name:          mysql-connector-python%{?product_suffix}
Version:       2.1.6
Release:       1%{?commercial:.1}%{?dist}
License:       Copyright (c) 2015, 2017, Oracle and/or its affiliates. All rights reserved. Under %{?license_type} license as shown in the Description field.
Group:         Development/Libraries
URL:           https://dev.mysql.com/downloads/connector/python/            
Source0:       https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{?commercial:commercial-}%{version}.tar.gz
#BuildArch:     noarch
%{!?with_mysql_capi:BuildRequires: mysql-devel}
BuildRequires: python-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # if with_python3
%if 0%{?commercial}
Obsoletes:     mysql-connector-python < %{version}-%{release}
Provides:      mysql-connector-python = %{version}-%{release}
%endif
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python and does not have any
dependencies except for the Python Standard Library.
The MySQL software has Dual Licensing, which means you can use the

MySQL software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from Oracle and/or its affiliates if you do not wish to be
bound by the terms of the GPL. See the chapter "Licensing and Support"
in the manual for further info.

The MySQL web site (http://www.mysql.com/) provides the latest news
and information about the MySQL software. Also please see the
documentation and the manual for more information.

%package       cext
Summary:       Standardized MySQL driver for Python with C Extension
Group:         Development/Libraries
%if 0%{?commercial}
Requires:      mysql-connector-python-commercial = %{version}-%{release}
Obsoletes:     mysql-connector-python-cext < %{version}-%{release}
Provides:      mysql-connector-python-cext = %{version}-%{release}
%else
Requires:      mysql-connector-python = %{version}-%{release}
%endif

%description   cext
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. This is a optional C Extension to the pure Python driver,
it's linked with MySQL Connector/C.

The MySQL software has Dual Licensing, which means you can use the
MySQL software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from Oracle and/or its affiliates if you do not wish to be
bound by the terms of the GPL. See the chapter "Licensing and Support"
in the manual for further info.

The MySQL web site (http://www.mysql.com/) provides the latest news
and information about the MySQL software. Also please see the
documentation and the manual for more information.

%if 0%{?with_python3}
%package    -n mysql-connector-python3%{?product_suffix}
Summary:       Standardized MySQL database driver for Python 3
Group:         Development/Libraries
%if 0%{?commercial}
Obsoletes:     mysql-connector-python3 < %{version}-%{release}
Provides:      mysql-connector-python3 = %{version}-%{release}
%endif

%description -n mysql-connector-python3%{?product_suffix}
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python and does not have any
dependencies except for the Python Standard Library.

This is the Python 3 version of the driver.

The MySQL software has Dual Licensing, which means you can use the
MySQL software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from Oracle and/or its affiliates if you do not wish to be
bound by the terms of the GPL. See the chapter "Licensing and Support"
in the manual for further info.

The MySQL web site (http://www.mysql.com/) provides the latest news
and information about the MySQL software. Also please see the
documentation and the manual for more information.

%package    -n mysql-connector-python3%{?product_suffix}-cext
Summary:       Standardized MySQL driver for Python with C Extension
Group:         Development/Libraries
%if 0%{?commercial}
Requires:      mysql-connector-python3-commercial = %{version}-%{release}
Obsoletes:     mysql-connector-python3-cext < %{version}-%{release}
Provides:      mysql-connector-python3-cext = %{version}-%{release}
%else
Requires:      mysql-connector-python3 = %{version}-%{release}
%endif

%description -n mysql-connector-python3%{?product_suffix}-cext
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. This is a optional C Extension to the pure Python driver,
it's linked with MySQL Connector/C.

This is the Python 3 version of the extension.

The MySQL software has Dual Licensing, which means you can use the
MySQL software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from Oracle and/or its affiliates if you do not wish to be
bound by the terms of the GPL. See the chapter "Licensing and Support"
in the manual for further info.

The MySQL web site (http://www.mysql.com/) provides the latest news
and information about the MySQL software. Also please see the
documentation and the manual for more information.
%endif # if with_python3

%prep
%setup -q
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # if with_python3

%build
%{__python} setup.py build
%{__python} setup.py build_ext%{?with_mysql_capi:_static --with-mysql-capi=%{with_mysql_capi}}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
%{__python3} setup.py build_ext%{?with_mysql_capi:_static --with-mysql-capi=%{with_mysql_capi}}
popd
%endif # with_python3

%install
rm -rf %{buildroot}
# skip-build is broken
%{__python} setup.py install --prefix=%{_prefix} --root %{buildroot} --with-mysql-capi=%{mysql_config}
rm -rf %{buildroot}%{python_sitearch}/mysql
%{__python} setup.py install --prefix=%{_prefix} --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --prefix=%{_prefix} --root %{buildroot} --with-mysql-capi=%{mysql_config}
rm -rf %{buildroot}%{python3_sitearch}/mysql
%{__python3} setup.py install --prefix=%{_prefix} --root %{buildroot}
popd
%endif # with_python3

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python_sitelib}/mysql
%if 0%{?rhel} > 5 || 0%{?fedora} > 12 || 0%{?suse_version} >= 1100
%{python_sitelib}/mysql_connector_python-*.egg-info
%endif

%files cext
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python_sitearch}/_mysql_connector.so
%{python_sitearch}/mysql_connector_python-*.egg-info

%if 0%{?with_python3}
%files -n mysql-connector-python3%{?product_suffix}
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python3_sitelib}/mysql
%{python3_sitelib}/mysql_connector_python-*.egg-info

%files -n mysql-connector-python3%{?product_suffix}-cext
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python3_sitearch}/_mysql_connector.cpython*.so
%{python3_sitearch}/mysql_connector_python-*.egg-info
%endif # with_python3

%changelog
* Tue Mar 28 2017  Nuno Mariz <nuno.mariz@oracle.com> - 2.1.6-1
- Updated for 2.1.6

* Thu Nov 17 2016  Nuno Mariz <nuno.mariz@oracle.com> - 2.1.5-1
- Updated for 2.1.5

* Wed Feb 10 2016  Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.1.4-1
- Updated for 2.1.4

* Fri Jul 31 2015 Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 2.1.3-1
- New spec file with support for cext, license options and Python 3 support

