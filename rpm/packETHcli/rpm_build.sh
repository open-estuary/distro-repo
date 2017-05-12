#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.8.1"
TAR_FILENAME="packETH-""${VERSION}"".tar.bz2"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://sourceforge.net/projects/packeth/files/packETH-${VERSION}.tar.bz2/
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/packETH.spec

${CUR_DIR}/../../utils/rpm_autobuild.sh  ${CUR_DIR}/src packETH.spec

