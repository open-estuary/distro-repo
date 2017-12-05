#!/bin/bash

yum install -y devtoolset-4-gcc
yum install -y devtoolset-4-gcc-c++
yum install -y devtoolset-4-libstdc++-devel
source /opt/rh/devtoolset-4/enable
echo "source enable==============="

yum install -y jetpack
