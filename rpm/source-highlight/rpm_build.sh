
#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.1.8"
NAME="source-highlight"
TAR_FILENAME="${NAME}-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} ftp://ftp.gnu.org/gnu/src-highlite/${NAME}-${VERSION}.tar.gz  
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME}.sig ftp://ftp.gnu.org/gnu/src-highlite/${NAME}-${VERSION}.tar.gz.sig
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/${NAME}.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src ${NAME}.spec
