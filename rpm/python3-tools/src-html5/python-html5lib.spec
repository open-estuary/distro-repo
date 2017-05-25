%global modulename html5lib
#%if 0%{?fedora}
%global with_python3 1
#%endif

Name:		python-%{modulename}
Summary:	A python based HTML parser/tokenizer
Version:	0.999
Release:	13%{?dist}
Epoch:		1
Group:		Development/Libraries
License:	MIT
URL:		https://pypi.python.org/pypi/%{modulename}

Source0:	https://pypi.python.org/packages/source/h/%{modulename}/%{modulename}-%{version}.tar.gz
# Patch for fixing invalid escape sequences with Python 3.6
Patch0:		fix-invalid-escape-sequences.patch

BuildArch:	noarch

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.

#%package -n python2-%{modulename}
#Summary:	A python based HTML parser/tokenizer 
#Group:		Development/Libraries 

#Requires:	python-six
#BuildRequires:	python-setuptools
#BuildRequires:	python2-devel
#BuildRequires:	python-nose
#BuildRequires:	python-six
#%{?python_provide:%python_provide python2-%{modulename}}

#%description -n python2-%{modulename}
#A python based HTML parser/tokenizer based on the WHATWG HTML5 
#specification for maximum compatibility with major desktop web browsers.

%if 0%{?with_python3}
%package -n python3-%{modulename}
Summary:	A python based HTML parser/tokenizer 
Group:		Development/Libraries 

Requires:	python34-six
BuildRequires:	python34-devel
BuildRequires:	python34-setuptools
BuildRequires:	python34-nose
BuildRequires:	python34-six
#%{?python_provide:%python_provide python3-%{modulename}}

%description -n python3-%{modulename}
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.
%endif


%prep
%setup -q -n %{modulename}-%{version} 
%patch0 -p1


%build
#%py2_build

%if 0%{?with_python3}
%py3_build
%endif


%install
%if 0%{?with_python3}
%py3_install
%endif

#%py2_install

%check
#nosetests-%{python2_version}

%if 0%{?with_python3}
nosetests-%{python3_version}
%endif

#%files -n python2-%{modulename}
#%license LICENSE 
#%doc CHANGES.rst README.rst
#%{python_sitelib}/%{modulename}-*.egg-info
#%{python_sitelib}/%{modulename}

%if 0%{?with_python3}
%files -n python3-%{modulename}
%license LICENSE 
%doc CHANGES.rst README.rst
%{python3_sitelib}/%{modulename}-*.egg-info
%{python3_sitelib}/%{modulename}
%endif 


%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 1:0.999-12
- Correct usage of the %%python_provide macro

* Fri Dec 30 2016 Orion Poplawski <orion@cora.nwra.com> - 1:0.999-11
- Ship python2-html5lib
- Modernize spec
- Use %%license

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1:0.999-10
- Rebuild for Python 3.6
- Fix invalid escape sequences

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 1:0.999-7
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.999-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 0.999-3
- move python3 Requires and BuildRequires into the python3 sub-package

* Wed Mar 12 2014 Dan Scott <dan@coffeecode.net> - 0.999-2
- "six" module is a runtime requirement

* Sat Mar 01 2014 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.999-1
- Added epoch information

* Wed Feb 26 2014 Dan Scott <dan@coffeecode.net> - 0.999-1
- Updated for new version
- Fixed bogus dates in changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 8 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0b2-2
- Updated python3 support which accidently removed from previous revision.

* Mon Jul 8 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0b2-1
- Updated new source

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.95-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.95-1
- Added python3 spec and updated new source

* Mon Jul 18 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.90-1
- Initial spec
