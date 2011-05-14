#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_layout
%define mod_conf 15_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Add custom header and/or footers for apache
Name:		apache-%{mod_name}
Version:	5.1
Release:	%mkrel 11
Group:		System/Servers
License:	BSD-style
URL:		http://software.tangent.org/
Source0:	http://download.tangent.org/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod_Layout creates a framework for doing design. Whether you need a simple
copyright or ad banner attached to every page, or need to have something more
challenging such a custom look and feel for a site that employs an array of
technologies (Java Servlets, mod_perl, PHP, CGI's, static HTML, etc...),
Mod_Layout creates a framework for such an environment. By allowing you to
cache static components and build sites in pieces, it gives you the tools for
creating large custom portal sites. 

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c mod_layout.c utility.c layout.c

cat > index.html <<EOF

<p>No documentation exists yet for this module, go to 
<a href="http://software.tangent.org/">tangent.org</a> 
for more information</p>

<p>Meanwhile take a look at the %{_sysconfdir}/httpd/modules.d/%{mod_conf} file</p>

<p>Also please take the time to check out the 
<a href=http://nux.se/apache/>modules for apache</a> 
repository for Mandriva Linux.</p>

<-- replace_me -->

EOF

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name} %{buildroot}%{_var}/www/html/addon-modules/%{name}

# make the example work... (ugly, but it works...)

NEW_URL=/addon-modules/%{name}/index.html
perl -pi -e "s|_REPLACE_ME_|$NEW_URL|g" %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog INSTALL README index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*
