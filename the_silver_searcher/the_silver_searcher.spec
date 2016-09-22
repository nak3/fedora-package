%global commit cda635000a771d20905b4fa07dfc8dfef511c794
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global bashcompdir %(pkg-config --variable=completionsdir bash-completion)
%if "%{bashcompdir}" == ""
%define bashcompdir "/etc/bash_completion.d"
%endif

Name:           the_silver_searcher
Version:        0.32.0
Release:        3%{?dist}
Summary:        Super-fast text searching tool (ag)
Group:          Applications/Text
License:        ASL 2.0 and BSD
URL:            https://github.com/ggreer/the_silver_searcher
Source:         https://github.com/ggreer/the_silver_searcher/archive/%{commit}/%{version}-%{shortcommit}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pcre-devel
%if ! 0%{?el6}
BuildRequires:  pkgconfig(bash-completion)
%endif
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
The Silver Searcher is a code searching tool similar to ack,
with a focus on speed.

%prep
%setup -q -n %{name}-%{commit}

%build
aclocal
autoconf
autoheader
automake --add-missing
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{bashcompdir}
install -pm 0644 ag.bashcomp.sh $RPM_BUILD_ROOT%{bashcompdir}/ag
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}

%files
%{_bindir}/ag
%{_mandir}/man1/ag.1*
%(dirname %{bashcompdir})
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%doc README.md
%license LICENSE
%else
%doc README.md LICENSE
%endif

%changelog
* Thu Sep 22 2016 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.32.0-3
- Fixed bz#1377596

* Thu Jun 30 2016 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.32.0-1
- update to 0.32.0

* Sun Jan 24 2016 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.31.0-2
- Build for RHEL6(EPEL)

* Tue Dec 29 2015 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.31.0-1
- update to 0.31.0

* Thu May 07 2015 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.30.0-1
- update to 0.30.0

* Mon Dec 15 2014 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.27.0-1
- update to 0.27.0

* Mon Nov 03 2014 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.26.0-1
- update to 0.26.0

* Wed Oct 15 2014 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.25.0-1
- update to 0.25.0

* Tue Sep 30 2014 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.24.1-1
- update to 0.24.1

* Sun Jun 22 2014 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.22.0-1
- update to 0.22.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.21.0-1
- update to 0.21.0

* Thu Sep 12 2013 Henrik Hodne <henrik@hodne.io> - 0.16-2
- Initial RPM release
