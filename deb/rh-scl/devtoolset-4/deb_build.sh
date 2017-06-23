#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

TARGETOS=ubuntu
if [ $# -eq 0 ];then
        TARGETOS=ubuntu
elif [ $# -eq 1 ];then
        TARGETOS=$1
else
        usage
        exit 1
fi

VERSION="4.0"
TAR_FILENAME="devtoolset-4_4.0.tar.gz"

SRC_RPM_FILE="devtoolset-4-4.0-9.el7.src.rpm"
SRC_DIR=src
#Disabl download so far
if [ -f ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi
    wget -O ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} http://vault.centos.org/centos/7/sclo/Source/rh/devtoolset-4/${SRC_RPM_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${SRC_RPM_FILE} | cpio -div
    popd > /dev/null
fi

#Remove unused files
#rm ${CUR_DIR}/${SRC_DIR}/*.rpm

${CUR_DIR}/../../../utils/deb_build.sh  ${CUR_DIR}/${SRC_DIR}  ${TAR_FILENAME} ${TARGETOS}
