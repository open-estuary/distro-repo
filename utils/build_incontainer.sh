#!/bin/bash

cd ~
export DEBEMAIL=sjtuhjh@hotmail.com
export DEBFULLNAME=Open-Estuary
#wget -O - http://repo.linaro.org/ubuntu/linarorepo.key | apt-key add -
#apt-get update
#apt-get install expect -y
#apt-get install automake -y
#apt-get install dh-make -y
#apt-get install devscripts -y

echo "DEBSIGN_KEYID=24CC6CF4" >> /etc/devscripts.conf
passphrase="OPENESTUARY@123"

SRC_DIR=$1
TAR_FILENAME=$2
FILENAME=${TAR_FILENAME%-*}
DISTRI=$3

if [ $DISTRI = "debian" ];then
	DESDIR=debbuild
fi
if [ $DISTRI = "ubuntu" ];then
	DESDIR=ububuild
fi

if [ ! -d ${SRC_DIR} ]; then
    echo "${SRC_DIR} directory does not exist !"
    exit 1
fi
if

if [ -d /root/${DESDIR}/SOURCES/${FILENAME} ]; then
    echo "${FILENAME} had been builded before, now begin clean the directory."
    rm -rf /root/${DESDIR}/SOURCES/${FILENAME}/*
else
    mkdir -p /root/${DESDIR}/SOURCES/${FILENAME}
fi

cp ${SRC_DIR}/* /root/${DESDIR}/SOURCES/${FILENAME}/
tar -zxvf /root/${DESDIR}/SOURCES/${FILENAME}/${TAR_FILENAME} -C /root/${DESDIR}/SOURCES/${FILENAME}/
tar -zxvf /root/${DESDIR}/SOURCES/${FILENAME}/debian.tar.gz -C /root/${DESDIR}/SOURCES/${FILENAME}/${FILENAME}-*/

cd /root/${DESDIR}/SOURCES/${FILENAME}/${FILENAME}-*
dh_make -s -copyright gpl2 -f ../${TAR_FILENAME} -y
apt-get build-dep ${FILENAME} -y

expect <<-END
        set timeout -1
        spawn debuild
        expect {
                "Enter passphrase:" {send "${passphrase}\r"}
                timeout {send_user "Enter pass phrase timeout\n"}
        }
        expect {
                "Enter passphrase:" {send "${passphrase}\r"}
                timeout {send_user "Enter pass phrase timeout\n"}
        }
        expect eof
END

if [ ! -d /root/${DESDIR}/DEBS ]; then
        mkdir -p /root/${DESDIR}/DEBS
fi

if [ ! -d /root/${DESDIR}/SDEBS ]; then
        mkdir -p /root/${DESDIR}/SDEBS
fi

if [ ! -d /root/${DESDIR}/BUILDS ]; then
        mkdir -p /root/${DESDIR}/BUILDS
fi

if [ ! -d /root/${DESDIR}/CHANGES ]; then
        mkdir -p /root/${DESDIR}/CHANGES
fi


cp /root/${DESDIR}/SOURCES/${FILENAME}/*.deb /root/${DESDIR}/DEBS/
cp /root/${DESDIR}/SOURCES/${FILENAME}/*.dsc /root/${DESDIR}/SDEBS/
cp /root/${DESDIR}/SOURCES/${FILENAME}/*.orig.tar.gz /root/${DESDIR}/SDEBS/
cp /root/${DESDIR}/SOURCES/${FILENAME}/*.debian.tar.xz /root/${DESDIR}/SDEBS/
cp /root/${DESDIR}/SOURCES/${FILENAME}/*.build /root/${DESDIR}/BUILDS/
cp /root/${DESDIR}/SOURCES/${FILENAME}/*.changes /root/${DESDIR}/CHANGES/

echo "Please check deb under ~/${DESDIR}/DEBS/ or ~/${DESDIR}/SDEBS/ directory !"

