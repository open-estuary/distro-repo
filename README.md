* [Introduction](#1)
* [How to use Open-Estuary repository](#2)
* [How to build packages](#3)
* [Packages Open-Estuary maintains](#4)
* [FAQ](#5)

# Open-Estuary Package Distrubtions Repository
## <a name="1">Introduction</a>
Distro-repo is to maintain everythings which are required to setup and use Open-Estuary RPM/Deb repository.  

## <a name="2">How to use Open-Estuary repository</a>
The open-estuary repository is supported on ARM64 platforms as follows:

|Distribution OS|Estuary Releases|Packages Type|
|--|--|--|
|CentOS(7.3)|3.1|RPM|
|CentOS(7.3)|5.0|RPM|
|Ubuntu(18.0)|5.0|Deb|
|Debian(8.0)|5.0|Deb|
||||

On the other hand, it is necessary to setup the repository firstly:

- CentOS:  
  - Setup
    ```
    sudo wget -O /etc/yum.repos.d/estuary.repo https://raw.githubusercontent.com/open-estuary/distro-repo/master/estuaryhttp.repo    
    sudo chmod +r /etc/yum.repos.d/estuary.repo
    sudo rpm --import http://repo.estuarydev.org/releases/ESTUARY-GPG-KEY
    yum clean dbcache
    ```
    
   - Use `yum install <package-name>` to install packages.   
   - Especially chinese users could use ftp server to improve speed as follows:    
     ```               
     sudo wget -O /etc/yum.repos.d/estuary.repo https://raw.githubusercontent.com/open-estuary/distro-repo/master/estuaryftp.repo     
     sudo chmod +r /etc/yum.repos.d/estuary.repo               
     sudo rpm --import ftp://repoftp:repopushez7411@117.78.41.188/releases/ESTUARY-GPG-KEY               
     yum clean dbcache
- Ubuntu: 
  - Setup
     ```
     ```
  - Use `apt-get install <package-name>` to install packages
       
- Debian:      
  - Setup       
     ```       
     ```     
  - Use `apt-get install <package-name>` to install packages

## <a name="3">How to build packages</a>  
It is strongly suggested to build on Estuary buildserver.  

#### RPM  
All packages for building rpm is in *distro-repo/rpm/*, as gcc, libtool, mysql and so on. And there is rpm_build.sh script in these packages directory commonly.  

1. Just run `sh rpm/xxxx(package_name)/rpm_build.sh` when you are in distro-repo directory, the corresponding rpm will be building in build-worker.

* Maybe you want to build all packages, Just run `sh util/rpm_buildall.sh`.Then all packages in rpm directory will be building.  

2. run `sh util/rpm_upload.sh` to upload all rpms which have been builded to repository.   

3. then you can install your own-building packages with `yum install xxxx(package-name)`.  

#### DEB
All packages for building deb is in *distro-repo/deb/*, as gcc, libtool, mysql and so on. And there is deb_build.sh script in these packages directory commonly.  

1. Just run `sh deb/xxxx(package_name)/deb_build.sh` when you are in distro-repo directory, the corresponding deb will be building in build-worker.

* Maybe you want to build all packages, Just run `sh util/deb_buildall.sh`.Then all packages in deb directory will be building.  

2. run "sh util/deb_upload.sh" to upload all debs which have been builded to repository.   

3. then you can install your own-building packages with `apt-get install xxxx(package-name)`.  

#### RPM&DEB
We also provider a method to build all rpms&debs.

1. run `sh util/rpmdeb_buildall.sh`(in distro-repo directory).   

2. run `sh util/rpmdeb_uploadall` to upload rpms&debs to repository 

3. run `yum install xxxx(package-name)` or `apt-get install xxxx(package-name)` to install packages.  

## <a name="4">Packages Open-Estuary maintains</a>  
Rpm&Deb packages which Open-Estuary support is listed in [packages_list.md](https://github.com/open-estuary/distro-repo/blob/master/packages_list.md).  

## <a name="5">FAQ</a>
* How to use specific glibc ?

  Currently you could use `yum install devlibset-4-glibc` to install glibc-2.25. Especially this new glibc will be installed into `/opt/rh/devlibset-4/root/user/` directory, and wouldn't affect system's glibc. 
  
* How to use new gcc ?
  
  Currently partial [software collections tools](https://www.softwarecollections.org/en/) have been ported to ARM64 platforms. Therefore, you could use `yum install devtoolset-4-gcc` or `yum install devtoolset-6-gcc` to install newer gcc. 
  As for how to use these tools, please refer to https://www.softwarecollections.org/en.

* How to integrate new packages with specific libs? 

  Currently the AliSQL has used glibc-2.25(that is devlibset-4-glibc) automatically. If you have any requests to use new packages with specific libs, just submit issue to Estuary via bugtrack system or leave message in this page.



