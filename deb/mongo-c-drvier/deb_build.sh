#!/bin/bash

echo "Not necessary to implement yet"
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

MAJOR="1.6"
VERSION="${MAJOR}.3"
SUFFIX=""
TAR_FILENAME="mongo-c-driver-${VERSION}${SUFFIX}.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

NEW_TAR_FILENAME="libmongoc_${VERSION}.tar.gz"
if [ ! -f ${CUR_DIR}/${SRC}/${NEW_TAR_FILENAME} ] ; then
    if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
        wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}   https://github.com/mongodb/mongo-c-driver/archive/${VERSION}${SUFFIX}.tar.gz
    fi

    LIBBSON_TAR_FILE="libbson-${VERSION}.tar.gz" 
    pushd ${CUR_DIR}/${SRC} > /dev/null

    wget -O ${LIBBSON_TAR_FILE} https://github.com/mongodb/libbson/archive/1.6.3.tar.gz
    tar -zxvf ${TAR_FILENAME}
    mv mongo-c-driver-${VERSION} libmongoc-${VERSION}
    #tar -xzvf ${LIBBSON_TAR_FILE} -C libmongoc-${VERSION}/src/
    rm -fr libmongoc-${VERSION}/src/libbson
    mv libmongoc-${VERSION}/src/libbson-${VERSION} libmongoc-${VERSION}/src/libbson
    tar -zcvf ${NEW_TAR_FILENAME} libmongoc-${VERSION}
    rm -r libmongoc-${VERSION}
    rm ${TAR_FILENAME}
    rm ${LIBBSON_TAR_FILE}
    popd > /dev/null
fi

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${NEW_TAR_FILENAME} ${TARGET}
