#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

if [ x"${1}" == x"workbench" ] ; then
    echo "Build MySQL workbench tool ..."
    if [ -z "$(which pip 2>/dev/null)" ] ; then
        sudo yum install -y python2-pip
        sudo python -m pip install --upgrade --force pip
        sudo pip install setuptools==33.1.1
    fi    
    sudo pip install paramiko
    SRC="workbench"
    SPEC_NAME="mysql-workbench.spec"
    
    if [ ! -f ${CUR_DIR}/${SRC}/antlr-3.4-complete.jar ] ; then
        sudo wget -O ${CUR_DIR}/${SRC}/antlr-3.4-complete.jar  http://www.antlr3.org/download/antlr-3.4-complete.jar
    fi

    RPM_SRC_FILE="mysql-workbench-community-6.3.9-1.el7.src.rpm"
    SRC_URL="http://repo.mysql.com/yum/mysql-tools-community/el/7/SRPMS/mysql-workbench-community-6.3.9-1.el7.src.rpm"
    RPM_EXTRA="--target=aarch64 --define='edition community'  --define='version 6.3.9'  --define='release 1'"
elif [ x"${1}" == x"util" ] ; then
    echo "Build MySQL utils tool ..."
    SRC="util"
    SPEC_NAME="mysql_utilities.spec"
    RPM_SRC_FILE="mysql-utilities-1.6.5-1.el7.src.rpm"
    SRC_URL="http://repo.mysql.com/yum/mysql-tools-community/el/7/SRPMS/mysql-utilities-1.6.5-1.el7.src.rpm"
elif [ x"${1}" == x"router" ] ; then
    SRC="router"
    SPEC_NAME="mysql-router.spec"
    RPM_SRC_FILE="mysql-router-2.1.3-1.el7.src.rpm"
    SRC_URL="http://repo.mysql.com/yum/mysql-tools-community/el/7/SRPMS/mysql-router-2.1.3-1.el7.src.rpm"
elif [ x"${1}" == x"shell" ] ; then
    SRC="shell"
    SPEC_NAME="mysql-shell.spec"
    RPM_SRC_FILE="mysql-shell-1.0.9-1.el7.src.rpm"
    SRC_URL="http://repo.mysql.com/yum/mysql-tools-community/el/7/SRPMS/mysql-shell-1.0.9-1.el7.src.rpm"
elif [ x"${1}" == x"connector-python" ] ; then
    SRC="connector-python"
    SPEC_NAME="mysql-connector-python.spec"
    RPM_SRC_FILE="mysql-connector-python-2.1.6-1.sles12.src.rpm"
    SRC_URL="http://repo.mysql.com/yum/mysql-connectors-community/sles/12/SRPMS/mysql-connector-python-2.1.6-1.sles12.src.rpm"
elif [ x"${1}" == x"connector-odbc" ] ; then
    SRC="connector-odbc"
    SPEC_NAME="myodbc3.spec"
    RPM_SRC_FILE="mysql-connector-odbc-5.3.8-1.sles12.src.rpm"
    SRC_URL="http://repo.mysql.com/yum/mysql-connectors-community/sles/12/SRPMS/mysql-connector-odbc-5.3.8-1.sles12.src.rpm"
elif [ x"${1}" == x"connector-cpp" ] ; then
    SRC="connector-cpp"
    SPEC_NAME="mysql-connector-c++.spec"
    RPM_SRC_FILE="mysql-connector-c++-1.1.2-1.remi.src.rpm"
    SRC_URL="http://rpms.remirepo.net/SRPMS/mysql-connector-c++-1.1.2-1.remi.src.rpm"
else
    echo "Please input valid tool names:workbench, util, router, shell, connector-python, connector-odbc, or connector-cpp"
    exit 1
fi

SRC_DIR=${SRC}

if [ ! -f ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ] ; then
    sudo wget -O ${CUR_DIR}/${SRC_DIR}/${RPM_SRC_FILE} ${SRC_URL}
    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null
    rpm2cpio ${RPM_SRC_FILE} | cpio -div
    popd > /dev/null
fi

if [ "${1}" == "connector-cpp" ] ; then
    SRC_FILE="mysql-connector-c++-1.1.8.tar.gz"
    DST_FILE="mysql-connector-c++-1.1.8.tar.gz"
    if [ ! -f ${CUR_DIR}/${SRC_DIR}/${DST_FILE} ] ; then
        rm -fr ${CUR_DIR}/${SRC_DIR}/*.tar.gz
        sudo wget -O ${CUR_DIR}/${SRC_DIR}/${DST_FILE} "http://ftp.ntu.edu.tw/MySQL/Downloads/Connector-C++/${SRC_FILE}"
    fi
fi

#sed -i 's/x86_64/aarch64/g' ${CUR_DIR}/${SRC_DIR}/mysql.spec

${CUR_DIR}/../../utils/rpm_build.sh ${CUR_DIR}/${SRC_DIR} ${SPEC_NAME} ${RPM_EXTRA}
