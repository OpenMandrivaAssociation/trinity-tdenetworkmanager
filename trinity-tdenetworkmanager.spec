%bcond clang 1
%bcond gamin 1

# TDE variables
%define tde_pkg tdenetworkmanager
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%undefine _debugsource_template

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	14.1.6
Release:	1
Summary:	Trinity applet for Network Manager
Group:		Applications/Internet
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/applications/settings/%{tarball_name}-%{version}.tar.xz
Source1:		%{name}-rpmlintrc

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share

BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdebase-devel >= %{version}
BuildRequires:	trinity-tde-cmake >= %{version}

BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires: libtool

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

Obsoletes:		trinity-knetworkmanager < %{EVRD}
Provides:		trinity-knetworkmanager = %{EVRD}

# NETWORKMANAGER support
BuildRequires:  pkgconfig(libnm)
Requires:		NetworkManager


# ACL support
BuildRequires:  pkgconfig(libacl)

# DBUS support
BuildRequires:	pkgconfig(dbus-1-tqt)
BuildRequires:	pkgconfig(dbus-tqt)


# UDEV support
BuildRequires:  pkgconfig(udev)

# IDN support
BuildRequires:	pkgconfig(libidn)

# GAMIN support
%{?with_gamin:BuildRequires:	pkgconfig(gamin)}

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
TDENetworkManager is a system tray applet for controlling network
connections on systems that use the NetworkManager daemon.

%post
# Prevent autostart of 'nm-applet', if installed.
if [ -r "/etc/xdg/autostart/nm-applet.desktop" ]; then
  if ! grep -qw "TDE" "/etc/xdg/autostart/nm-applet.desktop" ; then
    sed -i "/etc/xdg/autostart/nm-applet.desktop" -e "s|\(NotShowIn=.*\)|\1TDE;|"
  fi
fi

%files
%defattr(-,root,root,-)
%{tde_prefix}/bin/tdenetworkmanager
%{tde_prefix}/%{_lib}/*.la
%{tde_prefix}/%{_lib}/*.so
%{_sysconfdir}/dbus-1/system.d/tdenetworkmanager.conf
%{tde_prefix}/share/applications/tde/tdenetworkmanager.desktop
%{tde_prefix}/share/apps/tdenetworkmanager
%{tde_prefix}/share/icons/hicolor/*/apps/tdenetworkmanager*
%{tde_prefix}/share/servicetypes/tdenetworkmanager_plugin.desktop
%{tde_prefix}/share/servicetypes/tdenetworkmanager_vpnplugin.desktop
%{tde_prefix}/share/autostart/tdenetworkmanager.desktop
#{tde_datadir}/services/tdenetman_openvpn.desktop
#{tde_datadir}/services/tdenetman_pptp.desktop
#{tde_datadir}/services/tdenetman_strongswan.desktop
#{tde_datadir}/services/tdenetman_vpnc.desktop
#{tde_tdedocdir}/HTML/en/tdenetworkmanager/

##########

%package devel
Summary:		Common data shared among the MySQL GUI Suites
Group:			Development/Libraries
Requires:		%{name} = %{EVRD}

%description devel
Development headers for tdenetworkmanager

%files devel
%defattr(-,root,root,-)
%{tde_prefix}/include/tde/*.h
%{tde_prefix}/%{_lib}/trinity/*.la
%{tde_prefix}/%{_lib}/trinity/*.so

##########


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"

