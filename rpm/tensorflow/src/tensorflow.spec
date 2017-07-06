Name:           tensorflow
Version:        1.2.1
Release:        2.alonid%{?dist}
Summary:        test
License:        Apache License 2.0
URL:            http://www.tensorflow.org/
Source:         nothing

BuildRequires: bazel
BuildRequires: python-devel
BuildRequires: python-six
BuildRequires: python-wheel
BuildRequires: python-pip
BuildRequires: swig
BuildRequires: git
BuildRequires: gcc-c++
BuildRequires: numpy
BuildRequires: zlib-devel
BuildRequires: pkgconfig

%description
test

%prep

[ ! -d tensorflow ] && \
    git clone --depth 1 --recursive https://github.com/tensorflow/tensorflow.git -b v1.2.1

cd tensorflow
echo -e '\nn' | ./configure

%build

export LANG=en_US.UTF-8
cd tensorflow
bazel build --verbose_failures -c opt //tensorflow/tools/pip_package:build_pip_package

%check

%install

cd tensorflow
rm -rf dist-temp
bazel-bin/tensorflow/tools/pip_package/build_pip_package `pwd`/dist-temp
ls -l dist-temp
cd dist-temp
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/tensorflow
cp -a * $RPM_BUILD_ROOT/%{_prefix}/share/tensorflow

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_prefix}/share/tensorflow

%changelog
