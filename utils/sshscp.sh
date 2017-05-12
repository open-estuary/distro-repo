#! /bin/bash

exelocal=1

sshcmd_comm()
{
	srccommand="$1"
	descommand="$2"
	password="$3"
	r_option="$4"
	timeout=180

	if [ "x$srccommand" = "x" -o "x$descommand" = "x" ]; then
		echo "wrong parameter"
		exit 1
	fi

	if [ $r_option = 1 ]; then
		r_option="-r"
	else
		r_option=""
	fi

	expect <<-END1
		set timeout -1

		spawn scp -o "ConnectTimeout ${timeout}" ${r_option} $srccommand $descommand

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
	echo "Usage: sshscp.sh -s "src" -d "des" [-p login_password] [-r]"
}

delete_known_hosts()
{
	known_hosts=/root/.ssh/known_hosts
        sudo > ${known_hosts}
}

src=
des=
loginpassword=
r_option=0

while getopts "u:p:s:d:hr" OPTIONS
do
	case $OPTIONS in
		p) loginpassword="$OPTARG";;
		s) src="$OPTARG";;
		d) des="$OPTARG";;
		r) r_option=1;;
		h) usage;exit 1;;
		\?) echo "ERROR - Invalid Parameter"; echo "ERROR - Invalid parameter" >&2; usage; exit 1;;
		*) echo "ERROR - Invalid Parameter"; echo "ERROR - Invalid parameter" >&2; usage; exit 1;;
	esac
done

if [ "x$src" = "x" -o "x$des" = "x" ]; then
	echo "$src  $des"
	usage
	exit 1
fi

delete_known_hosts
sshcmd_comm "$src" "$des" "$loginpassword" "${r_option}"

exit $?
