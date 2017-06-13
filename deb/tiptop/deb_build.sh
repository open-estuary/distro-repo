#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.3"
TAR_FILENAME="tiptop-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://tiptop.gforge.inria.fr/releases/tiptop-2.3.tar.gz
fi

#${CUR_DIR}/../../utils/deb_build.sh  ${CUR_DIR}/src ${TAR_FILENAME}

