#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="0.4"
TAR_FILENAME="ktap-""${VERSION}"".tar.bz2"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	cd ${CUR_DIR}/src
	git clone https://github.com/ktap/ktap.git
	mv ktap ktap-${VERSION}
	tar -jcvf ktap-${VERSION}.tar.bz2 ktap-${VERSION}
	rm -rf ktap-${VERSION}
	cd -
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/ktap_v500.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src ktap_v500.spec

