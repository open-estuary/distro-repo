#!/bin/bash

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

MAJOR="5.7"
VERSION="${MAJOR}.18"
TAR_FILENAME="boost1.63_1.63.0+dfsg.orig.tar.bz2"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

DSC_FILE="boost1.63_1.63.0+dfsg-1.dsc"
DEBIAN_FILE="boost1.63_1.63.0+dfsg-1.debian.tar.xz"

NEW_TAR_FILENAME="boost1.63_1.63.0.orig.tar.bz2"
#NEW_TAR_FILENAME="boost1.63_1.63.0+dfsg.orig.tar.bz2"

if [ ! -f ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME} ] ; then
    wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}  https://launchpad.net/ubuntu/+archive/primary/+files/${TAR_FILENAME}
    #wget -O ${CUR_DIR}/${SRC}/${DSC_FILE}      https://launchpad.net/ubuntu/+archive/primary/+files/${DSC_FILE}
    #wget -O ${CUR_DIR}/${SRC}/${DEBIAN_FILE}   https://launchpad.net/ubuntu/+archive/primary/+files/${DEBIAN_FILE}
    mv ${CUR_DIR}/${SRC}/${TAR_FILENAME} ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME}
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${NEW_TAR_FILENAME} ${TARGET}
