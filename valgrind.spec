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
%ifarch riscv64
%define arch_val riscv64
%define arch_old_val %{nil}
%endif

Name:           valgrind
%ifarch riscv64
Version:        3.18.1
Release:	4
Epoch:		2
%else
Version:        3.16.0
Release:        1
Epoch:          1
%endif
Summary:        An instrumentation framework for building dynamic analysis tools
License:        GPLv2+
URL:            http://www.valgrind.org/
%ifarch riscv64
# A RISC-V fork, recompressed from https://github.com/petrpavlu/valgrind-riscv64/tree/e595f722440c59f13b2d3f48e499a54a0c7eb09f
Source0:        valgrind-riscv64.tar.gz
%else
Source0:        ftp://sourceware.org/pub/%{name}/%{name}-%{version}.tar.bz2
%endif

Patch1:         valgrind-3.9.0-cachegrind-improvements.patch
%ifnarch riscv64
Patch2:         valgrind-3.9.0-helgrind-race-supp.patch
%endif
Patch3:         valgrind-3.9.0-ldso-supp.patch

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
%ifarch riscv64
%autosetup -n %{name}-riscv64-riscv64-linux -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

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
%ifarch riscv64
./autogen.sh
%endif
%configure CC="$CC" CFLAGS="$OPTFLAGS" CXXFLAGS="$OPTFLAGS" --with-mpicc=/bin/false GDB=%{_bindir}/gdb
%make_build

%install
%ifarch riscv64
make DESTDIR=%{buildroot} install %{?_smp_mflags}
%else
%make_install
%endif

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

%ifarch riscv64
pushd %{buildroot}%{_libexecdir}/%{name}
mv ./* %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/%{name}/dh_view* ./
popd
%endif

%files
%license COPYING AUTHORS
%ifnarch riscv64
%doc %{_datadir}/doc/%{name}/{html,*.pdf}
%exclude %{_datadir}/doc/%{name}/*.ps
%endif
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*[^ao]
%attr(0755,root,root) %{_libdir}/valgrind/vgpreload*-%{arch_val}-*so
%if "%{arch_old_val}" != ""
%{_libdir}/%{name}/vgpreload*-%{arch_old_val}-*so
%endif
%{_libexecdir}/%{name}/*

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%files help
%doc NEWS README_*
%ifnarch riscv64
%{_mandir}/man1/*
%endif

%changelog
* Tue Jul 26 2022 YukariChiba <i@0x7f.cc> - 3.18.1-4
- Upgrade RISC-V version.

* Mon Jul 04 2022 laokz <laokz@foxmail.com> - 3.18.1-3
- Fix RISC-V special instruction preambles.

* Sat Jun 11 2022 YukariChiba <i@0x7f.cc> - 3.18.1-2
- Upgrade RISC-V version.
- Move RISC-V files to correct path.

* Thu Feb 17 2022 YukariChiba <i@0x7f.cc> - 3.16.0-2
- Add a supported version for RISC-V.
- The supported version is from https://github.com/petrpavlu/valgrind-riscv64 with commit `1b6359bf61d38eeb1a4651527e654d40d15c4dc7`

* Mon Aug 02 2021 shixuantong <shixuantong@huawei.com> - 3.16.0-1
- upgrade version to 3.16.0

* Wed Feb 3 2021 wangjie<wangjie294@huawei.com> - 3.15.0-1
- upgrade 3.15.0

* Sat Dec 7 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.13.0-29
- Package init
