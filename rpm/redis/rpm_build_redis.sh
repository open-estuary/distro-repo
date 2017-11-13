#!/bin/bash

CUR_DIR="$(cd `dirname $0`; pwd)"
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

VERSION="4.0.2"
RPM_SRC_FILE="redis-${VERSION}-1.fc28.src.rpm"
SUB_DIR="r"
SRC_DIR=src-redis

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/${SUB_DIR}/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#replace redis version to 4.0.2
VERSION="4.0.2"
sed -i "s/Version\:\ .*/Version\:\ \ \ \ \ \ \ \ \ \ \ ${VERSION}/g" ${CUR_DIR}/${SRC_DIR}/redis.spec

#download redis 4.0.2 package
REDIS_PACKAGE_FILE="redis-${VERSION}.tar.gz"
if [ ! -f ${CUR_DIR}/${SRC_DIR}/${REDIS_PACKAGE_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${REDIS_PACKAGE_FILE}  http://download.redis.io/releases/${REDIS_PACKAGE_FILE}
fi 

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} redis.spec
