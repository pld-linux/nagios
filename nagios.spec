#
# Conditional build:
%bcond_with	pgsql	# enable PostgreSQL support
%bcond_with	mysql	# enable MySQL support
%bcond_without	gd	# without statusmap and trends, which require gd library
#
# TODO:
#  - permissions in /etc. things to consider:
#   - cgi.cfg contains sensitive information
#   - /etc/nagios/*.cfg should be readable by nagios (and webserver if -cgi is used)
#   - all files should be owned by root as there's no write permission needed
#  - create group "nagios-data" for sharing access with httpd user (/etc/nagios/*.cfg)
%define	data_gid 147

Summary:	Host/service/network monitoring program
Summary(pl):	Program do monitorowania serwerów/us³ug/sieci
Summary(pt_BR):	Programa para monitoração de máquinas e serviços
Name:		nagios
Version:	2.0
%define	_rc     b2
Release:	0.%{_rc}.66
License:	GPL v2
Group:		Networking
Source0:	http://dl.sourceforge.net/nagios/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	72d21f961b28519529e8c96c35051fbc
Source1:	%{name}-apache.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	http://dl.sourceforge.net/nagios/imagepak-base.tar.gz
# Source4-md5:	35b75ece533dfdf4963a67ce4e77fc4a
Source5:	http://dl.sourceforge.net/nagios/imagepak-andrade.tar.gz
# Source5-md5:	6e3d35113812e19a2803281a3317fffb
Source6:	http://dl.sourceforge.net/nagios/imagepak-bernhard.tar.gz
# Source6-md5:	cd711110929fd2487234172a533e82c5
Source7:	http://dl.sourceforge.net/nagios/imagepak-cook.tar.gz
# Source7-md5:	248d682712c594fc4734c0158d2d2ee4
Source8:	http://dl.sourceforge.net/nagios/imagepak-didier.tar.gz
# Source8-md5:	83e98389e5b7fb39d2c0e3a96d5ca585
Source9:	http://dl.sourceforge.net/nagios/imagepak-remus.tar.gz
# Source9-md5:	76595744dae8153c921c4af6bf18383d
Source10:	http://dl.sourceforge.net/nagios/imagepak-satrapa.tar.gz
# Source10-md5:	3ed26d8b49379e0dc14f448d5c2a70c3
Source11:	http://dl.sourceforge.net/nagios/imagepak-werschler.tar.gz
# Source11-md5:	1a9cba019ccd27756977821aa735c40f
Patch0:		%{name}-pgsql.patch
Patch1:		%{name}-resources.patch
Patch2:		%{name}-iconv-in-libc.patch
Patch3:		%{name}-config.patch
Patch4:		%{name}-cgi.patch
URL:		http://www.nagios.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with gd}
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%endif
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.177
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
%{?with_pgsql:%patch0 -p1}
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-nagios-user=%{name} \
	--with-nagios-grp=%{name} \
	--with-command-user=%{name} \
	--with-command-grp=%{name} \
	--with-lockfile=%{_localstatedir}/%{name}.pid \
	--with-ping_command='/bin/ping -n %%s -c %%d' \
	%{?with_mysql:--with-mysql-xdata --with-mysql-status --with-mysql-comments --with-mysql-extinfo --with-mysql-retention --with-mysql-downtime --with-mysql-lib=%{_libdir} --with-mysql-inc=%{_includedir}/mysql} \
	%{?with_pgsql:--with-pgsql-xdata --with-pgsql-status --with-pgsql-comments --with-pgsql-extinfo --with-pgsql-retention --with-pgsql-downtime--with-pgsql-lib=%{_libdir} --with-pgsql-inc=%{_includedir}/postgresql} \
	%{!?with_gd:--disable-statusmap --disable-trends}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_includedir}/%{name},%{_libdir}/%{name}/plugins} \
	$RPM_BUILD_ROOT{%{_var}/log/%{name}/archives,%{_localstatedir},%{_sysconfdir}}

install include/locations.h	$RPM_BUILD_ROOT%{_includedir}/%{name}

%{__make} install install-html install-init install-commandmode fullinstall \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OPTS="" \
	INIT_OPTS="" \
	COMMAND_OPTS=""

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# install templated configuration files
install sample-config/{nagios,cgi,resource}.cfg $RPM_BUILD_ROOT%{_sysconfdir}
install sample-config/{contact{s,groups},{misccommand,dependencie,escalation,hostgroup,host,service,timeperiod,checkcommand}s}.cfg $RPM_BUILD_ROOT%{_sysconfdir}
> $RPM_BUILD_ROOT%{_sysconfdir}/passwd
echo 'nagios:' > $RPM_BUILD_ROOT%{_sysconfdir}/group

# install event handlers
cp -a contrib/eventhandlers $RPM_BUILD_ROOT%{_libdir}/%{name}/eventhandlers

# Install logos
install -d $RPM_BUILD_ROOT%{_datadir}/images/logos/{andrade,bernhard,cook}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos -f %{SOURCE4}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos/andrade --strip-path=1 -f %{SOURCE5}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos/bernhard --strip-path=1 -f %{SOURCE6}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos/cook -f %{SOURCE7}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos -f %{SOURCE8}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos -f %{SOURCE9}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos -f %{SOURCE10}
tar -xz -C $RPM_BUILD_ROOT%{_datadir}/images/logos -f %{SOURCE11}

# Object data/cache files
for i in {objects.cache,{comments,downtime,retention,status}.dat,nagios.tmp}; do
	> $RPM_BUILD_ROOT%{_localstatedir}/$i
done
> $RPM_BUILD_ROOT%{_localstatedir}/rw/nagios.cmd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid nagios`" ]; then
	if [ "`getgid nagios`" != "72" ]; then
		echo "Error: group nagios doesn't have gid=72. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	if [ -n "`getgid netsaint`" ] && [ "`getgid netsaint`" = "72" ]; then
		/usr/sbin/groupmod -n nagios netsaint
	else
		/usr/sbin/groupadd -g 72 -f nagios
	fi
fi

if [ -n "`getgid nagios-data`" ]; then
	if [ "`getgid nagios-data`" != "%{data_gid}" ]; then
		echo "Error: group nagios-data doesn't have gid=%{data_gid}. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
		/usr/sbin/groupadd -g %{data_gid} -f nagios-data
fi

if [ -n "`id -u nagios 2>/dev/null`" ]; then
	if [ "`id -u nagios`" != "72" ]; then
		echo "Error: user nagios doesn't have uid=72. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	if [ -n "`id -u netsaint 2>/dev/null`" ] && [ "`id -u netsaint`" = "72" ]; then
		/usr/sbin/usermod -d %{_libdir}/nagios -l nagios netsaint
	else
		/usr/sbin/useradd -u 72 -d %{_libdir}/nagios -s /bin/false -c "%{name} User" -g nagios -G nagios-data nagios 1>&2
	fi
fi

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

%triggerpostun -- nagios < 2.0-0.b2.53
chgrp nagios-data %{_sysconfdir}/*.cfg
%addusertogroup nagios nagios-data
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
fi

%triggerpostun -- nagios < 2.0-0.b2.66
/usr/sbin/usermod -G nagios-data nagios
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc Changelog README* UPGRADING INSTALLING LICENSE
%doc sample-config/template-object/{bigger,minimal}.cfg
%attr(750,root,nagios-data) %dir %{_sysconfdir}
%attr(640,root,nagios-data) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/[!r]*.cfg
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/resource.cfg
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

%defattr(755,root,root,755)
%{_libdir}/%{name}/eventhandlers

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
