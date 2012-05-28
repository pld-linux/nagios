# TODO
# - /var/log/nagios/archives -> /var/log/archive/nagios
# - system php-magpierss
# - system jquery
# - don't fetch rss if update fetching is disabled (privacy!)
#
# Conditional build:
%bcond_without	gd	# without statusmap and trends, which require gd library
%bcond_with	epn	# with Embedded Perl
# reeenable when http://tracker.nagios.org/view.php?id=51 is fixed
%bcond_with	tests

Summary:	Host/service/network monitoring program
Summary(pl.UTF-8):	Program do monitorowania serwerów/usług/sieci
Summary(pt_BR.UTF-8):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	3.4.1
Release:	0.8
License:	GPL v2+
Group:		Networking
Source0:	http://downloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
# Source0-md5:	2fa8acfb2a92b1bf8d173a855832de1f
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}-config-20090914.tar.bz2
# Source4-md5:	605f1cd28c00db961dad6f529d849f16
Source5:	%{name}-lighttpd.conf
Source6:	http://www.google.com/mapfiles/shadow50.png
# Source6-md5:	eff99f302f21b95a900d321743fce72b
Source7:	http://www.google.com/mapfiles/marker.png
# Source7-md5:	edefef4bdfc29e1c953694651f05b466
Source8:	googlemap.js
Patch0:		%{name}-resources.patch
Patch1:		%{name}-iconv-in-libc.patch
Patch2:		%{name}-webapps.patch
Patch3:		%{name}-cgi-http_charset.patch
Patch4:		%{name}-cmd-typo.patch
Patch5:		config.patch
Patch6:		%{name}-googlemap.patch
Patch7:		%{name}-doc-usermacros.patch
Patch8:		archivelog-timeformat.patch
URL:		http://www.nagios.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
%if %{with gd}
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%endif
%if %{with tests}
BuildRequires:	perl-HTML-Lint
BuildRequires:	perl-Test-WWW-Mechanize-CGI
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-common = %{version}-%{release}
Requires:	rc-scripts
Requires:	sh-utils
Suggests:	nagios-notify >= 0.13
Suggests:	nagios-plugin-check_load
Suggests:	nagios-plugin-check_ping
Suggests:	nagios-plugins
Provides:	nagios-core
Obsoletes:	netsaint
Conflicts:	iputils-ping < 1:ss020124
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		cgidir		%{_libdir}/%{name}/cgi
%define		htmldir		%{_prefix}/share/%{name}
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
# for dirs... and accessing local logs, nagios config
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
Suggests:	%{name}-doc

%description cgi
CGI webinterface for Nagios.

%description cgi -l pl.UTF-8
Interfejs CGI dla Nagiosa.

%package mrtggraphs
Summary:	MRTG Graphs: Nagios Statistics
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Provides:	mrtg-start

%description mrtggraphs
This pacakge graphs several Nagios statistics which can be useful for
debugging and trending purposes. The nagiostats binary is used to
generate the data.

%package doc
Summary:	HTML Documentation for Nagios
Group:		Documentation
# does not require base

%description doc
HTML Documentation for Nagios.

%package theme-classicui
Summary:	ClassicUI Nagios theme
Group:		Applications/WWW
Requires:	%{name}-cgi = %{version}-%{release}
Requires:	webserver(php)
Provides:	nagios-theme
Obsoletes:	nagios-theme

%description theme-classicui
Original theme from Nagios.

%description theme-classicui -l pl.UTF-8
Oryginalny motyw z Nagiosa.

%package theme-default
Summary:	Virtual package to handle Nagios theme migration
Group:		Applications/WWW
Requires:	nagios-theme
Suggests:	nagios-theme-classicui
Suggests:	nagios-theme-exfoliation
Suggests:	nagios-theme-nuvola
Obsoletes:	nagios-theme-default < 3.3.1-1.4

%description theme-default
Virtual package to handle Nagios theme migration

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
%setup -qc -a4
mv %{name}/* .
%undos cgi/*.c
%undos include/*.h
%undos base/*
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
#fixed
#%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

find -name .cvsignore -o -name .gitignore | xargs rm

mv nagios-config-*/objects/*.cfg sample-config/template-object
mv nagios-config-*/*.cfg sample-config

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

