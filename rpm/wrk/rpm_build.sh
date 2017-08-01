#!/bin/bash

TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="4.0.2"
RPM_SRC_FILE="wrk-${VERSION}.tar.gz"
LUA_JIT_SRC="LuaJIT-2.1.0-beta3.tar.gz"

SRC_DIR=src
export GOPATH=${CUR_DIR}/${SRC_DIR}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
        mkdir -p ${CUR_DIR}/${SRC_DIR}
    fi 

    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} https://github.com/wg/wrk/archive/4.0.2.tar.gz
    wget -O ${CUR_DIR}/${SRC_DIR}/${LUA_JIT_SRC} https://github.com/LuaJIT/LuaJIT/archive/v2.1.0-beta3.tar.gz

    #pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    #rpm2cpio ${RPM_SRC_FILE} | cpio -div
    #popd > /dev/null
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} wrk.spec
