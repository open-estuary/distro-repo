#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum erase -y python34
sudo yum install -y devtoolset-4-runtime
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel

source /opt/rh/devtoolset-4/enable

#VERSION="2.6.0"
#TAG="2.el7"
#RPM_SRC_FILE="grafana-${VERSION}-${TAG}.src.rpm"

VERSION="v4.4.1"
TAR_SRC_FILE="grafana-${VERSION}.tar.gz"


SRC_DIR=src

if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
    mkdir -p ${CUR_DIR}/${SRC_DIR}
fi

#if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
#    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://cbs.centos.org/kojifiles/packages/grafana/$VERSION/$TAG/src/${RPM_SRC_FILE}
#    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
#    rpm2cpio ${RPM_SRC_FILE} | cpio -div
#    popd > /dev/null
#fi

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${TAR_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${TAR_SRC_FILE} https://github.com/grafana/grafana/archive/${VERSION}.tar.gz
fi

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} grafana.spec
