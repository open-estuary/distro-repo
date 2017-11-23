#!/bin/bash

NEED_BUILD=0
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="1.1.2"
RPM_SRC_FILE="cli-parser-${VERSION}-7.fc26.src.rpm"
RPM_FILE="cli-parser-${VERSION}-7.fc26.noarch.rpm"

SUB_DIR="c"

if [ ! -f ~/rpmbuild/RPMS/noarch/${RPM_FILE} ] ; then
    sudo wget -O ~/rpmbuild/RPMS/noarch/${RPM_FILE}  ftp://195.220.108.108/linux/fedora-secondary/development/rawhide/Everything/aarch64/os/Packages/${SUB_DIR}/${RPM_FILE}
    ${CUR_DIR}/../../utils/rpm_resign.sh ~/rpmbuild/RPMS/noarch/
    exit 0
fi


