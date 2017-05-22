#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

python ${CUR_DIR}/rpm_generate_buildscript.py
python ${CUR_DIR}/rpm_build_packages.py > ${CUR_DIR}/buildlog 2>&1 &
