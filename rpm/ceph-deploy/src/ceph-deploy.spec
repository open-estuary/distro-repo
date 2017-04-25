%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           ceph-deploy
Version:   1.5.37
Release:        1%{?dist}
Summary:        Admin and deploy tool for Ceph

License:        MIT
URL:            https://github.com/ceph/ceph-deploy

Source0:        https://pypi.python.org/packages/source/c/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

# Tox tests requirements
BuildRequires:  openssh-clients
BuildRequires:  pytest
BuildRequires:  python-mock
BuildRequires:  python-remoto
BuildRequires:  python-tox

Requires:       python-remoto

%description
An easy to use admin tool for deploy ceph storage clusters.


%prep
%setup -q


%build
CEPH_DEPLOY_NO_VENDOR=1 %{__python2} setup.py build


%install
CEPH_DEPLOY_NO_VENDOR=1 %{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
# Tests are currently broken:
#   http://tracker.ceph.com/issues/8825
CEPH_DEPLOY_NO_VENDOR=1 tox -e py27-novendor || :


%files
%doc LICENSE README.rst
%{_bindir}/ceph-deploy
%{python2_sitelib}/*


%changelog
* Tue Apr 25 2017 Huang Jinhua <sjtuhjh@hotmail.com> - 1.5.37
- initial build
