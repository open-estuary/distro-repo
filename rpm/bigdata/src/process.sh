#!/bin/bash
CUR_DIR=$(cd `dirname $0`; pwd)
#source ${BIGDATA_HOME}/usrconf.properties
#CUR_DIR=$(cd `dirname $0`; pwd)
source $CUR_DIR/conf.properties
export TEMP_DIR=${BIGDATA_HOME}/install/temp
export HADOOP_ROOT=${BIGDATA_HOME}/install/hadoop
export SPARK_ROOT=${BIGDATA_HOME}/install/spark
export HADOOP_DAEMON=hadoop-daemon.sh
export YARN_DAEMON=yarn-daemon.sh
export ZKSERVER_SCRIPT=zkServer.sh
export HDFS_SCRIPT=hdfs
export SPARK_DAEMON=start-all.sh
export JAVA_HOME=${JAVA_HOME}

start_datanode(){
	echo "start $1 on $3"
	sh ${HADOOP_ROOT}/datanode/sbin/hadoop-daemon.sh start datanode
	sleep 5
}

stop_datanode(){
	echo "stop $1 on $3"
	sh ${HADOOP_ROOT}/datanode/sbin/hadoop-daemon.sh stop datanode
	sleep 5
}

start_zkfc(){
	echo "start zkfc"
	sh ${HADOOP_ROOT}/namenode/sbin/hadoop-daemon.sh start zkfc
}

stop_zkfc(){
	echo "stop zkfc"
	sh ${HADOOP_ROOT}/namenode/sbin/hadoop-daemon.sh stop zkfc
}

start_namenode(){
	start_zkfc
	echo "start $1 on $3"
	sh ${HADOOP_ROOT}/namenode/sbin/hadoop-daemon.sh start namenode
	sleep 5
}

stop_namenode(){
	echo "stop $1 on $3"
	sh ${HADOOP_ROOT}/namenode/sbin/hadoop-daemon.sh stop namenode
	sleep 5
	stop_zkfc
}

start_journalnode(){
	echo "start $1 on $3"
	sh ${HADOOP_ROOT}/journalnode/sbin/hadoop-daemon.sh start journalnode
	sleep 5
}

stop_journalnode(){
	echo "stop $1 on $3"
	sh ${HADOOP_ROOT}/journalnode/sbin/hadoop-daemon.sh stop journalnode
	sleep 5
}

start_rmzkfc(){
	echo "start rmzkfc"
	sh ${HADOOP_ROOT}/resourcemanager/sbin/yarn-daemon.sh start rmzkfc
}

stop_rmzkfc(){
	echo "stop rmzkfc"
	sh ${HADOOP_ROOT}/resourcemanager/sbin/yarn-daemon.sh stop rmzkfc
}

start_resourcemanager(){
	start_rmzkfc
	sleep 5
	echo "start $1 on $3"
	sh ${HADOOP_ROOT}/resourcemanager/sbin/yarn-daemon.sh start resourcemanager	
}

stop_resourcemanager(){
	echo "stop $1 on $3"
	sh ${HADOOP_ROOT}/resourcemanager/sbin/yarn-daemon.sh stop resourcemanager
	sleep 5
	stop_rmzkfc
}

start_nodemanager(){
	echo "start $1 on $3"
	sh ${HADOOP_ROOT}/nodemanager/sbin/yarn-daemon.sh start nodemanager
	sleep 5
}

stop_nodemanager(){
	echo "stop $1 on $3"
	sh ${HADOOP_ROOT}/nodemanager/sbin/yarn-daemon.sh stop nodemanager
	sleep 5
}

start_zookeeper(){
	echo "start $1 on $3"
	sh ${HADOOP_ROOT}/../zookeeper/bin/zkServer.sh start
	sleep 5
}

stop_zookeeper(){
	echo "stop $1 on $3"
	sh ${HADOOP_ROOT}/../zookeeper/bin/zkServer.sh stop 
	sleep 5
}

start_spark(){
	if [ $2 = 'NODE1' ];then
		echo "start $1 on $3"
		sh ${BIGDATA_HOME}/install/spark/sbin/start-all.sh
	fi
}

