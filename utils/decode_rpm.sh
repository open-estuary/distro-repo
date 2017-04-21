#!/bin/bash

rpmfile=${1}

if [ -z "${rpmfile}" ] ; then
    echo "Please input one rpm file"
    exit 0
fi

if [ -z "$(which rpm2cpio 2>/dev/null)" ] ; then
    sudo yum install -y rpm
fi

if [ -z "$(which cpio 2>/dev/null)" ] ; then
    sudo yum install -y cpio
fi

rpm2cpio ${rpmfile} | cpio -div

