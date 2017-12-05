#!/bin/bash

#build cxx-3x
yum install -y mongo-c-driver
yum install -y mongo-c-driver-devel

#build c
#pip install -U setup-tools
#pip install --upgrade sphinx

#build  cxx_legacy
#yum erase -y openssl-devel openssl openssl-libs  openssl-libs-1.0.2k-8.el7
#yum install -y mongo-c-driver mongo-c-driver-devel  compat-openssl10-devel scons cyrus-sasl-devel 
#pip install --upgrade boost-devel
