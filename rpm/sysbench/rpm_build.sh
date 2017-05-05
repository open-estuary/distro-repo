#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

MAJOR_VERSION="0"
RPM_SRC_FILE="sysbench-0.5-6.generic.src.rpm"

#MAJOR_VERSION="1"
#RPM_SRC_FILE="sysbench-1.0.2-1.generic.src.rpm"

SRC_DIR=src${MAJOR_VERSION}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://repo.percona.com/centos/6/SRPMS/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/sysbench.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} sysbench.spec
