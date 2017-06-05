#!/usr/bin/env python

import os
import sys
import subprocess
import re
import threading

MAX_THREAD_NUM = 16
global_lock = threading.Lock()
global_packages_list = []

RPM_AARCH64_DIR=os.path.join(os.environ['HOME'], "rpmbuild/RPMS/aarch64/")
RPM_NOARCH_DIR=os.path.join(os.environ['HOME'], "rpmbuild/RPMS/noarch/")

def save_rpm_build_result(packagename, logdir):
   is_successful = False 
   for filename in os.listdir(RPM_AARCH64_DIR):
       if filename.endswith('.aarch64.rpm') and filename.startswith(packagename):
           is_successful = True
           break

   if not is_successful:
       for filename in os.listdir(RPM_NOARCH_DIR):
           if filename.endswith('.noarch.rpm') and filename.startswith(packagename):
               is_successful = True
               break

   if is_successful :
       logfile = "successful_list"
   else : 
       logfile = "failure_list"
   
   global_lock.acquire()
   filehandle = open(os.path.join(logdir, logfile), 'a')
   filehandle.write(packagename + '\n')
   global_lock.release()   


def build_sub_package(buildfile, logdir, succ_dict):
    buildfile = os.path.abspath(buildfile)
    basename = os.path.basename(buildfile)
    dirname = os.path.dirname(buildfile)
    packagename = dirname.split('/')[-1]
    logfile = os.path.join(logdir, packagename)
    
    if not os.path.exists(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))
    
    if succ_dict.has_key(packagename):
        print("%s has been built successfully before"%packagename)
        return 0

    log_stderr = open(logfile+"_stderr", "w")
    try :

        log_stdout = open(logfile+"_stdout", 'w')
        proc = subprocess.check_call([buildfile], stdout=log_stdout, stderr=log_stderr, shell=True)

    except Exception as e:
        print("Catch exception:%s\n"%e)

    save_rpm_build_result(packagename, logdir)
    return 0

def get_all_build_files(dirname):
    file_list = []
    for filename in os.listdir(dirname):
        if re.search('fedora-rawhide', filename):
            print("Ignore fedor-rawhide directory")
            continue
        if re.search("obsolete", filename):
            print("Ignore not used scripts")
            continue
       
        fullname = os.path.join(dirname, filename)
        if os.path.isfile(fullname) and filename == 'rpm_build.sh':
            file_list.append(fullname)
        elif os.path.isdir(fullname):
            file_list.extend(get_all_build_files(fullname))
    return file_list

def build_packages_thread(packages_list, logdir, succ_dict):
    while True:
        is_empty = False
        package_name = ""
        global_lock.acquire()
        if len(packages_list) <= 0 :
            print("Finish all packages")
            is_empty = True
        else :
            package_name = packages_list.pop()
        global_lock.release()
    
        if is_empty:
            break

        try :
            print("Process %s"%package_name)
            build_sub_package(package_name, logdir, succ_dict)
        except Exception as e:
            print("Package:%s catch exception:%s"%(package_name, e))
            continue

    print("Current thread has finished")
    return
          
def build_packages(package_dir, logdir):
    global_packages_list = get_all_build_files(package_dir)
    all_packages_file = open(os.path.join(logdir, "all_packages_list"), 'w')
    for package in global_packages_list:
        packagename = package.split('/')[-2]
        all_packages_file.write("%s\t%s\n"%(packagename, ""))
    all_packages_file.close()

    global_packages_list.reverse()

    print("Total packages=%d"%len(global_packages_list))
    succ_dict = {} 
    previous_success_log = os.path.join(logdir, "successful_list")
    if os.path.exists(previous_success_log):
        for line in open(previous_success_log):
            succ_dict[line.strip()] = 0

    previous_failure_log = os.path.join(logdir, "failure_list") 
    if os.path.exists(previous_failure_log):
        os.system("rm " + previous_failure_log)
  
    thread_list = []
    for index in range(0, MAX_THREAD_NUM):
        thread = threading.Thread(target = build_packages_thread, args = (global_packages_list, logdir, succ_dict, ))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()
      
if __name__ == "__main__":
    packagedir = "./"
    logdir = "/tmp/rpmbuildlog"

    if len(sys.argv) >= 3:
        logdir = sys.argv[2]

    if len(sys.argv) >= 2:
        packagedir = sys.argv[1]

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    build_packages(packagedir, logdir)

    print("Please check rpm build logs under:%s"%logdir)
    print("Please check rpm packages under:~/rpmbuild/ or /root/rpmbuild")
