#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

TARGETOS="ubuntu"
if [ x"${1}" == x"debian" ] ; then
    TARGETOS=$1
elif [ ! -z "${1}" ] && [ x"${1}" != x"ubuntu" ] ; then
    echo "Unsupport platform: ${1}, it must be debian or ubuntu"
    exit 1
fi

VERSION="2.5.1"
TAR_FILENAME="lttng-modules-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
        wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://lttng.org/files/lttng-modules/lttng-modules-${VERSION}.tar.gz
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/src ${TAR_FILENAME} $TARGETOS
