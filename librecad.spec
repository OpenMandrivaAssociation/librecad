%define	name	librecad
%define	version	1.0.2

Summary:	Computer-aided design (CAD) system
Name:		%{name}
Version:	%{version}
Epoch:		1
Release:	1
Source0:	librecad-%{version}.tar.bz2
Patch0:		0001-Adding-DXF-.desktop-file.patch
Patch1:		librecad-1.0.0-mdv-desktop.patch

URL:		http://www.librecad.org
License:	GPLv2
Group:		Graphics
BuildRequires:	qt4-devel
BuildRequires:	qt4-assistant
BuildRequires:	qt4-linguist
BuildRequires:	muparser-devel
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
BuildArch:	noarch
 
%description data
Contains the platform-independent files for LibreCAD, including
fonts, patterns, translations.

#package doc
#Group:		Graphics
#Summary:	Documentation for %{name}
#Requires:	%{name}
#BuildArch:	noarch
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
make install INSTALL_ROOT=%buildroot
 
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/doc
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/fonts
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/library
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/patterns
%{__install} -m 755 -d %{buildroot}%{_datadir}/%{name}/qm
%{__install} -m 755 -d %{buildroot}%{_docdir}/%{name}
%{__install} -m 755 -d %{buildroot}%{_libdir}/%{name}/plugins
%{__install} -m 755 -d %{buildroot}%{_datadir}/mime/packages

#%__cp unix/resources/doc/* %{buildroot}%{_datadir}/%{name}/doc/
cp -a unix/resources/fonts/*.lff %{buildroot}%{_datadir}/%{name}/fonts/
cp -a unix/resources/library/* %{buildroot}%{_datadir}/%{name}/library/
cp -a unix/resources/patterns/*.dxf %{buildroot}%{_datadir}/%{name}/patterns/
cp -a unix/resources/qm/*.qm %{buildroot}%{_datadir}/%{name}/qm/
cp -a unix/resources/plugins/* %{buildroot}%{_libdir}/%{name}/plugins/
%__chmod 644 README
find %{buildroot}%{_datadir}/%{name} -type f -exec chmod 644 {} \;
 
%{__install} -Dm 755 -s unix/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -Dm 644 desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
%{__install} -Dm 644 desktop/%{name}.sharedmimeinfo %{buildroot}%{_datadir}/mime/packages/%{name}.xml
%{__install} -Dm 644 res/main/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%files
%doc README
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


%changelog
* Sun Jun 10 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1:1.0.2-1
+ Revision: 804314
- update to 1.0.2

* Tue Jan 10 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1:1.0.0-1
+ Revision: 759355
- add Epoch: 1
- remove Makefile and spec.in
- remove BuildRoot tag, replace spaces with tabs
- 1.0.0 final release

* Wed Aug 17 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0rc1.99.2-1
+ Revision: 694859
- Updating to latest git snapshot

* Sat Aug 13 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0rc1.99.1-1
+ Revision: 694367
- Adding missing source package for 1.0.0rc1.99.1
- Update to latest snapshot, still pre RC2

* Sat Aug 06 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0rc1.99-1
+ Revision: 693531
- Updating to pre-RC2 snapshot and using new patches capabilities of gitrpm helper
- Using 'mdv' branch for desktop file
- Updating stuff for new gitrpm
- Update for latest rpm-common changes
- Introducing GitRPM funny stuff, see http://git.mandriva.com/projects/?p=users/alissy/gitrpm.git;a=summary

* Thu Jun 23 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0rc1_55_g4f9b7c5-1
+ Revision: 686840
- Updating from 1.0.0beta5 to 1.0.0rc1

* Tue Jun 07 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0beta5_144_g0046d99-1
+ Revision: 683100
- Updating to latest git revision
- Dropping obsolete french locale patch

* Sun Jun 05 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0beta5_132_gf21f8b2-1
+ Revision: 682785
- Updating to latest git tree, and dropping merged patches.

* Thu Jun 02 2011 Alexandre Lissy <alissy@mandriva.com> 1.0.0beta5_116_g88b5983-1
+ Revision: 682483
- Fix missing BuildRequires against qt4-linguist
- Fix missing BuildRequires against qt4-assistant (providing qcollectiongenerator)
- Importing LibreCAD.
- Created package structure for librecad.

