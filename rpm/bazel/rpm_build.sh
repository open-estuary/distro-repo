#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum install -y devtoolset-4-gcc
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel
#source /opt/rh/devtoolset-4/enable

#export PATH=/opt/rh/devlibset-4/root/usr/bin/:$PATH

VERSION="0.4.5"
RPM_SRC_FILE="bazel-${VERSION}-1.el7.centos.src.rpm"

SRC_DIR=src
if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
    mkdir -p ${CUR_DIR}/${SRC_DIR}
fi

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://people.centos.org/tru/bazel-centos7/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null 
fi

sudo ${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} bazel.spec
