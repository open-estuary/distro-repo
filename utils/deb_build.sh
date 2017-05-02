#! /bin/bash

builddeb()
{
        program="$1"
        version="$2"
        sshcmd "export DEBFULLNAME="test"; export DEBEMAIL="test@test.com"; cd dmidecode-3.0; dh_make -s -copyright gpl3 -f ../dmidecode-3.0.tar.gz <<EOF
y
EOF; echo "override_dh_usrlocal:" >> debian/rules; dpkg-buildpackage -rfakeroot; cd -"
        if [ $? -ne 0]; then
                echo "dpkg package build failed"
        fi
}

