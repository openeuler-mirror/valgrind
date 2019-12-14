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
Version:        3.13.0
Release:        29
Epoch:          1
Summary:        An instrumentation framework for building dynamic analysis tools
License:        GPLv2+
URL:            http://www.valgrind.org/
Source0:        ftp://sourceware.org/pub/%{name}/%{name}-%{version}.tar.bz2

Patch1:         valgrind-3.9.0-cachegrind-improvements.patch
Patch2:         valgrind-3.9.0-helgrind-race-supp.patch
Patch3:         valgrind-3.9.0-ldso-supp.patch
Patch4:         valgrind-3.13.0-ppc64-check-no-vsx.patch
Patch5:         valgrind-3.13.0-epoll_pwait.patch
Patch6:         valgrind-3.13.0-ppc64-diag.patch
Patch7:         valgrind-3.13.0-arm64-hwcap.patch
Patch8:         valgrind-3.13.0-arm-index-hardwire.patch
Patch9:         valgrind-3.13.0-ucontext_t.patch
Patch10:        valgrind-3.13.0-gdb-8-testfix.patch
Patch11:        valgrind-3.13.0-disable-vgdb-child.patch
Patch12:        valgrind-3.13.0-xml-socket.patch
Patch13:        valgrind-3.13.0-ppc64-vex-fixes.patch
Patch14:        valgrind-3.13.0-amd64-eflags-tests.patch
Patch15:        valgrind-3.13.0-suppress-dl-trampoline-sse-avx.patch
Patch16:        valgrind-3.13.0-static-tls.patch
Patch17:        valgrind-3.13.0-ppc64-timebase.patch
Patch18:        valgrind-3.13.0-debug-alt-file.patch
Patch19:        valgrind-3.13.0-s390-cgijnl.patch
Patch20:        valgrind-3.13.0-ppc64-mtfprwa-constraint.patch
Patch21:        valgrind-3.13.0-build-id-phdrs.patch
Patch22:        valgrind-3.13.0-arm64-ptrace.patch
Patch23:        valgrind-3.13.0-ld-separate-code.patch
Patch24:        valgrind-3.13.0-arch_prctl.patch
Patch25:        valgrind-3.13.0-x86-arch_prctl.patch
Patch26:        valgrind-3.13.0-ppc64-xsmaxcdp.patch
Patch27:        valgrind-3.13.0-utime.patch

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

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%files help
%doc NEWS README_*
%{_mandir}/man1/*

%changelog
* Sat Dec 7 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.13.0-29
- Package init
