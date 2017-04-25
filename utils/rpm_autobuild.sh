#! /bin/bash

IP=192.168.1.180
loginuser=estuaryrepo
loginpassword=OpenEstuary@123

CUR_DIR=$(cd `dirname $0`; pwd)
echo ${CUR_DIR}
. common_function.sh

SRC_DIR=$1
SPEC_FILE=$2

if [ ! -d ${SRC_DIR} ]; then
	echo "${SRC_DIR} directory does not exist"
	exit 1
fi

#sshcmd "mkdir -p /home/$loginuser/rpm_scripts &> /dev/null"

sshscp $SRC_DIR/$SPEC_FILE /home/$loginuser/rpmbuild/SPECS  no to

sshscp $SRC_DIR/*tar* /home/$loginuser/rpmbuild/SOURCES no to

sshscp $CUR_DIR/rpm_autosign.sh /home/$loginuser/ no to

sshcmd "sh /home/$loginuser/rpm_autosign.sh $SPEC_FILE"

if [ $? == 0 ]; then
	echo "rpm build done, please check!"
else
	echo "build failed!!!"
fi
