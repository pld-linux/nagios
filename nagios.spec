#
# Conditional build:
# _with_pgsql - enable pgsql support
# _with_mysql - enable mysql support
# _without_gd - without statusmap and trends, which require gd library
#
Summary:	Host/service/network monitoring program
Summary(pl):	Program do monitorowania serwerów/us³ug/sieci
Summary(pt_BR):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	1.1
Release:	0.9
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	5f48ecd9bad2c4d7c9d88d0b6f347ecf
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Patch0:		%{name}-pgsql.patch
URL:		http://www.nagios.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_gd:BuildRequires:	gd-devel}
%{?_with_mysql:BuildRequires:	mysql-devel}
%{?_with_pgsql:BuildRequires:	postgresql-devel}
PreReq:		rc-scripts
PreReq:		sh-utils
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,postun):	/sbin/chkconfig
Conflicts:	iputils-ping < 1:ss020124
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	netsaint

%define _sysconfdir	/etc/%{name}

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
%{?_with_pgsql:%patch -p1}

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%configure \
	--with-nagios-user=%{name} \
	--with-nagios-grp=%{name} \
	--with-command-user=nobody \
	--with-command-grp=nobody \
	--with-lockfile=/var/run/%{name}.pid \
	--with-ping_command='/bin/ping -n %%s -c %%d' \
	%{?_with_mysql:--with-mysql-xdata --with-mysql-status --with-mysql-comments --with-mysql-extinfo --with-mysql-retention --with-mysql-downtime --with-mysql-lib=%{_libdir} --with-mysql-inc=%{_includedir}/mysql} \
	%{?_with_pgsql:--with-pgsql-xdata --with-pgsql-status --with-pgsql-comments --with-pgsql-extinfo --with-pgsql-retention --with-pgsql-downtime--with-pgsql-lib=%{_libdir} --with-pgsql-inc=%{_includedir}/postgresql} \
	%{?_without_gd:--disable-statusmap --disable-trends} \
	--bindir=%{_sbindir} \
	--sbindir=%{_libdir}/%{name}/cgi \
	--datadir=%{_datadir}/%{name} \
	--localstatedir=/var/lib/%{name}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,httpd},%{_includedir}/%{name},%{_libdir}/%{name}/plugins,%{_var}/log/%{name}}

install common/locations.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install install-html install-config install-init install-commandmode fullinstall \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid %{name}`" ]; then
       if [ "`getgid %{name}`" != "72" ]; then
               echo "Error: group %{name} doesn't have gid=72. Correct this before installing %{name}." 1>&2
               exit 1
       fi
else
       /usr/sbin/groupadd -g 72 -f %{name}
fi
if [ -n "`id -u %{name} 2>/dev/null`" ]; then
       if [ "`id -u %{name}`" != "72" ]; then
               echo "Error: user %{name} doesn't have uid=72. Correct this before installing %{name}." 1>&2
               exit 1
       fi
else
       /usr/sbin/useradd -u 72 -d %{_libdir}/%{name} -s /bin/false -c "%{name} User" -g %{name} %{name} 1>&2
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
       /usr/sbin/userdel %{name}
       /usr/sbin/groupdel %{name}
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
%attr(755,root,root) %{_sbindir}/%{name}
%attr(771,nagios,http) %{_var}/log/%{name}

%files cgi
%defattr(644,root,root,755)
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%attr(644,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/cgi.cfg-sample
%dir %{_libdir}/%{name}/cgi
%attr(755,root,root) %{_libdir}/%{name}/cgi/*.cgi
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
