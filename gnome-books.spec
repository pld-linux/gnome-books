# TODO: obsoletes gnome-documents?
Summary:	E-book manager for GNOME
Summary(pl.UTF-8):	Zarządca e-booków dla GNOME
Name:		gnome-books
Version:	40.0
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-books/40/%{name}-%{version}.tar.xz
# Source0-md5:	8a4e112280421373f3233101bf5cf28e
Patch0:		%{name}-gnome-desktop.patch
Patch1:		%{name}-meson.patch
URL:		https://wiki.gnome.org/Apps/Books
BuildRequires:	evince-devel >= 3.14.0
BuildRequires:	gdk-pixbuf2-devel >= 2.39.1
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gjs-devel >= 1.48.0
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gnome-desktop-devel >= 43
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	gtk+3-devel >= 3.22.15
BuildRequires:	gtk-webkit4-devel >= 2.6.0
BuildRequires:	libgepub-devel >= 0.6
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	tracker3-devel >= 3.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	glib2 >= 1:2.40.0
Requires:	evince >= 3.14.0
Requires:	gdk-pixbuf2 >= 2.39.1
Requires:	gjs >= 1.48.0
Requires:	glib2 >= 1:2.40.0
Requires:	gnome-desktop >= 43
Requires:	gobject-introspection >= 1.32.0
Requires:	gtk+3 >= 3.22.15
Requires:	gtk-webkit4 >= 2.6.0
Requires:	hicolor-icon-theme
Requires:	libgepub >= 0.6
Requires:	tracker3 >= 3.0
Suggests:	unoconv >= 0.5
Conflicts:	gnome-documents < 3.32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Books is an e-book manager application for GNOME.

%description -l pl.UTF-8
Books to aplikacja dla GNOME służąca do zarządzania e-bookami.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

# workaround "data/meson.build:6:0: ERROR: Sandbox violation: Tried to grab file gd-main-view.h from a nested subproject."
cp -p subprojects/libgd/libgd/gd-main-view{,-generic}.h data
%{__sed} -i -e "s!join_paths(libgd_src_path, \('[^']*'\))!\1!" data/meson.build

%build
%meson

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%files -f gnome-books.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/gnome-books
%dir %{_libdir}/gnome-books
%attr(755,root,root) %{_libdir}/gnome-books/libgd.so
%attr(755,root,root) %{_libdir}/gnome-books/libgdprivate-1.0.so
%dir %{_libdir}/gnome-books/girepository-1.0
%{_libdir}/gnome-books/girepository-1.0/Gd-1.0.typelib
%{_libdir}/gnome-books/girepository-1.0/GdPrivate-1.0.typelib
%{_datadir}/dbus-1/services/org.gnome.Books.service
%{_datadir}/glib-2.0/schemas/org.gnome.Books.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.books.gschema.xml
%dir %{_datadir}/gnome-books
%attr(755,root,root) %{_datadir}/gnome-books/org.gnome.Books
%{_datadir}/gnome-books/org.gnome.Books.*.gresource
%dir %{_datadir}/gnome-books/gir-1.0
%{_datadir}/gnome-books/gir-1.0/Gd-1.0.gir
%{_datadir}/gnome-books/gir-1.0/GdPrivate-1.0.gir
%{_datadir}/metainfo/org.gnome.Books.appdata.xml
%{_desktopdir}/org.gnome.Books.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Books.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Books-symbolic.svg
%{_mandir}/man1/gnome-books.1*
