#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.0"
TAR_FILENAME="dmidecode-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	cd ${CUR_DIR}/src/
	git clone git://git.savannah.nongnu.org/dmidecode.git
	mv dmidecode dmidecode-${VERSION}
	tar -zcvf dmidecode-${VERSION}.tar.gz dmidecode-${VERSION}
	rm -rf dmidecode-${VERSION}
	cd -
fi
sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/dmidecode.spec

${CUR_DIR}/../../utils/rpm_buildnew.sh  ${CUR_DIR}/src dmidecode.spec
