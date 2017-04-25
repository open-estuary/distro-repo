#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)
TARGET=$1

############################################################################
# To verify whether the rpm package has been signed successfully or not
############################################################################
verify_rpm_sign() {
    filename=$1

    if [ ! -z "$(rpm -qpi ${filename} | grep Signature | grep none)" ] ; then
        echo "Fail to sign ${filename}"
        exit 1
    fi
}

############################################################################
# Begin to sign rpm packages
############################################################################
if [ -d "${TARGET}" ] ; then
    for filename in $(find ${TARGET} -name '*.rpm')
    do
        if [ -f ${filename} ] ; then
            ${CUR_DIR}/rpmsign_expect ${filename}
            verify_rpm_sign ${filename}
        fi
    done
else
    ${CUR_DIR}/rpmsign_expect ${TARGET}
    verify_rpm_sign ${TARGET}
fi
