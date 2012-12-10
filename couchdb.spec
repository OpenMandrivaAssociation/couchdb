%define tarname apache-couchdb
%define couchdb_user couchdb
%define couchdb_group couchdb
%define couchdb_home %{_localstatedir}/lib/couchdb

Name:		couchdb
Version:	1.2.0
Release:	%mkrel 2
Summary:	A document database server, accessible via a RESTful JSON API
Group:		Databases
License:	Apache License
URL:		http://couchdb.apache.org/
Source0:	http://www.apache.org/dist/%{name}/releases/%{version}/%{tarname}-%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.tmpfiles.conf

BuildRequires:	erlang-devel erlang-compiler erlang-crypto erlang-eunit
BuildRequires:	libicu-devel 
BuildRequires:	js-devel 
BuildRequires:	help2man
BuildRequires:	curl-devel

Requires:	couchdb-bin

Requires(pre):	shadow-utils

%description
Apache CouchDB is a distributed, fault-tolerant and schema-free 
document-oriented database accessible via a RESTful HTTP/JSON API. 
Among other features, it provides robust, incremental replication 
with bi-directional conflict detection and resolution, and is 
queryable and indexable using a table-oriented view engine with 
JavaScript acting as the default view definition language.

This package contains the systemd unit needed to start a systemwide
instance of CouchDB.

%package	bin
Group:		Databases
Summary:	Binary for Couchdb, a document database server

Requires:	erlang 
Requires:	erlang-crypto
Requires:	erlang-ssl
Requires:	erlang-xmerl
Requires:	erlang-inets
Requires:	erlang-tools
Requires:	erlang-public_key
Requires:	erlang-os_mon

%description bin
Apache CouchDB is a distributed, fault-tolerant and schema-free 
document-oriented database accessible via a RESTful HTTP/JSON API. 
Among other features, it provides robust, incremental replication 
with bi-directional conflict detection and resolution, and is 
queryable and indexable using a table-oriented view engine with 
JavaScript acting as the default view definition language.

This package contains the binary needed to run a CouchDB instance.


%prep
%setup -q -n %{tarname}-%{version}


%build
autoreconf -fi
%configure2_5x \
    --with-js-include=%{_includedir}/js \
    --with-erlang=%{_libdir}/erlang%{_includedir}

%make 


%install
%makeinstall_std

# Libdir for systemd unit
sed -i -e 's|@LIBDIR@|%{_libdir}|' %{SOURCE1}

# Install systemd unit
install -D -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# Install /etc/tmpfiles.d entry
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

# Create /var/log/couchdb
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

# Create /var/run/couchdb
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}

# Create /var/lib/couchdb
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

# Create /etc/couchdb/default.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/default.d

# Create /etc/couchdb/local.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/local.d

## Use /etc/sysconfig instead of /etc/default
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mv %{buildroot}%{_sysconfdir}/default/couchdb \
%{buildroot}%{_sysconfdir}/sysconfig/%{name}
rm -rf %{buildroot}%{_sysconfdir}/default

# Remove unecessary files
rm %{buildroot}%{_sysconfdir}/rc.d/couchdb
rm -rf  %{buildroot}%{_datadir}/doc/couchdb

# clean-up .la archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%pre bin
%_pre_useradd %{couchdb_user}  %{couchdb_home} /bin/bash 


%post
%_post_service %{name}


%postun bin
%_postun_userdel %{couchdb_user}


%preun 
%_preun_service %{name}


%files
%doc AUTHORS BUGS CHANGES LICENSE NEWS NOTICE README THANKS
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service

%files bin
%{_bindir}/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/local.d
%dir %{_sysconfdir}/%{name}/default.d
%config(noreplace) %attr(0644,%{couchdb_user},root) %{_sysconfdir}/%{name}/default.ini
%config(noreplace) %attr(0644,%{couchdb_user},root) %{_sysconfdir}/%{name}/local.ini
%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%dir %attr(0755,%{couchdb_user},root) %{_localstatedir}/log/%{name}
%dir %attr(0755,%{couchdb_user},root) %{_localstatedir}/run/%{name}
%dir %attr(0755,%{couchdb_user},root) %{_localstatedir}/lib/%{name}
