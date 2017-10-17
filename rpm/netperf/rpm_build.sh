#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.7.0"
TAR_FILENAME="netperf-""${VERSION}"".tar.bz2"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} ftp://ftp.netperf.org/netperf/netperf-${version}.tar.bz2 
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/netperf.spec

${CUR_DIR}/../../utils/rpm_build.sh ${CUR_DIR}/src netperf.spec

