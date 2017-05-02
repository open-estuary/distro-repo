#! /bin/bash

sshcmd()
{
	myssh_cmd="$1"
	sleeptime=0
	sh sshcmd.sh -c "$myssh_cmd" -m "$IP" -u "$loginuser" -p "$loginpassword"
	if [ $? -ne 0 ]; then
                while true
                do
                        if ping -c5 "$IP" &> /dev/null; then
                                break
                        fi
                        if [ $sleeptime -ge 180 ]; then
                                echo "ERROR: ping $IP Failed"
                                break
                        fi
                        sleep 60
                        ((sleeptime = sleeptime + 60))
                done
                sh sshcmd.sh -c "$myssh_cmd" -m "$IP" -u "$loginuser" -p "$loginpassword"
                if [ $? -ne 0 ]; then
                	echo " Failed in sshscp.sh, maybe there is no enough space on $IP"
                        exit 1
                fi
        fi
		
}

sshscp()
{
	MYSOURCE="$1"
	MYDESTDIR="$2"
	isdir="$3"
	tofrom="$4"
	sleeptime=0
	scpcmd=
	if [ "$isdir" = "is" ]; then
		if [ $tofrom = "to" ]; then
			scpcmd="sh sshscp.sh -s $MYSOURCE -d $loginuser@$IP:$MYDESTDIR -p $loginpassword -r "
		elif [ $tofrom = "from" ]; then
			scpcmd="sh sshscp.sh -s $loginuser@$IP:$MYSOURCE -d $MYDESTDIR -p $loginpassword -r "
		else
			echo "wrong tofrom parameter"
			exit 1
		fi
	elif [ "$isdir" = "no" ]; then
		if [ $tofrom = "to" ]; then
                        scpcmd="sh sshscp.sh -s $MYSOURCE -d $loginuser@$IP:$MYDESTDIR -p $loginpassword  "
                elif [ $tofrom = "from" ]; then
                        scpcmd="sh sshscp.sh -s $loginuser@$IP:$MYSOURCE -d $MYDESTDIR -p $loginpassword  "
                else
                        echo "wrong tofrom parameter"
                        exit 1
                fi
	else
		echo "wrong isdir parameter"
		exit 1
	fi
	echo "$scpcmd"	
	eval $scpcmd
	if [ $? -ne 0 ]; then
		while true
		do
			if ping -c5 "$IP" &> /dev/null; then
				break
			fi
			if [ $sleeptime -ge 180 ]; then
				echo "ERROR: ping $IP Failed"
				break
			fi
			sleep 60
			((sleeptime = sleeptime + 60))
		done
		eval $scpcmd
		if [ $? -ne 0 ]; then
			echo " Failed in sshscp.sh, maybe there is no enough space on $IP"
			exit 1
		fi
	fi
}


builddeb()
{
        program="$1"
        version="$2"
        sshcmd "export DEBFULLNAME="test"; export DEBEMAIL="test@test.com"; cd dmidecode-3.0; dh_make -s -copyright gpl3 -f ../dmidecode-3.0.tar.gz <<EOF
y
EOF; echo "override_dh_usrlocal:" >> debian/rules; dpkg-buildpackage -rfakeroot; cd -"
        if [ $? -ne 0]; then
                echo "dpkg package build failed"
        fi
}

