#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.0"
TAR_FILENAME="eureka-""${VERSION}"".jar"
TAR_DIRNAME="eureka-""${VERSION}"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	git clone git@github.com:zhouxingchen1993/discovery.git  ${CUR_DIR}/src/eureka
fi

cd ${CUR_DIR}/src/eureka/discovery-service

mvn clean package

cd ../../

#mkdir "eureka-""${VERSION}"
mkdir ${TAR_DIRNAME}

#cp ./eureka/discovery-service/target/eureka-server-0.0.1-SNAPSHOT.jar ./"eureka-""${VERSION}"/"eureka-""${VERSION}"".jar"
cp ./eureka/discovery-service/target/eureka-server-0.0.1-SNAPSHOT.jar ./${TAR_DIRNAME}/${TAR_FILENAME}

#tar -zcvf eureka-1.0.tar.gz "eureka-""${VERSION}"
tar -zcvf eureka-1.0.tar.gz ${TAR_DIRNAME}

rm -rf eureka

cd ..

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src eureka.spec

