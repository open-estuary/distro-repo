#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.0"
TAR_FILENAME="dmidecode-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://download.savannah.gnu.org/releases/dmidecode/dmidecode-${VERSION}.tar.gz
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/dmidecode.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src dmidecode.spec
