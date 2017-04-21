#!/bin/bash

packagename=${1}

if [ -z "${packagename}" ] ; then
    echo "Please input the package name which need to be only downloaded"
    exit 0
fi

if [ -z "$(which yumdownloader 2>/dev/null)" ] ; then
    sudo yum install -y yum-utils
fi

yumdownloader ${packagename}

