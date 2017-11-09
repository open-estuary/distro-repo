#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.6"
TAR_FILENAME="Mycat-server-1.6-RELEASE-20161028204710-linux.tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://dl.mycat.io/1.6-RELEASE/Mycat-server-1.6-RELEASE-20161028204710-linux.tar.gz
fi
#sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/mycat.spec

${CUR_DIR}/../../utils/rpm_build.sh ${CUR_DIR}/src mycat.spec

