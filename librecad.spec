%define	name	librecad
%define	version	1.0.0

Summary: 	Computer-aided design (CAD) system
Name: 		%{name}
Version: 	%{version}
Release: 	1
Source0:	librecad-%{version}.tar.bz2
Patch0:		0001-Adding-DXF-.desktop-file.patch
Patch1:		librecad-1.0.0-mdv-desktop.patch

URL: 		http://www.librecad.org
License: 	GPLv2
Group: 		Graphics
BuildRequires: 	qt4-devel
BuildRequires:	qt4-assistant
BuildRequires:	qt4-linguist
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Requires:	librecad-data
Suggests:	librecad-doc
Suggests:	librecad-plugins

%description
LibreCAD is an application for computer aided design (CAD) in two
dimensions (2D). With LibreCAD you can create technical drawings
such as plans for buildings, interiors, mechanical parts or schemas
and diagrams. 

%package data
Group:		Graphics
Summary:	Platform-independant files for %{name}
Requires:	%{name}
BuildArch:      noarch
 
%description data
Contains the platform-independent files for LibreCAD, including
fonts, patterns, translations.

#package doc
#Group:		Graphics
#Summary:	Documentation for %{name}
#Requires:	%{name}
#BuildArch:      noarch
# 
#description doc
#Documentation for %{name}, a Qt4 application to design 2D CAD
#drawing based on the community edition of QCad.

%package plugins
Group:		Graphics
Summary:	Plugins libraries files for %{name}
Requires:	%{name}
 
%description plugins
Contains the plugins files for LibreCAD.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
find . -type f -executable -a \( -name '*.cpp' -o -name '*.h' \) | xargs -i{} chmod 644 {}

%build
%qmake_qt4
%make

pushd plugins
	%qmake_qt4
	%make
popd

%install
%makeinstall INSTALL_ROOT=%buildroot
 
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/doc
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/fonts
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/library
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/patterns
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/qm
%{__install} -m 755 -d %{buildroot}%{_docdir}/%{name}
%{__install} -m 755 -d %{buildroot}%{_libdir}/%{name}/plugins
%{__install} -m 755 -d %{buildroot}%{_datadir}/mime/packages

#%__cp unix/resources/doc/* %{buildroot}%{_datadir}/%{name}/doc/
%__cp unix/resources/fonts/*.lff %{buildroot}%{_datadir}/%{name}/fonts/
%__cp -r unix/resources/library/* %{buildroot}%{_datadir}/%{name}/library/
%__cp unix/resources/patterns/*.dxf %{buildroot}%{_datadir}/%{name}/patterns/
%__cp unix/resources/qm/*.qm %{buildroot}%{_datadir}/%{name}/qm/
%__cp unix/resources/plugins/* %{buildroot}%{_libdir}/%{name}/plugins/
%__mv gpl-2.0.txt LICENSE
%__chmod 644 LICENSE
%__chmod 644 README
find %{buildroot}%{_datadir}/%{name} -type f -exec chmod 644 {} \;
 
%{__install} -Dm 755 -s unix/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -Dm 644 desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
%{__install} -Dm 644 desktop/%{name}.sharedmimeinfo %{buildroot}%{_datadir}/mime/packages/%{name}.xml
%{__install} -Dm 644 res/main/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
%doc LICENSE README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/mime/packages/%{name}.xml

%files data
%{_datadir}/%{name}/fonts/*
%{_datadir}/%{name}/library/*
%{_datadir}/%{name}/patterns/*
%{_datadir}/%{name}/qm/*

#files doc
#%{_datadir}/%{name}/doc/*

%files plugins
%{_libdir}/%{name}/plugins/*
