#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
RPM_SRC_FILE="master.zip"

SRC_DIR=src

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://github.com/jpetazzo/pipework/archive/master.zip
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} pipework.spec
