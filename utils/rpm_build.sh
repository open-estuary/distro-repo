#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

usage() 
{
        echo "Usage: rpm_build.sh srcdir spec "
}

if [ $# -lt 2 ]; then 
        usage
        exit 1
fi

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
#Image_ID=`docker images | grep "openestuary/centos"| grep "latest" | awk '{print $3}'`

id=`id -u`
SRC_DIR_1=$1
SRC_DIR_2=${SRC_DIR_1#*/}
SRC_DIR_3=${SRC_DIR_2#*/}
SRC_DIR_4=${SRC_DIR_3#*/}
SPEC_NAME=$2

CONTAINER_NAME=${SPEC_NAME%.*}
CONTAINER_NAME=${CONTAINER_NAME/+/}

if [ ! -f ~/KEY_PASSPHRASE ] ; then
    cp /home/KEY_PASSPHRASE  ~/KEY_PASSPHRASE
fi

	docker run -d -v ~/:/root/ --name ${CONTAINER_NAME} openestuary/centos:3.0-build-1 bash /root/distro-repo/utils/rpm_build_incontainer.sh /root/${SRC_DIR_4} ${SPEC_NAME} $id

docker logs -f ${CONTAINER_NAME}

echo "Begin to remove building container."
docker rm ${CONTAINER_NAME}
if [ $? -ne 0 ]; then
        echo "Remove building container failed!"
else
        echo "Building container have been removed successfully!"
fi

