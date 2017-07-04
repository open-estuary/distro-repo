#!/bin/bash

echo "Not implement devtoolset-4-gcc"
exit 0

TARGET="ubuntu"
OS_VERSION="16.04"

if [ x"${1}" == x"debian" ] ; then
    TARGET=$1
    OS_VERSION="8"
elif [ ! -z "${1}" ] && [ x"${1}" != x"ubuntu" ] ; then
    echo "Unsupport platform: ${1}, it must be debian or ubuntu"
    exit 1
fi

CUR_DIR=$(cd `dirname $0`; pwd)

MAJOR="6.3"
VERSION="${MAJOR}.0"
TAR_FILENAME="gcc-6_6.3.0.orig.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

DSC_FILE="gcc-6_6.3.0-12ubuntu2.dsc"
DEBIAN_FILE="gcc-6_6.3.0-12ubuntu2.diff.gz"

if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
    wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}  https://launchpad.net/ubuntu/+archive/primary/+files/${TAR_FILENAME}
    wget -O ${CUR_DIR}/${SRC}/${DSC_FILE}      https://launchpad.net/ubuntu/+archive/primary/+files/${DSC_FILE}
    wget -O ${CUR_DIR}/${SRC}/${DEBIAN_FILE}   https://launchpad.net/ubuntu/+archive/primary/+files/${DEBIAN_FILE}
    #mv ${CUR_DIR}/${SRC}/${TAR_FILENAME} ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME}
fi

${CUR_DIR}/../../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${TAR_FILENAME} ${TARGET} "" "yes"
