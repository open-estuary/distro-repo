#!/bin/bash

NEED_BUILD=0
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0.2"
RPM_SRC_FILE="maven-injection-plugin-1.0.2-17.fc27.src.rpm"
RPM_FILE="maven-injection-plugin-1.0.2-17.fc27.noarch.rpm"

if [ "${NEED_BUILD}" == "0" ] ; then
    wget -O ~/rpmbuild/RPMS/noarch/${RPM_FILE}  ftp://195.220.108.108/linux/fedora-secondary/development/rawhide/Everything/aarch64/os/Packages/m/${RPM_FILE}
    ${CUR_DIR}/../../utils/rpm_sign.sh ~/rpmbuild/RPMS/noarch/
    exit 0
fi

SUB_DIR="m"
SRC_DIR=src-injection-plugin
if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/${SUB_DIR}/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/maven-injection-plugin.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} maven-injection-plugin.spec --without=gradle
