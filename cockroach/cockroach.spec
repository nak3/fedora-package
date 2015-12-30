%global provider        github
%global provider_tld    com
%global project         cockroachdb
%global repo            cockroach
# https://github.com/cockroachdb/cockroach
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          a7245786e0354754ee7ef3523ca7ce4db3673155
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Version:        0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        !!!!FILL!!!!
License:        !!!!FILL!!!!
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires: gcc-c++
BuildRequires: golang >= 1.5.1
BuildRequires: git

%description
%{summary}

Summary:       %{summary}
BuildArch:     noarch

%prep
%setup -q -n %{repo}-%{commit}

%build
export GOPATH=$(pwd)/_build:%{buildroot}%{gopath}:%{gopath}
export PATH=${GOPATH}/bin:${PATH}

go get -d github.com/cockroachdb/cockroach

#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildTag=%{shell git describe --dirty --tags}"
#export LDFLAGS=$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildTag=%{TAG}
#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildTime=$(shell date -u '+%Y/%m/%d %H:%M:%S')"
#export LDFLAGS="$LDFLAGS -X github.com/cockroachdb/cockroach/util.buildDeps=$(shell GOPATH=${GOPATH} build/depvers.sh)"

#export TAGS="release"
#export GOFLAGS="-a"

go build  $GOFLAGS -i -o cockroach
#go build -tags $TAGS $GOFLAGS -i -o cockroach
#go build -tags $TAGS $GOFLAGS -ldflags $LDFLAGS -i -o cockroach


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
install -pm 0755 cockroach $RPM_BUILD_ROOT%{_bindir}/

%files
%{_bindir}/cockroach
%doc README.md LICENSE

%changelog
* Tue Dec 29 2015 Kenjiro Nakayama <nakayamakenjiro@gmail.com> - 0-0.1.gita724578
- First package for Fedora
