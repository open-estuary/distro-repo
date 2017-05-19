#!/bin/bash

NEED_BUILD=0
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="2.8.2"
RPM_SRC_FILE="log4j-${VERSION}-1.fc27.src.rpm"
RPM_FILE="log4j-${VERSION}-1.fc27.noarch.rpm"

if [ ! -f ~/rpmbuild/RPMS/noarch/${RPM_FILE} ] ; then
    wget -O ~/rpmbuild/RPMS/noarch/${RPM_FILE}  ftp://195.220.108.108/linux/fedora-secondary/development/rawhide/Everything/aarch64/os/Packages/l/${RPM_FILE}
    ${CUR_DIR}/../../utils/rpm_sign.sh ~/rpmbuild/RPMS/noarch/
fi

