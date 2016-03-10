%global commit 3ba46df36d709641395298c9f178fc510eb23ddb
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           jo
Version:        0.8
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
make

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