stop_spark(){
	if [ $2 = 'NODE1' ];then
		echo "stop $1 on $3"
		sh ${BIGDATA_HOME}/install/spark/sbin/stop-all.sh
	fi
}

start_process(){
 start_$1 $1 $2 $3
}

stop_process(){
 stop_$1 $1 $2 $3
}

namenode_format(){
	if [ $2 = 'NODE2' ];then
		sleep 10
	fi
	if [ $2 = 'NODE1' ];then
		echo "format zkfc"
		sleep 5
		sh ${HADOOP_ROOT}/namenode/bin/hdfs zkfc -formatZK
		sleep 5
		sh ${HADOOP_ROOT}/namenode/bin/hdfs namenode -format -clusterId myhacluster
		sleep 5
		sh ${HADOOP_ROOT}/namenode/bin/hdfs namenode -initializeSharedEdits -nonInteractive
		sleep 5
		scp -r ${BIGDATA_HOME}/tmp root@${CLUSTER_NODE2_IP}:${BIGDATA_HOME}/
	fi
	start_namenode $1 $2 $3 
	sleep 5
}



install_zookeeper(){
	extract_zookeeper $1 $4
	update_zookeeper_conf $1 $2 $3 $4
}

install_journalnode(){
	extract_hadoop $1
	update_hadoop_conf $1 $2 $3 $4
}

install_namenode(){
	extract_hadoop $1
	update_hadoop_conf $1 $2 $3 $4
}

install_datanode(){
	extract_hadoop $1
	update_hadoop_conf $1 $2 $3 $4
}

install_resourcemanager(){
	extract_hadoop $1
	update_hadoop_conf $1 $2 $3 $4
}

install_nodemanager(){
	extract_hadoop $1
	update_hadoop_conf $1 $2 $3 $4
}

install_spark(){
	extract_spark $1 
	update_spark_conf $1 $2 $3 $4
}

