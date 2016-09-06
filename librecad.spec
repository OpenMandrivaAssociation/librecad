# Changes incorporated from Rallaz's spec file, which is
#
# Copyright (c) 2010-2012 Rallaz
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
Name:			librecad
Version:		2.1.1
Release:		1
Summary:		Computer Assisted Design (CAD) Application
License:		GPLv2 and GPLv2+
URL:			http://librecad.org/
Source0:		https://github.com/LibreCAD/LibreCAD/archive/%{version}.tar.gz
Source1:		ttf2lff.1
# GPL licensed parts files
Source2:		Architect8-LCAD.zip
Source3:		Electronic8-LCAD.zip
Patch1:			librecad-desktop.patch
Patch2:			librecad-install.patch
Patch3:			librecad-plugindir.patch
Patch5:			librecad-sys-iota.patch
Patch6:			librecad-gcc6.patch
BuildRequires:		boost-devel
BuildRequires:		fonts-ttf-wqy-microhei
BuildRequires:		qt5-devel
BuildRequires:		pkgconfig(Qt5Svg)
BuildRequires:		muparser-devel

Requires:		%{name}-fonts = %{version}-%{release}
Requires:		%{name}-langs = %{version}-%{release}
Requires:		%{name}-parts = %{version}-%{release}
Requires:		%{name}-patterns = %{version}-%{release}

# Do not check any files in the librecad plugin dir for requires
%global __provides_exclude_from ^(%{_libdir}/%{name}/plugins/.*\\.so)$

%description
A graphical and comprehensive 2D CAD application.

%package devel
Summary:	Development files for LibreCAD
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for LibreCAD.

%package fonts
Summary:	Fonts in LibreCAD (lff) format
License:	GPLv2+ and (ASL 2.0 or GPLv3 with exceptions)
BuildArch:	noarch

%description fonts
Fonts converted to LibreCAD (lff) format.

%package langs
Summary:	Language (qm) files for LibreCAD
BuildArch:	noarch

%description langs 
Language (qm) files for	LibreCAD.

%package parts
Summary:	Parts collection for LibreCAD
BuildArch:	noarch

%description parts
Collection of parts for LibreCAD.

%package patterns
Summary:	Pattern files for LibreCAD
BuildArch:	noarch

%description patterns
Pattern files for LibreCAD.

%prep
%setup -qn LibreCAD-%{version} -a 2 -a 3
%apply_patches
sed -i 's|##LIBDIR##|%{_libdir}|g' librecad/src/lib/engine/rs_system.cpp
sed -i 's|$${DXFRW_INCLUDEDIR}|%{dxfrw_includedir}|g' librecad/src/src.pro

# unset +x flags on some source files
for i in plugins/*/*.cpp plugins/*/*.h librecad/src/plugins/qc_plugininterface.h; do
  chmod -x $i
done

%build
%{qmake_qt5} librecad.pro 'CONFIG+=release' 'BOOST_DIR=/usr' 'BOOST_LIBDIR=%{_libdir}' 'MUPARSER_DIR=/usr' 'QMAKE_LFLAGS_RELEASE=' 'DISABLE_POSTSCRIPT=true'

%make MUPARSER_DIR=/usr
rm -rf unix/resources/fonts/wqy-unicode.lff
mkdir -p unix/resources/fonts
./unix/ttf2lff -L "ASL 2.0 or GPLv3 with exceptions" /usr/share/fonts/TTF/wqy-microhei/wqy-microhei.ttc unix/resources/fonts/wqy-unicode.lff 

