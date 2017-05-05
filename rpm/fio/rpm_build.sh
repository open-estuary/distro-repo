#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.19"
RPM_SRC_FILE="fio-${VERSION}.tar.bz2"

sudo yum install librbd librbd-devel

SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://brick.kernel.dk/snaps/fio-${VERSION}.tar.bz2
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/fio.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} fio.spec
