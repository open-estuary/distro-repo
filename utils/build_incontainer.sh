#!/bin/bash

cd ~
export DEBEMAIL=situhjh@hotmail.com
export DEBFULLNAME=Open-Estuary
wget -O - http://repo.linaro.org/ubuntu/linarorepo.key | apt-key add -
apt-get update
apt-get install expect -y
apt-get install automake -y
apt-get install dh-make -y
apt-get install devscripts -y

echo "DEBSIGN_KEYID=24CC6CF4" >> /etc/devscripts.conf
passphrase="OPENESTUARY@123"

SRC_DIR=$1
TAR_FILENAME=$2
FILENAME=${TAR_FILENAME%-*}
if [ ! -d ${SRC_DIR} ]; then
    echo "${SRC_DIR} directory does not exist !"
    exit 1
fi

if [ -d /root/debbuild/SOURCES/${FILENAME} ]; then
    echo "${FILENAME} had been builded before, now begin clean the directory."
    rm -rf /root/debbuild/SOURCES/${FILENAME}/*
else
    mkdir -p /root/debbuild/SOURCES/${FILENAME}
fi

cp ${SRC_DIR}/* /root/debbuild/SOURCES/${FILENAME}/
tar -zxvf /root/debbuild/SOURCES/${FILENAME}/${TAR_FILENAME} -C /root/debbuild/SOURCES/${FILENAME}/
tar -zxvf /root/debbuild/SOURCES/${FILENAME}/debian.tar.gz -C /root/debbuild/SOURCES/${FILENAME}/${FILENAME}-*/

cd /root/debbuild/SOURCES/${FILENAME}/${FILENAME}-*
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

if [ ! -d /root/debbuild/DEBS ]; then
        mkdir -p /root/debbuild/DEBS
fi

if [ ! -d /root/debbuild/SDEBS ]; then
        mkdir -p /root/debbuild/SDEBS
fi

if [ ! -d /root/debbuild/BUILDS ]; then
        mkdir -p /root/debbuild/SDEBS
fi

if [ ! -d /root/debbuild/CHANGES ]; then
        mkdir -p /root/debbuild/SDEBS
fi


cp /root/debbuild/SOURCES/${FILENAME}/*.deb /root/debbuild/DEBS/
cp /root/debbuild/SOURCES/${FILENAME}/*.dsc /root/debbuild/SDEBS/
cp /root/debbuild/SOURCES/${FILENAME}/*.orig.tar.gz /root/debbuild/SDEBS/
cp /root/debbuild/SOURCES/${FILENAME}/*.debian.tar.xz /root/debbuild/SDEBS/
cp /root/debbuild/SOURCES/${FILENAME}/*.build /root/debbuild/BUILDS/
cp /root/debbuild/SOURCES/${FILENAME}/*.changes /root/debbuild/CHANGES/

echo "Please check deb under ~/debbuild/DEBS/ or ~/debbuild/SDEBS/ directory !"

