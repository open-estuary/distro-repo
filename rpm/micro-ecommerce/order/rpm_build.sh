#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
TAR_FILENAME="order-""${VERSION}"".jar"
TAR_DIRNAME="order-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:zhouxingchen1993/discovery.git  ${CUR_DIR}/src/ecommerce
fi

cd ${CUR_DIR}/src/ecommerce/order-service

mvn clean package

cd ../../

mkdir ${TAR_DIRNAME}

cp ./ecommerce/order-service/target/order-0.0.1-SNAPSHOT.jar ./${TAR_DIRNAME}/${TAR_FILENAME}

tar -zcvf order-1.0.tar.gz ${TAR_DIRNAME}

rm -rf ecommerce

cd ..

${CUR_DIR}/../../../utils/rpm_build.sh  ${CUR_DIR}/src order.spec

