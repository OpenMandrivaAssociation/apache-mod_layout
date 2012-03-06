#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_layout

Summary:	Add custom header and/or footers for apache
Name:		apache-%{mod_name}
Version:	5.1
Release:	14
Group:		System/Servers
License:	BSD-style
URL:		http://software.tangent.org/
Source0:	http://download.tangent.org/%{mod_name}-%{version}.tar.gz
Source1:	115_mod_layout.conf
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}

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

cp %{SOURCE1} .
perl -pi -e "s|_MODULE_DIR_|%{_libdir}/apache|g" *.conf

%build
apxs -c mod_layout.c utility.c layout.c

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache/
install -m0644 *.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc ChangeLog INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
