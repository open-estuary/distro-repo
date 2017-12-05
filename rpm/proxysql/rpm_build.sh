#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#Proxysql needs gcc-5, so it will use gcc-5 from devtoolset-4 
#sudo yum install -y devtoolset-4-gcc
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel

#source /opt/rh/devtoolset-4/enable

RPM_SRC_FILE="proxysql-1.3.5-1.1.src.rpm"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://repo.percona.com/centos/6/SRPMS/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/proxysql.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} proxysql.spec
