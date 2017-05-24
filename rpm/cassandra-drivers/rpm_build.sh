#!/bin/bash

CUR_DIR="$(cd `dirname $0`; pwd)"
TARGET_OS="centos"
if [ ! -z "${1}" ] ; then
    TARGET_OS=${1}
fi

${CUR_DIR}/rpm_build_cxx.sh
${CUR_DIR}/rpm_build_java.sh

