%global qt_module qtquickcontrols2

%define docs 1

Name:    qt5-%{qt_module}
Summary: Qt5 - module with set of QtQuick controls for embedded
Version: 5.9.2
Release: 1%{?dist}
License: GPLv2+ or LGPLv3 and GFDL
Url:     http://www.qt.io
Source0: https://download.qt.io/official_releases/qt/5.9/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

# filter qml provides
%global __provides_exclude_from ^%{_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: qt5-qtbase-devel >= %{version}
BuildRequires: qt5-qtdeclarative-devel

Requires: qt5-qtdeclarative%{?_isa} >= %{version}
Requires: qt5-qtgraphicaleffects%{_isa} >= %{version}

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
Requires: %{name} = %{version}-%{release}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
%description doc
%{summary}.
%endif

%description
The Qt Labs Controls module provides a set of controls that can be used to
build complete interfaces in Qt Quick.

Unlike Qt Quick Controls, these controls are optimized for embedded systems
and so are preferred for hardware with limited resources.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
Requires: qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:        Examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}


%build
%{qmake_qt5}

make %{?_smp_mflags}

%if 0%{?docs}
# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt-project.org/browse/QTBUG-42071
QT_HASH_SEED=0; export QT_HASH_SEED
make %{?_smp_mflags} docs
%endif

%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# Remove .la leftovers
rm -f %{buildroot}%{_qt5_libdir}/libQt5*.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.LGPLv3 LICENSE.GPLv3
%{_qt5_libdir}/libQt5QuickTemplates2.so.5*
%{_qt5_libdir}/libQt5QuickControls2.so.5*
%{_qt5_qmldir}/Qt/labs/calendar
%{_qt5_qmldir}/Qt/labs/platform
%{_qt5_archdatadir}/qml/QtQuick/Controls.2/
%{_qt5_archdatadir}/qml/QtQuick/Templates.2/

%if 0%{?docs}
%files doc
%doc LICENSE.FDL
%{_qt5_docdir}/qtlabscalendar.qch
%{_qt5_docdir}/qtlabscalendar/
%{_qt5_docdir}/qtlabsplatform.qch
%{_qt5_docdir}/qtlabsplatform/
%{_qt5_docdir}/qtquickcontrols2.qch
%{_qt5_docdir}/qtquickcontrols2/
%endif

%files examples
%{_qt5_examplesdir}/quickcontrols2/

%files devel
%{_qt5_headerdir}/
%{_qt5_libdir}/pkgconfig/*.pc
%{_qt5_libdir}/libQt5QuickTemplates2.so
%{_qt5_libdir}/libQt5QuickControls2.so
%{_qt5_libdir}/libQt5QuickTemplates2.prl
%{_qt5_libdir}/libQt5QuickControls2.prl
%{_qt5_libdir}/qt5/mkspecs/modules/*
%{_libdir}/cmake/Qt5QuickControls2/


%changelog
* Fri Oct 06 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- Update to 5.9.2
  Resolves: bz#1482807

* Thu Sep 21 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.1-1
- 5.9.1 - initial RHEL release
  Resolves: bz#1482807

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop shadow/out-of-tree builds (#1456211,QTBUG-37417)

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Tue May 09 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Mon Jan 30 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- New upstream version

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-3
- filter qml provides

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- 5.7.1 dec5 snapshot
- tighten deps

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-0.1
- Prepare 5.7.0

* Sat Jun 11 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.6.1-2
- Add qt5-qtgraphicaleffects dependency

* Thu Jun 09 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1

* Sun Apr 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-4
- BR: qt5-qtbase-private-devel qt5-qtdeclarative-private-devel

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org>
- 5.6.0 final release

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.4.rc
- Update to final RC

* Thu Feb 18 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.6.0-0.3.rc
- Update to rc

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.2.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com> - 5.6.0-0.1.beta
- Initial packaging
