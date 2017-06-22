#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

#sudo yum install -y devtoolset-4-gcc
#sudo yum install -y devtoolset-4-gcc-c++
#sudo yum install -y devtoolset-4-libstdc++-devel
#source /opt/rh/devtoolset-4/enable

#export PATH=/opt/rh/devlibset-4/root/usr/bin/:$PATH

sudo yum erase -y openssl
sudo yum erase -y openssl-devel

VERSION="5.6.32"
TAR_FILENAME="AliSQL-${VERSION}-5.tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/alibaba/AliSQL/archive/${TAR_FILENAME}
fi

#if [ ! -f ${CUR_DIR}/src/alisql.spec ] ; then
#    wget -O ${CUR_DIR}/src/alisql.spec https://raw.githubusercontent.com/alibaba/AliSQL/master/packaging/rpm-sles/alisql.spec.in
#fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/alisql.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src alisql.spec
