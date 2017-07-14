#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum erase -y python34
sudo yum install -y devtoolset-4-runtime
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel

source /opt/rh/devtoolset-4/enable

VERSION="1.0.3"
RPM_SRC_FILE="cockroach-0-0.1.gita724578.fc23.src.rpm"

SRC_DIR=src

if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
    mkdir -p ${CUR_DIR}/${SRC_DIR}
fi

TAR_FILE_NAME="cockroach-v${VERSION}.src.tgz"

if [ ! -f "${CUR_DIR}/${SRC_DIR}/${TAR_FILE_NAME}" ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${TAR_FILE_NAME} https://binaries.cockroachdb.com/${TAR_FILE_NAME}
fi

#if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
#    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://kenjiro.fedorapeople.org/copr/${RPM_SRC_FILE}
#    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
#    rpm2cpio ${RPM_SRC_FILE} | cpio -div
#    popd > /dev/null
#fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/cockroach.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} cockroach.spec
