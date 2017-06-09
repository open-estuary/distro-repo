#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

SRC_RPM_FILE=devtoolset-6-6.0-6.el7.src.rpm
SRC_DIR=src
if [ ! -f ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi
    wget -O ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} http://vault.centos.org/centos/7/sclo/Source/rh/devtoolset-6/${SRC_RPM_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${SRC_RPM_FILE} | cpio -div
    popd > /dev/null
fi

${CUR_DIR}/../../../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR}  devtoolset-6.spec
