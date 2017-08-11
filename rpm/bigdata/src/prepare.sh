#!/bin/bash

#echo "please input config file(properties and xml)"
#echo "e.g.: config.properties config.xml"
#read pro xml
echo $1 $2
source $1
CUR_DIR=$(cd `dirname $0`; pwd)
export BIGDATA_HOME=${BIGDATA_HOME}
cp $1 ${CUR_DIR}/usrconf.properties
cp $2 ${CUR_DIR}/conf.xml
pro=`basename $1`
xml=`basename $2`
export PRO_FILE=$1
if [ ! -f ${CUR_DIR}/hadoop-${HADOOP_VERSION}.tar.gz ] ; then
 #sudo wget http://apache.fayea.com/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz -P ${CUR_DIR}
 sudo wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz -P ${CUR_DIR}
fi
if [ ! -f ${CUR_DIR}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz ] ; then
 #sudo wget http://apache.fayea.com/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz -P ${CUR_DIR}
 sudo wget http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-${ZOOKEEPER_VERSION}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz -P ${CUR_DIR}
fi
version=${HADOOP_VERSION}
if [ ! -f ${CUR_DIR}/spark-${SPARK_VERSION}-bin-hadoop${version%.*}.tgz ] ; then
 #sudo wget http://apache.fayea.com/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${version%.*}.tgz -P ${CUR_DIR}
 sudo wget http://mirror.bit.edu.cn/apache/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${version%.*}.tgz -P ${CUR_DIR}
fi
#sh $CUR_DIR/install.sh install
