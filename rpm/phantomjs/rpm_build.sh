#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.1.1"
RPM_SRC_FILE="phantomjs-2.1.1-1.el7.adsecure1.src.rpm"

SRC_DIR=src
export GOPATH=${CUR_DIR}/${SRC_DIR}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} wget http://dl.marmotte.net/rpms/redhat/el7/x86_64/phantomjs-2.1.1-1.el7.adsecure1/phantomjs-2.1.1-1.el7.adsecure1.src.rpm
    
pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi


${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} phantomjs.spec
