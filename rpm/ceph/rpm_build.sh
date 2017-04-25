#!/bin/bash

#####################################################################################
# To build RPM packages for Ceph
#####################################################################################
CUR_DIR=$(cd `dirname $0`; pwd)
BUILD_DIR="/tmp/builddir_ceph"
VERSION="v12.0.1"

####################################################################################
# Prepare for build
####################################################################################
sudo rm -fr ${BUILD_DIR}
mkdir -p ${BUILD_DIR}
pushd ${BUILD_DIR} > /dev/null

#Make sure GCC is 5.x version
echo "Make sure that gcc is 5.x version"
#export CC=/usr/local/bin/gcc
#export CXX=/usr/local/bin/g++
#export LD_LIBRARY_PATH=/usr/local/lib64

git clone --recursive https://github.com/ceph/ceph.git
cd ceph
git checkout --f ${VERSION}

# Replace x86_64 with aarch64
sed -i 's/x86_64/aarch64/g' install-deps.sh
./install-deps.sh

# 
# Warning: If it fails to compile/link due to leveldb issue, 
# please install latest leveldb based on latest Estuary repository

./do_cmake.sh
./make-dist $1

rpmbuild -D"_sourcedir `pwd`" -D"_specdir `pwd`" -D"_srcrpmdir `pwd`" -ba ceph.spec
${CUR_DIR}/rpm_sign.sh ~/rpmbuild/RPMS/aarch64/

echo "Please check *.src.rpm under ${SRC_DIR} directory !"
echo "Please check other rpm under ~/rpmbuild/RPMS/aarch64/ directory !"
popd > /dev/null


