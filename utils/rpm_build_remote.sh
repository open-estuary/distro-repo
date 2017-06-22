#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

. ${CUR_DIR}/function_cmd_scp.sh

packages=
IP="192.168.1.180"
loginuser="estuaryrepo"
loginpassword=`cat ~/PASSWORD_WORKER`
giturl="https://github.com/open-estuary/distro-repo.git"
reponame="distro-repo"


usage()
{
        echo "Usage: rpm_build_remote.sh -k "packages" [-m remoteip] [-u login_user] [-p login_password]"
}

while getopts "k:m:p:u:h" OPTIONS
do
        case $OPTIONS in
                k) packages="$OPTARG";;
                m) IP="$OPTARG";;
                u) loginuser="$OPTARG";;
                p) loginpassword="$OPTARG";;
		h) usage;exit 1;;
                \?) echo "ERROR - Invalid Parameter"; echo "ERROR - Invalid parameter" >&2; usage; exit 1;;
                *) echo "ERROR - Invalid Parameter"; echo "ERROR - Invalid parameter" >&2; usage; exit 1;;
        esac 
done            

if [ "x$packages" = "x" ];then
	echo "Packages must not be void!"
	usage
	exit 1
fi

sshcmd "if \[ \`ls /home/${loginuser} | grep "$reponame"\` \];then  cd /home/${loginuser}/$reponame;git pull;cd -;else cd /home/${loginuser};git clone ${giturl};cd -;fi"

if [ "${packages}" = "all" ];then
	sshcmd "sh /home/${loginuser}/${reponame}/rpm/rpm_build_all.sh"
	exit
fi

for package in $packages
do
	sshcmd "sh /home/${loginuser}/${reponame}/rpm/$package/rpm_build.sh"
done

echo "Build have done, please check!"


	
