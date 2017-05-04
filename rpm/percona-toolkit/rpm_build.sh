#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

RPM_SRC_FILE="percona-toolkit-3.0.2-1.src.rpm"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://repo.percona.com/centos/6/SRPMS/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/percona-toolkit.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} percona-toolkit.spec
