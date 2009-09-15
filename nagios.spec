#
# Conditional build:
%bcond_without	gd	# without statusmap and trends, which require gd library
# reeenable when http://tracker.nagios.org/view.php?id=51 is fixed
%bcond_with	tests
#
Summary:	Host/service/network monitoring program
Summary(pl.UTF-8):	Program do monitorowania serwerów/usług/sieci
Summary(pt_BR.UTF-8):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	3.2.0
Release:	6
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/nagios/%{name}-%{version}.tar.gz
# Source0-md5:	3566167cc60ddeaad34e7d2e26ed4a58
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	http://www.nagios.org/images/favicon.ico
# Source4-md5:	1c4201c7da53d6c7e48251d3a9680449
Source5:	%{name}-config-20090914.tar.bz2
# Source5-md5:	605f1cd28c00db961dad6f529d849f16
Source6:	%{name}-lighttpd.conf
Patch0:		%{name}-resources.patch
Patch1:		%{name}-iconv-in-libc.patch
Patch2:		%{name}-webapps.patch
Patch3:		%{name}-cgi-http_charset.patch
Patch4:		%{name}-cmd-typo.patch
Patch5:		config.patch
URL:		http://www.nagios.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with gd}
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts
Requires:	sh-utils
Suggests:	nagios-notify >= 0.13
Provides:	nagios-core
Obsoletes:	netsaint
Conflicts:	iputils-ping < 1:ss020124
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_bindir		%{_prefix}/sbin
%define		_sbindir	%{_libdir}/%{name}/cgi
%define		_datadir	%{_prefix}/share/%{name}
%define		_localstatedir	/var/lib/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}

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

%description -l pl.UTF-8
Nagios to program, który monitoruje serwery oraz usługi w naszej
sieci. Posiada on możliwość wysyłania informacji o wystąpieniu oraz
rozwiązaniu problemu. Nagios został napisany w C oraz jest
zaprojektowany do pracy pod Linuksem (i niektórymi innymi uniksami)
jako proces pracujący w tle i bezustannie wykonujący pewne operacje
sprawdzające.

Właściwe sprawdzanie jest wykonywane przez osobne programy
("wtyczki"), które zwracają informacje o statusie do Nagiosa. Wtyczki
są dostępne na stronie w pakietach nagios-plugins.

Nagios jest następcą NetSainta.

%description -l pt_BR.UTF-8
O Nagios é um programa que monitora máquinas e serviços na sua rede.
Ele pode enviar um email ou um aviso de pager para o administrador
quando surgir um problema e quando ele for resolvido. Nagios é escrito
em C e foi desenvolvido para rodar em plataformas Linux (e algumas
variações de *NIX) como um processo em segundo plano, periodicamente
executando checagens nos diversos serviços que forem especificados.

%package common
Summary:	Common files needed by both nagios and nrpe
Summary(pl.UTF-8):	Wspólne pliki wymagane zarówno przez nagiosa jak i nrpe
Group:		Networking
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/groupmod
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Provides:	group(nagcmd)
Provides:	group(nagios)
Provides:	user(nagios)

%description common
Common files needed by both nagios and nrpe.

%description common -l pl.UTF-8
Wspólne pliki wymagane zarówno przez nagiosa jak i nrpe.

%package cgi
Summary:	CGI webinterface for Nagios
Summary(pl.UTF-8):	Interfejs WWW/CGI dla Nagiosa
Group:		Applications/WWW
# for dirs... and accessing local logs.
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-imagepaks
Requires:	%{name}-theme
Requires:	group(http)
Requires:	webapps
Requires:	webserver
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(auth)
Requires:	webserver(cgi)
Requires:	webserver(indexfile)

%description cgi
CGI webinterface for Nagios.

%description cgi -l pl.UTF-8
Interfejs CGI dla Nagiosa.

%package theme-default
Summary:	Default Nagios theme
Summary(pl.UTF-8):	Domyślny motyw Nagiosa
Group:		Applications/WWW
Requires:	nagios-cgi = %{version}-%{release}
Requires:	webserver(php)
Provides:	nagios-theme
Obsoletes:	nagios-theme

%description theme-default
Original theme from Nagios.

%description theme-default -l pl.UTF-8
Oryginalny motyw z Nagiosa.

