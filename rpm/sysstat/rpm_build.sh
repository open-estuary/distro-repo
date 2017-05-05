
#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="11.5.5"
TAR_FILENAME="sysstat-""${VERSION}"".tar.gz"

if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://pagesperso-orange.fr/sebastien.godard/${TAR_FILENAME}
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/sysstat.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src sysstat.spec
