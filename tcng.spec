%include        /usr/lib/rpm/macros.perl
Summary:	Traffic Control - Next Generation
Summary(pl):	Kontrola Ruchu - Nastêpna Generacja
Name:		tcng
Version:	8u
Release:	1
License:	GPL/LGPL
Group:		Networking/Admin
Source0:	http://tcng.sourceforge.net/dist/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.inr.ac.ru/ip-routing/iproute2-2.4.7-now-ss010803.tar.gz
URL:		http://tcng.sourceforge.net/
BuildRequires:	flex
%{!?_without_dist_kernel:BuildRequires:	kernel-source >= 2.4.0}
BuildRequires:	perl
BuildRequires:	psutils
BuildRequires:	rpm-perlprov
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	yacc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tcng is a redesign of the Linux traffic control architecture. In the
first phase, the configuration language will be improved. In the
second phase, kernel components will be generated directly by
configuration utilities. Throughout all this, full compatibility with
the existing traffic control infrastructure will be maintained.

%description -l pl
tcng jest od nowa zaprojektowan± architektór± kontroli ruchu dla
Linuxa. W pierwszej fazie jêzyk konfiguracji bêdzie usprawniony. W
drugiej fazie komponenty j±dra bêd± generowane bezpo¶rednio poprzez
narzêdzia konfiguruj±ce. Wszystko to pod ka¿dym wzglêdem jest w pe³ni
kompatybilne z istniej±c± infrastruktur± kontroli ruchu.

%package devel
Summary:	C library for processing tcc external output
Summary(pl):	Biblioteka C do parsowania plików wygenerowanych przez tcc
Group:		Development/Libraries

%description devel
The library "libtccext", which offers a convenient C interface to the
data provided by tcc at its "external" interface. The library is
accompanied by header files for itself, and for the debugging
functions echoh, which are also included in libtccext.

%description devel -l pl
Biblioteka ,,libtccext'' oferuje interfejs C do danych dostarczanych
przez tcc jako jego ,,zewnêtrzny'' interfejs.

%package -n tcsim
Summary:	Linux Traffic Control simulator
Summary(pl):	Symulator Kontroli Ruchu w Linuxie
Group:		Applications/Emulators

%description -n tcsim
tcsim combines the original traffic control code from the Linux kernel
with the user-space code of the configuration utility tc, and adds the
framework for communication among the two, plus an event-driven
simulation engine.

The resulting program runs entirely in user space, but executes almost
exactly the same code as a "real" system.

%description -n tcsim -l pl
tcsim ³±czy w sobie oryginalny kod kontroli ruchu z j±dra Linuxa wraz
z kodem z przestrzeni u¿ytkownika, a mianowicie narzêdziem tc oraz
dodatkowo dodaje czê¶æ umo¿liwiaj±c± komunikacjê miêdzy nimi plus
silnik symulacji.

%package -n tcsim-devel
Summary:	Cross-compilers and header files for building tcsim modules
Summary(pl):	Cross-kompilatory i nag³ówki do budowania modu³ów tcsim
Group:		Development/Tools

%description -n tcsim-devel
The "cross-compilers" kmod_cc and tcmod_cc compile kernel and tc
modules such that they can be used with tcsim.

This package also includes all header files necessary for generating
the tcsim environment.

%description -n tcsim-devel -l pl
,,Cross-kompilatory'' kmod_cc oraz tcmod_cc kompiluj± modu³y kernela
oraz modu³y tc w taki sposób, ¿e mog± byæ one u¿ywane wraz z tcsim.

%prep
%setup -q -n %{name} -a1

%build
echo '
KSRC="%{_kernelsrcdir}"
ISRC="tcsim/iproute2"
TCSIM="true"
%ifarch %{ix86} alpha
BYTEORDER="LITTLE_ENDIAN"
%else
BYTEORDER="BIG_ENDIAN"
%endif
' > config

ln -s %{_kernelsrcdir} tcsim/linux
ln -s ../iproute2 tcsim/iproute2

install -d $RPM_BUILD_ROOT%{_prefix}

./configure \
	--install-directory $RPM_BUILD_ROOT%{_prefix}

%{__make} \
	RPM_OPT_FLAGS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_prefix},%{_libdir},%{_includedir}/tcng}

TCNG_INSTALL_CWD=%{_prefix} %{__make} install

cp -f $RPM_BUILD_ROOT%{_libdir}/tcng/lib/*.a $RPM_BUILD_ROOT%{_libdir}
cp -f $RPM_BUILD_ROOT%{_libdir}/tcng/include/*.h $RPM_BUILD_ROOT%{_includedir}/tcng

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO doc/tcng.txt doc/tcng.ps examples examples-ng
%attr(755,root,root) %{_bindir}/tcc
%attr(755,root,root) %{_bindir}/tcc.bin
%dir %{_libdir}/tcng
%dir %{_libdir}/tcng/bin
%{_libdir}/tcng/bin/tcc-*
%dir %{_libdir}/tcng/lib
%{_libdir}/tcng/lib/*.c
%dir %{_libdir}/tcng/include
%{_libdir}/tcng/include/*.tc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*.pl
%{_libdir}/*.a
%{_includedir}/tcng

%files -n tcsim
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tcsim*
%{_libdir}/tcng/include/*.def

%files -n tcsim-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/tcng/bin/*_cc
%dir %{_libdir}/tcng/include/klib
%{_libdir}/tcng/include/klib/include
%dir %{_libdir}/tcng/include/klib/kernel
%{_libdir}/tcng/include/klib/kernel/include
%dir %{_libdir}/tcng/include/ulib
%dir %{_libdir}/tcng/include/ulib/iproute2
%{_libdir}/tcng/include/ulib/iproute2/include
%{_libdir}/tcng/include/ulib/iproute2/include-glibc
%dir %{_libdir}/tcng/include/ulib/iproute2/tc
%{_libdir}/tcng/include/ulib/iproute2/tc/*.h
