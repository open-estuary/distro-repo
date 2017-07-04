#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

TARGETOS=ubuntu
if [ $# -eq 0 ];then
        TARGETOS=ubuntu
elif [ $# -eq 1 ];then
        TARGETOS=$1
else
        usage
        exit 1
fi

VERSION="1.0"
TAR_FILENAME="scl-utils_1.0.tar.gz"

SRC_DIR=src

#Remove unused files
#rm ${CUR_DIR}/${SRC_DIR}/*.rpm

${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/${SRC_DIR}  ${TAR_FILENAME} ${TARGETOS}
