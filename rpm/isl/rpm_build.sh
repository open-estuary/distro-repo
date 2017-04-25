#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="0.16.1"
TAR_FILENAME="isl-""${VERSION}"".tar.xz"

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src isl.spec
