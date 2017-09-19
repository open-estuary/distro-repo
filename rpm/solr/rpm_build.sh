#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="6.6.1"
#RPM_SRC_FILE="solr3-${VERSION}-13.fc26.src.rpm"
RPM_SRC_FILE="solr-${VERSION}.tgz"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 
    
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://mirror.bit.edu.cn/apache/lucene/solr/${VERSION}/${RPM_SRC_FILE}
    #wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/s/${RPM_SRC_FILE}
    #pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    #rpm2cpio ${RPM_SRC_FILE} | cpio -div
    #popd > /dev/null
fi


#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/solr.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} solr.spec
