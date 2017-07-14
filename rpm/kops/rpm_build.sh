#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum erase -y python34
sudo yum install -y devtoolset-4-runtime
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel

source /opt/rh/devtoolset-4/enable

VERSION="1.6.2"
RPM_SRC_FILE="kops-${VERSION}.tar.gz"

SRC_DIR=src

if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
    mkdir -p ${CUR_DIR}/${SRC_DIR}
fi

#if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
#    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://github.com/kubernetes/kops/archive/${VERSION}.tar.gz
#fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/kops.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} kops.spec
