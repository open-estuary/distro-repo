
#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

RPMVERSION="4.9.20"
PKGRELEASE="3.1.rc1"
TAR_FILENAME="kernel-""${RPMVERSION}""-""$PKGRELEASE"".tar.gz"

#if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    #sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://tiptop.gforge.inria.fr/releases/tiptop-2.3.tar.gz 
#fi

sed -i "s/define\ rpmversion\ .*/define\ rpmversion\ ${RPMVERSION}/g" ${CUR_DIR}/src/kernel-aarch64.spec
sed -i "s/define\ pkgrelease\ .*/define\ pkgrelease\ ${PKGRELEASE}/g" ${CUR_DIR}/src/kernel-aarch64.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src kernel-aarch64.spec
