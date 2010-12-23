Name:           ogmrip
Version:        0.13.6
Release:        1%{?dist}
Summary:        DVD ripping and encoding graphical user interface

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://ogmrip.sourceforge.net/
Source0:        http://downloads.sourceforge.net/ogmrip/ogmrip-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel, libglade2-devel, GConf2-devel, libxml2-devel
BuildRequires:  dbus-glib-devel, enchant-devel, enca-devel
BuildRequires:  libdvdread-devel, libtheora-devel, libvorbis-devel
BuildRequires:  libtiff-devel
BuildRequires:  tesseract-devel
BuildRequires:  libnotify-devel
BuildRequires:  gettext-devel, intltool
BuildRequires:  desktop-file-utils

# Not technically build required, but configure checks for it...
Buildrequires:  mplayer, mencoder, ogmtools, vorbis-tools, theora-tools
BuildRequires:  mkvtoolnix, lame

# Now, all the same as runtime requirements
Requires: mplayer, mencoder, ogmtools, vorbis-tools, theora-tools
Requires: mkvtoolnix, lame
Requires: gpac
Requires: subtitleripper
Requires: tesseract

Requires(post): GConf2
Requires(postun): GConf2

#Patch0: ogmrip-0.13.4-build_fix.patch

%description
OGMRip is an application and a set of libraries for ripping and encoding DVDs
into AVI, OGM MP4 or Matroska files using a wide variety of codecs. It relies
on mplayer, mencoder, ogmtools, mkvtoolnix, oggenc, lame and faac to perform
its tasks.


%package devel
Summary: Development files for ogmrip
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires:  gtk2-devel, libglade2-devel, GConf2-devel, libxml2-devel
Requires:  hal-devel, dbus-glib-devel, enchant-devel, enca-devel
Requires:  libdvdread-devel, libtheora-devel, libvorbis-devel
Requires:  libtiff-devel
Requires:  tesseract-devel
Requires:  libnotify-devel
Requires:  pkgconfig

%description devel
Development headers and libraries for ogmrip.


%prep
%setup -q
#patch0 -p1

%build
%configure \
    --disable-static \
    --disable-schemas-install \
    --with-ocr=tesseract
# Disable RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name}

# Remove useless files
find %{buildroot} -name '*.la' -delete

desktop-file-install \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}/%{_datadir}/applications/ogmrip.desktop


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/ogmrip.schemas &>/dev/null || :

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
        %{_sysconfdir}/gconf/schemas/ogmrip.schemas &>/dev/null || :
fi

%postun -p /sbin/ldconfig



%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_sysconfdir}/gconf/schemas/ogmrip.schemas
%{_bindir}/dvdcpy
%{_bindir}/avibox
%{_bindir}/ogmrip
%{_bindir}/subp2pgm
%{_bindir}/subp2png
%{_bindir}/subp2tiff
%{_bindir}/subptools
%{_bindir}/theoraenc
%{_libdir}/*.so.*
%{_libdir}/ogmrip/
%{_datadir}/applications/ogmrip.desktop
%doc %{_datadir}/gtk-doc/html/ogm*
%{_datadir}/ogmrip/
%{_datadir}/pixmaps/ogmrip.png
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Tue Oct 26 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.13.6-1
- update to 0.13.6

* Fri May 22 2010 Gianluca Sforna <giallu gmail com> - 0.13.5-1
- new upstream release
- drop upstreamed patch

* Mon Mar 22 2010 Gianluca Sforna <giallu gmail com> - 0.13.4-1
- New upstream release
- Add patch to compile against GTK 2.19

* Thu Dec 24 2009 Gianluca Sforna <giallu gmail com> - 0.13.3-1
- New upstream release

* Thu Oct  8 2009 Gianluca Sforna <giallu gmail com> - 0.13.2-1
- New upstream release
- drop dependencies on hal-devel and eject

* Mon Sep 21 2009 Gianluca Sforna <giallu gmail com> - 0.13.1-1
- New upstream release
- drop upstreamed patches

* Fri Aug 14 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-4
- Require tesseract for subtitle extraction

* Sun Jul 19 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-3
- add patch to compile against gtk2-2.17.4

* Fri Jul 17 2009 Gianluca Sforna <giallu gmail com> - 0.13.0-1
- New upstream release
- drop upstreamed patches

* Mon Apr 20 2009 Gianluca Sforna <giallu gmail com> - 0.12.3-3
- Add Requires on -devel
- Find and remove .la files
- Properly install .desktop file

* Mon Feb 16 2009 Gianluca Sforna <giallu gmail com> - 0.12.3-2
- Rebase Patch0

* Mon Feb  9 2009 Gianluca Sforna <giallu gmail com> - 0.12.3-1
- Upstream release 0.12.3

* Sat Dec 13 2008 Gianluca Sforna <giallu gmail com> - 0.12.2-1
- New spec based off freshrpms for Fedora submission
