#!/bin/bash

TARGET="ubuntu"
OS_VERSION="16.04"
CUR_DIR=$(cd `dirname $0`; pwd)

if [ x"${1}" == x"debian" ] ; then
    TARGET=$1
    OS_VERSION="8"
elif [ ! -z "${1}" ] && [ x"${1}" != x"ubuntu" ] ; then
    echo "Unsupport platform: ${1}, it must be debian or ubuntu"
    exit 1
fi


BUILDDIR_BASE=ububuild/SOURCES/cassandra_dir/
BUILDDIR="$(cd ~;pwd)"/${BUILDDIR_BASE}

if [ -d ${BUILDDIR} ] ; then
    #sudo rm -fr ${BUILDDIR}/*
    echo ""
else 
    sudo mkdir -p ${BUILDDIR}
fi

VERSION="3.0"

FILELIST="fileList-${VERSION}.txt"
sudo wget -O ${BUILDDIR}/${FILELIST} http://debian.datastax.com/community/fileList_${VERSION}.txt

pushd ${BUILDDIR} > /dev/null
while read -r line
do
    filename=(${line//\// })
    #sudo wget http://debian.datastax.com/community/pool/${filename[-1]}
done < ${FILELIST}

# Remove unnecessary files
sudo rm -fr *amd64.deb
sudo rm -fr *i386.deb
popd > /dev/null

################################################################################
# Re-sign packages
################################################################################
CONTAINER_NAME="cassandra_${TARGET}_build"
if [ $TARGET = "debian" ]; then
	docker run -d -v ~/:/root/ --name ${CONTAINER_NAME} openestuary/debian:3.1-full   bash /root/distro-repo/utils/deb_resign.sh /root/${BUILDDIR_BASE}

elif [ $TARGET = "ubuntu" ]; then
	docker run -d -v ~/:/root/ --name ${CONTAINER_NAME} openestuary/ubuntu:3.1-full bash /root/distro-repo/utils/deb_resign.sh /root/${BUILDDIR_BASE}
fi

while true
do
	container_status=`docker ps -a | grep ${CONTAINER_NAME} | awk '{print $8}' | grep Exited`
        if [ -z ${container_status} ]; then
                sleep 10s
        else
                break
        fi
done

echo "Begin to remove building container."
docker logs ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}
if [ $? -ne 0 ]; then
        echo "Remove building container failed!"
else
        echo "Building container have been removed successfully!"
fi

##############################################################################
#Upload to estuary repository
##############################################################################
${CUR_DIR}/../../utils/pkg_upload.sh ${BUILDDIR}/ ${TARGET}

