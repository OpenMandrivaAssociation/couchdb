%define tarname apache-couchdb
%define couchdb_user couchdb
%define couchdb_group couchdb
%define couchdb_home %{_localstatedir}/lib/couchdb

Name:           couchdb
Version:        1.0.2
Release:        %mkrel 2
Summary:        A document database server, accessible via a RESTful JSON API

Group:          Databases
License:        Apache License
URL:            http://couchdb.apache.org/
Source0:        http://www.apache.org/dist/%{name}/%{version}/%{tarname}-%{version}.tar.gz
Source1:        %{name}.init

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  erlang-devel erlang-compiler
BuildRequires:  libicu-devel 
BuildRequires:  pkgconfig(libjs)
BuildRequires:  help2man
BuildRequires:  curl-devel

Requires:       couchdb-bin
#Initscripts
Requires(post): chkconfig
Requires(preun): chkconfig initscripts

Requires(pre): shadow-utils


%description
Apache CouchDB is a distributed, fault-tolerant and schema-free 
document-oriented database accessible via a RESTful HTTP/JSON API. 
Among other features, it provides robust, incremental replication 
with bi-directional conflict detection and resolution, and is 
queryable and indexable using a table-oriented view engine with 
JavaScript acting as the default view definition language.

This package contains the initscript needed to start a systemwide instance
of CouchDB.

%package bin
Group: Databases
Summary: Binary for Couchdb, a document database server

Requires:   erlang 
Requires:	erlang-crypto
Requires:	erlang-ssl
Requires:	erlang-xmerl
Requires:	erlang-inets
Requires:	erlang-tools


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
%configure2_5x  \
    --with-js-include=$(pkg-config --cflags libjs | sed 's/-I//') \
    --with-erlang=%_libdir/erlang%_includedir 

# build seems to fail on klodia, with make -j16
# (no error logger present) error: "Failed to create 16 scheduler-threads(no er (eagain:11); ror logger present) 
# error: "Failed to creaonly 15 scheduler-threads te 16 scheduler-twhreerae dcs (eagain:11); on(rno erealy 1ror 
# logger present) teed.\n"
# 3 scheduler-threads rror: "Failed to create 16were created.\n"
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## Install couchdb initscript
install -D -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# Create /var/log/couchdb
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

# Create /var/run/couchdb
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

# Create /var/lib/couchdb
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

# Create /etc/couchdb/default.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/default.d

# Create /etc/couchdb/local.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/local.d

## Use /etc/sysconfig instead of /etc/default
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mv $RPM_BUILD_ROOT%{_sysconfdir}/default/couchdb \
$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/default

# Remove unecessary files
rm $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/couchdb
rm -rf  $RPM_BUILD_ROOT%{_datadir}/doc/couchdb

# clean-up .la archives
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%pre bin
%_pre_useradd %{couchdb_user}  %{couchdb_home} /bin/bash 

%post
%_post_service %{name}

%postun bin
%_postun_userdel %{couchdb_user}

%preun 
%_preun_service %{name}

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS CHANGES LICENSE NEWS NOTICE README THANKS
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_initrddir}/%{name}

%files bin
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/local.d
%dir %{_sysconfdir}/%{name}/default.d
%config(noreplace) %attr(0644,%{couchdb_user},root) %{_sysconfdir}/%{name}/default.ini
%config(noreplace) %attr(0644,%{couchdb_user},root) %{_sysconfdir}/%{name}/local.ini
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%dir %attr(0755,%{couchdb_user},root) %{_localstatedir}/log/%{name}
%dir %attr(0755,%{couchdb_user},root) %{_localstatedir}/run/%{name}
%dir %attr(0755,%{couchdb_user},root) %{_localstatedir}/lib/%{name}


