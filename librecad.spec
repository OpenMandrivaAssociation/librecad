%define commit 2241a8102d345f650502d12e3ab54e8387c2721a

Summary:	Computer-aided design (CAD) system
Name:		librecad
Version:	2.0.2
Release:	2
Epoch:		1
License:	GPLv2+
Group:		Graphics
Url:		http://www.librecad.org
Source0:	https://github.com/LibreCAD/LibreCAD/archive/%{commit}/%{name}-%{version}.tar.gz
Patch0:		librecad-1.0.0-mdv-desktop.patch
Patch1:		librecad-2.0.2-install.patch
Patch2:		librecad-2.0.2-plugindir.patch
BuildRequires:	boost-devel
BuildRequires:	qt4-devel
BuildRequires:	qt4-assistant
BuildRequires:	qt4-linguist
BuildRequires:	muparser-devel
Requires:	%{name}-data
Suggests:	%{name}-plugins

%description
LibreCAD is an application for computer aided design (CAD) in two
dimensions (2D). With LibreCAD you can create technical drawings
such as plans for buildings, interiors, mechanical parts or schemas
and diagrams.

%files
%{_bindir}/%{name}
%{_bindir}/ttf2lff
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/%{name}.1*

#----------------------------------------------------------------------------

%package data
Summary:	Platform-independant files for %{name}
Group:		Graphics
Requires:	%{name}
BuildArch:	noarch

%description data
Contains the platform-independent files for LibreCAD, including
fonts, patterns, translations.

%files data
%{_datadir}/%{name}/doc/*
%{_datadir}/%{name}/fonts/*
%{_datadir}/%{name}/library/*
%{_datadir}/%{name}/patterns/*
%{_datadir}/%{name}/qm/*

#----------------------------------------------------------------------------

%package plugins
Summary:	Plugins libraries files for %{name}
Group:		Graphics
Requires:	%{name}

%description plugins
Contains the plugins files for LibreCAD.

%files plugins
%{_libdir}/%{name}/plugins/*

#----------------------------------------------------------------------------

%prep
%setup -q -n LibreCAD-%{commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
find . -type f -executable -a \( -name '*.cpp' -o -name '*.h' \) | xargs -i{} chmod 644 {}

sed -i 's|##LIBDIR##|%{_libdir}|g' librecad/src/lib/engine/rs_system.cpp

%build
%qmake_qt4
%make

%install
export BUILDDIR="%{buildroot}%{_datadir}/%{name}"
sh scripts/postprocess-unix.sh

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins
mv unix/resources/plugins/* %{buildroot}%{_libdir}/%{name}/plugins/
install -Dpm 755 unix/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 755 unix/ttf2lff %{buildroot}%{_bindir}/ttf2lff
install -Dpm 644 desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 librecad/res/main/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -Dpm 644 desktop/%{name}.sharedmimeinfo %{buildroot}%{_datadir}/mime/packages/%{name}.xml
install -Dpm 644 desktop/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

