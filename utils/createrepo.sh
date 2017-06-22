#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

. ${CUR_DIR}/function_cmd_scp.sh
IP="117.78.41.188"
loginuser="repo"
loginpassword=`cat /home/PASSWORD_REPO`

TARGETOS=$1
if [ "${TARGETOS}" = "CentOS" ] || [ "${TARGETOS}" = "centos" ] ; then
	sshcmd "createrepo /est-repo/releases/5.0/centos"	
elif [ "${TARGETOS}" = "Ubuntu" ] || [ "${TARGETOS}" = "ubuntu" ] ; then
	sshcmd "dpkg-scanpackages /est-repo/releases/5.0/ubuntu /dev/null | gzip > /est-repo/releases/5.0/ubuntu/Packages.gz;dpkg-scansources /est-repo/releases/5.0/ubuntu | gzip > /est-repo/releases/5.0/ubuntu/Sources.gz"
elif [ "${TARGETOS}" = "Debian" ] || [ "${TARGETOS}" = "debian" ] ; then
	sshcmd "dpkg-scanpackages /est-repo/releases/5.0/debian /dev/null | gzip > /est-repo/releases/5.0/debian/Packages.gz;dpkg-scansources /est-repo/releases/5.0/debian | gzip > /est-repo/releases/5.0/debian/Sources.gz"
else
    echo "Currently it only support CentOS, Ubuntu or Debian"
    exit 0
fi

if [ $? -ne 0 ];then
	echo "repo create failed!"
else
	echo "repo create successfully!"
fi