extract_hadoop(){
	#mkdir ${HADOOP_ROOT}
	sh ${basedir}/untar.sh ${BIGDATA_HOME}/hadoop-${HADOOP_VERSION}.tar.gz 
	mv ${TEMP_DIR}/hadoop-${HADOOP_VERSION} ${HADOOP_ROOT}/$1
	echo  > ${HADOOP_ROOT}/$1/etc/hadoop/slaves
	chmod  777 ${HADOOP_ROOT}/$1/bin/*
	chmod  777 ${HADOOP_ROOT}/$1/sbin/*
}

update_hadoop_conf(){
	echo "update hadoop conf start"
	export NODEMANAGER_RESOURCE_MEMORY=${yarn_nodemanager_resource_memory_mb}
	export NODEMANAGER_RESOURCE_CPU=${yarn_nodemanager_resource_cpu_vcores}
	export MAX_ALLOCATION_VCORES=${yarn_scheduler_maximum_allocation_vcores}
	export MAX_ALLOCATION_MEMORY=${yarn_scheduler_maximum_allocation_mb}
	export hadoop_tmp_dir=${hadoop_tmp_dir}
		export dfs_ha_namenode_id_1=nn1
    export dfs_ha_namenode_id_2=nn2
	export dfs_namenode_rpc_address_hacluster_nn1=${dfs_namenode_rpc_address_hacluster_nn1}
    export dfs_namenode_rpc_address_hacluster_nn2=${dfs_namenode_rpc_address_hacluster_nn2}
    export dfs_namenode_http_address_hacluster_nn1=${dfs_namenode_http_address_hacluster_nn1}
    export dfs_namenode_http_address_hacluster_nn2=${dfs_namenode_http_address_hacluster_nn2}
    export dfs_namenode_shared_edits_dir=${dfs_namenode_shared_edits_dir}
    export namenode_dfs_name_dir=${namenode_dfs_name_dir}
    export datanode_dfs_data_dir=${datanode_dfs_data_dir}
    export zk_address=${zk_address}
    export yarn_resourcemanager_address_rm1=${yarn_resourcemanager_address_rm1}
    export yarn_resourcemanager_admin_address_rm1=${yarn_resourcemanager_admin_address_rm1}
    export yarn_resourcemanager_resource_tracker_address_rm1=${yarn_resourcemanager_resource_tracker_address_rm1}
    export yarn_resourcemanager_scheduler_address_rm1=${yarn_resourcemanager_scheduler_address_rm1}
    export yarn_resourcemanager_webapp_address_rm1=${yarn_resourcemanager_webapp_address_rm1}

    export yarn_resourcemanager_address_rm2=${yarn_resourcemanager_address_rm2}
    export yarn_resourcemanager_admin_address_rm2=${yarn_resourcemanager_admin_address_rm2}
    export yarn_resourcemanager_resource_tracker_address_rm2=${yarn_resourcemanager_resource_tracker_address_rm2}
    export yarn_resourcemanager_scheduler_address_rm2=${yarn_resourcemanager_scheduler_address_rm2}
    export yarn_resourcemanager_webapp_address_rm2=${yarn_resourcemanager_webapp_address_rm2}
    export yarn_web_proxy_address=${yarn_web_proxy_address}
    export yarn_nodemanager_remote_app_log_dir=/tmp/logs
    export mapred_local_dir=${BIGDATA_HOME}/nmlocal
	export yarn_nodemanager_log_dirs=${BIGDATA_HOME}/nmlog
	export mapreduce_jobhistory_address=${mapreduce_jobhistory_address}
	export mapreduce_jobhistory_webapp_address=${mapreduce_jobhistory_webapp_address}

#	python ${basedir}/update.py $1 $2 $3 $4
	python ${basedir}/updatexml.py $1 $4
	echo "update hadoop conf completed"
}

extract_zookeeper(){
	echo "setup zookeeper start"
	mkdir ${BIGDATA_HOME}/install/zookeeper
	sh ${basedir}/untar.sh ${BIGDATA_HOME}/zookeeper-${ZOOKEEPER_VERSION}.tar.gz
	mv ${TEMP_DIR}/zookeeper-${ZOOKEEPER_VERSION}/* ${BIGDATA_HOME}/install/zookeeper
	chmod 777 ${BIGDATA_HOME}/install/zookeeper/bin/*	
	echo $2 > ${zk_data_dir}/myid
	echo "setup zookeeper completed"
}

update_zookeeper_conf(){
	mv ${BIGDATA_HOME}/install/zookeeper/conf/zoo_sample.cfg ${BIGDATA_HOME}/install/zookeeper/conf/zoo.cfg
	echo "server.1=${CLUSTER_NODE1_IP}:2888:3888" >> ${BIGDATA_HOME}/install/zookeeper/conf/zoo.cfg
	echo "server.2=${CLUSTER_NODE2_IP}:2888:3888" >> ${BIGDATA_HOME}/install/zookeeper/conf/zoo.cfg
	echo "server.3=${CLUSTER_NODE3_IP}:2888:3888" >> ${BIGDATA_HOME}/install/zookeeper/conf/zoo.cfg
	echo "maxSessionTimeout=600000" >> ${BIGDATA_HOME}/install/zookeeper/conf/zoo.cfg
	sed -i "s,dataDir=/tmp/zookeeper,dataDir=${zk_data_dir},g" ${BIGDATA_HOME}/install/zookeeper/conf/zoo.cfg
	sed -i "s,zookeeper.log.dir=.,zookeeper.log.dir=,g" ${BIGDATA_HOME}/install/zookeeper/conf/log4j.properties
	chmod 777 ${BIGDATA_HOME}/install/zookeeper/bin/*
}

extract_spark(){
	mkdir ${SPARK_ROOT}
	version=${HADOOP_VERSION}
	sh ${basedir}/untar.sh ${BIGDATA_HOME}/spark-${SPARK_VERSION}-bin-hadoop${version%.*}.tgz
	mv ${TEMP_DIR}/spark-${SPARK_VERSION}-bin-hadoop${version%.*}/* ${BIGDATA_HOME}/install/spark
	chmod 777 ${BIGDATA_HOME}/install/spark/bin/*
	chmod 777 ${BIGDATA_HOME}/install/spark/sbin/*
}

update_spark_conf(){
	cp ${HADOOP_ROOT}/datanode/etc/hadoop/*site.xml ${SPARK_ROOT}/conf/
	cp ${SPARK_ROOT}/lib/spark-*-yarn-shuffle.jar ${HADOOP_ROOT}/nodemanager/share/hadoop/yarn/
	cp ${basedir}/conf/spark/* ${SPARK_ROOT}/conf
	sed -i "s,@SPARK_CLASSPATH@,${SPARK_ROOT}/lib/*,g" `grep -rl '@SPARK_CLASSPATH@' ${SPARK_ROOT}/conf/`
	sed -i "s,@HADOOP_CONF_DIR@,${SPARK_ROOT}/conf,g" `grep -rl '@HADOOP_CONF_DIR@' ${SPARK_ROOT}/conf/`
	sed -i "s,@SPARK_LOG_CONF_PATH@,${SPARK_ROOT}/conf,g" `grep -rl '@SPARK_LOG_CONF_PATH@' ${SPARK_ROOT}/conf/`
	sed -i "s,@SPARK_DRIVER_LOG_PATH@,${BIGDATA_HOME},g" `grep -rl '@SPARK_DRIVER_LOG_PATH@' ${SPARK_ROOT}/conf/`
	sed -i "s,@YARN_JAR_PATH@,${SPARK_ROOT}/lib/*,g" `grep -rl '@YARN_JAR_PATH@' ${SPARK_ROOT}/conf/`
	sed -i "s,@SPARK_HOME@,${SPARK_ROOT}/,g" `grep -rl '@SPARK_HOME@' ${SPARK_ROOT}/conf/`
	sed -i "s,@SNAPPY_LIB_PATH@,${BIGDATA_HOME}/install/hadoop/nodemanager/lib/native,g" `grep -rl '@SNAPPY_LIB_PATH@' ${SPARK_ROOT}/conf/`
	sed -i "s,@JAVA_HOME@,${JAVA_HOME},g" `grep -rl '@JAVA_HOME@' ${SPARK_ROOT}/conf/`
#	cp ${BIGDATA_HOME}/wc2frm-2.1.11.jar ${SPARK_ROOT}/lib
	export spark_shuffle_service_port=23050
#	python ${basedir}/update.py $1 $2 $3 $4 
#	python ${basedir}/updatexml.py $1
	cp ${HADOOP_ROOT}/journalnode/etc/hadoop/slaves ${SPARK_ROOT}/conf/	
	for nodeno in ${CLUSTER_NODES[@]}
         do
          IP=$(eval echo $`echo 'CLUSTER_'$nodeno'_IP'` ) 
	  echo $IP >> ${SPARK_ROOT}/conf/slaves
	 done
}


add_dn_dir(){
    for node in ${CLUSTER_NODES[@]}
    do
	USERNAME=$(eval echo $`echo 'CLUSTER_'$node'_USERNAME'` )
        IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
        PWD=$(eval echo $`echo 'CLUSTER_'$node'_PWD'` )
        ssh $USERNAME@$IP "rm -rf ${zk_data_dir}/*;mkdir -p ${zk_data_dir};chown ${DN_SECURE_USER}:${DN_SECURE_USER_GROUP} -R ${zk_data_dir};"                        
	ssh $USERNAME@$IP "rm -rf ${datanode_dfs_data_dir};mkdir -p ${datanode_dfs_data_dir}; chown ${DN_SECURE_USER}:${DN_SECURE_USER_GROUP} -R ${datanode_dfs_data_dir};"
        ssh $USERNAME@$IP "rm -rf ${namenode_dfs_name_dir};mkdir -p ${namenode_dfs_name_dir}; chown ${DN_SECURE_USER}:${DN_SECURE_USER_GROUP} -R ${namenode_dfs_name_dir};"
    done
}

input=$1
if [ $# -lt 1 ]; then
    echo "Usage: install.sh {install | startup | start | install_all}"
    exit 0
fi

if [ $input = 'namenode_format' ];then
 namenode_format $2 $3 $4
elif [ $input = 'start_process' ];then
 start_process $2 $3 $4
elif [ $input = 'stop_process' ];then
 stop_process $2 $3 $4
fi
