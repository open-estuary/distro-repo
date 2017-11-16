#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.6"
TAR_FILENAME="Mycat-server-1.6-RELEASE-20161028204710-linux.tar.gz"

WRAPPER_VERSION="3.5.34"
WRAPPER_FILENAME="Wrapper_3.5.34_20170927/wrapper_3.5.34_src.tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://dl.mycat.io/1.6-RELEASE/Mycat-server-1.6-RELEASE-20161028204710-linux.tar.gz
fi

if [ ! -f ${CUR_DIR}/src/${WRAPPER_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${WRAPPER_FILENAME}   https://sourceforge.net/projects/wrapper/files/wrapper_src/Wrapper_3.5.34_20170927/wrapper_3.5.34_src.tar.gz
fi

${CUR_DIR}/../../utils/rpm_build.sh ${CUR_DIR}/src mycat.spec

