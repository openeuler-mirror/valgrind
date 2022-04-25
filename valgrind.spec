%ifarch %{ix86}
%define arch_val x86
%define arch_old_val %{nil}
%endif
%ifarch x86_64
%define arch_val amd64
%define arch_old_val x86
%endif
%ifarch aarch64
%define arch_val arm64
%define arch_old_val %{nil}
%endif

Name:           valgrind
Version:        3.16.0
Release:        2
Epoch:          1
Summary:        An instrumentation framework for building dynamic analysis tools
License:        GPLv2+
URL:            http://www.valgrind.org/
Source0:        ftp://sourceware.org/pub/%{name}/%{name}-%{version}.tar.bz2

Patch1:         valgrind-3.9.0-cachegrind-improvements.patch
Patch2:         valgrind-3.9.0-helgrind-race-supp.patch
Patch3:         valgrind-3.9.0-ldso-supp.patch
Patch4:         backport-Generate-a-ENOSYS-sys_ni_syscall-for-clone3-on-all-linux-arches.patch

BuildRequires:  glibc glibc-devel gdb procps gcc-c++ perl(Getopt::Long)

%description
Valgrind is an instrumentation framework for building dynamic analysis tools. There are
Valgrind tools that can automatically detect many memory management and threading bugs,
and profile your programs in detail. You can also use Valgrind to build new tools.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
This files contains the development files for %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
CC=gcc
%ifarch x86_64
mkdir -p shared/libgcc/32
ar r shared/libgcc/32/libgcc_s.a
ar r shared/libgcc/libgcc_s_32.a
CC="gcc -B `pwd`/shared/libgcc/"
%endif

%undefine _hardened_build
%undefine _strict_symbol_defs_build
OPTFLAGS="`echo " %{optflags} " | sed 's/ -m\(64\|3[21]\) / /g;s/ -fexceptions / /g;s/ -fstack-protector\([-a-z]*\) / / g;s/ -Wp,-D_FORTIFY_SOURCE=2 / /g;s/ -O2 / /g;s/ -mcpu=\([a-z0-9]\+\) / /g;s/^ //;s/ $//'`"
%configure CC="$CC" CFLAGS="$OPTFLAGS" CXXFLAGS="$OPTFLAGS" --with-mpicc=/bin/false GDB=%{_bindir}/gdb
%make_build

%install
%make_install

pushd %{buildroot}%{_libdir}/valgrind/
rm -f *.supp.in *.a
%if "%{arch_old_val}" != ""
rm -f *-%{arch_old_val}-* || :
for i in *-%{arch_val}-*; do
  j=`echo $i | sed 's/-%{arch_val}-/-%{arch_old_val}-/'`
  ln -sf ../../lib/valgrind/$j $j
done
%endif
popd

pushd %{buildroot}%{_includedir}/%{name}
rm -rf config.h libvex*h pub_tool_*h vki/
popd

%files
%license COPYING AUTHORS
%doc %{_datadir}/doc/%{name}/{html,*.pdf}
%exclude %{_datadir}/doc/%{name}/*.ps
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*[^ao]
%attr(0755,root,root) %{_libdir}/valgrind/vgpreload*-%{arch_val}-*so
%if "%{arch_old_val}" != ""
%{_libdir}/%{name}/vgpreload*-%{arch_old_val}-*so
%endif
%{_libexecdir}/valgrind/*

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%files help
%doc NEWS README_*
%{_mandir}/man1/*

%changelog
* Wed Feb 09 2022 gaoxingwang <gaoxingwang@huawei.com> - 3.16.0-2
- backport patch :Generate a ENOSYS (sys_ni_syscall) for clone3 on all linux arches

* Mon Aug 02 2021 shixuantong <shixuantong@huawei.com> - 3.16.0-1
- upgrade version to 3.16.0

* Wed Feb 3 2021 wangjie<wangjie294@huawei.com> - 3.15.0-1
- upgrade 3.15.0

* Sat Dec 7 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.13.0-29
- Package init