%package devel
Summary:	Include files that Nagios-related applications may compile against
Summary(pl.UTF-8):	Pliki nagłówkowe, wykorzystywane przez aplikacje nagiosa
Summary(pt_BR.UTF-8):	Arquivos de cabeçalho necessários para desenvolvimento de aplicativos para o Nagios
Group:		Development/Libraries
# doesn't require base

%description devel
This package provides include files that Nagios-related applications
may compile against.

%description devel -l pl.UTF-8
Ten pakiet dostarcza pliki nagłówkowe, które mogą być wykorzystywane
przez aplikacje związane z nagiosem podczas kompilacji.

%description devel -l pt_BR.UTF-8
Este pacote contém arquivos de cabeçalho usados no desenvolvimento de
aplicativos para o Nagios.

%prep
%setup -q -a5
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

find -name .cvsignore -o -name .gitignore | xargs rm

mv nagios-config-*/objects/*.cfg sample-config/template-object
mv nagios-config-*/*.cfg sample-config

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

sed -i -e '
	s,".*/var/rw/nagios.cmd,"%{_localstatedir}/rw/nagios.cmd,
	s,".*/libexec/eventhandlers,"%{_libdir}/%{name}/eventhandlers,
' $(find contrib/eventhandlers -type f)

sed -e 's,%{_prefix}/lib/,%{_libdir}/,' %{SOURCE1} > apache.conf
sed -e 's,%{_prefix}/lib/,%{_libdir}/,' %{SOURCE6} > lighttpd.conf

# fixup cgi config
%{__sed} -i -e '
	# kill trailing spaces
	s, \+$,,
	# use real paths
	s,/usr/local/nagios/share,@datadir@,g
	# we want all authorized users have default access
	s,=nagiosadmin,=*,g
' sample-config/*.cfg.in

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	--with-nagios-user=%{name} \
	--with-nagios-grp=%{name} \
	--with-command-user=%{name} \
	--with-command-grp=%{name} \
	--with-lockfile=%{_localstatedir}/%{name}.pid \
	--with-checkresult-dir=%{_var}/spool/%{name}/checkresults \
	--with-ping_command='/bin/ping -n %%s -c %%d' \
	%{!?with_gd:--disable-statusmap --disable-trends} \
	%{?with_tests:--enable-libtap} \
	--enable-event-broker

%{__make} all

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_webapps}/%{_webapp}} \
	$RPM_BUILD_ROOT{%{_var}/log/%{name}/archives,%{_localstatedir}/rw} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{plugins,objects} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/{eventhandlers,plugins} \
%if "%{_lib}" != "lib"
	$RPM_BUILD_ROOT%{_prefix}/lib/%{name}/{eventhandlers,plugins} \
