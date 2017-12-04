#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="0.3"
TAR_FILENAME="bcc-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
	cd ${CUR_DIR}/src
        git clone https://github.com/iovisor/bcc.git
        mv bcc bcc-${VERSION}
        tar -zcvf bcc-${VERSION}.tar.gz bcc-${VERSION}
        rm -rf bcc-${VERSION}
        cd -

fi
#sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/bcc.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src bcc_v500.spec

