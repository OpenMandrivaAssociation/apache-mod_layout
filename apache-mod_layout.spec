#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_layout
%define mod_conf 15_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Add custom header and/or footers for apache
Name:		apache-%{mod_name}
Version:	5.1
Release:	17
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

%{_bindir}/apxs -c mod_layout.c utility.c layout.c

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


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 5.1-11mdv2011.0
+ Revision: 674428
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 5.1-10
+ Revision: 662776
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1-9mdv2011.0
+ Revision: 588282
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1-8mdv2010.1
+ Revision: 515837
- rebuilt for apache-2.2.15

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1-7mdv2010.0
+ Revision: 451700
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1-6mdv2010.0
+ Revision: 405138
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 5.1-5mdv2009.1
+ Revision: 326495
- drop the register patch

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1-4mdv2009.0
+ Revision: 235641
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1-3mdv2009.0
+ Revision: 215291
- rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1-2mdv2008.1
+ Revision: 181439
- rebuild

* Mon Jan 07 2008 Oden Eriksson <oeriksson@mandriva.com> 5.1-1mdv2008.1
+ Revision: 146256
- 5.1

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0-6mdv2008.0
+ Revision: 82361
- rebuild

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0-5mdv2008.0
+ Revision: 64321
- use the new %%serverbuild macro

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0-4mdv2008.0
+ Revision: 38413
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0-3mdv2007.1
+ Revision: 140583
- rebuild

* Tue Feb 27 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0-2mdv2007.1
+ Revision: 126615
- general cleanups

* Thu Feb 22 2007 Oden Eriksson <oeriksson@mandriva.com> 5.0-1mdv2007.1
+ Revision: 124406
- 5.0
- drop upstream patches
- rediffed the register patch (P0)

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 4.0.1a-5mdv2007.1
+ Revision: 79252
- Import apache-mod_layout

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 4.0.1a-5mdv2007.0
- rebuild

* Mon Dec 26 2005 Oden Eriksson <oeriksson@mandriva.com> 4.0.1a-4mdk
- rebuilt against apache-2.2.0 (P2)

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 4.0.1a-3mdk
- rebuilt to provide a -debug package too

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.0.1a-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 4.0.1a-1mdk
- rebuilt for apache-2.0.55

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_4.0.1a-3mdk
- added another work around for a rpm bug

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_4.0.1a-2mdk
- added a work around for a rpm bug, "Requires(foo,bar)" don't work

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_4.0.1a-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Thu Mar 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_4.0.1a-6mdk
- use the %%mkrel macro

* Sun Feb 27 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_4.0.1a-5mdk
- fix %%post and %%postun to prevent double restarts

* Wed Feb 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_4.0.1a-4mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_4.0.1a-3mdk
- fix deps

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_4.0.1a-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_4.0.1a-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_4.0.1a-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_4.0.1a-1mdk
- built for apache 2.0.51

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_4.0.1a-3mdk
- rebuilt

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_4.0.1a-2mdk
- remove redundant provides

* Thu Jul 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_4.0.1a-1mdk
- built for apache 2.0.50

* Sat Jun 12 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_4.0.1a-1mdk
- built for apache 2.0.49
- added P1

