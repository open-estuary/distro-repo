#!/bin/bash

echo "Not supported yet"
exit 1

CUR_DIR=$(cd `dirname $0`; pwd)

SRC_DIR=src-java

VERSION="3.1.4"

if [ ! -f ${CUR_DIR}/${SRC_DIR}/cassandra-java-driver-$VERSION-1.fc27.src.rpm ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi
    wget -O ${CUR_DIR}/${SRC_DIR}/cassandra-java-driver-$VERSION-1.fc27.src.rpm http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/c/cassandra-java-driver-$VERSION-1.fc27.src.rpm
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio cassandra-java-driver-$VERSION-1.fc27.src.rpm | cpio -div
    popd > /dev/null
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR}  cassandra-java-driver.spec
