#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

TARGET="centos"
BUILDDIR_BASE=rpmbuild/RPMS/noarch/
BUILDDIR="$(cd ~;pwd)"/${BUILDDIR_BASE}

if [ -d ${BUILDDIR} ] ; then
    rm -fr ${BUILDDIR}/*
else 
    mkdir -p ${BUILDDIR}
fi

VERSION="3.0"

python ${CUR_DIR}/cassandra_pkgs_download.py ${BUILDDIR}

${CUR_DIR}/../../utils/rpm_resign.sh ${BUILDDIR}

#Upload to estuary repository
#${CUR_DIR}/../../utils/pkg_upload.sh ${BUILDDIR}/ ${TARGET}


