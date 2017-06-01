#!/usr/bin/env python

import sys
import os
import requests
import urlparse
import BeautifulSoup
import re

SRC_URL="http://vault.centos.org/centos/7.3.1611/sclo/Source/rh"
PARENT_URL="centos/7/sclo/Source"

INGORE_PACK_DICT={}

def init_candidate_packages(candidate_filename):
    """
    Initialize packages dict which need to be be built
    """
    name_dict = {}
    
    if not os.path.exists(candidate_filename):
        return name_dict

    file_handle = open(candidate_filename)
    for line in file_handle:
        name_dict[line.strip()] = 0
    return name_dict

def get_href_list(html):
    href_list = []
    parser = BeautifulSoup.BeautifulSoup(html)
    for link in parser.findAll('a'):
        sub_ref = link.get('href')
        href_list.append(sub_ref)
    return href_list

def is_subref_candidate(sub_ref):
    if re.search(PARENT_URL, sub_ref):
        return True

    if re.search('\.\.', sub_ref):
        return True

    if re.search('\?', sub_ref):
        return True
    
    if sub_ref == '/' or sub_ref == '//' or sub_ref == '.' or sub_ref == '..' or sub_ref == './' or sub_ref == '../':
        return True

    if re.search("repodata", sub_ref):
        return True

    return False


def get_candidate_urls(src_url):
    """
    To get candidate urls
    """
    #print("Open:%s"%src_url) 
    if src_url.endswith('.rpm'):
        dst_url = []
        dst_url.append(src_url)
        return dst_url

    try :
        url_request = requests.get(src_url)
        url_rsp = url_request.text
    except :
        dst_url = []
        dst_url.append(src_url)
        return dst_url

    url_dict = {}
    ref_list = get_href_list(url_rsp)
    for sub_ref in ref_list:
        if is_subref_candidate(sub_ref):
            continue

        #url_dict[sub_ref] = urlparse.urljoin(src_url, sub_ref)
        if src_url[-1] != '/':
            src_url += '/'
        url_dict[sub_ref] = src_url + sub_ref

    dst_url = []
    for url in url_dict.keys():
        url_list = get_candidate_urls(url_dict[url])
        dst_url.extend(url_list)
    return dst_url


def get_candidate_packages_name(src_url, dst_dir):
    """
    To get candidate packages name and store them into the speicifed directory
    """ 
    dst_url_list = get_candidate_urls(src_url)
    print("Final:%s"%dst_url_list)

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    candidate_file = open(os.path.join(dst_dir, "candidate_urls"), "w") 
    packages_file_name = os.path.join(dst_dir, "packages_name_list")
    filehandle = open(packages_file_name, 'w')
    for url in dst_url_list:
        print("Parse :%s"%url)
        file_is_open = False
       
        rpm_url = url 
        if not rpm_url.endswith('.src.rpm'):
            candidate_file.write("not src rpm file:%s"%rpm_url)
            print("Ingore non rpm address:%s"%rpm_url)
            continue

        pos = url.rfind('/')
        subfilename = url[pos:]

        filehandle.write("%s\t%s\t%s\n"%(subfilename, rpm_url, 0))

def generate_package_rpm_build_scripts(package_listdir, dst_builddir, candidate_dict):
    """
    To generate rpm build scripts for each package
    """
    

    file_lists = [os.path.join(package_listdir, name) for name in os.listdir(package_listdir) 
                   if os.path.isfile(os.path.join(package_listdir, name)) ] 

    for package_file in file_lists:
        filehandle = open(package_file)
        for line in filehandle:
            elems = line.strip().split('\t')
            if len(elems) <= 2:
                continue

            if elems[0][0] == '/':
                elems[0] = elems[0][1:]
            
            rpm_url = elems[1]
            pos = elems[0].rfind('-')
            packagename = elems[0][:pos] 
            if packagename[0] == '/':
                packagename = packagename[1:]
            pos = packagename.rfind('-')
            packagename = packagename[:pos] 

            if len(candidate_dict.keys()) > 0 and not candidate_dict.has_key(packagename):
                continue

            dst_dir = os.path.join(dst_builddir, packagename)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            build_filename = os.path.join(dst_dir, "rpm_build.sh")
            build_file = open(build_filename, "w")

            #print("generating %s for %s:%s"%(build_filename, packagename, elems[0]))
            pos = rpm_url.rfind('/')
            base_url = rpm_url[:pos]

            build_file.write('#!/bin/bash\n')
            build_file.write("\n")
            build_file.write('CUR_DIR=$(cd `dirname $0`; pwd)\n'); 
            build_file.write("\n")
            build_file.write('SRC_RPM_FILE=' + elems[0] + '\n')
            build_file.write('SRC_DIR=src\n')
            build_file.write('if [ ! -f ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} ] ; then\n')
            build_file.write('    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then\n')
            build_file.write('        mkdir -p ${CUR_DIR}/${SRC_DIR}\n')
            build_file.write('    fi\n')
            build_file.write('    wget -O ${CUR_DIR}/${SRC_DIR}/${SRC_RPM_FILE} ' + base_url + '/${SRC_RPM_FILE}\n')
            build_file.write('    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null\n')
            build_file.write('    rpm2cpio ${SRC_RPM_FILE} | cpio -div\n')
            build_file.write('    popd > /dev/null\n')
            build_file.write('fi\n')
            build_file.write('\n')
            build_file.write('${CUR_DIR}/../../../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR}  ' + packagename + '.spec\n')
            build_file.close()
            os.chmod(build_filename, 0o755)


if __name__ == "__main__":
    candidate_filename = "./candidate_packages"
    dst_namelist = "./namelist"
    dst_builddir = "./packages"    

    if len(sys.argv) >= 2:
        candidate_filename = sys.argv[1]
    if len(sys.argv) >= 3:
        dst_namelist = sys.argv[2]
    if len(sys.argv) >= 4:
        packages_dir = sys.argv[3]

    candidate_dict = init_candidate_packages(candidate_filename)
    #get_candidate_packages_name(SRC_URL, dst_namelist)
    generate_package_rpm_build_scripts(dst_namelist, dst_builddir, candidate_dict)

