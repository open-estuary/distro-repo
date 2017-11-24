#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum install -y devtoolset-4-gcc
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel

#source /opt/rh/devtoolset-4/enable

RPM_SRC_FILE="python-lit-0.5.1-1.fc28.src.rpm"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/p/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

mv src/python-lit_real.spec src/python-lit.spec
SPECFILE="python-lit.spec"

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} ${SPECFILE} ${BUILD_DEVTOOL} 