%install
export BUILDDIR="%{buildroot}%{_datadir}/%{name}"
sh scripts/postprocess-unix.sh

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins
mv unix/resources/plugins/* %{buildroot}%{_libdir}/%{name}/plugins/
%{__install} -Dpm 755 -s unix/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -Dpm 755 -s unix/ttf2lff %{buildroot}%{_bindir}/ttf2lff
%{__install} -Dpm 644 desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
%{__install} -Dpm 644 unix/appdata/%{name}.appdata.xml  %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
%{__install} -Dpm 644 librecad/res/main/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{__install} -Dpm 644 desktop/%{name}.sharedmimeinfo %{buildroot}%{_datadir}/mime/packages/%{name}.xml
%{__install} -Dpm 644 desktop/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -Dpm 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/ttf2lff.1
%{__install} -Dpm 644 librecad/src/plugins/document_interface.h %{buildroot}%{_includedir}/%{name}/document_interface.h
%{__install} -Dpm 644 librecad/src/plugins/qc_plugininterface.h %{buildroot}%{_includedir}/%{name}/qc_plugininterface.h
mkdir -p %{buildroot}%{_datadir}/%{name}/fonts
cp -a unix/resources/fonts/*.lff %{buildroot}%{_datadir}/%{name}/fonts/
mkdir -p %{buildroot}%{_datadir}/%{name}/qm
cp -a unix/resources/qm/* %{buildroot}%{_datadir}/%{name}/qm/
mkdir -p %{buildroot}%{_datadir}/%{name}/library
cp -a unix/resources/library/* %{buildroot}%{_datadir}/%{name}/library/
mkdir -p %{buildroot}%{_datadir}/%{name}/patterns
cp -a unix/resources/patterns/* %{buildroot}%{_datadir}/%{name}/patterns/

mkdir -p %{buildroot}%{_datadir}/%{name}/library/architecture
cp -a Architect8-LCAD %{buildroot}%{_datadir}/%{name}/library/architecture

mkdir -p %{buildroot}%{_datadir}/%{name}/library/electronics
cp -a Electronic8-LCAD %{buildroot}%{_datadir}/%{name}/library/electronics

#% {_fixperms} %{buildroot}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%files
%doc LICENSE README.md
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/ttf2lff.1*
%{_bindir}/%{name}
%{_bindir}/ttf2lff
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/mime/packages/%{name}.xml
%dir %{_datadir}/%{name}
%{_libdir}/%{name}/

%files devel
%{_includedir}/%{name}/

%files fonts
%doc LICENSE LICENSE_Apache2.txt LICENSE_GPLv3.txt
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/fonts/

%files langs
%doc LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/qm/

%files parts
%doc LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/library/

%files patterns
%doc LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/patterns/

%changelog
* Mon Jun  6 2016 Tom Callaway <spot@fedoraproject.org> - 2.1.0-1
- update to 2.1.0

* Mon May 16 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.10-1
- update to 2.0.10

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 2.0.9-2
- Rebuilt for Boost 1.60

* Tue Jan 12 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.9-1
- update to 2.0.9

* Fri Sep 11 2015 Tom Callaway <spot@fedoraproject.org> - 2.0.8-1
- update to 2.0.8

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 2.0.7-8
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 2.0.7-6
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.7-4
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 2.0.7-3
- Add an AppData file for the software center

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 2.0.7-2
- Rebuild for boost 1.57.0

* Mon Jan  5 2015 Tom Callaway <spot@fedoraproject.org> - 2.0.7-1
- update to 2.0.7

* Wed Nov  5 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.6-1
- update to 2.0.6

* Thu Sep 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.5-2
- add Architect8 and Electronic8 parts libraries

* Mon Aug 18 2014 Richard Shaw <hobbes1069@gmail.com> - 2.0.5-1
- Update to latest upstream release.

* Mon Aug 18 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-4
- update mime scriptlets

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Richard Shaw <hobbes1069@gmail.com> - 2.0.4-1
- Update to latest upstream release.

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 2.0.3-2
- Rebuild for boost 1.55.0

* Fri May  2 2014 Richard Shaw <hobbes1069@gmail.com> - 2.0.3-1
- Update to 2.0.3.

* Wed Jan 22 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Sun Oct 20 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.0-0.6.rc2
- add missing LICENSE files to subpackages
- add dir ownership to subpackages
- readd all mime scriptlets

* Sun Oct 20 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.0-0.5.rc2
- fix mime-type desktop scriptlets
- unbundle shapelib
- do not have provides for unversioned plugins
- fix permissions
- nuke unused code
- make patterns and langs noarch subpackages
- preserve timestamps in install commands
- fix link flags to not have -O1 by overriding 

* Fri Oct 18 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.0-0.4.rc2
- update to rc2

* Tue Apr 30 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.0-0.3.beta5
- add BR: boost-devel
- update to beta5

* Tue Apr  9 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.0-0.2.beta2
- update to beta2

* Sun Feb 24 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.0-0.1.beta1
- initial package
