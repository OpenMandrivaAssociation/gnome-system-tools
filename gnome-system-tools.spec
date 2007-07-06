Summary:	GNOME System Tools
Name: 		gnome-system-tools 
Version: 2.18.1
Release: %mkrel 1
License: 	LGPL
Group: 		System/Configuration/Other
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
URL: 		http://www.gnome.org/projects/gst/

Obsoletes:  ximian-setup-tools
Obsoletes:  ximian-setup-tools-devel
Provides:   ximian-setup-tools-devel = %{version}
Provides:   ximian-setup-tools = %{version}-%{release}
BuildRequires:  cracklib-devel
BuildRequires:	libnautilus-devel >= 2.9.3
BuildRequires:  libvte-devel >= 0.10.20
BuildRequires:  gtk2-devel >= 2.9.0
BuildRequires:  libncurses-devel
BuildRequires:  scrollkeeper
BuildRequires:  libmesaglu-devel
BuildRequires:  liboobs-devel >= 2.17.5
BuildRequires:  ImageMagick
BuildRequires:	gnome-doc-utils
BuildRequires:	desktop-file-utils
#gw for intltool
BuildRequires:	perl-XML-Parser
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Requires: system-tools-backends2 >= 2.2.0-3mdv
Requires: usermode

%description
Day-to-day system management on Unix systems is a chore. Even when 
you're using a friendly graphical desktop, seemingly basic tasks 
like setting the system time, changing the network setup, importing 
and exporting network shared filesystems and configuring swap partitions 
requires editing configuration files by hand, and the exact procedure 
varies between different operating systems and distributions.

The GNOME System Tools solve all these problems, giving you a simple
graphical interface for each task, which uses an advanced backend to 
edit all the relevant files and apply your changes. The interface 
looks and acts in exactly the same way regardless of what platform 
you're using.

%prep
%setup -q

%build
%configure2_5x --enable-services --enable-boot
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std desktopdir=%_datadir/applications
rm -f %buildroot%_libdir/nautilus/extensions-1.0/libnautilus*a
rm -rf %buildroot/var/lib/scrollkeeper
%{find_lang} %{name}
%{find_lang} boot-admin --with-gnome
%{find_lang} shares-admin --with-gnome
%{find_lang} network-admin --with-gnome
%{find_lang} services-admin --with-gnome
%{find_lang} time-admin --with-gnome
%{find_lang} users-admin --with-gnome
cat *-admin.lang >> %name.lang
for omf in %buildroot%_datadir/omf/*/*-??.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration-BootandInit" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/services.desktop
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration-Networking" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/{network.desktop,shares.desktop}
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration-Other" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/{time.desktop,users.desktop}

#symlinks for consolehelper
cd %buildroot
mkdir ./%_sbindir
mv ./%_bindir/* ./%_sbindir
cd ./%_sbindir
for bin in *;do ln -s consolehelper %buildroot%_bindir/$bin;done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_scrollkeeper
%update_menus
%post_install_gconf_schemas %name
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_scrollkeeper
%clean_menus
%clean_icon_cache hicolor


%files -f %{name}.lang
%defattr(-, root, root)
%doc README AUTHORS COPYING HACKING NEWS ChangeLog 
%_sysconfdir/gconf/schemas/gnome-system-tools.schemas
%{_bindir}/network-admin
%{_bindir}/services-admin
%{_bindir}/shares-admin
%{_bindir}/time-admin
%{_bindir}/users-admin
%{_sbindir}/network-admin
%{_sbindir}/services-admin
%{_sbindir}/shares-admin
%{_sbindir}/time-admin
%{_sbindir}/users-admin
%{_datadir}/%{name}
%{_datadir}/applications/network.desktop
%{_datadir}/applications/services.desktop
%{_datadir}/applications/shares.desktop
%{_datadir}/applications/time.desktop
%{_datadir}/applications/users.desktop
%_datadir/icons/hicolor/*/devices/*
%dir %{_datadir}/omf/*/
%{_datadir}/omf/*/*-C.omf
%_libdir/nautilus/extensions-1.0/libnautilus-gst-shares.so
%_libdir/pkgconfig/gnome-system-tools.pc
