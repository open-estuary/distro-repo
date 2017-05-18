#%if 0%{?fedora} > 1
%global with_python3 1
#%endif
%global oname   beautifulsoup4

Name:           python-beautifulsoup4
Version:        4.6.0
Release:        1%{?dist}
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
Group:          Development/Languages
License:        MIT
URL:            http://www.crummy.com/software/BeautifulSoup/
Source0:        https://files.pythonhosted.org/packages/source/b/%{oname}/%{oname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel >= 2.7
# html5lib BR just for test coverage
BuildRequires:  python-html5lib
BuildRequires:  python-setuptools
BuildRequires:  python-lxml
Requires:       python-lxml

%description
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.

%if 0%{?with_python3}
%package -n     python3-beautifulsoup4
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
Group:          Development/Languages
BuildRequires:  python-tools
# html5lib BR just for test coverage
#BuildRequires:  python3-html5lib
BuildRequires:  python34-devel
BuildRequires:  python34-setuptools
#BuildRequires:  python3-lxml
#Requires:       python3-lxml
Obsoletes:      python3-BeautifulSoup < 1:3.2.1-2

%description -n python3-beautifulsoup4
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:

Beautiful Soup won't choke if you give it bad markup.

Beautiful Soup provides a few simple methods and Pythonic idioms for
navigating, searching, and modifying a parse tree.

Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.

Beautiful Soup parses anything you give it.

Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.

This is the Python 3 build of Beautiful Soup.

%endif # if with_python3

%prep
%setup -q -n %{oname}-%{version}
mv AUTHORS.txt AUTHORS.txt.iso
iconv -f ISO-8859-1 -t UTF-8 -o AUTHORS.txt AUTHORS.txt.iso
touch -r AUTHORS.txt.iso AUTHORS.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
#%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
2to3 --write --nobackups .
%{__python3} setup.py build
%endif

%install
#%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%check
#%{__python} -m unittest discover -s bs4
#%if 0%{?with_python3}
#pushd %{py3dir}
#%{__python3} -m unittest discover -s bs4
#%endif

%files
#%license COPYING.txt
#%doc AUTHORS.txt NEWS.txt README.txt TODO.txt
#%{python_sitelib}/beautifulsoup4-%{version}*.egg-info
#%{python_sitelib}/bs4

%if 0%{?with_python3}
%files -n python3-beautifulsoup4
%license COPYING.txt
%doc AUTHORS.txt NEWS.txt README.txt TODO.txt
%{python3_sitelib}/beautifulsoup4-%{version}*.egg-info
%{python3_sitelib}/bs4
%endif

%changelog
* Mon May 08 2017 Terje Rosten <terje.rosten@ntnu.no> - 4.6.0-1
- 4.6.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Terje Rosten <terje.rosten@ntnu.no> - 4.5.3-1
- 4.5.3

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-3
- Un-bootstrap for Python 3.6

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-2
- Rebuild for Python 3.6

* Tue Aug 09 2016 Terje Rosten <terje.rosten@ntnu.no> - 4.5.1-1
- 4.5.1

* Tue Jul 26 2016 Ville Skyttä <ville.skytta@iki.fi> - 4.5.0-1
- Update to 4.5.0
- Mark COPYING.txt as %%license
- Don't require html5lib
- Require lxml on EL too

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 03 2015 Terje Rosten <terje.rosten@ntnu.no> - 4.4.1-1
- 4.4.1

* Sat Jul 04 2015 Terje Rosten <terje.rosten@ntnu.no> - 4.4.0-1
- 4.4.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Oct 17 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.3.2-1
- 4.3.2

* Mon Aug 19 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.3.1-1
- 4.3.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.2.1-1
- 4.2.1

* Mon May 27 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.2.0-1
- 4.2.0

* Tue Mar 19 2013 Ralph Bean <rbean@redhat.com> - 4.1.3-3
- Don't include python-lxml for el6.
- Conditionalize python3 support.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.3-1
- 4.1.3

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.1.1-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sun Jul 22 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.1-4
- Move python3 req to sub package

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.1-2
- License is MIT
- Remove old cruft
- Fix obsolete

* Mon Jul 09 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.1-1
- 4.1.1
- Obsolete the old py3-bs4 from bs3 package

* Mon May 28 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.0.5-1
- 4.0.5

* Sat Mar 24 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.0.1-1
- initial package based on python-BeautifulSoup.

