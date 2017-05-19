
#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="3.1"
TAR_FILENAME="systemtap-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} https://sourceware.org/systemtap/ftp/releases/${TAR_FILENAME}
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/systemtap.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src systemtap.spec
