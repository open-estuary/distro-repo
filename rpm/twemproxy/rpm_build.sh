#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="0.4.1"
RPM_SRC_FILE="twemproxy-0.4.1-0.el7.src.rpm"
#RPM_SRC_FILE="v0.4.1.tar.gz"

SRC_DIR=src
export GOPATH=${CUR_DIR}/${SRC_DIR}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.marmotte.net/rpms/redhat/el7/x86_64/twemproxy-0.4.1-0.el7/twemproxy-0.4.1-0.el7.src.rpm
   # wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://github.com/twitter/twemproxy/archive/v0.4.1.tar.gz
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#mv ${CUR_DIR}/${SRC_DIR}/v0.4.1.tar.gz ${CUR_DIR}/${SRC_DIR}/nutcracker-v0.4.1.tar.gz

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} twemproxy.spec
