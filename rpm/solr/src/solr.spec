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

%define solr_base_version 7.1.0
%define solr_version 7.1.0
%define solr_release 1
%define solr_name solr
%define solr_service /usr/lib/systemd/system/solr.service
%define solr_installdir /opt/solr
%define run_solr /var/run/solr

Name: solr
Version: %{solr_version}
Release: %{solr_release}
Summary: Apache Solr is the popular, blazing fast open source enterprise search platform
URL: http://lucene.apache.org/solr
Group: Development/Libraries
BuildArch: noarch
License: ASL 2.0
Source0: solr-%{solr_base_version}.tgz
Source1: solr.service.in
Source2: solr.sysconfig.in

%description 
Solr is the popular, blazing fast open source enterprise search platform from
the Apache Lucene project. Its major features include powerful full-text
search, hit highlighting, faceted search, dynamic clustering, database
integration, rich document (e.g., Word, PDF) handling, and geospatial search.
Solr is highly scalable, providing distributed search and index replication,
and it powers the search and navigation features of many of the world's
largest internet sites.

Solr is written in Java and runs as a standalone full-text search server within
a servlet container such as Tomcat. Solr uses the Lucene Java search library at
its core for full-text indexing and search, and has REST-like HTTP/XML and JSON
APIs that make it easy to use from virtually any programming language. Solr's
powerful external configuration allows it to be tailored to almost any type of
application without Java coding, and it has an extensive plugin architecture
when more advanced customization is required.

%prep
%setup -n solr-%{solr_base_version}

%build

%install
%__rm -rf $RPM_BUILD_ROOT
%__install -d $RPM_BUILD_ROOT/%{solr_installdir}
cp -fr ./* $RPM_BUILD_ROOT/%{solr_installdir}/

%__install -D -m0755 "%{SOURCE1}" $RPM_BUILD_ROOT/%{solr_service}
%__install -D -m0644 "%{SOURCE2}" $RPM_BUILD_ROOT/etc/sysconfig/solr
%__install -d $RPM_BUILD_ROOT/%{_bindir}
cd $RPM_BUILD_ROOT/%{_bindir}
ln -s ../../opt/solr/bin/solr solr

%pre
getent group solr >/dev/null || groupadd -r solr
getent passwd solr > /dev/null || useradd -c "Solr" -s /sbin/nologin -g solr -r -d %{run_solr} solr 2> /dev/null || :

%post
/usr/bin/systemctl daemon-reload

%preun
if [ $1 = 0 ] ; then
        service solr stop > /dev/null 2>&1
fi

%postun
if [ $1 -ge 1 ]; then
        service solr restart > /dev/null 2>&1
fi

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,solr,solr,755)
%attr(0755,solr,solr) %{solr_installdir}
%config(noreplace) %{solr_service}
%{_bindir}/solr
/etc/sysconfig/solr

%changelog 
* Tue Sep 12 2017 sjtuhjh@hotmail.com 
- Estuary initial ARM64 packages 
- Port from Apache bigtop solr rpm spec

