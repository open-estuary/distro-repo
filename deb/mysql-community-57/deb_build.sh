#!/bin/bash

TARGET="debian"
OS_VERSION="8"

if [ x"${1}" == x"ubuntu" ] ; then
    TARGET=$1
    OS_VERSION="16.04"
elif [ ! -z "${1}" ] && [ x"${1}" != x"debian" ] ; then
    echo "Unsupport platform: ${1}, it must be debian or ubuntu"
    exit 1
fi

CUR_DIR=$(cd `dirname $0`; pwd)

MAJOR="5.7"
VERSION="${MAJOR}.18"
TAR_FILENAME="mysql-community_${VERSION}.orig.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

DSC_FILE=mysql-community_${VERSION}-1${TARGET}${OS_VERSION}.dsc
DEBIAN_FILE=mysql-community_${VERSION}-1${TARGET}${OS_VERSION}.debian.tar.xz

if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
    wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME} http://repo.mysql.com/apt/${TARGET}/pool/mysql-${MAJOR}/m/mysql-community/${TAR_FILENAME}
    wget -O ${CUR_DIR}/${SRC}/${DSC_FILE} http://repo.mysql.com/apt/${TARGET}/pool/mysql-${MAJOR}/m/mysql-community/${DSC_FILE}
    wget -O ${CUR_DIR}/${SRC}/${DEBIAN_FILE} http://repo.mysql.com/apt/${TARGET}/pool/mysql-${MAJOR}/m/mysql-community/${DEBIAN_FILE}
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${TAR_FILENAME} ${TARGET}
