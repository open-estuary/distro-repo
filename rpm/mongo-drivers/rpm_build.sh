#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

${CUR_DIR}/rpm_build_c.sh
${CUR_DIR}/rpm_build_cxx_3x.sh
${CUR_DIR}/rpm_build_java.sh


