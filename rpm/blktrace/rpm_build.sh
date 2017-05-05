#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0.5"
TAR_FILENAME="blktrace-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://brick.kernel.dk/snaps/blktrace-${VERSION}.tar.gz 
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/blktrace.spec

${CUR_DIR}/../../utils/rpm_autobuild.sh  ${CUR_DIR}/src blktrace.spec

