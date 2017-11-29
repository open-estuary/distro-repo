#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

TAR_DIRNAME="orzdba-1.0"

if [ ! -f ${CUR_DIR}/src/${TAR_DIRNAME} ] ; then
	wget -r -np --reject=html http://code.taobao.org/svn/orzdba/trunk/

	pushd ${CUR_DIR}/src > /dev/null

	mkdir ${TAR_DIRNAME}

	mv ../code.taobao.org/svn/orzdba/trunk/* ${TAR_DIRNAME}

	tar -zcvf ${TAR_DIRNAME}.tar.gz ${TAR_DIRNAME}

	popd > /dev/null

	rm -rf code.taobao.org

fi
${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src orzdba.spec
