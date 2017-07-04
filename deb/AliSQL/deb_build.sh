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

MAJOR="5.6"
VERSION="${MAJOR}.32"
TAR_FILENAME="AliSQL-${VERSION}-5.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

NEW_TAR_FILENAME="alisql_5.6.32.tar.gz"
if [ ! -f ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME} ] ; then
    if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
        wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}   https://github.com/alibaba/AliSQL/archive/${TAR_FILENAME}
    fi

    pushd ${CUR_DIR}/${SRC} > /dev/null
    tar -zxvf ${TAR_FILENAME}
    mv AliSQL-AliSQL-${VERSION}-5 alisql-${VERSION}
    tar -zcvf ${NEW_TAR_FILENAME} alisql-${VERSION}
    rm -r AliSQL-AliSQL-${VERSION}-5
    rm -r alisql-${VERSION}
    rm ${TAR_FILENAME}
    popd > /dev/null
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${NEW_TAR_FILENAME} ${TARGET}
