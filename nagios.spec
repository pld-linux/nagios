#
# Conditional build:
%bcond_with	pgsql	# enable pgsql support
%bcond_with	mysql	# enable mysql support
%bcond_without	gd	# without statusmap and trends, which require gd library
#
# TODO:
# - remove *-sample from /etc - move it to %doc or place without "-sample" suffix
Summary:	Host/service/network monitoring program
Summary(pl):	Program do monitorowania serwerów/us³ug/sieci
Summary(pt_BR):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	1.2
Release:	5
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	414d70e5269d5b8d7c21bf3ee129309f
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Source3:	http://dl.sf.net/nagios/imagepak-base.tar.gz
Patch0:		%{name}-pgsql.patch
Patch1:		%{name}-resources.patch
Patch2:		%{name}-iconv-in-libc.patch
URL:		http://www.nagios.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gd:BuildRequires:	gd-devel, libjpeg-devel, libpng-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.159
PreReq:		rc-scripts
PreReq:		sh-utils
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/groupmod
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires(post,postun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	user(nagios)
Provides:	group(nagios)
Conflicts:	iputils-ping < 1:ss020124
Obsoletes:	netsaint
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_bindir		%{_prefix}/sbin
%define		_sbindir	%{_libdir}/%{name}/cgi
%define		_datadir	%{_prefix}/share/%{name}
%define		_localstatedir	/var/lib/%{name}

%description
Nagios is a program that will monitor hosts and services on your
network. It has the ability to email or page you when a problem arises
and when a problem is resolved. Nagios is written in C and is designed
to run under Linux (and some other *NIX variants) as a background
process, intermittently running checks on various services that you
specify.

The actual service checks are performed by separate "plugin" programs
which return the status of the checks to Nagios. The plugins are
available in nagios-plugins packages.

Nagios is successor to NetSaint.

%description -l pl
Nagios to program, który monitoruje serwery oraz us³ugi w naszej
sieci. Posiada on mo¿liwo¶æ wysy³ania informacji o wyst±pieniu oraz
rozwi±zaniu problemu. Nagios zosta³ napisany w C oraz jest
zaprojektowany do pracy pod Linuksem (i niektórymi innymi uniksami)
jako proces pracuj±cy w tle i bezustannie wykonuj±cy pewne operacje
sprawdzaj±ce.

W³a¶ciwe sprawdzanie jest wykonywane przez osobne programy
("wtyczki"), które zwracaj± informacje o statusie do Nagiosa. Wtyczki
s± dostêpne na stronie w pakietach nagios-plugins.

Nagios jest nastêpc± NetSainta.

%description -l pt_BR
O Nagios é um programa que monitora máquinas e serviços na sua rede.
Ele pode enviar um email ou um aviso de pager para o administrador
quando surgir um problema e quando ele for resolvido. Nagios é escrito
em C e foi desenvolvido para rodar em plataformas Linux (e algumas
variações de *NIX) como um processo em segundo plano, periodicamente
executando checagens nos diversos serviços que forem especificados.

%package cgi
Summary:	CGI webinterface for Nagios
Summary(pl):	Interfejs WWW/CGI dla Nagiosa
Group:		Networking
# for dirs... and accessing local logs(?)
Requires:	%{name} = %{version}-%{release}
Requires:	apache

%description cgi
CGI webinterface for Nagios.

%description cgi -l pl
Interfejs CGI dla Nagiosa.

%package devel
Summary:	Include files that Netsaint-related applications may compile against
Summary(pl):	Pliki nag³ówkowe, wykorzystywane przez aplikacje nagiosa
Summary(pt_BR):	Arquivos de cabeçalho necessários para desenvolvimento de aplicativos para o Nagios
Group:		Development/Libraries
# doesn't require base

%description devel
This package provides include files that Netsaint-related applications
may compile against.

%description devel -l pl
Ten pakiet dostarcza pliki nag³ówkowe, które mog± byæ wykorzystywane
przez aplikacje zwi±zane z nagiosem podczas kompilacji.

%description devel -l pt_BR
Este pacote contém arquivos de cabeçalho usados no desenvolvimento de
aplicativos para o Nagios.

%prep
%setup -q
%{?with_pgsql:%patch0 -p1}
%patch1 -p0
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-nagios-user=%{name} \
	--with-nagios-grp=%{name} \
	--with-command-user=nobody \
	--with-command-grp=nobody \
	--with-lockfile=/var/run/%{name}.pid \
	--with-ping_command='/bin/ping -n %%s -c %%d' \
	%{?with_mysql:--with-mysql-xdata --with-mysql-status --with-mysql-comments --with-mysql-extinfo --with-mysql-retention --with-mysql-downtime --with-mysql-lib=%{_libdir} --with-mysql-inc=%{_includedir}/mysql} \
	%{?with_pgsql:--with-pgsql-xdata --with-pgsql-status --with-pgsql-comments --with-pgsql-extinfo --with-pgsql-retention --with-pgsql-downtime--with-pgsql-lib=%{_libdir} --with-pgsql-inc=%{_includedir}/postgresql} \
	%{!?with_gd:--disable-statusmap --disable-trends}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,httpd},%{_includedir}/%{name},%{_libdir}/%{name}/plugins} \
	$RPM_BUILD_ROOT{%{_var}/log/%{name},%{_localstatedir}}

install common/locations.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install install-html install-config install-init install-commandmode fullinstall \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

### Install logos
tar -xvz -C $RPM_BUILD_ROOT%{_datadir}/images/logos -f %{SOURCE3}


%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid nagios`" ]; then
	if [ "`getgid nagios`" != "72" ]; then
		echo "Error: group nagios doesn't have gid=72. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	if [ -n "`getgid netsaint`" -a "`getgid netsaint`" = "72" ]; then
		/usr/sbin/groupmod -n nagios netsaint
	else
		/usr/sbin/groupadd -g 72 -f nagios
	fi
fi
if [ -n "`id -u nagios 2>/dev/null`" ]; then
	if [ "`id -u nagios`" != "72" ]; then
		echo "Error: user nagios doesn't have uid=72. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	if [ -n "`id -u netsaint 2>/dev/null`" -a "`id -u netsaint`" = "72" ]; then
		/usr/sbin/usermod -d /tmp -l nagios netsaint
	else
		/usr/sbin/useradd -u 72 -d %{_libdir}/nagios -s /bin/false -c "%{name} User" -g nagios nagios 1>&2
	fi
fi

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
fi

%preun
if [ "$1" = "0" ] ; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove nagios
	%groupremove nagios
fi

%files
%defattr(644,root,root,755)
%doc Changelog README* UPGRADING contrib/database
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(751,root,nagios) %dir %{_sysconfdir}
%attr(644,root,nagios) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/[!c]*
%attr(644,root,nagios) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/c[!g]*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_bindir}/%{name}
%attr(771,nagios,http) %{_var}/log/%{name}
%attr(775,nagios,nagios) %dir %{_localstatedir}
%attr(775,nagios,nagios) %dir %{_localstatedir}/archives
%attr(2775,nagios,http) %dir %{_localstatedir}/rw

%files cgi
%defattr(644,root,root,755)
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%attr(644,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/cgi.cfg-sample
%dir %{_libdir}/%{name}/cgi
%attr(755,root,root) %{_libdir}/%{name}/cgi/*.cgi
%{_datadir}

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
