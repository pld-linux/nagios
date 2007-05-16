#
# Conditional build:
%bcond_without	gd	# without statusmap and trends, which require gd library
#
Summary:	Host/service/network monitoring program
Summary(pl.UTF-8):	Program do monitorowania serwerów/usług/sieci
Summary(pt_BR.UTF-8):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	2.9
Release:	2
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/nagios/%{name}-%{version}.tar.gz
# Source0-md5:	b6e3a21c91edb063c00712c6001e15ec
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	http://www.nagios.org/images/favicon.ico
# Source4-md5:	1c4201c7da53d6c7e48251d3a9680449
Source5:	%{name}-config-20050514.tar.bz2
# Source5-md5:	a2883c65377ef7beb55d48af85ec7ef7
Source6:	%{name}-lighttpd.conf
Patch0:		%{name}-resources.patch
Patch1:		%{name}-iconv-in-libc.patch
Patch2:		%{name}-favicon.patch
Patch3:		%{name}-webapps.patch
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
BuildRequires:	tar >= 1:1.15.1
Requires(post,preun):	/sbin/chkconfig
Requires(triggerpostun):	sed >= 4.0
Requires:	%{name}-common = %{version}-%{release}
Requires:	/bin/mail
Requires:	nagios-plugins
Requires:	rc-scripts
Requires:	sh-utils
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
Provides:	group(nagios)
Provides:	group(nagios-data)
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
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e '
	s,".*/var/rw/nagios.cmd,"%{_localstatedir}/rw/nagios.cmd,
	s,".*/libexec/eventhandlers,"%{_libdir}/%{name}/eventhandlers,
' $(find contrib/eventhandlers -type f)

sed -e 's,%{_prefix}/lib/,%{_libdir}/,' %{SOURCE1} > apache.conf
sed -e 's,%{_prefix}/lib/,%{_libdir}/,' %{SOURCE6} > lighttpd.conf

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure \
	--with-nagios-user=%{name} \
	--with-nagios-grp=%{name} \
	--with-command-user=%{name} \
	--with-command-grp=%{name} \
	--with-lockfile=%{_localstatedir}/%{name}.pid \
	--with-ping_command='/bin/ping -n %%s -c %%d' \
	--enable-event-broker \
	%{!?with_gd:--disable-statusmap --disable-trends}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_webapps}/%{_webapp}} \
	$RPM_BUILD_ROOT{%{_var}/log/%{name}/archives,%{_localstatedir}/rw} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{plugins,local} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/{eventhandlers,plugins} \
%if "%{_lib}" != "lib"
	$RPM_BUILD_ROOT%{_prefix}/lib/%{name}/{eventhandlers,plugins} \
