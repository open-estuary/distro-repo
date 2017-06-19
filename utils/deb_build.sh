#/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

usage()
{
        echo "Usage: deb_build.sh srcdir tarfile debian/ubuntu"
}

if [ $# -ne 3 ]; then
	usage
	exit 1
fi

docker_status=`service docker status | grep "inactive" | awk '{print $2}'`
if [ -z ${docker_status} ]; then
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
Container_Name=${TAR_FILENAME%-*}-$DISTRI

if [ $DISTRI = "debian" ]; then
	docker run -d -v ~/:/root/ --name ${Container_Name} openestuary/debian:3.0-build bash /root/distro-repo/utils/build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME} ${DISTRI}
fi

if [ $DISTRI = "ubuntu" ]; then
	docker run -d -v ~/:/root/ --name ${Container_Name} openestuary/ubuntu:3.0-build bash /root/distro-repo/utils/build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME} ${DISTRI}
fi

echo "It may take some times to build, please wait."
while true
do
	container_status=`docker ps -a | grep ${Container_Name} | awk '{print $8}' | grep Exited`
        if [ -z ${container_status} ]; then
                sleep 10s
        else
                break
        fi
done
echo "Building has been done. Please check deb under ~/debbuild(ububuild)/DEBS/ or ~/debbuild(ububuild)/SDEBS/ directory !"

echo "Begin to remove building container."
docker logs ${Container_Name}
docker rm ${Container_Name}
if [ $? -ne 0 ]; then
        echo "Remove building container failed!"
else
        echo "Building container have been removed successfully!"
fi

