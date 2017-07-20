#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="0.12.0"
TAR_FILENAME="ycsb-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/brianfrankcooper/YCSB/archive/${VERSION}.tar.gz
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/YCSB.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src ycsb.spec
