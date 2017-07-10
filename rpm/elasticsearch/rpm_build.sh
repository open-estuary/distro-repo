#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

TARGET="centos"
BUILDDIR_BASE=rpmbuild/SOURCES/elasticsearch_dir/
BUILDDIR="$(cd ~;pwd)"/${BUILDDIR_BASE}

if [ -d ${BUILDDIR} ] ; then
    rm -fr ${BUILDDIR}/*
else 
    mkdir -p ${BUILDDIR}
fi

VERSION="5.5.0"

pushd ${BUILDDIR} > /dev/null
wget -O elasticsearch-${VERSION}.noarch.rpm https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}.rpm
popd > /dev/null

${CUR_DIR}/../../utils/rpm_resign.sh ${BUILDDIR}

#Upload to estuary repository
${CUR_DIR}/../../utils/pkg_upload.sh ${BUILDDIR}/ ${TARGET}

