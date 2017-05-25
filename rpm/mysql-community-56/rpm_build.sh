#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

echo "Build MySQL 5.6 community version ..."
VERSION="5.6"
RPM_SRC_FILE="mysql-community-5.6.36-2.el7.src.rpm"

SRC_DIR=src${VERSION}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://repo.mysql.com/yum/mysql-${VERSION}-community/el/7/SRPMS/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/mysql.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} mysql.spec
