#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.3"
#RPM_SRC_FILE="jmeter3-${VERSION}-13.fc26.src.rpm"
RPM_SRC_FILE="apache-jmeter-${VERSION}.tgz"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://mirrors.tuna.tsinghua.edu.cn/apache//jmeter/binaries/${RPM_SRC_FILE}
    #pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    #rpm2cpio ${RPM_SRC_FILE} | cpio -div
    #popd > /dev/null
fi


#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/jmeter.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} jmeter.spec
