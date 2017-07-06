#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)
TARGET=$1

if [ ! -d "${1}" ] ; then
    echo "Input must be one directory!"
    exit -1
fi

passphrase=$(cat /home/KEY_PASSPHRASE)

############################################################################
# To verify whether the rpm package has been signed successfully or not
############################################################################
verify_rpm_sign() {
    filename=$1

    rpm -qpi ${filename} | grep Signature
    if [ ! -z "$(rpm -qpi ${filename} | grep Signature | grep none)" ] ; then
        echo "Fail to sign ${filename}"
        exit 1
    fi
}

############################################################################
# Begin to sign rpm packages
############################################################################
for filename in ${TARGET}/*.rpm
do
expect <<-END
        set timeout -1
        spawn rpm --resign ${filename}
        expect {
                "Enter pass phrase:" {send "${passphrase}\r"}
                timeout {send_user "Enter pass phrase timeout\n"}
        }
        expect eof
END
   verify_rpm_sign ${filename}
done


