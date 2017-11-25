#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.10.3"
TAR_FILENAME="lttng-modules-""${VERSION}"".tar.bz2"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://lttng.org/files/lttng-modules/lttng-modules-${VERSION}.tar.bz2
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/lttng-modules.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src lttng-modules_v500.spec

