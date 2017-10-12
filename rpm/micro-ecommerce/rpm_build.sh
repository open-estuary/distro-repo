#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
TAR_DIRNAME="micro-service-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:open-estuary/packages.git  ${CUR_DIR}/src/package
fi

pushd src/package/solutions > /dev/null

mv e-commerce-springcloud-microservices ${TAR_DIRNAME}

tar -zcvf ${TAR_DIRNAME}.tar.gz ${TAR_DIRNAME}

mv ${TAR_DIRNAME}.tar.gz ../../${TAR_DIRNAME}.tar.gz

popd > /dev/null

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src micro-service.spec

