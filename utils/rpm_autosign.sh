#! /bin/bash

passphrase=`cat /home/KEY_PASSPHRASE`
CUR_DIR=$(cd `dirname $0`; pwd)

SPEC_FILE=$1

expect <<-END1
        spawn rpmbuild --sign -ba ${CUR_DIR}/rpmbuild/SPECS/$SPEC_FILE
        expect {
                "Enter pass phrase:"{
                        send "${passphrase}\r"
                }
	
        }               

END1

