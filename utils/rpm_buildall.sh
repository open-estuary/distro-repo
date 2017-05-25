#!/bin/bash


CUR_DIR=$(cd `dirname $0`; pwd)
rpm_pkgs=`ls ${CUR_DIR}/../rpm`

for rpm_pkg in $rpm_pkgs
do
    sh ${CUR_DIR}/../rpm/${rpm_pkg}/rpm_build.sh
#    if [ $? -ne 0 ];then
#	echo "${rpm_pkg} rpm package build failed, please check!!!"
#	exit 1
#    fi
done

echo "all rpm packages build succeed!"

