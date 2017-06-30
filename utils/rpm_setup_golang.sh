#!/bin/bash


BUILD_DIR="./tmp-golang-packaging"

mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}
wget https://github.com/marguerite/golang-packaging/archive/v14.10.tar.gz
tar -xzvf *.tar.gz
sudo cp golang-packaging-*/macros.go /etc/rpm/
sudo cp golang-packaging-*/golang.* /usr/lib/rpm/
sudo cp -r golang-packaging-*/golang /usr/lib/rpm/
cd ..
rm -r ${BUILD_DIR}

