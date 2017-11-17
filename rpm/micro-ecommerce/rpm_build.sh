#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.0"
TAR_DIRNAME="micro-service-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:open-estuary/packages.git  ${CUR_DIR}/src/package

	#git clone git@github.com:zhouxingchen1993/packages.git  ${CUR_DIR}/src/package

	pushd src/package/solutions > /dev/null

	mv e-commerce-springcloud-microservices ${TAR_DIRNAME}

	tar -zcvf ${TAR_DIRNAME}.tar.gz ${TAR_DIRNAME}

	mv ${TAR_DIRNAME}.tar.gz ../../${TAR_DIRNAME}.tar.gz

	popd > /dev/null

fi
${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src micro-service.spec
