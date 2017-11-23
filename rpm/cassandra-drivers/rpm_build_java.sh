#!/bin/bash

echo "Not supported yet"
exit 1

CUR_DIR=$(cd `dirname $0`; pwd)

SRC_DIR=src-java

VERSION="3.1.4"
SRC_RPM_FILE="cassandra-java-driver-3.1.4-2.fc27.src.rpm"

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi
    wget -O ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/c/${SRC_RPM_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${SRC_RPM_FILE} | cpio -div
    popd > /dev/null
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR}  cassandra-java-driver.spec
