#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
TAR_FILENAME="api-""${VERSION}"".jar"
TAR_DIRNAME="api-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:zhouxingchen1993/discovery.git  ${CUR_DIR}/src/ecommerce
fi

cd ${CUR_DIR}/src/ecommerce/apigateway-service

mvn clean package

cd ../../

mkdir ${TAR_DIRNAME}

cp ./ecommerce/apigateway-service/target/api-gateway.jar ./${TAR_DIRNAME}/${TAR_FILENAME}

tar -zcvf api-1.0.tar.gz ${TAR_DIRNAME}

rm -rf ecommerce

cd ..

${CUR_DIR}/../../../utils/rpm_build.sh  ${CUR_DIR}/src api.spec