sed -i -e '
	s,".*/var/rw/%{name}.cmd,"%{_localstatedir}/rw/%{name}.cmd,
	s,".*/libexec/eventhandlers,"%{_libdir}/%{name}/eventhandlers,
' $(find contrib/eventhandlers -type f)

%{__sed} -i -e '
	s,/usr/local/nagios/var/,/var/log/%{name}/,g
' p1.pl

sed -e 's,%{_prefix}/lib/,%{_libdir}/,' %{SOURCE1} > apache.conf
sed -e 's,%{_prefix}/lib/,%{_libdir}/,' %{SOURCE5} > lighttpd.conf

# fixup cgi config
%{__sed} -i -e '
	# kill trailing spaces
	s, \+$,,
	# use real paths
	s,/usr/local/%{name}/share,@datadir@,g
	# we want all authorized users have default access
	s,=nagiosadmin,=*,g
' sample-config/*.cfg.in

# fixup paths in doc
#%{__sed} -i -e '
#	s,/usr/local/%{name}/var/archives/,/var/log/%{name}/archives/,
#' html/docs/configmain.html

#rm t/611cgistatus-hosturgencies.t

%build
cp -f /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%if %{with tests}
cd tap
%{__libtoolize}
%{__aclocal}
%{__autoconf}
cd ..
%endif
%configure \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	--bindir=%{_sbindir} \
	--sbindir=%{cgidir} \
	--datadir=%{htmldir} \
	--with-nagios-user=%{name} \
	--with-nagios-grp=%{name} \
	--with-command-user=%{name} \
	--with-command-grp=%{name} \
	--with-lockfile=%{_localstatedir}/%{name}.pid \
	--with-checkresult-dir=%{_var}/spool/%{name}/checkresults \
	--with-ping_command='/bin/ping -n %%s -c %%d' \
	%{!?with_gd:--disable-statusmap --disable-trends} \
	%{?with_epn:--enable-embedded-perl --with-perlcache} \
	%{?with_tests:--enable-libtap} \
	--enable-event-broker

%{__make} all

%if %{with epn}
%{__make} -C contrib mini_epn
%endif

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_webapps}/%{_webapp}} \
	$RPM_BUILD_ROOT{%{_var}/log/%{name}/archives,%{_localstatedir}/rw} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{plugins,objects} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/{eventhandlers,plugins,brokers} \
%if "%{_lib}" != "lib"
	$RPM_BUILD_ROOT%{_prefix}/lib/%{name}/{eventhandlers,plugins} \
