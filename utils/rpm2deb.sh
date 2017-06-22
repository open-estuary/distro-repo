#!/bin/bash

$SRC_DIR='./'
$DEST_DIR='./'
if [ ! -z "${1}" ] ; then
    SRC_DIR=${1}
fi

if [ ! -z "${2}" ] ; then
    DEST_DIR=${2}
fi

apt-get update
if [ -z "$(which alien 2>/dev/null)" ] ; then
    sudo apt-get install -y alien
fi

if [ -z "$(which debsigs 2>/dev/null)" ] ; then
    sudo apt-get install -y debsigs
fi
sudo apt-get install -y expect
sudo apt-get install -y policycoreutils

TMP_BUILD="/tmp/tmp_rpm2deb/"
if [ -d ${TMP_BUILD} ] ; then 
    rm -fr ${TMP_BUILD}/*
else 
    mkdir -p ${TMP_BUILD}
fi

#Convert RPM files to Deb files
cd ${TMP_BUILD}
for rpmfile in ${SRC_DIR}/*.rpm
do
     echo ""
     alien --target=arm64 ${rpmfile}
done

if [ "${SRC_DIR}" != "${DEST_DIR}" ] ; then
    if [ ! -d ${DEST_DIR} ] ; then
        mkdir -p ${DEST_DIR}
    fi
    mv ${TMP_BUILD}/*.deb ${DEST_DIR}/
fi 

#Re-sign deb files
GPG_KEY="24CC6CF4"
KEY_PASSPHRASE="$(cat /root/KEY_PASSPHRASE)"
for debfile in ${DEST_DIR}/*.deb
do
expect <<-END
        set timeout -1
        spawn debsigs --sign=origin -k ${GPG_KEY} ${debfile}
        expect {
                "Enter passphrase:" {send "${KEY_PASSPHRASE}\r"}
                timeout {send_user "Enter pass phrase timeout\n"}
        }
        expect eof
END
done

