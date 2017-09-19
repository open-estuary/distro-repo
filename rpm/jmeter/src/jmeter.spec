# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define jmeter_base_version 3.2
%define jmeter_version 3.2
%define jmeter_release 1
%define jmeter_name jmeter
%define jmeter_installdir /opt/jmeter

Name: jmeter
Version: %{jmeter_version}
Release: %{jmeter_release}
Summary: The Apache JMeter™ application is open source software, a 100% pure Java application designed to load test functional behavior and measure performance.
URL: http://lucene.apache.org/jmeter
Group: Development/Libraries
BuildArch: noarch
License: ASL 2.0
Source0: apache-jmeter-%{jmeter_base_version}.tgz

%description 
The Apache JMeter™ application is open source software, a 100% pure Java application designed to load test functional behavior and measure performance. It was originally designed for testing Web Applications but has since expanded to other test functions. 

%prep
%setup -n apache-jmeter-%{jmeter_base_version}

%build

%install
%__rm -rf $RPM_BUILD_ROOT
%__install -d $RPM_BUILD_ROOT/%{jmeter_installdir}
%__install -d $RPM_BUILD_ROOT/%{_bindir}
cp -fr ./* $RPM_BUILD_ROOT/%{jmeter_installdir}/

cd $RPM_BUILD_ROOT/%{_bindir}
ln -s ../../opt/jmeter/bin/jmeter jmeter

#######################
#### FILES SECTION ####
#######################
%files 
#%defattr(-,jmeter,jmeter,755)
%{jmeter_installdir}
%{_bindir}/jmeter

%changelog 
* Tue Sep 12 2017 sjtuhjh@hotmail.com 
- Estuary initial ARM64 packages 

