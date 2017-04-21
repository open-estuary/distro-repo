#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.20"
TAR_FILENAME="leveldb-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/google/leveldb/archive/v${VERSION}.tar.gz
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/leveldb.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src leveldb.spec
