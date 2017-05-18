#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.4.1"
RPM_SRC_FILE="javapackages-tools-${VERSION}-11.el7.src.rpm"

SUB_DIR="j"
SRC_DIR=src-3.4

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://cbs.centos.org/kojifiles/packages/javapackages-tools/3.4.1/11.el7/src/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi


#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/javapackages-tools.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} javapackages-tools.spec
