* [Introduction](#1)
* [Open-Estuary Repository](#2)
* [Packages List](#3)
* [Packages Building](#4)
* [FAQ](#5)

# Open-Estuary Package Distrubtions Repository
## <a name="1">Introduction</a>
Distro-repo is to maintain everythings which are required to setup and use Open-Estuary RPM/Deb repository.  

## <a name="2">Open-Estuary Repository</a>
The open-estuary repository is supported on ARM64 platforms as follows:

|Distribution OS|Estuary Releases|Packages Type|
|--|--|--|
|CentOS(7.3)|3.1|RPM|
|CentOS(7.3)|5.0|RPM|
|Ubuntu(18.0)|5.0|Deb|
|Debian(8.0)|5.0|Deb|
||||

On the other hand, it is necessary to setup the repository firstly:
> By default, we should use http repository(such as estuaryhttp.repo or estuaryhttp_xxx.list).
> However Chinese users could use ftp repository in order to enjoy better access speed.

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
     ```
- Ubuntu: 
  - Setup
     ```
     sudo wget -O - http://repo.estuarydev.org/releases/ESTUARY-GPG-KEY | apt-key add -
     sudo wget -O /etc/apt/sources.list.d/estuary.list https://raw.githubusercontent.com/open-estuary/distro-repo/master/estuaryhttp_ubuntu.list
     sudo apt-get update
     ```
  - Use `apt-get install <package-name>` to install packages
       
- Debian:      
  - Setup       
     ```    
     sudo wget -O - http://repo.estuarydev.org/releases/ESTUARY-GPG-KEY | apt-key add -     
     sudo wget -O /etc/apt/sources.list.d/estuary.list https://raw.githubusercontent.com/open-estuary/distro-repo/master/estuaryhttp_debian.list
     sudo apt-get update
     ```
  - Use `apt-get install <package-name>` to install packages

## <a name="4">Packages List</a>  
As for the list of packages which are integrated into Estuary, please refer to [Estuary New Packages Lists](https://github.com/open-estuary/distro-repo/blob/master/packages_list.md).  

## <a name="3">Packages Building</a>  

It is strongly suggested to build on Estuary buildboard or buildserver.  

- RPM:  
All packages for building rpm is in *distro-repo/rpm/*.   
  - Build
    ```
    git clone https://github.com/open-estuary/distro-repo.git
    sh distro-repo/rpm/xxxx(package_name)/rpm_build.sh
    ```
  - Upload
    ```
    sh distro-repo/utils/pkg_upload rpmbuild centos
    ```
    > "rpmbuild" refer to the directory which has rpms.
  - Create repo
    ```
    sh createrepo.sh centos
    ```

- DEB:
All packages for building deb is in *distro-repo/deb/*.
  - Build
    ```
    git clone https://github.com/open-estuary/distro-repo.git
    sh distro-repo/deb/xxxx(package_name)/deb_build.sh debian(or ubuntu)
    ```
  - Upload
    ```
    sh distro-repo/utils/pkg_upload debbuild debian(or ubuntu)
    ```
    > "debbuild" refer to the directory which has debs.
  - Create repo
    ```
    sh createrepo.sh debian(or ubuntu)
    ```

## <a name="5">FAQ</a>
* How to use specific glibc ?

  Currently you could use `yum install devlibset-4-glibc` to install glibc-2.25. Especially this new glibc will be installed into `/opt/rh/devlibset-4/root/user/` directory, and wouldn't affect system's glibc. 
  
* How to use new gcc ?
  
  Currently partial [software collections tools](https://www.softwarecollections.org/en/) have been ported to ARM64 platforms. Therefore, you could use `yum install devtoolset-4-gcc` or `yum install devtoolset-6-gcc` to install newer gcc. 
  As for how to use these tools, please refer to https://www.softwarecollections.org/en.

* How to integrate new packages with specific libs? 

  Currently the AliSQL has used glibc-2.25(that is devlibset-4-glibc) automatically. If you have any requests to use new packages with specific libs, just submit issue to Estuary via bugtrack system or submit one issue in this repository.

* How to use other versions Estuary packages?
 
  By default, the estuaryftp.repo or estuaryhttp.repo contain the latest version. If you want to use specific version, just replace the version number in baseurl with specific version. For example, replace `5.0` with `3.0` in baseurl in order to use Estuary 3.0 packages. Then the baseurl looks like `baseurl=http://repo.estuarydev.org/releases/3.0/centos/`.
  
