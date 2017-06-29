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

MAJOR="6.3"
VERSION="${MAJOR}.0"
TAR_FILENAME="gcc-6_6.3.0.orig.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

DSC_FILE="gcc-6_6.3.0-19.dsc"
DEBIAN_FILE="gcc-6_6.3.0-19.diff.gz"

if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
    wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}  http://ftp.cn.debian.org/debian/pool/main/g/gcc-6/${TAR_FILENAME}
    wget -O ${CUR_DIR}/${SRC}/${DSC_FILE}      http://ftp.cn.debian.org/debian/pool/main/g/gcc-6/${DSC_FILE}
    wget -O ${CUR_DIR}/${SRC}/${DEBIAN_FILE}   http://ftp.cn.debian.org/debian/pool/main/g/gcc-6/${DEBIAN_FILE}
    #mv ${CUR_DIR}/${SRC}/${TAR_FILENAME} ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME}
fi

${CUR_DIR}/../../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${TAR_FILENAME} ${TARGET}
