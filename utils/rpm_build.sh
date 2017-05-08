#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)
echo "Begin to build RPM Packages for aarch64 platform"

if [ -d ~/rpmbuild/RPMS ] ; then
    echo "Previous RPM build still exists, so it might be necessary to clear them before building new one"
fi 

if [ "$(uname -m)" != "aarch64" ] ; then
    echo "Please build this package on arm64 platform"
    exit 1
fi

if [ -z "$(which rpmsign 2>/dev/null)" ] ; then
    sudo yum install rpm-sign
fi

SRC_DIR=$1
SPEC_FILE=$2

if [ ! -d ${SRC_DIR} ] ; then
    echo "${SRC_DIR} directory does not exist !"
    exit 1
fi

sudo yum-builddep -y ${SRC_DIR}/${SPEC_FILE}
rpmbuild -D"_sourcedir ${SRC_DIR}" -D"_specdir ${SRC_DIR}" -D"_srcrpmdir ${SRC_DIR}" -ba ${SRC_DIR}/${SPEC_FILE} ${@:3}
${CUR_DIR}/rpm_sign.sh ~/rpmbuild/RPMS/
${CUR_DIR}/rpm_sign.sh ${SRC_DIR}

echo "Please check *.src.rpm under ${SRC_DIR} directory !"
echo "Please check other rpm under ~/rpmbuild/RPMS/aarch64/ directory !"

