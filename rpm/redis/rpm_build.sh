#!/bin/bash

CUR_DIR="$(cd `dirname $0`; pwd)"
${CUR_DIR}/rpm_build_redis.sh
${CUR_DIR}/rpm_build_protocol.sh

