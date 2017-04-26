#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

VERSION="5.4.0"
#The DATE is also specifed in gcc.spec
DATE="20160603"
TAR_FILENAME="gcc-""${VERSION}""-${DATE}.tar.bz2"
SVNREV="247088"

nvptx_tools_gitrev="c28050f60193b3b95a18866a96f03334e874e78f"
nvptx_newlib_gitrev="aadc8eb0ec43b7cd0dd2dfb484bae63c8b05ef24"

# Prepare GCC Source 
if [ ! -f ${CUR_DIR}/src/${TAR_FILENAME} ] ; then
    #sudo wget -O ${CUR_DIR}/src/${TAR_FILENAME} http://ftp.tsukuba.wide.ad.jp/software/gcc/releases/gcc-${VERSION}/gcc-${VERSION}.tar.bz2
    svn export svn://gcc.gnu.org/svn/gcc/branches/gcc-5-branch@${SVNREV} gcc-${VERSION}-${DATE}
    tar cf - gcc-${VERSION}-${DATE} | bzip2 -9 > ${CUR_DIR}/src/gcc-${VERSION}-${DATE}.tar.bz2
    rm -fr gcc-${VERSION}-${DATE}
fi

# Prepare isl lib
${CUR_DIR}/isl_build.sh

# Prepare others sources files
if [ ! -f ${CUR_DIR}/src/nvptx-tools-${nvptx_tools_gitrev}.tar.bz2 ] ; then
    git clone https://github.com/MentorEmbedded/nvptx-tools.git
    cd nvptx-tools
    git archive origin/master --prefix=nvptx-tools-${nvptx_tools_gitrev}/ | bzip2 -9 > ../nvptx-tools-${nvptx_tools_gitrev}.tar.bz2
    cd ..; rm -rf nvptx-tools
    mv nvptx-tools-${nvptx_tools_gitrev}.tar.bz2 ${CUR_DIR}/src/
fi

if [ ! -f ${CUR_DIR}/src/nvptx-newlib-${nvptx_newlib_gitrev}.tar.bz2 ] ; then
    git clone https://github.com/MentorEmbedded/nvptx-newlib.git
    cd nvptx-newlib
    git archive origin/master --prefix=nvptx-newlib-${nvptx_newlib_gitrev}/ | bzip2 -9 > ../nvptx-newlib-${nvptx_newlib_gitrev}.tar.bz2
    cd ..; rm -rf nvptx-newlib
    mv nvptx-newlib-${nvptx_newlib_gitrev}.tar.bz2 ${CUR_DIR}/src/nvptx-newlib-${nvptx_newlib_gitrev}.tar.bz2
fi

sed -i "s/Version\:\ .*/Version\:\ \ \ ${VERSION}/g" ${CUR_DIR}/src/gcc.spec

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src gcc.spec
