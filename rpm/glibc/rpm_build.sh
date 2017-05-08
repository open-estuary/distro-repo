#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

RPM_SRC_FILE="glibc-2.25.90-2.fc27.src.rpm"
SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/g/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

sudo cp ${CUR_DIR}/src/SUPPORTED /root/rpmbuild/SOURCES/SUPPORTED
#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/glibc.spec

sudo ${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} glibc.spec arch=aarch64 without-testsuite without-bootstrap
