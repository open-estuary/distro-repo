#!/usr/bin/env python

import sys
import os
#import requests
import urlparse
#import BeautifulSoup
import re
import threading

global_lock = threading.Lock()

#REPO_URLS = [ 
#   "http://repo.estuarydev.org/releases/5.0/centos/"
#]
#"""
#REPO_URLS = [ 
#   "http://repo.linaro.org/rpm/linaro-overlay/centos-7/repo",
#   "http://download.fedoraproject.org/pub/epel/7/aarch64",
#   "http://repo.estuarydev.org/releases/5.0/centos/"
#   "http://mirror.centos.org/altarch/7/os/aarch64/"
#]
#"""
#PARENT_URLS = []


def get_all_packages_name():
    """
    To get candidate packages name
    """ 
    name_dict = {}
    num = 0
    os.system("mv /etc/apt/sources.list /root/")
    os.system("wget -O - http://repo.estuarydev.org/releases/ESTUARY-GPG-KEY | apt-key add -")
    if targetos == "ubuntu":
        os.system("wget -O /etc/apt/sources.list.d/estuary.list https://raw.githubusercontent.com/open-estuary/distro-repo/master/estuaryftp_ubuntu.list")
    elif targetos == "debian":
        os.system("wget -O /etc/apt/sources.list.d/estuary.list https://raw.githubusercontent.com/open-estuary/distro-repo/master/estuaryftp_debian.list") 
    os.system("apt-get update")
    packages_list = os.popen("apt-cache search all ").readlines()
    for packagename in packages_list:
        #packagename = packagename.split(':')[0]
        pos = packagename.rfind('-')
        packagename = packagename[:pos]
        name_dict[packagename] = name_dict.get(packagename, 0) + 1
        num += 1
    print("The repository has %d packages"%(num))
    os.system("mv /root/sources.list /etc/apt/")
    os.system("apt-get update")
    print name_dict
    return name_dict

#    name_dict = {}
#    repos_list = []
#    available_repos = os.popen("yum repolist").readlines()
#    begin_to_parse = False
#    for key in available_repos:
#        if re.search('repo id', key):
#            begin_to_parse = True
#            continue      
#        elif not begin_to_parse:
#            continue
#        
#        if not re.search("repolist", key):
#            repo_id = re.split(' +', key)[0]
#            if repo_id[0] == '!':
#                repo_id = repo_id[1:]
#            repo_id = repo_id.split('/')[0]
#            repos_list.append(repo_id)

#    for repo_id in repos_list:
#        num = 0
#        packages_list = os.popen("repoquery -qa --repoid=" + repo_id).readlines()
#        for packagename in packages_list:
#            packagename = packagename.split(':')[0]
#            pos = packagename.rfind('-')
#            packagename = packagename[:pos]
#            name_dict[packagename] = name_dict.get(packagename, 0) + 1
#            num += 1
#        print("The repository:%s has %d packages"%(repo_id, num))
#    return name_dict

def rpm_erase_all_packages(logdir):
    packages_name = get_all_packages_name()
    
    del_failure = open(os.path.join(logdir, "del_failure_list"), "w")
    del_success = open(os.path.join(logdir, "del_success_list"), "w")
    for package in packages_name.keys():
        os.system("apt-get remove -y " + package)
        ret = os.popen("dpkg -l | grep " + package).readlines()
        
        if len(ret) > 0:
            del_failure.write("%s\t\n"%package)
	else :
            del_success.write("%s\t\n"%package)
    return

def rpm_install_all_packages(logdir):
    packages_name = get_all_packages_name()

    install_failure = open(os.path.join(logdir, "install_failure_list"), "w")
    install_success = open(os.path.join(logdir, "install_success_list"), "w")
    for package in packages_name.keys():
        os.system("apt-get install -y " + package)
        ret = os.popen("dpkg -l | grep " + package).readlines()
        
        if len(ret) > 0:
            install_success.write("%s\t\n"%package)
	else :
            install_failure.write("%s\t\n"%package)
    return

if __name__ == "__main__":
    logdir = "/tmp/debverifylog"
    cmd = ""
    targetos = "ubuntu" 
    if len(sys.argv) >= 4:
        targetos = str(sys.argv[3])
    if len(sys.argv) >= 3:
        logdir = str(sys.argv[2])
    if len(sys.argv) >= 2:
        cmd = str(sys.argv[1])
       
    if not os.path.exists(logdir):
        os.makedirs(logdir)    

    if cmd == "install" :
        rpm_install_all_packages(logdir)
    elif cmd == "erase" :
        rpm_erase_all_packages(logdir)
    else :
        print("Usage: ./rpm_verify.py {install | erase} <log dir> <debian/ubuntu>")


