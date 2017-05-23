#!/bin/bash

CUR_DIR="$(cd `dirname $0`; pwd)"
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

VERSION="2.7.0"

RPM_SRC_FILE="cpp-driver-${VERSION}.tar.gz"
SRC_DIR=src-cpp

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE}  https://github.com/datastax/cpp-driver/archive/${VERSION}.tar.gz
    tar -zxvf ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} -C ${CUR_DIR}/${SRC_DIR}
fi

sudo yum install -y openssl-devel

#sed -i "s/${OLD_VERSION}/${NEW_VERSION}/g" ${CUR_DIR}/${SRC_DIR}/cassandra.spec
cd ${CUR_DIR}/${SRC_DIR}/"cpp-driver-${VERSION}"/packaging
./build_rpm.sh aarch64 

${CUR_DIR}/../../utils/rpm_sign.sh ${CUR_DIR}/${SRC_DIR}/cpp-driver-${VERSION}/packaging/build/SRPMS/
${CUR_DIR}/../../utils/rpm_sign.sh ${CUR_DIR}/${SRC_DIR}/cpp-driver-${VERSION}/packaging/build/RPMS/aarch64/

if [ ! -d ~/rpmbuild/SRPMS ] ; then
    mkdir -p ~/rpmbuild/SRPMS
fi

cp ${CUR_DIR}/${SRC_DIR}/cpp-driver-${VERSION}/packaging/build/SRPMS/* ~/rpmbuild/SRPMS/
cp ${CUR_DIR}/${SRC_DIR}/cpp-driver-${VERSION}/packaging/build/RPMS/aarch64/* ~/rpmbuild/RPMS/aarch64/
#${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} cassandra.spec
