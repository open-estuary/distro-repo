#!/bin/bash

BUILD_DEVTOOL_GCC=1
CUR_DIR=$(cd `dirname $0`; pwd)

sudo yum install -y devtoolset-4-gcc
sudo yum install -y devtoolset-4-gcc-c++
sudo yum install -y devtoolset-4-libstdc++-devel

source /opt/rh/devtoolset-4/enable

RPM_SRC_FILE="glibc-2.26.9000-27.fc28.src.rpm"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/g/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

sudo cp ${CUR_DIR}/src/SUPPORTED /root/rpmbuild/SOURCES/SUPPORTED
#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/glibc.spec


if [ ${BUILD_DEVTOOL_GCC} -eq 0 ] ; then
    SPECFILE="glibc_raw.spec"
else 
    SPECFILE="glibc.spec"
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} ${SPECFILE} arch=aarch64 without-testsuite without-bootstrap
