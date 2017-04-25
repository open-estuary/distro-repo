#!/bin/bash

VERSION="5.0"

SRC_DIR=$1
TARGETOS=$2
DST_IP="117.78.41.188"
DST_USER="repo"

if [ -z "${TARGETOS}" ] ; then 
    echo "Usage: ./rpm_upload.sh <src_dir> <target os(such as CentOS/Ubuntu/Debian)>"
    exit 0
fi

# Verify that it must upload proper files
file_type=""
if [ "${TARGETOS}" == "CentOS" ] || [ "${TARGETOS}" == "centos" ] ; then
    file_type="rpm"
    TARGETOS="centos"
elif [ "${TARGETOS}" == "Ubuntu" ] || [ "${TARGETOS}" == "ubuntu" ] ; then
    file_type="deb"
    TARGETOS="ubuntu"
elif [ "${TARGETOS}" == "Debian" ] || [ "${TARGETOS}" == "debian" ] ; then
    file_type="deb"
    TARGETOS="debian"
else
    echo "Currently it only support CentOS, Ubuntu or Debian"
    exit 0
fi

if [ -z "$(find ${SRC_DIR} -name "*.${file_type}")" ] ; then
    echo "There is no ${file_type} files under ${SRC_DIR} for ${TARGETOS}"
    exit 0
fi


if [ ! -z "$(find ${SRC_DIR} -name "*.aarch64.${file_type}")" ] ; then
    DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/aarch64"
elif [ ! -z "$(find ${SRC_DIR} -name "*.noarch.${file_type}")" ] ; then
    DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/noarch"
elif [ ! -z "$(find ${SRC_DIR} -name "*.src.${file_type}")" ] ; then
    DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/SRPMS"
else 
    echo "It only support files which suffix is aarch64.rpm, noarch.rpm or src.rpm"
    exit 1
fi

scp -r ${SRC_DIR}/*.${file_type} ${DST_USER}@${DST_IP}:${DST_DIR}