%endif

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
install include/*.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install-unstripped \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}

# install templated configuration files
tar jxf %{SOURCE5} --strip-components=1 -C $RPM_BUILD_ROOT%{_sysconfdir}
sed -i -e 's,%{_prefix}/lib/,%{_libdir}/,' $RPM_BUILD_ROOT%{_sysconfdir}/resource.cfg

# webserver files
install apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
install lighttpd.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/lighttpd.conf
mv $RPM_BUILD_ROOT{%{_sysconfdir}/cgi.cfg,%{_webapps}/%{_webapp}}
> $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/passwd
echo 'nagios:' > $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/group

# install event handlers
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib/eventhandlers $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# Object data/cache files
for i in {objects.cache,{comments,downtime,retention,status}.dat,nagios.tmp}; do
	> $RPM_BUILD_ROOT%{_localstatedir}/$i
done
> $RPM_BUILD_ROOT%{_localstatedir}/rw/nagios.cmd

%clean
rm -rf $RPM_BUILD_ROOT

%post
for i in %{_localstatedir}/{objects.cache,{comments,downtime,retention,status}.dat}; do
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
if [ "`getgid netsaint`" = "72" ]; then
	/usr/sbin/groupmod -n nagios netsaint
fi
%groupadd -g 72 nagios
%groupadd -g 147 -f nagios-data
if [ -n "`id -u netsaint 2>/dev/null`" ] && [ "`id -u netsaint`" = "72" ]; then
	/usr/sbin/usermod -d %{_libdir}/nagios -l nagios -c "Nagios User" -G nagios-data netsaint
fi
%useradd -u 72 -d %{_libdir}/nagios -s /bin/false -c "Nagios User" -g nagios -G nagios-data nagios

%postun common
if [ "$1" = "0" ]; then
	%userremove nagios
	%groupremove nagios
	%groupremove nagios-data
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
%addusertogroup http nagios-data
%webapp_register apache %{_webapp}

%triggerun cgi -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin cgi -- apache < 2.2.0, apache-base
%addusertogroup http nagios-data
%webapp_register httpd %{_webapp}

%triggerun cgi -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin cgi -- lighttpd
%addusertogroup lighttpd nagios-data
%webapp_register lighttpd %{_webapp}

%triggerun cgi -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- nagios-cgi < 2.0-0.b3.21
chown root:http %{_sysconfdir}/cgi.cfg

%triggerpostun -- nagios < 2.0-0.b3.21
chown root:nagios %{_sysconfdir}/*.cfg
chown root:nagios-data %{_sysconfdir}/nagios.cfg
%addusertogroup nagios nagios-data

# must unify nagios.cfg
sed -i -e '
s,^status_file=.*,status_file=%{_localstatedir}/status.dat,
s,^comment_file=.*,comment_file=%{_localstatedir}/comments.dat,
s,^downtime_file=.*,downtime_file=%{_localstatedir}/downtime.dat,
s,^lock_file=.*,lock_file=%{_localstatedir}/nagios.pid,
s,^temp_file=.*,temp_file=%{_localstatedir}/nagios.tmp,
s,^state_retention_file=.*,state_retention_file=%{_localstatedir}/retention.dat,

# option changes
s,^log_passive_service_checks=,log_passive_checks=,
s,^inter_check_delay_method=,service_inter_check_delay_method=,
s,^use_agressive_host_checking=,use_aggressive_host_checking=,
s,^freshness_check_interval=,service_freshness_check_interval=,

' %{_sysconfdir}/nagios.cfg

sed -i -e '
s,\$DATETIME\$,$LONGDATETIME$,g
s,Nagios/1.2,Nagios/%{version},g
' %{_sysconfdir}/misccommands.cfg

mv -f /var/log/nagios/status.log %{_localstatedir}/status.dat 2>/dev/null
mv -f /var/log/nagios/comment.log %{_localstatedir}/comments.dat 2>/dev/null
mv -f /var/log/nagios/downtime.log %{_localstatedir}/downtime.dat 2>/dev/null
mv -f /var/run/nagios.pid %{_localstatedir}/nagios.pid 2>/dev/null
mv -f /var/log/nagios/nagios.tmp %{_localstatedir}/nagios.tmp 2>/dev/null
mv -f /var/log/nagios/status.sav %{_localstatedir}/retention.dat 2>/dev/null
chown nagios:nagios %{_localstatedir}/nagios.pid 2>/dev/null
chown nagios:nagios-data %{_localstatedir}/rw/nagios.cmd 2>/dev/null

%service -q %{name} restart

%banner -e %{name}-2.0 <<'EOF'
Please read <http://nagios.sourceforge.net/docs/2_0/whatsnew.html>
there are changes that no longer work in Nagios 2.0.

You could also try use <http://oss.op5.se/nagios/object_config_fix.php.gz>
to convert your config (yes i know it's too late to say it now, after
the upgrade, but still :))
EOF
#'vim

# webapps trigger
%triggerpostun cgi -- %{name}-cgi < 2.0-0.b6.0.2
for i in cgi.cfg group passwd; do
	if [ -f /etc/nagios/$i.rpmsave ]; then
		mv -f %{_webapps}/%{_webapp}/$i{,.rpmnew}
		mv -f /etc/nagios/$i.rpmsave %{_webapps}/%{_webapp}/$i
	fi
done

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache-nagios.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_webapps}/%{_webapp}/apache.conf{,.rpmnew}
		cp -f /etc/%{name}/apache-nagios.conf.rpmsave %{_webapps}/%{_webapp}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_webapps}/%{_webapp}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache-nagios.conf.rpmsave %{_webapps}/%{_webapp}/httpd.conf
	fi
	rm -f /etc/%{name}/apache-nagios.conf.rpmsave
fi

# place new config location, as trigger puts config only on first install, do it here.
if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/99_%{name}.conf
	apache_reload=1
fi
if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	httpd_reload=1
fi

if [ "$apache_reload" ]; then
	/usr/sbin/webapp register apache %{_webapp}
	%service -q apache reload
fi
if [ "$httpd_reload" ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc Changelog README* UPGRADING INSTALLING LICENSE
%doc sample-config/template-object/{localhost,commands}.cfg
%attr(640,root,nagios-data) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nagios.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/[!n]*.cfg

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/nagiostats

%attr(770,root,nagios-data) %dir %{_var}/log/%{name}
%attr(770,root,nagios-data) %dir %{_var}/log/%{name}/archives

%attr(770,root,nagios-data) %dir %{_localstatedir}
%attr(2770,root,nagios-data) %dir %{_localstatedir}/rw
%attr(660,nagios,nagios-data) %ghost %{_localstatedir}/rw/nagios.cmd
%attr(664,root,nagios) %ghost %{_localstatedir}/objects.cache
%attr(664,root,nagios) %ghost %{_localstatedir}/*.dat
%attr(664,root,nagios) %ghost %{_localstatedir}/%{name}.tmp

%{_examplesdir}/%{name}-%{version}

%files common
%defattr(644,root,root,755)
%attr(750,root,nagios-data) %dir %{_sysconfdir}
%attr(2750,root,nagios) %dir %{_sysconfdir}/plugins
%attr(2750,root,nagios) %dir %{_sysconfdir}/local
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
%{_datadir}/*.html
%{_datadir}/images/*
%{_datadir}/stylesheets/*

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
