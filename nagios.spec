#
# Conditional build:
%bcond_without	gd	# without statusmap and trends, which require gd library
#
Summary:	Host/service/network monitoring program
Summary(pl):	Program do monitorowania serwerów/us³ug/sieci
Summary(pt_BR):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	2.0
%define	_rc     b3
Release:	0.%{_rc}.23
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/nagios/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	051760458d961b6ee015b5932a8437c4
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	http://www.nagios.org/images/favicon.ico
# Source4-md5:	1c4201c7da53d6c7e48251d3a9680449
Patch0:		%{name}-resources.patch
Patch1:		%{name}-iconv-in-libc.patch
Patch2:		%{name}-config.patch
Patch3:		%{name}-favicon.patch
URL:		http://www.nagios.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with gd}
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	sed >= 4.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.202
PreReq:		rc-scripts
PreReq:		sh-utils
Requires:	mailx
Requires:	nagios-plugins
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/groupmod
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires(post,postun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(triggerpostun):	sed >= 4.0
Provides:	nagios-core
Provides:	user(nagios)
Provides:	group(nagios)
Provides:	group(nagios-data)
Conflicts:	iputils-ping < 1:ss020124
Obsoletes:	netsaint
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_bindir		%{_prefix}/sbin
%define		_sbindir	%{_libdir}/%{name}/cgi
%define		_datadir	%{_prefix}/share/%{name}
%define		_localstatedir	/var/lib/%{name}

%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

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
Requires:	%{name}-imagepaks
Requires:	webserver = apache
Requires:	apache(mod_alias)
Requires:	apache(mod_cgi)
Requires:	apache(mod_auth)
Requires:	group(http)

%description cgi
CGI webinterface for Nagios.

%description cgi -l pl
Interfejs CGI dla Nagiosa.

%package devel
Summary:	Include files that Nagios-related applications may compile against
Summary(pl):	Pliki nag³ówkowe, wykorzystywane przez aplikacje nagiosa
Summary(pt_BR):	Arquivos de cabeçalho necessários para desenvolvimento de aplicativos para o Nagios
Group:		Development/Libraries
# doesn't require base

%description devel
This package provides include files that Nagios-related applications
may compile against.

%description devel -l pl
Ten pakiet dostarcza pliki nag³ówkowe, które mog± byæ wykorzystywane
przez aplikacje zwi±zane z nagiosem podczas kompilacji.

%description devel -l pt_BR
Este pacote contém arquivos de cabeçalho usados no desenvolvimento de
aplicativos para o Nagios.

%prep
%setup -q -n %{name}-%{version}%{?_rc}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e '
	s,".*/var/rw/nagios.cmd,"%{_localstatedir}/rw/nagios.cmd,
	s,".*/libexec/eventhandlers,"%{_libdir}/%{name}/eventhandlers,
' $(find contrib/eventhandlers -type f)

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
	%{!?with_gd:--disable-statusmap --disable-trends}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_includedir}/%{name},%{_libdir}/%{name}/{eventhandlers,plugins}} \
	$RPM_BUILD_ROOT{%{_var}/log/%{name}/archives,%{_localstatedir},%{_sysconfdir},%{_examplesdir}/%{name}-%{version}}

install include/locations.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install install-html install-init install-commandmode fullinstall \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}

# install templated configuration files
install sample-config/{nagios,cgi,resource}.cfg $RPM_BUILD_ROOT%{_sysconfdir}
install sample-config/{contact{s,groups},{misccommand,dependencie,escalation,hostgroup,host,service,timeperiod,checkcommand}s}.cfg $RPM_BUILD_ROOT%{_sysconfdir}
install sample-config/{service,host}extinfo.cfg $RPM_BUILD_ROOT%{_sysconfdir}
> $RPM_BUILD_ROOT%{_sysconfdir}/passwd
echo 'nagios:' > $RPM_BUILD_ROOT%{_sysconfdir}/group

# install event handlers
cp -a contrib/eventhandlers $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# Object data/cache files
for i in {objects.cache,{comments,downtime,retention,status}.dat,nagios.tmp}; do
	> $RPM_BUILD_ROOT%{_localstatedir}/$i
done
> $RPM_BUILD_ROOT%{_localstatedir}/rw/nagios.cmd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "`getgid netsaint`" = "72" ]; then
	/usr/sbin/groupmod -n nagios netsaint
fi
%groupadd -g 72 nagios
%groupadd -g 147 -f nagios-data
if [ -n "`id -u netsaint 2>/dev/null`" ] && [ "`id -u netsaint`" = "72" ]; then
	/usr/sbin/usermod -d %{_libdir}/nagios -l nagios -c "Nagios User" -G nagios-data netsaint
fi
%useradd -u 72 -d %{_libdir}/nagios -s /bin/false -c "Nagios User" -g nagios -G nagios-data nagios

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
fi

for i in %{_localstatedir}/{objects.cache,{comments,downtime,retention,status}.dat}; do
	[ ! -f $i ] && touch $i
	chown root:nagios $i
	chmod 664 $i
done

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
	%groupremove nagios-data
fi

%post cgi
%addusertogroup http nagios-data

# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<EOF
NOTE:
You need to add user to %{_sysconfdir}/passwd and %{_sysconfdir}/group to acccess nagios via web.

EOF
fi

%preun cgi
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

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

if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2 || :
fi

# apache2 config was also moved.
if [ -f /etc/httpd/nagios.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f /etc/httpd/nagios.conf.rpmsave %{_sysconfdir}/apache-%{name}.conf

	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2 || :
	fi
fi

echo "Please read http://nagios.sourceforge.net/docs/2_0/whatsnew.html
there are changes that no longer work in Nagios 2.0"

%files
%defattr(644,root,root,755)
%doc Changelog README* UPGRADING INSTALLING LICENSE
%doc sample-config/template-object/{bigger,minimal}.cfg
%attr(750,root,nagios-data) %dir %{_sysconfdir}
%attr(640,root,nagios-data) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nagios.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/[!n]*.cfg
%exclude %{_sysconfdir}/cgi.cfg

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins

%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/nagiostats

%attr(770,root,nagios-data) %{_var}/log/%{name}
%attr(770,root,nagios-data) %dir %{_var}/log/%{name}/archives

%attr(770,root,nagios-data) %dir %{_localstatedir}
%attr(2770,root,nagios-data) %dir %{_localstatedir}/rw
# NOTE: the permissions are set in post script
%ghost %{_localstatedir}/rw/nagios.cmd
%ghost %{_localstatedir}/objects.cache
%ghost %{_localstatedir}/*.dat
%ghost %{_localstatedir}/%{name}.tmp

%{_examplesdir}/%{name}-%{version}

%dir %{_libdir}/%{name}/eventhandlers

%files cgi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache-%{name}.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cgi.cfg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/passwd
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/group
%dir %{_sbindir}
%attr(755,root,root) %{_sbindir}/*.cgi
%{_datadir}

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
