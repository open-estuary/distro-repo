#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.8.2"
RPM_SRC_FILE="mongo-c-driver-1.8.2-1.fc28.src.rpm"

SRC_DIR=src-c

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/m/${RPM_SRC_FILE}
fi

pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
rpm2cpio ${RPM_SRC_FILE} | cpio -div
popd > /dev/null


#rm ${CUR_DIR}/${SRC_DIR}/mongo-c-driver-${VERSION}.tar.gz
#wget -O ${CUR_DIR}/${SRC_DIR}/mongo-c-driver-${VERSION}.tar.gz https://github.com/mongodb/mongo-c-driver/releases/download/${VERSION}/mongo-c-driver-${VERSION}.tar.gz


#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/mongo-c-driver.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} mongo-c-driver.spec
