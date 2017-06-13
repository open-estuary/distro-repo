#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="7.1.7"
TAR_FILENAME="crash-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
        sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://github.com/crash-utility/crash/archive/${VERSION}.tar.gz 
fi

#${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/src ${TAR_FILENAME} debian 
