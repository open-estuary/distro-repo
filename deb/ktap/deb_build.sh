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

VERSION="0.4"
TAR_FILENAME="ktap-""${VERSION}+git20150927"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
        sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/ktap/ktap.git 
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/src ${TAR_FILENAME} $TARGETOS
