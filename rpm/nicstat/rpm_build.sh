#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.95"
TAR_FILENAME="nicstat-src-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://sourceforge.net/projects/nicstat/files/nicstat-src-${VERSION}.tar.gz 
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/nicstat.spec

${CUR_DIR}/../../utils/rpm_autobuild.sh  ${CUR_DIR}/src nicstat.spec

