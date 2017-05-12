#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0.1"
TAR_FILENAME="open-lldp-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://ftp-osl.osuosl.org/pub/open-lldp/open-lldp-${VERSION}.tar.gz
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/open-lldp.spec

${CUR_DIR}/../../utils/rpm_autobuild.sh  ${CUR_DIR}/src open-lldp.spec

