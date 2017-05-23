#!/usr/bin/env python

import sys
import os
import requests
import urlparse
import BeautifulSoup
import re

SRC_URL="http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/source/tree/Packages/"
PARENT_URL="pub/fedora/linux/development/rawhide"

INGORE_PACK_DICT={}

def init_ingore_packages(ignore_filename):
    """
    Initialize packages dict which are not need to be be built
    """
    name_dict = {}
    file_handle = open(ignore_filename)
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

def is_subref_ingored(sub_ref):
    if re.search(PARENT_URL, sub_ref):
        return True
    if re.search('\?', sub_ref):
        return True
    return False

def get_candidate_packages_name(src_url, dst_dir):
    """
    To get candidate packages name and store them into the speicifed directory
    """ 
    url_request = requests.get(src_url)
    url_rsp = url_request.text

    url_dict = {}

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    ignore_file = open(os.path.join(dst_dir, "ignored_urls"), "w")
    ref_list = get_href_list(url_rsp)
    for sub_ref in ref_list:
        if is_subref_ingored(sub_ref):
            ignore_file.write("%s\n"%sub_ref)
            continue
        url_dict[sub_ref] = urlparse.urljoin(src_url, sub_ref)

    for sub_key in url_dict.keys():
        sub_url = url_dict[sub_key]
        try :
            print("Try to open %s"%sub_url)
            url_request = requests.get(sub_url)
            url_rsp = url_request.text       
            url_request.close()      
        except :
            print("Ignore %s"%sub_url)
            continue
        
        print("Parse :%s"%sub_url)
        subfilename = sub_key
        subfilename = subfilename.replace("/", "") + "_name_list"
        subfilename = os.path.join(dst_dir, subfilename)
        file_is_open = False
        
        ref_list = get_href_list(url_rsp)
        for sub_ref in ref_list:
            if is_subref_ingored(sub_ref):
                ignore_file.write("%s\n"%sub_ref)
                continue

            rpm_url = urlparse.urljoin(sub_url, sub_ref) 
            if not rpm_url.endswith('.src.rpm'):
                ignore_file.write("not src rpm file:%s"%rpm_url)
                print("Ingore non rpm address:%s"%rpm_url)
                continue

            #try :
            #    url_request = urllib3.urlopen(rpm_url)
            #    url_request.close()
            #except :
            #    ignore_file.write("not exist:%s"%rpm_url)
            #    print("Ingore not exist address:%s"%rpm_url)
            
            if not file_is_open :
                file_is_open = True
                filehandle = open(subfilename, 'w')

            filehandle.write("%s\t%s\t%s\n"%(sub_ref, rpm_url, 0))

def generate_package_rpm_build_scripts(package_listdir, dst_builddir, ignored_dict):
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

            subdir = elems[0][0]
            rpm_url = elems[1]

            pos = elems[0].rfind('-')
            packagename = elems[0][:pos] 
            pos = packagename.rfind('-')
            packagename = packagename[:pos] 

            if ignored_dict.has_key(packagename):
                print("Ignore %s"%packagename)
                continue            

            dst_dir = os.path.join(dst_builddir, subdir)
            dst_dir = os.path.join(dst_dir, packagename)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            build_filename = os.path.join(dst_dir, "rpm_build.sh")
            build_file = open(build_filename, "w")

            #print("generating %s for %s:%s"%(build_filename, packagename, elems[0]))
            
            build_file.write('#!/bin/bash\n')
            build_file.write("\n")
            build_file.write('CUR_DIR=$(cd `dirname $0`; pwd)\n'); 
            build_file.write("\n")
            build_file.write('SRC_DIR=src\n')
            build_file.write('if [ ! -f ${CUR_DIR}/${SRC_DIR}/' + elems[0] +' ] ; then\n')
            build_file.write('    if [ ! -d ${CUR_DIR}/${SRC_DIR} ] ; then\n')
            build_file.write('        mkdir -p ${CUR_DIR}/${SRC_DIR}\n')
            build_file.write('    fi\n')
            build_file.write('    wget -O ${CUR_DIR}/${SRC_DIR}/' + elems[0] + ' ' + rpm_url + '\n')
            build_file.write('    pushd ${CUR_DIR}/${SRC_DIR} > /dev/null\n')
            build_file.write('    rpm2cpio ' + elems[0] + ' | cpio -div\n')
            build_file.write('    popd > /dev/null\n')
            build_file.write('fi\n')
            build_file.write('\n')
            build_file.write('${CUR_DIR}/../../../../../utils/rpm_build.sh  ${CUR_DIR}/${SRC_DIR}  ' + packagename + '.spec\n')
            build_file.close()
            os.chmod(build_filename, 0o755)


if __name__ == "__main__":
    ignore_filename = "./ignored_packages"
    dst_namelist = "./namelist"
    dst_builddir = "./packages"    

    if len(sys.argv) >= 2:
        ignore_filename = sys.argv[1]
    if len(sys.argv) >= 3:
        dst_namelist = sys.argv[2]
    if len(sys.argv) >= 4:
        packages_dir = sys.argv[3]

    ignored_dict = init_ingore_packages(ignore_filename)
    get_candidate_packages_name(SRC_URL, dst_namelist)
    generate_package_rpm_build_scripts(dst_namelist, dst_builddir, ignored_dict)

