#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="5.0"
if [ $# -eq 2 ];then
        VERSION=$2
fi

. ${CUR_DIR}/function_cmd_scp.sh
IP="117.78.41.188"
loginuser="repo"
loginpassword=`cat /home/PASSWORD_REPO`

TARGETOS=$1

###############################################################################################
# Utility to create deb repo"
###############################################################################################
create_deb_repo() {
    platform=$1    
   
    sshcmd " \[ -d /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64 \] || mkdir -p /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64 "
   
    sshcmd " \[ -d /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source \] || mkdir -p /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source "

    sshcmd "cd /est-repo/releases/${VERSION}/${platform} && apt-ftparchive contents pool/main > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/Contents-arm64; cat /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/Contents-arm64 | gzip > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/Contents-arm64.gz"
    
    sshcmd "cd /est-repo/releases/${VERSION}/${platform} && dpkg-scanpackages pool/main /dev/null > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64/Packages; cat /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64/Packages | gzip > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64/Packages.gz; cat /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64/Packages | bzip2 >  /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/binary-arm64/Packages.bz2"
        
    sshcmd "cd /est-repo/releases/${VERSION}/${platform} && dpkg-scansources pool/main > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source/Sources; cat /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source/Sources | gzip > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source/Sources.gz; cat /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source/Sources | bzip2 > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/main/source/Sources.bz2; "
        
    sshcmd "apt-ftparchive release /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION} > /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/Release"
    
    home_dir="$(cd ~ ; pwd)"
    tmp_dir="${home_dir}/debrepo_release/"
    if [ -d ${tmp_dir} ] ; then 
        rm -fr ${tmp_dir}/*
    else
        mkdir -p ${tmp_dir}
    fi

    wget -O ${tmp_dir}/Release ftp://repoftp:repopushez7411@117.78.41.188/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/Release
    gpg --batch --passphrase-file /home/KEY_PASSPHRASE  --yes --default-key "3108CDA4" --armor --output ${tmp_dir}/Release.gpg --detach-sig ${tmp_dir}/Release
    sshscp ${tmp_dir}/Release.gpg /est-repo/releases/${VERSION}/${platform}/dists/estuary-${VERSION}/ no to
}


if [ "${TARGETOS}" = "CentOS" ] || [ "${TARGETOS}" = "centos" ] ; then
    sshcmd "createrepo /est-repo/releases/${VERSION}/centos"	
elif [ "${TARGETOS}" = "Ubuntu" ] || [ "${TARGETOS}" = "ubuntu" ] ; then
    create_deb_repo "ubuntu"
elif [ "${TARGETOS}" = "Debian" ] || [ "${TARGETOS}" = "debian" ] ; then
    create_deb_repo "debian"
else
    echo "Currently it only support CentOS, Ubuntu or Debian"
    exit 0
fi

if [ $? -ne 0 ];then
	echo "repo create failed!"
else
	echo "repo create successfully!"
fi
