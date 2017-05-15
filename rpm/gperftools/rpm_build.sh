#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.5"
RPM_SRC_FILE="gperftools-${VERSION}.tar.gz"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://github.com/gperftools/gperftools/releases/download/gperftools-${VERSION}/${RPM_SRC_FILE}
    tar -xzf ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} -C ${CUR_DIR}/${SRC_DIR}
fi

if [ -z "$(cat ${CUR_DIR}/${SRC_DIR}/gperftools-${VERSION}/packages/rpm/rpm.spec | grep "define NAME gperftools")" ] ; then
    sed -i '1i\\%define NAME gperftools'  ${CUR_DIR}/${SRC_DIR}/gperftools-${VERSION}/packages/rpm/rpm.spec
fi

if [ -z "$(cat ${CUR_DIR}/${SRC_DIR}/gperftools-${VERSION}/packages/rpm/rpm.spec | grep "define VERSION 2\.5")" ] ; then
    sed -i '1i\\%define VERSION 2.5' ${CUR_DIR}/${SRC_DIR}/gperftools-${VERSION}/packages/rpm/rpm.spec
fi

#cp ${CUR_DIR}/${SRC_DIR}/gperftools-${VERSION}/packages/rpm/rpm.spec ${CUR_DIR}/${SRC_DIR}/rpm.spec
${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} rpm.spec 
