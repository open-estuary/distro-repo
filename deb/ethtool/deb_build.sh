#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

usage()
{
        echo "Usage: deb_build.sh [targetos(debian or ubuntu)]"
}

TARGETOS=debian
if [ $# -eq 0 ];then
        TARGETOS=debian
elif [ $# -eq 1 ];then
        TARGETOS=$1
else
        usage
        exit 1
fi

VERSION="4.8"
TAR_FILENAME="ethtool-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
        sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://kernel.org/pub/software/network/ethtool/ethtool-${VERSION}.tar.gz
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/src ${TAR_FILENAME} $TARGETOS
