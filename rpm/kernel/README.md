You can use the following steps to compile the kernel related packages.

### 1. prepare the kernel source code 
  The name of the source code shoule be like ```kernel-rpmversion-pkgrelease.tar.gz```

  > For example:
     ```kernel-4.9.20-3.1.rc1.tar.gz```

  The ```rpmversion``` means the kernel version and the ```pkgrelease``` means the Estuary release version.

  You can  git clone the source code from ```https://github.com/open-estuary/kernel.git```, then use the release tag. 
  
  > Remember move the ```kernel``` directory to ```kernel-rpmversion-pkgrelease```, and the make the tarball.

### 2. Prepare files for the rpmbuild
  Put the kernel source code and the files in ```distro-repo/rpm/kernel/src``` into the ```rpmbuild/BUILD``` directory.

  Put ```distro-repo/rpm/kernel/src/kernel-aarch64.spec``` file to the ```rpmbuild/SPEC``` directory

  > Remember to modify the ```rpmversion``` and ```pkgrelease``` value accroding to your version.

### 3. Compiling 
  Use the ```rpmbuild -bb rpmbuild/SPEC/kernel-aarch64.spec``` to build the kernel-related packages.

### 4. Packages
  After building, there are 16 packages generated at ```rpmbuild/RPMS``` direstory.


