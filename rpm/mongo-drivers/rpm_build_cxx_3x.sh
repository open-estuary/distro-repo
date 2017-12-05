#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.1.1"
RPM_SRC_FILE="mongo-cxx-driver-r${VERSION}-tar.gz"

SRC_DIR=src-cxx-3x

if [ ! -f ${CUR_DIR}/${SRC_DIR}/r${VERSION}.tar.gz ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/r${VERSION}.tar.gz https://github.com/mongodb/mongo-cxx-driver/archive/r${VERSION}.tar.gz
fi

#CXX driver relies on C-driver
#sudo yum install -y mongo-c-driver
#sudo yum install -y mongo-c-driver-devel
#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/mongo-cxx-driver.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} mongo-cxx-driver.spec
