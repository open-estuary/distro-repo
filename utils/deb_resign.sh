#!/bin/bash

cd ~
export DEBEMAIL=sjtuhjh@hotmail.com
export DEBFULLNAME=Open-Estuary

apt-get update
apt-get install dpkg-sig
apt-get install expect

echo "DEBSIGN_KEYID=3108CDA4" >> /etc/devscripts.conf
passphrase=$(cat /root/KEY_PASSPHRASE)
gpg --import /root/ESTUARY-GPG-SECURE-KEY

SRC_DIR=${1}

for deb_file in ${SRC_DIR}/*.deb
do

expect <<-END
        set timeout -1
        spawn dpkg-sig --sign builder ${deb_file}
        expect {
                "Enter passphrase:" {send "${passphrase}\r"}
                timeout {send_user "Enter pass phrase timeout\n"}
        }
        expect eof
END
    
done

