#!/bin/bash

IP=192.168.1.180
loginuser=estuaryrepo
loginpassword=OpenEstuary@123

CUR_DIR=$(cd `dirname $0`; pwd)

. ${CUR_DIR}/common_function.sh

sshscp $CUR_DIR/rpm_upload.sh /home/$loginuser/ no to

sshcmd "sh /home/$loginuser/rpm_upload.sh /home/$loginuser/rpmbuild/RPMS/aarch64 CentOS"

sshcmd "sh /home/$loginuser/rpm_upload.sh /home/$loginuser/rpmbuild/RPMS/noarch CentOS"

sshcmd "sh /home/$loginuser/rpm_upload.sh /home/$loginuser/rpmbuild/SRPMS CentOS"
