* [Introduction](#1)
* [How to use Open-Estuary repository](#2)
* [How to build packages](#3)
* [Packages Open-Estuary maintains](#4)

# Open-Estuary Package Distrubtions Repository
## <a name="1">Introduction</a>
Distro-repo is to maintain everythings which are required to setup and use RPM/Deb repository.  

## <a name="2">How to use Open-Estuary repository</a>
Make sure which distrobution you are using, ***CentOS*** or ***Ubuntu/Debian***.

#### CentOS  
1. Defaultly, estuary.repo is in */etc/yum.repos.d/* directory. Please to make sure.  
If not, just download estuary.repo from *distro-repo/util/estuary.repo*, then move it to */etc/yum.repos.d/*.  
Also, you can make a new estuary.repo in */etc/yum.repos.d/* as *distro-repo/util/estuary.repo*.  

2. run `yum clean all`.

3. run `yum repolist`.
You will find estuary-repo in standard output, if all is done.  

Now you can use `yum install xxxxx` to install packages Open-Estuary supports.  

#### Ubuntu/Debian
1. Defaultly, estuary repository is listed in */etc/apt/source.list*. Please to make sure.  
If not, just download source.list from *distro-repo/util/source.list*, then move it to */etc/apt/*.  
Also, you can make a new source.list in */etc/apt/* as *distro-repo/util/source.list*.  

2. run `apt-get update`.  
    
Now you can use `apt-get install xxxxx` to install packages Open-Estuary supports. 

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
Rpm packages which Open-Estuary support is listed in [RPM.md](https://github.com/open-estuary/distro-repo/blob/master/RPM.md).  

Deb packages which Open-Estuary support is listed in [DEB.md](https://github.com/open-estuary/distro-repo/blob/master/DEB.md).







