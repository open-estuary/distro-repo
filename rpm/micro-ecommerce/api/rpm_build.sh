#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
TAR_DIRNAME="api-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:zhouxingchen1993/service-code.git  ${CUR_DIR}/src/${TAR_DIRNAME}
fi

cd ${CUR_DIR}/src/

tar -zcvf api-1.0.tar.gz ${TAR_DIRNAME}

cd ..

${CUR_DIR}/../../../utils/rpm_build.sh  ${CUR_DIR}/src api.spec

