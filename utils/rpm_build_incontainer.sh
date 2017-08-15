#!/bin/bash

cd ~
useradd test -u 1001

if [ -d ~/rpmbuild/RPMS ] ; then
    echo "Previous RPM build still exists, so it might be necessary to clear them before building new one"
fi

if [ "$(uname -m)" != "aarch64" ] ; then
    echo "Please build this package on arm64 platform"
    exit 1
fi

yum clean all
	
yum install expect yum-utils -y
if [ -z "$(which rpmsign 2>/dev/null)" ] ; then
    yum install rpm-sign -y
fi

SRC_DIR=$1
SPEC_FILE=$2
id=$3
scl=$4

if [ $scl -eq 1]; then
	yum install -y scl-utils scl-utils-build
	yum install -y devtoolset-4-gcc
	yum install -y devtoolset-4-gcc-c++
	yum install -y devtoolset-4-libstdc++-devel
	source /opt/rh/devtoolset-4/enable
fi

useradd test -u $id

if [ ! -d ${SRC_DIR} ] ; then
    echo "${SRC_DIR} directory does not exist !"
    exit 1
fi

yum-builddep -y ${SRC_DIR}/${SPEC_FILE}
passphrase=`cat /root/KEY_PASSPHRASE`
expect <<-END
        set timeout -1
        spawn rpmbuild --sign  --target aarch64 -ba ${SRC_DIR}/${SPEC_FILE} "--define=_sourcedir ${SRC_DIR}" "--define=_specdir ${SRC_DIR}" ${@:3}
        expect {
                "Enter pass phrase:" {send "${passphrase}\r"}
                timeout {send_user "Enter pass phrase timeout\n"}
        }
        expect eof
END
echo "Please check rpm under ~/rpmbuild/RPMS/ or ~/rpmbuild/SRPMS/ directory !"
