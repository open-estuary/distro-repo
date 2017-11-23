#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum install -y devtoolset-4-gcc
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel

#source /opt/rh/devtoolset-4/enable

VERSION="5.0.0"
RPM_SRC_FILE="compiler-rt-5.0.0-1.fc28.src.rpm"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/c/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/glibc.spec


if [ ${BUILD_DEVTOOL} -eq 1 ] ; then
    mv compiler-rt_scl.spec compiler-rt.spec
fi
SPECFILE="clang.spec"

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} ${SPECFILE} 

