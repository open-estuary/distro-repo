CUR_DIR=$(cd `dirname $0`; pwd)

${CUR_DIR}/../../utils/rpm_build.sh  ${CUR_DIR}/src bigdata.spec
