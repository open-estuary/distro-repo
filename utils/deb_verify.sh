#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

usage()
{
        echo "Usage: deb_verify.sh {install | erase} <log dir> <debian/ubuntu>"
}

cmd=""
logdir="/tmp/debverifylog"
targetos="ubuntu"

if [ $# -ge 3 ];then
	targetos=$3
fi
if [ $# -ge 2 ];then
	logdir=$2
fi
if [ $# -ge 1 ];then
	cmd=$1
fi
 
logdir="${logdir}/${targetos}" 

docker_status=`service docker status | grep "inactive" | awk '{print $2}'`
if [ ! -z ${docker_status} ]; then
        echo "Docker service is inactive, begin to start docker service"
        sudo service docker start
        if [ $? -ne 0 ] ; then
                echo "Starting docker service failed!"
                exit 1
        else
                echo "Docker service start sucessfully!"
        fi
fi

echo "Start container to build."
CONTAINER_NAME=debverify-${targetos}
if [ $targetos = "ubuntu" ];then
	docker run -it -v ${logdir}:/tmp/debverifylog -v ${CUR_DIR}/:/root/ --name ${CONTAINER_NAME} openestuary/ubuntu:3.0-build-1 python /root/verify_incontainer.py $cmd /tmp/debverifylog $targetos 
elif [ $targetos = "debian" ];then
	docker run -d -v ${logdir}:/tmp/debverifylog -v ${CUR_DIR}/:/root/ --name ${CONTAINER_NAME} openestuary/debian:3.0-build python /root/verify_incontainer.py $cmd /tmp/debverifylog $targetos
fi

docker logs -f ${CONTAINER_NAME}

echo "Begin to remove building container."
docker rm ${CONTAINER_NAME}
if [ $? -ne 0 ];then
	echo "Remove building container failed!"
else
	echo "Building container have benn removed successfully!"
fi

echo "Deb verify finished, please check result in ${logdir}"

