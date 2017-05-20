#!/usr/bin/env python

import os
import sys
import subprocess
import re
import multiprocessing

MAX_PROCESS_NUM = 64
global_lock = multiprocessing.Lock()

RPM_AARCH64_DIR=os.path.join(os.environ['HOME'], "rpmbuild/RPMS/aarch64/")
RPM_NOARCH_DIR=os.path.join(os.environ['HOME'], "rpmbuild/RPMS/noarch/")

def save_rpm_build_result(packagename, logdir, backdir):
   is_sucessful = False 
   for filename in os.listdir(RPM_AARCH64_DIR):
       if filename.endswith('.aarch64.rpm') and filename.startwith(packagename):
           is_successful = True
           break

   if not is_successful:
       for filename in os.listdir(RPM_NOARCH_DIR):
           if filename.endswith('.noarch.rpm') and filename.startwith(packagename):
               is_successful = True
               break

   if is_successful :
       logfile = "successful_list"
   else : 
       logfile = "failure_list"
   
   global_lock.acquire()
   filehandle = open(logfile, 'w+')
   filehandlw.write(packagename + '\n')
   global_lock.release()   

   os.system("mv " + RPM_AARCH64_DIR + "/" + packagename + '* ' + backdir + "/aarch64/")
   os.system("mv " + RPM_NOARCH_DIR + "/" + packagename + '* ' + backdir + "/noarch/")

def build_sub_package(buildfile, logdir, backdir, succ_dict):
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    buildfile = os.path.abspath(buildfile)
    basename = os.path.basename(buildfile)
    dirname = os.path.dirname(buildfile)
    logfile = os.path.join(logdir, dirname.split('/')[-1])  
    packagename = dirname.split('/')[-1]

    if succ_dict.has_key(packagename):
        print("%s has been built successfully before")
        return 0

    proc = subprocess.Popen([buildfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    log_stdout = open(logfile+"_stdout", 'w')
    for line in proc.stdout:
        log_stdout.write(line)

    log_stderr = open(logfile+"_stderr", "w")
    for line in proc.stderr:
        log_stderr.write(line)

    save_rpm_build_result(packagename, logdir, backdir)
    return 0

def get_all_build_files(dirname):
    file_list = []
    for filename in os.listdir(dirname):
        fullname = os.path.join(dirname, filename)
        if os.path.isfile(fullname) and filename == 'rpm_build.sh':
            file_list.append(fullname)
        elif os.path.isdir(fullname):
            file_list.extend(get_all_build_files(fullname))
    return file_list

def build_packages(package_dir, logdir, rpm_backdir):
    buildfiles_list = get_all_build_files(package_dir)

    succ_dict = {} 
    previous_success_log = os.path.join(logdir, "successful_list")
    if os.path.exists(previous_success_log):
        for line in open(previous_success_log):
            succ_dict[line.strip()] = 0

    process_list = []
    for package in buildfiles_list:
        if len(process_list) >= MAX_PROCESS_NUM:
            for process in process_list:
                process.join()
            process_list = []

        print("Begin to build:%s"%package)
        process = multiprocessing.Process(target = build_sub_package, args=(package, logdir, rpm_backdir, succ_dict))
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()
    process_list = []
       

if __name__ == "__main__":
    packagedir = "./packages"
    logdir = "./logdir"
    rpm_backdir = "./rpmback"

    if len(sys.argv) >= 2:
        packagedir = sys.argv[1]
    if len(sys.argv) >= 3:
        logdir = sys.argv[2]
    if len(sys.argv) >= 4:
        rpm_backdir = sys.argv[3]  

    if not os.path.exists(rpm_backdir):
        os.makedirs(os.path.join(rpm_backdir, "noarch"))
        os.makedirs(os.path.join(rpm_backdir, "aarch64"))
    
    build_packages(packagedir, logdir, rpm_backdir)

