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

MAJOR="3.4"
VERSION="${MAJOR}.6"
SUFFIX="-rc0"
TAR_FILENAME="mongo-tools-${VERSION}${SUFFIX}.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

NEW_TAR_FILENAME="mongo-tools_${VERSION}.tar.gz"
if [ ! -f ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME} ] ; then
    if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
        wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}   https://github.com/mongodb/mongo-tools/archive/r${VERSION}${SUFFIX}.tar.gz
    fi

    pushd ${CUR_DIR}/${SRC} > /dev/null
    tar -zxvf ${TAR_FILENAME}
    mv mongo-tools-r${VERSION}${SUFFIX} mongo-tools-${VERSION}
    tar -zcvf ${NEW_TAR_FILENAME} mongo-tools-${VERSION}
    rm -r mongo-tools-r${VERSION}${SUFFIX}
    rm -r mongo-tools-${VERSION}
    rm ${TAR_FILENAME}
    popd > /dev/null
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${NEW_TAR_FILENAME} ${TARGET}
