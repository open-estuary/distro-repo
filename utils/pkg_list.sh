#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION_LIST=("3.0" "5.0")

for version in ${VERSION_LIST[@]}
do
    python ${CUR_DIR}/pkg_list_update.py ${CUR_DIR}/../docs/packages_list_${version}.md ${version}
done

