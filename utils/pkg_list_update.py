#!/usr/bin/env python

import sys
import os
import requests
import urlparse
import commands
import BeautifulSoup
import re


VERSION="5.0"

g_pkg_src = { 
    "CentOS" : { "rpm": "ftp://repoftp:repopushez7411@117.78.41.188/releases/"+VERSION+"/centos/SRPMS" },
    "Ubuntu" : { "deb": "ftp://repoftp:repopushez7411@117.78.41.188/releases/"+VERSION+"/ubuntu/dists/estuary-"+VERSION+"/main/source/Sources" },
    "Debian" : { "deb": "ftp://repoftp:repopushez7411@117.78.41.188/releases/"+VERSION+"/debian/dists/estuary-"+VERSION+"/main/source/Sources" },
}

def decode_rpm_packages_list(ftp_url, platform, pkg_dict):
    """
    To get candidate packages 
    """
  
    status, packages_rsp = commands.getstatusoutput("curl -l " + ftp_url + "/*")
   
    packages_rsp = packages_rsp.split('\n')
    for packagename in packages_rsp:
        packagename = packagename.strip()
        if packagename.endswith('.src.rpm'):
            pos = packagename.rfind('-')
            packagename = packagename[:pos]
            pos = packagename.rfind('-')
            basename = packagename[:pos]
            version =  packagename[pos+1:]

            packagename = basename + "\t" + version
            if pkg_dict.has_key(packagename):
                pkg_dict[packagename] = pkg_dict[packagename] + "," + platform
            else :
                pkg_dict[packagename] = platform
    return


def decode_deb_packages_list(src_url, platform, pkg_dict):
    source_file = "./local_tmp_deb_source_file"
    os.system("wget -O " + source_file + " " + src_url)
    
    deb_dict = {}
    file_handle = open(source_file)
    for line in file_handle:
        elems = re.split('\ +', line)
        packagename = ""
        if len(elems) >= 3 and re.search('.orig.tar', elems[2]):
            packagename = elems[2]
        elif len(elems) >=4 and re.search('.orig.tar', elems[3]):
            packagename = elems[3] 
            
        if packagename != "":            
            pos = packagename.find('.orig')
            packagename = packagename[:pos]
            pack_elems = packagename.split('_')
            basename = pack_elems[0]
            version = pack_elems[1]
            
            deb_dict[basename + "\t" + version] = 0

    for key in deb_dict.keys():
        if pkg_dict.has_key(key):
            pkg_dict[key] = pkg_dict[key] + "," + platform
        else:
            pkg_dict[key] = platform
    
    os.system("rm " + source_file)
    return

def gen_pkg_list(pkg_list_filename):
    pkg_dict = {}

    for key in g_pkg_src.keys():
        for pkg_type in g_pkg_src[key].keys():
            if pkg_type == "rpm" :
                decode_rpm_packages_list(g_pkg_src[key][pkg_type], key, pkg_dict)
            elif pkg_type == "deb" :
                decode_deb_packages_list(g_pkg_src[key][pkg_type], key, pkg_dict)


    filehandle = open(pkg_list_filename, "w")
    
    default_str = '''
* [Introduction](#1)
* [Packages List](#2)


# Open-Estuary Packages List
## <a name="1">Introduction</a>  
It lists the packages which are maintained by Open-Estuary team so far.

## <a name="2">Packages List</a> 
Currently the following packages are supported by Open-Estuary repo:
'''
    filehandle.write("%s\n"%default_str)
    filehandle.write("|Package Name|Estuary Releases|Packages Releases|CentOS|Ubuntu|Debian|Notes|\n")
    filehandle.write("|--|--|--|--|--|--|--|\n")

    pkg_keys = pkg_dict.keys()
    pkg_keys.sort()
    for pkg in pkg_keys:
        elems = pkg.split('\t')
        distro = pkg_dict[pkg]
        distro_enable_dict = {}
        for distro_key in g_pkg_src.keys():
            if re.search(distro_key, distro):
                distro_enable_dict[distro_key] = "Y"
        centos = distro_enable_dict.get("CentOS", "")
        ubuntu = distro_enable_dict.get("Ubuntu", "")
        debian = distro_enable_dict.get("Debian", "")
        filehandle.write("|%s|%s|%s|%s|%s|%s|%s|\n"%(elems[0], VERSION, elems[1], centos, ubuntu, debian, ""))

    filehandle.write("||||||||\n")
    filehandle.close()
    return


if __name__ == "__main__":
    output_filename = "../packages_list.md"
    if len(sys.argv) >= 2:
        output_filename = sys.argv[1]

    gen_pkg_list(output_filename)

