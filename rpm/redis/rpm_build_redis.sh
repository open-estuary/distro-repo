#!/bin/bash

CUR_DIR="$(cd `dirname $0`; pwd)"
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

RPM_SRC_FILE="redis-4.0.2-2.fc28.src.rpm"
SUB_DIR="r"
SRC_DIR=src-redis

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/${SUB_DIR}/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi


${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} redis.spec
