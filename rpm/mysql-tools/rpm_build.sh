#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)
${CUR_DIR}/rpm_build_internal.sh "workbench"
${CUR_DIR}/rpm_build_internal.sh "util"
${CUR_DIR}/rpm_build_internal.sh "router"
${CUR_DIR}/rpm_build_internal.sh "shell"
${CUR_DIR}/rpm_build_internal.sh "connector-python"
${CUR_DIR}/rpm_build_internal.sh "connector-odbc"
${CUR_DIR}/rpm_build_internal.sh "connector-cpp"


