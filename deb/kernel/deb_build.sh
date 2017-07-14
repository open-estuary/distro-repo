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

RPMVERSION="4.9.20"
PKGRELEASE="3.1.rc1"
TAR_FILENAME="linux-""${RPMVERSION}.estuary.$PKGRELEASE"".tar.gz"


#if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
#        sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/crash-utility/crash/archive/${VERSION}.tar.gz 
#fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/src ${TAR_FILENAME} $TARGETOS
