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

docker_status=`service docker status | grep "inactive"`
if [ -z ${docker_status} ]; then
        sudo service docker start
fi

echo "Start container to build." 
#Image_ID=`docker images | grep "openestuary/debian"| grep "latest" | awk '{print $3}'`

SRC_DIR_1=$1
SRC_DIR_2=${SRC_DIR_1#*/}
SRC_DIR_3=${SRC_DIR_2#*/}
SRC_DIR_4=${SRC_DIR_3#*/}
TAR_FILENAME=$2
DISTRI=$3

if [ $DISTRI = "debian" ]; then
	docker run -d -v ~/:/root/ openestuary/debian:latest sh /root/distro-repo/utils/build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME}
fi

if [ $DISTRI = "ubuntu" ]; then
	docker run -d -v ~/:/root/ openestuary/ubuntu:latest sh /root/distro-repo/utils/build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME}
fi

if [ $? -ne 0 ]; then
        echo "Build failed, please check!"
else
        echo "Build succeed."
fi

