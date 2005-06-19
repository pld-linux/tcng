%include	/usr/lib/rpm/macros.perl
Summary:	Traffic Control - Next Generation
Summary(pl):	Kontrola Ruchu - Nastêpna Generacja
Name:		tcng
Version:	10b
Release:	1
License:	GPL/LGPL
Group:		Networking/Admin
Source0:	http://tcng.sourceforge.net/dist/%{name}-%{version}.tar.gz
# Source0-md5:	d28bc6b1ed8973814213942288ab5d18
Source1:	http://developer.osdl.org/dev/iproute2/download/iproute2-2.4.7-now-ss020116-try.tar.bz2
# Source1-md5:	a669dd60bfb568fa69309c86ec1031f6
Source2:	http://luxik.cdi.cz/~devik/qos/htb/v3/htb3.6-020525.tgz
# Source2-md5:	3064fd8642ce6a7e155a29c5205b99d4
Source3:	ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-2.4.27.tar.bz2
# Source3-md5:	59a2e6fde1d110e2ffa20351ac8b4d9e
URL:		http://tcng.sourceforge.net/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	perl-base
BuildRequires:	psutils
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	transfig
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
Linuksa. W pierwszej fazie jêzyk konfiguracji bêdzie usprawniony. W
drugiej fazie komponenty j±dra bêd± generowane bezpo¶rednio poprzez
narzêdzia konfiguruj±ce. Wszystko to pod ka¿dym wzglêdem jest w pe³ni
kompatybilne z istniej±c± infrastruktur± kontroli ruchu.

%package -n tcsim
Summary:	Linux Traffic Control simulator
Summary(pl):	Symulator Kontroli Ruchu w Linuksie
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
tcsim ³±czy w sobie oryginalny kod kontroli ruchu z j±dra Linuksa wraz
z kodem z przestrzeni u¿ytkownika, a mianowicie narzêdziem tc oraz
dodatkowo dodaje czê¶æ umo¿liwiaj±c± komunikacjê miêdzy nimi plus
silnik symulacji.

%prep
%setup -q -n %{name} -a1 -a2 -a3
cd tcsim
ln -s ../linux-*.*.* linux
ln -s ../iproute2 iproute2
patch -s -p1 -d iproute2 < ../htb3.6_tc.diff
sed -i -e 's#type -path#whence#g' ../configure

%build
echo '
KSRC="tcsim/linux"
ISRC="tcsim/iproute2"
TCSIM="true"
BUILD_MANUAL="true"
%ifarch %{ix86} %{x8664} alpha ia64
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
%attr(755,root,root) %{_bindir}/tcng
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