%endif

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -p include/*.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install-unstripped \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

%if %{with epn}
mv $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}/%{name}}/p1.pl
install -d $RPM_BUILD_ROOT%{_bindir}
install -p contrib/mini_epn $RPM_BUILD_ROOT%{_bindir}
%endif

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# install templated configuration files
for a in %{name}.cfg resource.cfg commands.cfg contactgroups.cfg contacts.cfg templates.cfg timeperiods.cfg; do
	cp -p sample-config/$a $RPM_BUILD_ROOT%{_sysconfdir}
done

# webserver files
cp -p apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/lighttpd.conf
cp -p sample-config/cgi.cfg $RPM_BUILD_ROOT%{_webapps}/%{_webapp}
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{htmldir}/images
cp -p %{SOURCE7} $RPM_BUILD_ROOT%{htmldir}/images
cp -p %{SOURCE8} $RPM_BUILD_ROOT%{htmldir}/images
> $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/passwd
echo 'nagios:' > $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/group

# install event handlers, sample config
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a contrib/eventhandlers $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a sample-config $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name '*.in' | xargs rm

# mrtg script
install -d $RPM_BUILD_ROOT/etc/mrtg/conf.d
cp -a sample-config/mrtg.cfg $RPM_BUILD_ROOT/etc/mrtg/conf.d/%{name}.cfg

# Object data/cache files
for i in {objects.{cache,precache},{retention,status}.dat,%{name}.{tmp,pid}}; do
	> $RPM_BUILD_ROOT%{_localstatedir}/$i
done
> $RPM_BUILD_ROOT%{_localstatedir}/rw/%{name}.cmd

install -d $RPM_BUILD_ROOT%{_docdir}/%{name}
mv $RPM_BUILD_ROOT{%{htmldir}/docs/*,%{_docdir}/%{name}}

%clean
rm -rf $RPM_BUILD_ROOT

%post
for i in %{_localstatedir}/{objects.{cache,precache},{retention,status}.dat}; do
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
if [ "$(getgid netsaint 2>/dev/null)" = "72" ]; then
	/usr/sbin/groupmod -n nagios netsaint
fi
# rename group nagios-data -> nagcmd
if [ "$(getgid nagios-data 2>/dev/null)" = "147" ]; then
	/usr/sbin/groupmod -n nagcmd nagios-data
fi
%groupadd -g 72 nagios
%groupadd -g 147 -f nagcmd
if [ -n "$(id -u netsaint 2>/dev/null)" ] && [ "$(id -u netsaint)" = "72" ]; then
	/usr/sbin/usermod -d %{_libdir}/%{name} -l nagios -c "Nagios Daemon" -G nagcmd netsaint
fi
%useradd -u 72 -d %{_libdir}/%{name} -s /bin/false -c "Nagios Daemon" -g nagios -G nagcmd nagios

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
%{__sed} -i -e 's,^check_result_path=.*,check_result_path=%{_var}/spool/%{name}/checkresults,' %{_sysconfdir}/%{name}.cfg

%files
%defattr(644,root,root,755)
%doc Changelog README* UPGRADING INSTALLING LICENSE
%attr(750,root,nagios) %dir %{_sysconfdir}/objects

# leave main nagios config readable for -cgi.
%attr(640,root,nagcmd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.cfg

%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/commands.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/contactgroups.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/contacts.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/resource.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/templates.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/timeperiods.cfg

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_sbindir}/nagiostats
%dir %{_libdir}/%{name}/brokers

%attr(770,root,nagcmd) %dir %{_var}/log/%{name}
%attr(770,root,nagcmd) %dir %{_var}/log/%{name}/archives

%attr(770,root,nagcmd) %dir %{_localstatedir}
%attr(2770,root,nagcmd) %dir %{_localstatedir}/rw
%attr(660,nagios,nagcmd) %ghost %{_localstatedir}/rw/%{name}.cmd
%attr(664,root,nagios) %ghost %{_localstatedir}/objects.cache
%attr(664,root,nagios) %ghost %{_localstatedir}/objects.precache
%attr(664,root,nagios) %ghost %{_localstatedir}/*.dat
%attr(664,root,nagios) %ghost %{_localstatedir}/%{name}.tmp
%attr(664,root,nagios) %ghost %{_localstatedir}/%{name}.pid

%attr(770,root,nagcmd) %dir %{_var}/spool/%{name}/checkresults

%{_examplesdir}/%{name}-%{version}

# epn
%if %{with epn}
%attr(755,root,root) %{_libdir}/%{name}/p1.pl
%attr(755,root,root) %{_bindir}/mini_epn
%endif

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

%attr(770,root,nagcmd) %dir %{_var}/spool/%{name}

%files mrtggraphs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/mrtg/conf.d/%{name}.cfg

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}

%files cgi
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/cgi.cfg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/passwd
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/group
%dir %{cgidir}
%attr(755,root,root) %{cgidir}/*.cgi

%dir %{htmldir}
%dir %{htmldir}/includes
%dir %{htmldir}/images
%dir %{htmldir}/stylesheets
%{htmldir}/robots.txt
%{htmldir}/contexthelp
%{htmldir}/media
%{htmldir}/ssi
%{htmldir}/images/favicon.ico
%{htmldir}/images/marker.png
%{htmldir}/images/shadow50.png

%files theme-classicui
%defattr(644,root,root,755)
%{htmldir}/*.php
%{htmldir}/includes/*
%{htmldir}/images/*
%exclude %{htmldir}/images/favicon.ico
%exclude %{htmldir}/images/marker.png
%exclude %{htmldir}/images/shadow50.png
%{htmldir}/stylesheets/*

%files theme-default
%defattr(644,root,root,755)

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
