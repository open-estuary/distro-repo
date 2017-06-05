#!/bin/bash

echo "Currently we should try to avoid maintain libtool directly"
exit 0

CUR_DIR=$(cd `dirname $0`; pwd)

MAJOR_VERSION="2.4.6"
RPM_SRC_FILE="libtool-2.4.6-13.fc24.src.rpm"

SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/updates/24/SRPMS/l/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/libtool.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} libtool.spec arch=aarch64
