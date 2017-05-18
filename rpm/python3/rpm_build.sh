#!/bin/bash

CUR_DIR=$(cd `dirname $0`; pwd)

${CUR_DIR}/rpm_build_lxml.sh
${CUR_DIR}/rpm_build_html5lib.sh
${CUR_DIR}/rpm_build_cssselect.sh
${CUR_DIR}/rpm_build_beautifulsoup.sh


