
#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.3"
TAR_FILENAME="tiptop-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://tiptop.gforge.inria.fr/releases/tiptop-2.3.tar.gz 
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/tiptop.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src tiptop.spec
