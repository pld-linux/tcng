%include        /usr/lib/rpm/macros.perl
Summary:	Traffic Control - Next Generation
Summary(pl):	Kontrola Ruchu - Nastêpna Generacja
Name:		tcng
Version:	9m
Release:	1
License:	GPL/LGPL
Group:		Networking/Admin
Source0:	http://tcng.sourceforge.net/dist/%{name}-%{version}.tar.gz
# Source0-md5:	636d382f6db917b385e7a6f158136ca2
Source1:	ftp://ftp.inr.ac.ru/ip-routing/iproute2-2.4.7-now-ss020116.tar.gz
# Source1-md5:	2c7e5f3a10e703745ecdc613f7a7d187
Source2:	http://luxik.cdi.cz/~devik/qos/htb/v3/htb3.6-020525.tgz
# Source2-md5:	3064fd8642ce6a7e155a29c5205b99d4
Source3:	ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-2.4.26.tar.bz2
# Source3-md5:	88d7aefa03c92739cb70298a0b486e2c
BuildRequires:	flex
BuildRequires:	perl
BuildRequires:	psutils
BuildRequires:	rpm-perlprov
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex
BuildRequires:	yacc
Obsoletes:	tcng-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tcng is a redesign of the Linux traffic control architecture. In the
first phase, the configuration language will be improved. In the
second phase, kernel components will be generated directly by
configuration utilities. Throughout all this, full compatibility with
the existing traffic control infrastructure will be maintained.

%description -l pl
tcng jest od nowa zaprojektowan± architektur± kontroli ruchu dla
Linuxa. W pierwszej fazie jêzyk konfiguracji bêdzie usprawniony. W
drugiej fazie komponenty j±dra bêd± generowane bezpo¶rednio poprzez
narzêdzia konfiguruj±ce. Wszystko to pod ka¿dym wzglêdem jest w pe³ni
kompatybilne z istniej±c± infrastruktur± kontroli ruchu.

%package -n tcsim
Summary:	Linux Traffic Control simulator
Summary(pl):	Symulator Kontroli Ruchu w Linuxie
Group:		Applications/Emulators
Obsoletes:	tcsim-devel

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

%prep
%setup -q -n %{name} -a1 -a2 -a3
cd tcsim
ln -s ../linux-*.*.* linux
ln -s ../iproute2 iproute2
patch -s -p1 -d iproute2 < ../htb3.6_tc.diff

%build
echo '
KSRC="tcsim/linux"
ISRC="tcsim/iproute2"
TCSIM="true"
%ifarch %{ix86} alpha amd64
BYTEORDER="LITTLE_ENDIAN"
%else
BYTEORDER="BIG_ENDIAN"
%endif
' > config

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO doc/tcng.txt doc/tcng.ps examples examples-ng
%attr(755,root,root) %{_bindir}/tcc
%attr(755,root,root) %{_bindir}/tcc.bin
%attr(755,root,root) %{_bindir}/*.pl
%dir %{_libdir}/tcng
%dir %{_libdir}/tcng/bin
%attr(755,root,root) %{_libdir}/tcng/bin/tcc-*
%dir %{_libdir}/tcng/lib
%{_libdir}/tcng/lib/*.c
%{_libdir}/tcng/lib/*.a
%dir %{_libdir}/tcng/include
%{_libdir}/tcng/include/*.tc
%{_libdir}/tcng/include/*.h


%files -n tcsim
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tcsim*
%attr(755,root,root) %{_libdir}/tcng/bin/*_cc
%{_libdir}/tcng/include/*.def
%{_libdir}/tcng/include/*.tcsim
%{_libdir}/tcng/include/klib
%{_libdir}/tcng/include/ulib
