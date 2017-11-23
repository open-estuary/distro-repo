#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="7.1.0"
RPM_SRC_FILE="solr-${VERSION}.tgz"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://mirror.bit.edu.cn/apache/lucene/solr/${VERSION}/${RPM_SRC_FILE}
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} solr.spec
