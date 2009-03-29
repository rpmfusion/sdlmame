%define beta 0130u2

%if "0%{?beta}" != "0"
%define _version %{?beta}
%else
%define _version %{version}
%endif

%ifarch x86_64
%define arch_flags PTR64=1
%endif
%ifarch ppc
%define arch_flags BIGENDIAN=1
%endif
%ifarch ppc64
%define arch_flags BIGENDIAN=1 PTR64=1
%endif

Name:           sdlmame
Version:        0131
Release:        0.3.%{?beta}%{?dist}
Summary:        SDL Multiple Arcade Machine Emulator

Group:          Applications/Emulators
License:        MAME License
URL:            http://rbelmont.mameworld.info/?page_id=163
Source0:        http://rbelmont.mameworld.info/%{name}%{_version}.zip
#ui.bdc generated from ui.bdf
Source1:        ui.bdc
Patch0:         %{name}-warnings.patch
Patch1:         %{name}-expat.patch
Patch3:         %{name}-fortify.patch
BuildRoot:      %{_tmppath}/%{name}-%{_version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  SDL-devel expat-devel zlib-devel libGL-devel gtk2-devel
BuildRequires:  GConf2-devel
%if 0%{?fedora} == 10
BuildRequires:  dbus-devel
%endif

%description
MAME stands for Multiple Arcade Machine Emulator.  When used in conjunction
with an arcade game's data files (ROMs), MAME will more or less faithfully
reproduce that game on a PC.

The ROM images that MAME utilizes are "dumped" from arcade games' original
circuit-board ROM chips.  MAME becomes the "hardware" for the games, taking
the place of their original CPUs and support chips.  Therefore, these games
are NOT simulations, but the actual, original games that appeared in arcades.

MAME's purpose is to preserve these decades of video-game history.  As gaming
technology continues to rush forward, MAME prevents these important "vintage"
games from being lost and forgotten.  This is achieved by documenting the
hardware and how it functions, thanks to the talent of programmers from the
MAME team and from other contributors.  Being able to play the games is just
a nice side-effect, which doesn't happen all the time.  MAME strives for
emulating the games faithfully.

%package tools
Summary:        Tools used for the sdlmame package
Group:          Applications/Emulators
Requires:       %{name} = %{version}-%{release}

%description tools
%{summary}.

%package debug
Summary:        Debug enabled version of sdlmame
Group:          Applications/Emulators

%description debug
%{summary}.

%package ldplayer
Summary:        Standalone laserdisc player based on sdlmame
Group:          Applications/Emulators

%description ldplayer
%{summary}.


%prep
%setup -qn %{name}%{_version}
%patch0 -p0 -b .warnings~
%patch1 -p0 -b .expat~
%patch3 -p0 -b .fortify

# Create mame.ini file
cat > mame.ini << EOF
# Define multi-user paths
artpath            %{_datadir}/mame/artwork;%{_datadir}/mame/effects
ctrlrpath          %{_datadir}/mame/ctrlr
fontpath           %{_datadir}/mame/fonts
rompath            %{_datadir}/mame/roms;%{_datadir}/mame/chds
samplepath         %{_datadir}/mame/samples
cheatpath          %{_datadir}/mame/cheats

# Allow user to override ini settings
inipath            \$HOME/.mame/ini;%{_sysconfdir}/mame

# Set paths for local storage
cfg_directory      \$HOME/.mame/cfg
comment_directory  \$HOME/.mame/comments
diff_directory     \$HOME/.mame/diff
input_directory    \$HOME/.mame/inp
memcard_directory  \$HOME/.mame/memcard
nvram_directory    \$HOME/.mame/nvram
snapshot_directory \$HOME/.mame/snap
state_directory    \$HOME/.mame/sta

# Fedora custom defaults
video              opengl
autosave           1
joystick           1
EOF

# Fix end-of-line encoding
sed -i 's/\r//' whatsnew.txt

#Fix whatsnew.txt encoding
/usr/bin/iconv -f iso8859-1 -t utf-8 whatsnew.txt > whatsnew.txt.conv
/bin/mv -f whatsnew.txt.conv whatsnew.txt

#Fix newvideo.txt encoding
pushd docs
/usr/bin/iconv -f cp1250 -t utf-8 newvideo.txt > newvideo.txt.conv
/bin/mv -f newvideo.txt.conv newvideo.txt
popd


%build
make %{?_smp_mflags} %{?arch_flags} TARGET=ldplayer SYMBOLS=1 OPTIMIZE=2\
    OPT_FLAGS='%{optflags} -DINI_PATH="\"%{_sysconfdir}/mame;\""'
make %{?_smp_mflags} %{?arch_flags} DEBUG=1 SYMBOLS=1 OPTIMIZE=2\
    OPT_FLAGS='%{optflags} -DINI_PATH="\"%{_sysconfdir}/mame;\""'
make %{?_smp_mflags} %{?arch_flags} SYMBOLS=1 OPTIMIZE=2\
    OPT_FLAGS='%{optflags} -DINI_PATH="\"%{_sysconfdir}/mame;\""'


%install
rm -rf %{buildroot}

# create directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/mame/artwork
install -d %{buildroot}%{_datadir}/mame/chds
install -d %{buildroot}%{_datadir}/mame/ctrlr
install -d %{buildroot}%{_datadir}/mame/effects
install -d %{buildroot}%{_datadir}/mame/fonts
install -d %{buildroot}%{_datadir}/mame/keymaps
install -d %{buildroot}%{_datadir}/mame/roms
install -d %{buildroot}%{_datadir}/mame/samples
install -d %{buildroot}%{_datadir}/mame/cheats
install -d %{buildroot}%{_sysconfdir}/mame
install -d %{buildroot}%{_sysconfdir}/skel/.mame/cfg
install -d %{buildroot}%{_sysconfdir}/skel/.mame/comments
install -d %{buildroot}%{_sysconfdir}/skel/.mame/diff
install -d %{buildroot}%{_sysconfdir}/skel/.mame/ini
install -d %{buildroot}%{_sysconfdir}/skel/.mame/inp
install -d %{buildroot}%{_sysconfdir}/skel/.mame/memcard
install -d %{buildroot}%{_sysconfdir}/skel/.mame/nvram
install -d %{buildroot}%{_sysconfdir}/skel/.mame/snap
install -d %{buildroot}%{_sysconfdir}/skel/.mame/sta

# install binaries and config files
install -pm 644 mame.ini %{buildroot}%{_sysconfdir}/mame
install -pm 644 keymaps/* %{buildroot}%{_datadir}/mame/keymaps
install -pm 644 ui.bdf %{SOURCE1} %{buildroot}%{_datadir}/mame/fonts
install -pm 755 chdman jedutil ldplayer ldresample ldverify mame mamed romcmp \
    testkeys %{buildroot}%{_bindir}
for tool in regrep runtest src2html srcclean
do
install -pm 755 $tool %{buildroot}%{_bindir}/mame-$tool
done


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc whatsnew*.txt SDLMAME.txt docs/*
%config(noreplace) %{_sysconfdir}/mame/mame.ini
%dir %{_sysconfdir}/mame
%{_bindir}/mame
%{_datadir}/mame
%{_sysconfdir}/skel/.mame

%files tools
%defattr(-,root,root,-)
%doc docs/license.txt
%{_bindir}/chdman
%{_bindir}/jedutil
%{_bindir}/ldresample
%{_bindir}/ldverify
%{_bindir}/mame-regrep
%{_bindir}/romcmp
%{_bindir}/mame-runtest
%{_bindir}/mame-src2html
%{_bindir}/mame-srcclean
%{_bindir}/testkeys

%files debug
%defattr(-,root,root,-)
%doc docs/license.txt
%{_bindir}/mamed

%files ldplayer
%defattr(-,root,root,-)
%doc docs/license.txt
%{_bindir}/ldplayer


%changelog
* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0131-0.3.0130u2
- rebuild for new F11 features

* Sun Mar 29 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0131-0.2.0130u2
- Updated to 0.130u2

* Tue Mar 19 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0131-0.1.0130u1
- Updated to 0.130u1
- Conditionalised the Fedora 10 pkgconfig fix
- Dropped the upstreamed bne patch

* Mon Mar 09 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-1
- Updated to 0.130

* Thu Mar 05 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-0.6.0129u6
- Updated to 0.129u6
- Dropped the upstreamed gcc-4.4 fix
- Updated the warnings patch

* Thu Feb 26 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-0.5.0129u5
- Updated to 0.129u5
- Use macros consistently
- Fixed whatsnew.txt encoding

* Tue Feb 17 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-0.4.0129u4
- Updated to 0.129u4
- Fixed building with gcc-4.4

* Fri Jan 30 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-0.3.0129u3
- Updated to 0.129u3

* Thu Jan 22 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-0.2.0129u2
- Updated to 0.129u2
- Removed the upstreamed ppc patch

* Thu Jan 15 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0130-0.1.0129u1
- Updated to 0.129u1

* Mon Jan  5 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-1
- Updated to 0.129
- Re-enabled ldplayer
- Added OPTIMIZE=2 to all builds since makefile seems to override OPT_FLAGS
- Install ui.bdf and pre-generated ui.bdc to %%{_datadir}/mame/fonts

* Mon Dec 22 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.7.0128u7
- Updated to 0.128u7
- Enabled symbols in all builds
- Added mame prefix to ambiguously named tools
- Added ldresample tool
- Disabled ldplayer temporarily

* Mon Dec 15 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.6.0128u6
- Updated to 0.128u6

* Sun Dec  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.5.0128u5
- Updated to 0.128u5

* Mon Nov 24 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.4.0128u4
- Updated to 0.128u4

* Mon Nov 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.3.0128u3
- Updated to 0.128u3
- Fixed typo in %%changelog

* Sun Nov  2 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.2.0128u2
- Updated to 0.128u2
- Added patch disabling undefining _FORTIFY_SOURCE

* Fri Oct 24 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0129-0.1.0128u1
- Updated to 0.128u1

* Thu Oct 16 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-1
- Updated to 0.128

* Mon Oct 13 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.8.0127u8
- Updated to 0.127u8

* Thu Oct  9 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.7.0127u7
- Updated to 0.127u7

* Fri Oct  3 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.6.0127u6
- Updated to 0.127u6

* Sun Sep 28 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.5.0127u5
- Updated to 0.127u5

* Fri Sep 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.4.0127u4
- Updated to 0.127u4
- The -debug subpackage no longer depends on -debuginfo

* Fri Sep 12 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.3.0127u3
- Updated to 0.127u3

* Sun Sep  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.2.0127u2
- Updated to 0.127u2

* Sat Aug 30 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0128-0.1.0127u1
- Updated to 0.127u1
- Dropped cheat_file and added cheatpath to the default ini
- Added -ldplayer subpackage containing the standalone laserdisc player

* Tue Aug 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0127-1
- Updated to 0.127

* Sun Aug 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0127-0.5.0126u5
- Updated to 0.126u5

* Thu Aug  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0127-0.4.0126u4
- Updated to 0.126u4
- Added ldverify, dropped makemeta

* Thu Jul 31 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0127-0.3.0126u3
- Updated to 0.126u3

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0127-0.2.0126u1
- rebuild for buildsys cflags issue

* Thu Jul 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0127-0.1.0126u1
- Updated to 0.126u1

* Mon Jul 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-3
- Patched bne-- inline assembly to allow ppc64 build

* Mon Jul 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-2
- Added ppc64 arch_flags

* Mon Jul  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-1
- Updated to 0.126

* Fri Jun 27 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.7.0125u8
- Updated to 0.125u8
- Dropped DEBUGGER=1, it is default now

* Wed Jun 18 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.6.0125u6
- Updated to 0.125u6

* Thu Jun 12 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.5.0125u5
- Updated to 0.125u5
- Finally dropped listxml segfault patch

* Fri May 30 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.4.0125u4
- Updated to 0.125u4
- Patched segfault upon -lx once again

* Fri May 30 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.3.0125u3
- Updated to 0.125u3
- Patched bug #01840

* Thu May 22 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.2.0125u2
- Updated to 0.125u2

* Fri May 16 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0126-0.1.0125u1
- Updated to 0.125u1
- Dropped %%{?dist} from %%changelog
- Added hyphen before version number in %%changelog

* Sat May 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0125-1
- Updated to 0.125

* Fri Apr 18 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0125-0.3.0124u3
- Updated to 0.124u3

* Sat Apr 12 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0125-0.2.0124u2
- Updated to 0.124u2

* Thu Apr  3 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0125-0.1.0124u1
- Updated to 0.124u1

* Wed Mar 26 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-1
- Updated to 0.124
- Fixed newvideo.txt encoding

* Wed Mar 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-0.6.0123u6
- Updated to 0.123u6

* Fri Mar 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-0.5.0123u5
- Updated to 0.123u5

* Fri Mar  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-0.4.0123u4
- Updated to 0.123u4

* Tue Feb 28 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-0.3.0123u3
- Updated to 0.123u3

* Sat Feb 23 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-0.2.0123u2
- Updated to 0.123u2
- Changed the inipath to %%{_sysconfdir}/mame;\$HOME/.mame/ini
- Updated the warnings patch
- Dropped upstreamed patches

* Thu Feb 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0124-0.1.0123u1
- Updated to 0.123u1
- Patched src/build/build.mak to fix png2bdc linking failure

* Tue Feb  5 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-1
- Updated to 0.123
- Added DEBUGGER=1 to -debug subpackage build command
- Patched src/osd/sdl/sdl.mak to remove invalid rpath

* Sat Jan 26 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-0.6.0122u7
- Updated to 0.122u7

* Fri Jan 18 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-0.5.0122u6
- Updated to 0.122u6

* Sat Jan 12 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-0.4.0122u5
- Updated to 0.122u5

* Thu Jan 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-0.3.0122u4
- Updated to 0.122u4

* Thu Jan  3 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-0.2.0122u3
- Updated to 0.122u3

* Tue Jan  1 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0123-0.1.0122u2
- Updated to 0.122u2

* Tue Dec 18 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-1
- Updated to 0.122

* Thu Dec 13 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-0.4.0121u4
- Updated to 0.121u4

* Fri Dec  7 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-0.3.0121u3
- Updated to 0.121u3
- Reintroduced patch disabling -Werror

* Fri Nov 30 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-0.2.0121u2
- Updated to 0.121u2

* Mon Nov 26 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0122-0.1.0121u1
- Updated to 0.121u1

* Mon Nov 19 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0121-1
- Updated to 0.121

* Thu Nov 15 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0121-0.4.0120u4
- Updated to 0.120u4

* Fri Nov  9 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0121-0.3.0120u3
- Updated to 0.120u3

* Sat Nov  3 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0121-0.2.0120u2
- Updated to 0.120u2

* Thu Oct 25 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0121-0.1.0120u1
- Updated to 0.120u1
- Dropped warnings patch

* Mon Oct 15 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120a-1
- Updated to 0.120a

* Mon Oct 15 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120-1
- Updated to 0.120

* Sat Oct 13 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120-0.4.0119u4
- Updated to 0.119u4

* Sat Oct  6 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120-0.3.0119u3
- Updated to 0.119u3
- Killed the ppc ExcludeArch, since the build error seems to be gone
- Dropped the verbose build patch

* Sun Sep 30 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120-0.2.0119u2
- Updated to 0.119u2

* Tue Sep 25 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0120-0.1.0119u1
- Updated to 0.119u1
- Hopefully fixed the PPC build

* Fri Sep 14 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0119-1
- Updated to 0.119
- ExcludeArch: ppc for stable releases until the build errors get fixed

* Sat Sep  8 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0119-0.2.0118u5
- Updated to 0.118u5

* Sun Sep  2 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0118-2
- Patch the makefile to make the build verbose

* Fri Aug 31 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0118-1
- Updated to 0.118

* Thu Aug 02 2007 XulChris <tkmame@retrogames.com> - 0118-0.2.0117u3
- Upstream sync

* Thu Jul 26 2007 XulChris <tkmame@retrogames.com> - 0118-0.1.0117u2
- Upstream sync
- Remove no longer needed rtdsc patch
- Add patch to use external expat and zlib libraries

* Tue Jul 24 2007 XulChris <tkmame@retrogames.com> - 0117-1
- Upstream sync
- Add patch to remove rtdsc code to hopefully fix PPC builds

* Thu Jul 05 2007 XulChris <tkmame@retrogames.com> - 0117-0.5.0116u4
- Upstream sync
- Apply warnings patch

* Thu Jun 28 2007 XulChris <tkmame@retrogames.com> - 0117-0.4.0116u3
- Upstream Sync
- Remove no longer needed CPS3 and Makefile patches
- Remove PM= from make line

* Thu Jun 21 2007 XulChris <tkmame@retrogames.com> - 0117-0.3.0116u2a
- Upstream sync
- Remove no longer needed CFLAGS patch
- Add patch to remove -Werror from makefile
- Add cps3 patch

* Thu Jun 21 2007 XulChris <tkmame@retrogames.com> - 0117-0.2.0116u2
- Upstream sync
- Add patch to re-add OPT_FLAGS to CFLAGS

* Thu Jun 21 2007 XulChris <tkmame@retrogames.com> - 0117-0.1.0116u1
- Upstream sync

* Thu Jun 21 2007 XulChris <tkmame@retrogames.com> - 0116-1
- Upstream sync

* Thu Jun 07 2007 XulChris <tkmame@retrogames.com> - 0116-0.4.0115u4
- Upstream sync

* Sun Jun 03 2007 XulChris <tkmame@retrogames.com> - 0116-0.3.0115u3
- Upstream sync

* Wed May 23 2007 XulChris <tkmame@retrogames.com> - 0116-0.2.0115u2
- Upstream sync

* Sat May 19 2007 XulChris <tkmame@retrogames.com> - 0116-0.1.0115u1
- Upstream sync

* Sun May 06 2007 XulChris <tkmame@retrogames.com> - 0115-1
- Upstream sync

* Sat May 05 2007 XulChris <tkmame@retrogames.com> - 0115-0.3.0114u4
- Upstream sync

* Fri Apr 27 2007 XulChris <tkmame@retrogames.com> - 0115-0.2.0114u3
- Upstream sync

* Sun Apr 22 2007 XulChris <tkmame@retrogames.com> - 0115-0.1.0114u2
- Upstream sync

* Mon Apr 02 2007 XulChris <tkmame@retrogames.com> - 0114-1
- Upstream sync

* Fri Mar 30 2007 XulChris <tkmame@retrogames.com> - 0114-0.4.0113u4
- Upstream sync

* Thu Mar 22 2007 XulChris <tkmame@retrogames.com> - 0114-0.3.0113u3
- Upstream sync

* Thu Mar 15 2007 XulChris <tkmame@retrogames.com> - 0114-0.2.0113u2
- Upstream sync
- Add srcclean to tools
- Remove volume patch

* Fri Mar 09 2007 XulChris <tkmame@retrogames.com> - 0114-0.1.0113u1
- Upstream sync
- Remove no longer needed patches
- Add regrep and runtest to tools package

* Tue Mar 06 2007 XulChris <tkmame@retrogames.com> - 0113-1
- Upstream sync
- Install makemeta and testkeys
- No longer install file2str
- Add makemeta and testkeys to tools subpackage
- Add keymap directory for keymap files
- Add effects directory for effect files
- Add chds directory for chd files
- More correct fix for SDL on FC5 patch
- Add patch to fix volume option
- Add patch to fix deco32 CRC

* Thu Mar 01 2007 XulChris <tkmame@retrogames.com> - 0113-0.4.0112u4
- Upstream sync
- Remove no longer needed sound latency patch
- Remove no longer needed PREFIX=sdl change
- Restore autosave in ini file
- Add patch for old versions of SDL

* Mon Feb 26 2007 XulChris <tkmame@retrogames.com> - 0113-0.3.0112u3
- Upstream sync
- Add patch to fix sound latency
- Set PREFIX=sdl for non-debug build
- Comment autosave in ini file as it breaks mame in this release

* Sun Feb 18 2007 XulChris <tkmame@retrogames.com> - 0113-0.2.0112u2
- Upstream sync
- Enable autosave and joystick support by default

* Mon Feb 12 2007 XulChris <tkmame@retrogames.com> - 0113-0.1.0112u1
- Upstream sync
- Add dist tags to %%changelog
- Move creation of ini file to %%prep

* Mon Feb 05 2007 XulChris <tkmame@retrogames.com> - 0112-1
- Upstream sync

* Mon Jan 29 2007 XulChris <tkmame@retrogames.com> - 0112-0.6.0111u6
- Upstream sync
- Add %%{?_smp_mflags} to make

* Fri Jan 26 2007 XulChris <tkmame@retrogames.com> - 0112-0.5.0111u5
- Upstream sync
- Remove no longer needed optflags patch
- Remove no longer needed ppc patch

* Thu Jan 18 2007 XulChris <tkmame@retrogames.com> - 0112-0.4.0111u4
- Upstream sync
- Add OPT_FLAGS patch

* Fri Jan 12 2007 XulChris <tkmame@retrogames.com> - 0112-0.3.0111u3
- Upstream sync
- Remove no longer needed CPS2 patch

* Fri Jan 05 2007 XulChris <tkmame@retrogames.com> - 0112-0.2.0111u2
- Upstream sync

* Thu Jan 04 2007 XulChris <tkmame@retrogames.com> - 0112-0.1.0111u1
- Upstream sync

* Mon Dec 11 2006 XulChris <tkmame@retrogames.com> - 0111-1
- Upstream sync

* Sun Dec 10 2006 XulChris <tkmame@retrogames.com> - 0111-0.6.0110u5
- Upstream sync
- Remove no longer needed ini path patch
- Unset USE_DECRYPTION_CHD_IF_PRESENT for cps2 games

* Fri Dec 01 2006 XulChris <tkmame@retrogames.com> - 0111-0.5.0110u4
- Upstream sync

* Wed Nov 29 2006 XulChris <tkmame@retrogames.com> - 0111-0.4.0110u3
- Change config patch to set inipath from command line
- Add inipath to $HOME/.mame to allow for user overrides

* Tue Nov 28 2006 XulChris <tkmame@retrogames.com> - 0111-0.3.0110u3
- Fix $HOME in mame.ini file
- Add %%{_datadir} directories to main package
- No longer require roms subpackage
- Move roms to sdlmame-data package

* Tue Nov 28 2006 XulChris <tkmame@retrogames.com> - 0111-0.2.0110u3
- Upstream sync
- Only compile with symbols on DEBUG build
- Add patch to remove mlong-branch gcc option on ppc
- Modify config patch to only change ini path
- Create ini %%config file that defines directory paths
- Add local mame directories to %%{_sysconfdir}/skel
- Remove unnecessary warnings patch
- Add fonts dir to %%{_datadir}/mame

* Sun Nov 19 2006 XulChris <tkmame@retrogames.com> - 0111-0.1.0110u2
- Upstream sync
- Update URL tag

* Sun Oct 01 2006 XulChris <tkmame@retrogames.com> - 0109-2
- Add new version of scale2x patch that uses SDLMAME_UNSUPPORTED

* Sat Sep 30 2006 XulChris <tkmame@retrogames.com> - 0109-1
- Upstream sync
- Remove unneeded generic patch
- Add PM= because RB refuses to make a generic makefile
- Only include beta whatsnew in %%doc if %%beta is set

* Sun Sep 24 2006 XulChris <tkmame@retrogames.com> - 0109-0.4.0108u5
- Upstream sync

* Wed Sep 20 2006 XulChris <tkmame@retrogames.com> - 0109-0.3.0108u4
- Add licenses to %%doc of %%files roms
- Remove license URLs from %%description roms
- Use %%{_version} in whatsnew file specification
- Remove unnecessary %%{arch_flags} for i386 builds
- security patch is more "correct"
- update scale2x patch
- use latest sdlSep18 overlay patch

* Mon Sep 18 2006 XulChris <tkmame@retrogames.com> - 0109-0.2.0108u4
- 0.108u4 + debug source overrides
- generic patch is more "correct"
- Add roms subpackage
- Add Hans de Goede's scale2x and keyboard LED patches
- Add whatsnew to %%doc
- Add multi-user defaults to config

* Sun Sep 10 2006 XulChris <tkmame@retrogames.com> - 0109-0.1.0108u3
- Initial release for Fedora
