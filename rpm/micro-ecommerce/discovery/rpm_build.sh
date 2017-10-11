#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
TAR_DIRNAME="eureka-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:zhouxingchen1993/service-code.git  ${CUR_DIR}/src/${TAR_DIRNAME}
fi

cd ${CUR_DIR}/src/

#tar -zcvf eureka-1.0.tar.gz "eureka-""${VERSION}"

#cd ..

#cd ${CUR_DIR}/src/eureka/discovery-service

#mvn clean package

#cd ../../

#mkdir ${TAR_DIRNAME}

#cp ./eureka/discovery-service/target/eureka-server-0.0.1-SNAPSHOT.jar ./${TAR_DIRNAME}/${TAR_FILENAME}

tar -zcvf eureka-1.0.tar.gz ${TAR_DIRNAME}

#rm -rf eureka

cd ..

${CUR_DIR}/../../../utils/rpm_build.sh  ${CUR_DIR}/src eureka.spec

