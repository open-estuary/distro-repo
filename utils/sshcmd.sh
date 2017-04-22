#! /bin/sh

execcmd=
machineip=
loginuser=
loginpassword=

sshcmd_comm()
{
	cmd="$1"
	testip="$2"
	password="${3}"
	user="${4}"
	timeout=180

	if [ "$1x" = "x" ]; then
		echo "ssh_password cmd targetip [password] [user]"
		return 1
	fi

	if [ "x${testip}" = "x" ]; then
		testip=$testmachine
	fi

	#cmd=${cmd//\"/\\\"}
	#cmd=${cmd//\$/\\\$}

	if [ "x$testip" = "x" -o "x${cmd}" = "x" ]; then
		echo "isup time testmachine [password] [user]"
		exit 1
	fi
	
	expect <<-END1
		set timeout -1

		spawn ssh -o "ConnectTimeout ${timeout}" ${user}@${testip} "${cmd}"

		expect {
			"Are you sure you want to continue connecting (yes/no)?" {
				send "yes\r"
				expect -re "\[P|p]assword:"
				send "${password}\r"
			}
			
			-re "\[P|p]assword:" {
				send "${password}\r"
			}

			timeout {
				send_user "connection to $targetip timed out: \$expect_out(buffer)\n"
				exit 13
			}
				
			eof {
				catch wait result
				exit [lindex \$result 3]
			}
		}
		expect {
			eof {
                                catch wait result
                                exit [lindex \$result 3]
                        }
			
			-re "\[P|p]assword:" {
				send_user "invalid password or account. \$expect_out(buffer)\n"
				exit 13
			}
			
			timeout {
				send_user "connection to $targetip time out: \$expect_out(buffer)\n"
				exit 13
			}
		}
	END1
	return $?
}

usage()
{
	echo "Usage: sshcmd.sh -c "command" -m "machineip" [-u login_user] [-p login_password]"
}
while getopts "c:m:p:u:h" OPTIONS
do
	case $OPTIONS in
		c) execcmd="$OPTARG";;
		m) machineip="$OPTARG";;
		u) loginuser="$OPTARG";;
		p) loginpassword="$OPTARG";;
		\?) echo "ERROR - Invalid Parameter"; echo "ERROR - Invalid parameter" >&2; usage; exit 1;;
		*) echo "ERROR - Invalid Parameter"; echo "ERROR - Invalid parameter" >&2; usage; exit 1;;
	esac
done

if [ "x$execcmd" = "x" -o "x$machineip" = "x" ]; then
	usage
	exit
fi

sshcmd_comm "$execcmd" "$machineip" "$loginpassword" "$loginuser"

exit $?
