#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

MAJOR_VERSION="56"
RPM_SRC_FILE="Percona-Server-56-5.6.35-rel81.0.generic.src.rpm"

SRC_DIR=src${MAJOR_VERSION}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://repo.percona.com/centos/6/SRPMS/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/percona-server.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} percona-server.spec
