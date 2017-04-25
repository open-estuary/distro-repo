#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.5.37"
TAR_FILENAME="ceph-deploy-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/ceph/ceph-deploy/archive/v${VERSION}.tar.gz
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/ceph-deploy.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src ceph-deploy.spec