%endif

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -a include/*.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install-unstripped \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}

# install templated configuration files
for a in nagios.cfg resource.cfg commands.cfg contactgroups.cfg contacts.cfg templates.cfg timeperiods.cfg; do
	cp -a sample-config/$a $RPM_BUILD_ROOT%{_sysconfdir}
done

# webserver files
cp -a apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/lighttpd.conf
cp -a sample-config/cgi.cfg $RPM_BUILD_ROOT%{_webapps}/%{_webapp}
> $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/passwd
echo 'nagios:' > $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/group

# install event handlers, sample config
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib/eventhandlers $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a sample-config $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name '*.in' | xargs rm

# Object data/cache files
for i in {objects.{cache,precache},{comments,downtime,retention,status}.dat,nagios.tmp}; do
	> $RPM_BUILD_ROOT%{_localstatedir}/$i
done
> $RPM_BUILD_ROOT%{_localstatedir}/rw/nagios.cmd

%clean
rm -rf $RPM_BUILD_ROOT

%post
for i in %{_localstatedir}/{objects.{cache,precache},{comments,downtime,retention,status}.dat}; do
	[ ! -f $i ] && touch $i
	chown root:nagios $i
	chmod 664 $i
done

/sbin/chkconfig --add %{name}
%service %{name} restart "Nagios service"

%preun
if [ "$1" = "0" ] ; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%pre common
# rename group netsaint -> nagios
if [ "`getgid netsaint 2>/dev/null`" = "72" ]; then
	/usr/sbin/groupmod -n nagios netsaint
fi
# rename group nagios-data -> nagcmd
if [ "`getgid nagios-data 2>/dev/null`" = "147" ]; then
	/usr/sbin/groupmod -n nagcmd nagios-data
fi
%groupadd -g 72 nagios
%groupadd -g 147 -f nagcmd
if [ -n "`id -u netsaint 2>/dev/null`" ] && [ "`id -u netsaint`" = "72" ]; then
	/usr/sbin/usermod -d %{_libdir}/nagios -l nagios -c "Nagios Daemon" -G nagcmd netsaint
fi
%useradd -u 72 -d %{_libdir}/nagios -s /bin/false -c "Nagios Daemon" -g nagios -G nagcmd nagios

%postun common
if [ "$1" = "0" ]; then
	%userremove nagios
	%groupremove nagios
	%groupremove nagcmd
fi

%post cgi
if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
NOTE:
You need to add user to %{_webapps}/%{_webapp}/passwd and
%{_webapps}/%{_webapp}/group to access Nagios via web.

EOF
fi

%triggerin cgi -- apache1 < 1.3.37-3, apache1-base
%addusertogroup http nagcmd
%webapp_register apache %{_webapp}

%triggerun cgi -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin cgi -- apache < 2.2.0, apache-base
%addusertogroup http nagcmd
%webapp_register httpd %{_webapp}

%triggerun cgi -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin cgi -- lighttpd
%addusertogroup lighttpd nagcmd
%webapp_register lighttpd %{_webapp}

%triggerun cgi -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- nagios-cgi < 2.0-0.b3.21
chown root:http %{_sysconfdir}/cgi.cfg

%triggerpostun -- nagios < 3.1.2-4
# restore lost files
for a in dependencies.cfg services.cfg serviceextinfo.cfg hosts.cfg hostgroups.cfg hostextinfo.cfg escalations.cfg checkcommands.cfg misccommands.cfg; do
	if [ -f %{_sysconfdir}/$a.rpmsave -a ! -f %{_sysconfdir}/$a ]; then
		mv -f %{_sysconfdir}/$a{.rpmsave,}
	fi
done
%{__sed} -i -e 's,^check_result_path=.*,check_result_path=%{_var}/spool/%{name}/checkresults,' %{_sysconfdir}/nagios.cfg

%files
%defattr(644,root,root,755)
%doc Changelog README* UPGRADING INSTALLING LICENSE
%attr(750,root,nagios) %dir %{_sysconfdir}/objects
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.cfg

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/nagiostats

%attr(770,root,nagcmd) %dir %{_var}/log/%{name}
%attr(770,root,nagcmd) %dir %{_var}/log/%{name}/archives

%attr(770,root,nagcmd) %dir %{_localstatedir}
%attr(2770,root,nagcmd) %dir %{_localstatedir}/rw
%attr(660,nagios,nagcmd) %ghost %{_localstatedir}/rw/nagios.cmd
%attr(664,root,nagios) %ghost %{_localstatedir}/objects.cache
%attr(664,root,nagios) %ghost %{_localstatedir}/objects.precache
%attr(664,root,nagios) %ghost %{_localstatedir}/*.dat
%attr(664,root,nagios) %ghost %{_localstatedir}/%{name}.tmp

%dir %{_var}/spool
%attr(770,root,nagios) %dir %{_var}/spool/%{name}
%attr(770,root,nagios) %dir %{_var}/spool/%{name}/checkresults

%{_examplesdir}/%{name}-%{version}

%files common
%defattr(644,root,root,755)
%attr(750,root,nagcmd) %dir %{_sysconfdir}
%attr(750,root,nagios) %dir %{_sysconfdir}/plugins
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/eventhandlers

%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/plugins
%dir %{_prefix}/lib/%{name}/eventhandlers
%endif

%files cgi
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/cgi.cfg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/passwd
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/group
%dir %{_sbindir}
%attr(755,root,root) %{_sbindir}/*.cgi

%dir %{_datadir}
%dir %{_datadir}/includes
%dir %{_datadir}/images
%dir %{_datadir}/stylesheets
%{_datadir}/favicon.ico
%{_datadir}/robots.txt
%{_datadir}/contexthelp
%{_datadir}/docs
%{_datadir}/media
%{_datadir}/ssi

%files theme-default
%defattr(644,root,root,755)
%{_datadir}/*.php
%{_datadir}/includes/*
%{_datadir}/images/*
%{_datadir}/stylesheets/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
