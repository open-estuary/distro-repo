#!/usr/bin/env python

import sys
import os
import requests
import urlparse
import commands
import BeautifulSoup
import re


CASSANDRA_RPM_URL="http://rpm.datastax.com/community/noarch"

def get_href_list(html):
    href_list = []
    parser = BeautifulSoup.BeautifulSoup(html)
    for link in parser.findAll('a'):
        sub_ref = link.get('href')
        href_list.append(sub_ref)
    return href_list

def download_rpm_pkg(src_url, output_dir):
    """
    To get candidate packages 
    """

    url_request = requests.get(src_url)
    url_rsp = url_request.text

    pkg_dict = {}
    ref_list = get_href_list(url_rsp)  
    for link_name in ref_list:
        if not link_name.endswith(".rpm"):
            continue 
        if link_name[0] != '/':
            link_name = "/" + link_name

        base_name = link_name.split('.')[0]
        pos = base_name.rfind('-')
        base_name = base_name[:pos]
        if pkg_dict.has_key(base_name):
            if link_name > pkg_dict[base_name]:
                pkg_dict[base_name] = link_name
        else :
            pkg_dict[base_name] = link_name

    for base_name in pkg_dict.keys():
        link_name = pkg_dict[base_name]
        package_url = src_url + link_name
        os.system("wget -O " + output_dir + link_name + " " + package_url)
    return

if __name__ == "__main__":
    output_dir = sys.argv[1]
    download_rpm_pkg(CASSANDRA_RPM_URL, output_dir)

