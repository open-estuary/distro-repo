Summary: Integer point manipulation library
Name: isl
Version: 0.16.1
License: MIT
Group: System Environment/Libraries
URL: http://isl.gforge.inria.fr/

%global libmajor 15
%global libversion %{libmajor}.1.1

%global oldversion 0.14
%global oldlibmajor 13
%global oldlibversion %{oldlibmajor}.1.0

# Please set buildid below when building a private version of this rpm to
# differentiate it from the stock rpm.
#
# % global buildid .local

Release: 1%{?buildid}%{?dist}

BuildRequires: gmp-devel
BuildRequires: pkgconfig
Provides: isl = %{oldversion}

Source0: http://isl.gforge.inria.fr/isl-%{version}.tar.xz

# Current gcc requires exactly 0.14
Source1: http://isl.gforge.inria.fr/isl-%{oldversion}.tar.xz

%description
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%package devel
Summary: Development for building integer point manipulation library
Requires: isl%{?_isa} == %{version}-%{release}
Requires: gmp-devel%{?_isa}
Group: Development/Libraries

%description devel
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints.  Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, computing the lexicographic
minimum using parametric integer programming, coalescing and parametric
vertex enumeration.  It also includes an ILP solver based on generalized
basis reduction, transitive closures on maps (which may encode infinite
graphs), dependence analysis and bounds on piecewise step-polynomials.

%prep
%global docdir isl-%{version}
%setup -q -n isl -c
%setup -b 1 -q -n isl -c

%build
cd isl-%{oldversion}
%configure
make %{?_smp_mflags} V=1
cd ..

cd isl-%{version}
%configure
make %{?_smp_mflags} V=1

%install
cd isl-%{oldversion}
%make_install INSTALL="install -p" install-libLTLIBRARIES
cd ..

cd isl-%{version}
%make_install INSTALL="install -p"
rm -f %{buildroot}/%{_libdir}/libisl.a
rm -f %{buildroot}/%{_libdir}/libisl.la
mkdir -p %{buildroot}/%{_datadir}
%global gdbprettydir %{_datadir}/gdb/auto-load/%{_libdir}
mkdir -p %{buildroot}/%{gdbprettydir}
mv %{buildroot}/%{_libdir}/*-gdb.py* %{buildroot}/%{gdbprettydir}

%check
cd isl-%{oldversion}
#make check
cd ..

cd isl-%{version}
#make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libisl.so.%{libmajor}
%{_libdir}/libisl.so.%{libversion}
%{_libdir}/libisl.so.%{oldlibmajor}
%{_libdir}/libisl.so.%{oldlibversion}
%{gdbprettydir}/*
%license %{docdir}/LICENSE
%doc %{docdir}/AUTHORS %{docdir}/ChangeLog %{docdir}/README

%files devel
%{_includedir}/*
%{_libdir}/libisl.so
%{_libdir}/pkgconfig/isl.pc
%doc %{docdir}/doc/manual.pdf


%changelog
* Sat Apr 22 2017 Huang Jinhua <sjtuhjh@hotmail.com> - 0.16.1-1
- Initial packaging.
