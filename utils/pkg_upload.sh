#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

. ${CUR_DIR}/function_cmd_scp.sh

VERSION="5.0"
if [ $# -eq 3 ];then
        VERSION=$3
fi

SRC_DIR=$1
TARGETOS=$2
IP="117.78.41.188"
loginuser="repo"
loginpassword=`cat /home/PASSWORD_REPO`

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
#   exit 0
fi

upload_files_repo() {
    filelist=$1
    dst_dir=$2
  
    if [ -z "${filelist}" ] ; then
        return 
    fi

    tmpdir="/tmp/pkg_upload"$(date +%N)
    if [ -d ${tmpdir} ] ; then
        rm -fr ${tmpdir}/*
    else 
        mkdir -p ${tmpdir}
    fi

    for filename in ${filelist[@]} ; 
    do
        cp ${filename} ${tmpdir}/
    done

    sshcmd " \[ -d ${dst_dir} \] || mkdir -p ${dst_dir} "
 
    echo "Upload files to ${DST_IP}:${dst_dir}"
    all_files=`ls ${tmpdir}/`
    for file in ${all_files} ;
    do
        sshscp ${tmpdir}/$file ${dst_dir} no to
    done

    #scp -r ${tmpdir}/* ${DST_USER}@${DST_IP}:${dst_dir}
    rm -fr ${tmpdir}
}

echo "Begin to upload files!"
if [ ${TARGETOS} = "centos" ];then
	filelist="$(find ${SRC_DIR} -name "*.aarch64.${file_type}")"
	DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/aarch64"
	upload_files_repo "${filelist}" "${DST_DIR}"

	filelist="$(find ${SRC_DIR} -name "*.noarch.${file_type}")"
	DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/noarch"
	upload_files_repo "${filelist}" "${DST_DIR}"

	filelist="$(find ${SRC_DIR} -name "*.src.${file_type}")"
	DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/SRPMS"
	upload_files_repo "${filelist}" "${DST_DIR}"
elif [ ${TARGETOS} = "debian" ];then
	filelist="$(find ${SRC_DIR} -name "*.u${file_type}")"
	DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
	upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.${file_type}")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"
	
	filelist="$(find ${SRC_DIR} -name "*.orig.*")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

	filelist="$(find ${SRC_DIR} -name "*.debian.*")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.diff.*")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"
	
	filelist="$(find ${SRC_DIR} -name "*.dsc")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

	filelist="$(find ${SRC_DIR} -name "*.tar.xz")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"
else
        filelist="$(find ${SRC_DIR} -name "*.u${file_type}")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

	filelist="$(find ${SRC_DIR} -name "*.${file_type}")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.orig.*")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.debian.*")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.diff.*")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.dsc")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"

        filelist="$(find ${SRC_DIR} -name "*.tar.gz")"
        DST_DIR="/est-repo/releases/${VERSION}/${TARGETOS}/pool/main"
        upload_files_repo "${filelist}" "${DST_DIR}"
fi
echo "Upload done!"



