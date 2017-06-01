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

upload_files_repo() {
    filelist=$1
    dst_dir=$2
  
    if [ -z "${filelist}" ] ; then
        return 
    fi

    tmpdir="/tmp/rpm_upload"$(date +%N)
    if [ -d ${tmpdir} ] ; then
        rm -fr ${tmpdir}/*
    else 
        mkdir -p ${tmpdir}
    fi

    for filename in ${filelist[@]} ; 
    do
        cp ${filename} ${tmpdir}/
    done
 
    echo "Upload files to ${DST_IP}:${dst_dir}"
    scp -r ${tmpdir}/* ${DST_USER}@${DST_IP}:${dst_dir}
    rm -fr ${tmpdir}
}


filelist="$(find ${SRC_DIR} -name "*.aarch64.${file_type}")"
DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/aarch64"
upload_files_repo "${filelist}" "${DST_DIR}"

filelist="$(find ${SRC_DIR} -name "*.noarch.${file_type}")"
DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/noarch"
upload_files_repo "${filelist}" "${DST_DIR}"

filelist="$(find ${SRC_DIR} -name "*.${TARGETOS}.src.${file_type}")"
DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/SRPMS"
upload_files_repo "${filelist}" "${DST_DIR}"

