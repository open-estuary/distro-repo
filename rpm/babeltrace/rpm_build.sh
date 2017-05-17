#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.2.4"
TAR_FILENAME="babeltrace-""${VERSION}"".tar.bz2"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://lttng.org/files/babeltrace/babeltrace-${VERSION}.tar.bz2
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/babeltrace.spec

${CUR_DIR}/../../utils/rpm_autobuild.sh  ${CUR_DIR}/src babeltrace.spec

