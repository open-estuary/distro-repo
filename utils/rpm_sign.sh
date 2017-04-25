#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)
TARGET=$1

if [ -d "${TARGET}" ] ; then
    for filename in $(find ${TARGET} -name '*.rpm')
    do
        if [ -f ${filename} ] ; then
            ${CUR_DIR}/rpmsign_expect ${filename}
        fi
    done
else
    ${CUR_DIR}/rpmsign_expect ${filename}
fi
