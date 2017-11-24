#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum install -y devtoolset-4-gcc
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel
#source /opt/rh/devtoolset-4/enable

#export PATH=/opt/rh/devlibset-4/root/usr/bin/:$PATH

VERSION="0.8.0"
RPM_SRC_FILE="tensorflow-${VERSION}-2.alonid.el7.centos.src.rpm"

SRC_DIR=src
if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then
    mkdir -p ${CUR_DIR}/${SRC_DIR}
fi

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} http://copr-be.cloud.fedoraproject.org/results/alonid/tensorflow/epel-7-x86_64/00342448-tensorflow/${RPM_SRC_FILE}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null 
fi

if [ ! -f /usr/include/stropts.h ] ; then
    sudo touch /usr/include/stropts.h
fi

#Probably need to configure some parameters manually

rm -fr ~/.cache/bazel/
#rm -fr ~/rpmbuild/BUILD/tensorflow/
${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR} tensorflow.spec
