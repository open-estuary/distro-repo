#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

RPM_SRC_FILE="cadvisor-0.22.2-2.fc25.src.rpm"

SRC_DIR=src${VERSION}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi

    #wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/c/${RPM_SRC_FILE}
    #pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    #rpm2cpio ${RPM_SRC_FILE} | cpio -div
    #popd > /dev/null
fi

LATEST_VERSION="v0.26.1"

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${LATEST_VERSION}.tar.gz ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${LATEST_VERSION}.tar.gz https://github.com/google/cadvisor/archive/${LATEST_VERSION}.tar.gz
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} cadvisor.spec
