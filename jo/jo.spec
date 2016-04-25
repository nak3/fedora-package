%global commit 6afdb7f4864b59783b209bd26b7e77aba9b14994
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           jo
Version:        1.0
Release:        1%{?dist}
Summary:        Command-line to create JSON objects
Group:          Applications/Text
License:        GPLv2+
URL:            https://github.com/jpmens/jo
Source:         https://github.com/jpmens/jo/archive/%{commit}/%{version}-%{shortcommit}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake

%description
jo is a small utility to create JSON objects

%prep
%setup -q -n %{name}-%{commit}

%build
autoreconf -i
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}

%files
%{_bindir}/jo
%{_mandir}/man1/jo.1*
%doc jo.md COPYING

%changelog
* Thu Mar 10 2016 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0.8-1
- Initial RPM release
