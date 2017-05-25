#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="4.8"
TAR_FILENAME="ethtool-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://kernel.org/pub/software/network/ethtool/ethtool-${VERSION}.tar.gz
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/ethtool.spec

${CUR_DIR}/../../utils/rpm_autobuild.sh  ${CUR_DIR}/src ethtool.spec

