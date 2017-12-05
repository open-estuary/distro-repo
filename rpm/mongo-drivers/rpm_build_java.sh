#!/bin/bash
echo "Not support yet !"

exit 0

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.2.1"
RPM_SRC_FILE="mongo-java-driver-${VERSION}-3.fc26.src.rpm"

SRC_DIR=src-java

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/m/${RPM_SRC_FILE}
fi

pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
rpm2cpio ${RPM_SRC_FILE} | cpio -div
popd > /dev/null


#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/mongo-java-driver.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} mongo-java-driver.spec
