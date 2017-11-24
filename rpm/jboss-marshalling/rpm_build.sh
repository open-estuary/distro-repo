#!/bin/bash

NEED_BUILD=0
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

if [ ! -z "${2}" ] ; then
    NEED_BUILD=$2
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.4.11"
RPM_FILE="jboss-marshalling-${VERSION}-3.fc27.noarch.rpm"

if [ "${NEED_BUILD}" == "0" ] ; then
    echo "Download no-arch rpm packages directly !"
    sudo wget -O ~/rpmbuild/RPMS/noarch/${RPM_FILE}  ftp://195.220.108.108/linux/fedora-secondary/development/rawhide/Everything/aarch64/os/Packages/j/${RPM_FILE}
    ${CUR_DIR}/../../utils/rpm_resign.sh ~/rpmbuild/RPMS/noarch/
    exit 0
fi

echo "Try to build from source ..."
VERSION="1.4.6"
RPM_SRC_FILE="jboss-marshalling-${VERSION}-2.el7.src.rpm"
SUB_DIR="j"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://cbs.centos.org/kojifiles/packages/jboss-marshalling/1.4.6/2.el7/src/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

sudo yum install -y maven-shade-plugin

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/jboss-marshalling.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} jboss-marshalling.spec
