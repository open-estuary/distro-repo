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

MAJOR="2.25"
VERSION="${MAJOR}"
TAR_FILENAME="glibc-${MAJOR}.tar.gz"
SRC=src-${TARGET}

if [ ! -d "${SRC}" ] ; then
    mkdir -p ${SRC}
fi

NEW_ORIG_NAME="devlibset-4-glibc_2.25.orig.tar.gz"
if [ ! -f ${CUR_DIR}/${SRC}/${NEW_ORIG_NAME} ] ; then
    if [ ! -f ${CUR_DIR}/${SRC}/${TAR_FILENAME} ] ; then
       wget -O ${CUR_DIR}/${SRC}/${TAR_FILENAME}  https://ftp.gnu.org/gnu/glibc/${TAR_FILENAME}
    fi
    mv ${CUR_DIR}/${SRC}/${TAR_FILENAME}  ${CUR_DIR}/${SRC}/${NEW_ORIG_NAME}
fi

#Ignore tests because some test cases will fail on Docker 
${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC} ${NEW_ORIG_NAME} ${TARGET} "nocheck"
