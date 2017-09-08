#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

usage()
{
        echo "Usage: deb_build.sh srcdir tarfile debian/ubuntu"
}

if [ $# -lt 3 ]; then
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
#Image_ID=`docker images | grep "openestuary/debian"| grep "latest" | awk '{print $3}'`

SRC_DIR_1=$1
SRC_DIR_2=${SRC_DIR_1#*/}
SRC_DIR_3=${SRC_DIR_2#*/}
SRC_DIR_4=${SRC_DIR_3#*/}
TAR_FILENAME=$2
DISTRI=$3
BUILD_OPTIONS=$4
PPA_TEST_ENABLE=$5

CONTAINER_NAME=${TAR_FILENAME%-*}-$DISTRI
CONTAINER_NAME=${CONTAINER_NAME/+/}

if [ ! -f ~/KEY_PASSPHRASE ] ; then
    cp /home/KEY_PASSPHRASE  ~/KEY_PASSPHRASE
fi

if [ $DISTRI = "debian" ]; then
	docker run -d -v ~/:/root/ --name ${CONTAINER_NAME} openestuary/debian:3.1-full bash /root/distro-repo/utils/deb_build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME} ${DISTRI} "${BUILD_OPTIONS}" "${PPA_TEST_ENABLE}"
elif [ $DISTRI = "ubuntu" ]; then
	docker run -d -v ~/:/root/ --name ${CONTAINER_NAME} openestuary/ubuntu:3.1-full bash /root/distro-repo/utils/deb_build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME} ${DISTRI} "${BUILD_OPTIONS}" "${PPA_TEST_ENABLE}"
fi

docker logs -f ${CONTAINER_NAME}

echo "Begin to remove building container."
docker rm ${CONTAINER_NAME}
if [ $? -ne 0 ]; then
        echo "Remove building container failed!"
else
        echo "Building container have been removed successfully!"
fi

