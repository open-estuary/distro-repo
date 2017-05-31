#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.8"
TAR_FILENAME="packETHcli-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://sourceforge.net/projects/packeth/files/packETHcli-${VERSION}.tar.gz/
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/packETHcli.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src packETHcli.spec

