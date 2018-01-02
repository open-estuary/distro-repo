#!/bin/bash
CUR_DIR=$(cd `dirname $0`; pwd)
source $CUR_DIR/conf.properties

. $CUR_DIR/process.sh
basedir=$CUR_DIR
export HADOOP_ROOT=${BIGDATA_HOME}/install/hadoop

startup_cluster(){
for node in ${CLUSTER_NODES[@]}
 do	
  IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
  processes=$(eval echo $`echo 'CLUSTER_'$node'_PROCESSES'` )
  IFS=$OLD_IFS
  arr=($processes)
  IFS=","		
  for process in ${arr[@]}
   do
    if [ $process = 'journalnode' ];then
      ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh start_process $process $node $IP"
     elif [ $process = 'zookeeper' ];then
      ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh start_process $process $node $IP"
    fi
   done      
 done
for node in ${CLUSTER_NODES[@]}
 do
  IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
  processes=$(eval echo $`echo 'CLUSTER_'$node'_PROCESSES'` )
  IFS=$OLD_IFS
  arr=($processes)
  IFS=","
  for process in ${arr[@]}
   do
    if [ $process = 'journalnode' ];then
      echo $process
     elif [ $process = 'zookeeper' ];then
      echo $process
     elif [ $process = 'namenode' ];then
      ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh namenode_format $process $node $IP"
     else
      ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh start_process $process $node $IP"
    fi
   done
 done	
}

start_cluster(){
for node in ${CLUSTER_NODES[@]}
 do
  IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
  processes=$(eval echo $`echo 'CLUSTER_'$node'_PROCESSES'` )
  IFS=$OLD_IFS
  arr=($processes)
  IFS=","
  for process in ${arr[@]}
   do
    if [ $process = 'journalnode' ];then
      ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh start_process $process $node $IP"
     elif [ $process = 'zookeeper' ];then
      ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh start_process $process $node $IP"
    fi
   done
 done
for node in ${CLUSTER_NODES[@]}
    do	
	IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
	processes=$(eval echo $`echo 'CLUSTER_'$node'_PROCESSES'` )
	IFS=$OLD_IFS
        arr=($processes)
        IFS=","		
        for process in ${arr[@]}
        do			
	 if [ $process = 'journalnode' ];then
          echo $process
    	 elif [ $process = 'zookeeper' ];then
     	  echo $process
	 else
	  ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh start_process $process $node $IP"
	fi
        done      
done	
}

stop_cluster(){
for node in ${CLUSTER_NODES[@]}
    do
        IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
        processes=$(eval echo $`echo 'CLUSTER_'$node'_PROCESSES'` )
        IFS=$OLD_IFS
        arr=($processes)
        IFS=","
        for process in ${arr[@]}
        do
         ssh root@${IP} "cd ${BIGDATA_HOME} ;sh ./process.sh stop_process $process $node $IP"
        done
    done
}

remove_cluster(){
	for node in ${CLUSTER_NODES[@]}
	do
		USERNAME=$(eval echo $`echo 'CLUSTER_'$node'_USERNAME'` )
		IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
		PWD=$(eval echo $`echo 'CLUSTER_'$node'_PWD'` )
		echo "Remove cluster on $IP"
		ssh ${USERNAME}@${IP} rm -rf ${BIGDATA_HOME}			
	done
}

install_all(){
    rm -rf ${BIGDATA_HOME}/install
    mkdir -p ${BIGDATA_HOME}/install
    rm -rf ${TEMP_DIR}
    mkdir -p ${TEMP_DIR}
    mkdir ${HADOOP_ROOT}
    echo 'tarfile=$1;destdir=${TEMP_DIR};tar -xzf $tarfile -C $destdir' > ${basedir}/untar.sh
    processes=$(eval echo $`echo 'CLUSTER_'$1'_PROCESSES'` )
    IFS=$OLD_IFS
    arr=($processes)
    IFS=","
    for process in ${arr[@]}
    do
	echo "Begin to install $process on $2"
        install_$process $process $1 $2 $3
    done 
    rm -rf ${TEMP_DIR}
    rm -rf ${basedir}/untar.sh
}

remote_setup(){
for node in ${CLUSTER_NODES[@]}
    do
	echo "Begin to setup cluster"
	USERNAME=root
	ID=$(eval echo $`echo 'CLUSTER_'$node'_ID'` )
        IP=$(eval echo $`echo 'CLUSTER_'$node'_IP'` )
        PWD=$(eval echo $`echo 'CLUSTER_'$node'_PWD'` )
	ssh ${USERNAME}@${IP} "mkdir -p ${BIGDATA_HOME}; chown $USERNAME:users -R ${BIGDATA_HOME}"
	scp -r ${basedir}/* ${USERNAME}@${IP}:${BIGDATA_HOME}
	ssh ${USERNAME}@${IP} "cd ${BIGDATA_HOME}; dos2unix *.sh ; chmod +x *"
	ssh ${USERNAME}@${IP} "cd ${BIGDATA_HOME} ;echo ${IP} ;sh ./install.sh remote $node $IP $ID "
    done
}


install_cluster(){
        OLD_IFS=$IFS
        IFS=","
        remove_cluster
        add_dn_dir
	remote_setup
        IFS=$OLD_IFS
}

uninstall_cluster(){
  stop_cluster
  OLD_IFS=$IFS
  IFS=","
  remove_cluster
  IFS=$OLD_IFS

}


input=$1
if [ $# -lt 1 ]; then
    echo "Usage: install.sh {install | startup | start | stop}"
    exit 0
fi
OLD_IFS=$IFS
IFS=","
if [ $input = 'install' ];then
 install_cluster
elif [ $input = 'start' ];then
 start_cluster
elif [ $input = 'startup' ];then
 startup_cluster
elif [ $input = 'remote' ];then
 install_all $2 $3 $4
elif [ $input = 'stop' ];then
 stop_cluster
elif [ $input = 'uninstall' ];then
 uninstall_cluster
fi
IFS=$OLD_IFS


