#/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

docker_status=`service docker status | grep "inactive"`
if [ -z ${docker_status} ]; then
        sudo service docker start
fi
echo "Start container to build." 
Image_ID=`docker images | grep "openestuary/debian"| grep "latest" | awk '{print $3}'`

SRC_DIR_1=$1
SRC_DIR_2=${SRC_DIR_1#*/}
SRC_DIR_3=${SRC_DIR_2#*/}
SRC_DIR_4=${SRC_DIR_3#*/}
TAR_FILENAME=$2

docker run -d -v ~/:/root/ ${Image_ID} sh /root/distro-repo/utils/build_incontainer.sh /root/${SRC_DIR_4} ${TAR_FILENAME}

if [ $? -ne 0 ]; then
        echo "Build failed, please check!"
else
        echo "Build succeed."
fi

