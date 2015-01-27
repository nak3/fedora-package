Name:             apt-cacher-ng
Version:          0.8.0
Release:          1%{?dist}
Summary:          Caching proxy for package files from Debian
Group:            Applications/Internet

License:          BSD and zlib
URL:              http://www.unix-ag.uni-kl.de/~bloch/acng/
Source0:          http://ftp.debian.org/debian/pool/main/a/apt-cacher-ng/%{name}_%{version}.orig.tar.xz
Source1:          http://ftp.debian.org/debian/pool/main/a/apt-cacher-ng/%{name}_%{version}-1.debian.tar.xz
Source2:          apt-cacher-ng.service

Provides:         bundled(sha1-hollerbach)
Provides:         bundled(md5-deutsch-c++)

BuildRequires:    zlib-devel
BuildRequires:    bzip2-devel
BuildRequires:    xz-devel
BuildRequires:    fuse-devel
BuildRequires:    tcp_wrappers-devel
BuildRequires:    cmake
BuildRequires:    openssl-devel
BuildRequires:    boost-devel
BuildRequires:    systemd

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

Requires:         crontabs
Requires:         logrotate

%description
A caching proxy. Specialized for package files from Linux distributors,
primarily for Debian (and Debian based) distributions.

%prep
%setup -q
tar xfvJ %{SOURCE1}
# Replace all instances of /usr/lib/apt-cacher-ng/ with /usr/libexec/apt-cacher-ng/
find . -name "*" -exec sed -i "s#/usr/lib/apt-cacher-ng#/usr/libexec/apt-cacher-ng#g" '{}' \;

%build
mkdir build && cd build && %cmake ..
make %{?_smp_mflags}

%install

# Install adapted from debian/rules
mkdir -p $RPM_BUILD_ROOT%{_sbindir}/
install -pm 0755 build/apt-cacher-ng $RPM_BUILD_ROOT%{_sbindir}/
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/apt-cacher-ng/
install -pm 0755 build/in.acng scripts/expire-caller.pl scripts/urlencode-fixer.pl scripts/distkill.pl $RPM_BUILD_ROOT%{_libexecdir}/apt-cacher-ng/
# optional
cp build/acngfs $RPM_BUILD_ROOT%{_libexecdir}/apt-cacher-ng/
cp -a conf/{*mirror*,*.html,*.css} $RPM_BUILD_ROOT%{_libexecdir}/apt-cacher-ng/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apt-cacher-ng/
cp -a conf/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/apt-cacher-ng/
cd $RPM_BUILD_ROOT%{_sysconfdir}/apt-cacher-ng
cp -s ../../%{_libexecdir}/apt-cacher-ng/{*mirror*,*.html,*.css} .
cd -
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/apt-cacher-ng/
ln -sf ../../%{_sharedstatedir}/apt-cacher-ng/backends_debian.default $RPM_BUILD_ROOT%{_sysconfdir}/apt-cacher-ng/backends_debian.default
ln -sf ../../%{_sharedstatedir}/apt-cacher-ng/backends_ubuntu.default $RPM_BUILD_ROOT%{_sysconfdir}/apt-cacher-ng//backends_ubuntu.default

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -D -pm 0750 debian/apt-cacher-ng.cron.daily $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/apt-cacher-ng

install -D -pm 0644 debian/apt-cacher-ng.default    $RPM_BUILD_ROOT%{_sysconfdir}/default/apt-cacher-ng

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -D -pm 0644 debian/apt-cacher-ng.logrotate  $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/apt-cacher-ng

## systemd.service instead of init.d script
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_unitdir}/

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/
install -pm 0644 doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/apt-cacher-ng/
chmod 0700 $RPM_BUILD_ROOT%{_var}/lib/apt-cacher-ng/
mkdir -p $RPM_BUILD_ROOT%{_var}/log/apt-cacher-ng/
mkdir -p $RPM_BUILD_ROOT%{_var}/cache/apt-cacher-ng/
mkdir -p $RPM_BUILD_ROOT%{_var}/run/apt-cacher-ng/

%pre
getent group apt-cacher-ng > /dev/null || groupadd -r apt-cacher-ng
getent passwd apt-cacher-ng > /dev/null || useradd -r -d %{_sharedstatedir}/apt-cacher-ng -g apt-cacher-ng -s /sbin/nologin -c "Apt-cacher proxy" apt-cacher-ng

%post
%systemd_post apt-cacher-ng.service

%preun
%systemd_preun apt-cacher-ng.service

%postun
%systemd_postun_with_restart apt-cacher-ng.service

%files
%doc TODO doc/README
%attr(700,apt-cacher-ng,apt-cacher-ng) %dir %{_var}/lib/apt-cacher-ng/
%attr(700,apt-cacher-ng,apt-cacher-ng) %dir %{_var}/log/apt-cacher-ng/
%attr(700,apt-cacher-ng,apt-cacher-ng) %dir %{_var}/cache/apt-cacher-ng/
%attr(700,apt-cacher-ng,apt-cacher-ng) %dir %{_var}/run/apt-cacher-ng/

%config(noreplace) %{_sysconfdir}/apt-cacher-ng/
%config(noreplace) %{_sysconfdir}/cron.daily/apt-cacher-ng
%config(noreplace) %{_sysconfdir}/default/apt-cacher-ng
%config(noreplace) %{_sysconfdir}/logrotate.d/apt-cacher-ng
%{_unitdir}/apt-cacher-ng.service
%{_libexecdir}/apt-cacher-ng/
%{_sbindir}/apt-cacher-ng
%{_mandir}/man8/*

%changelog
* Tue Jan 27 2015 Kenjiro Nakayama <knakayam@redhat.com> - 0.8.0-1
- update to 0.8.0

* Wed Jun 25 2014 Kenjiro Nakayama <knakayam@redhat.com> - 0.7.26-2
- update to 0.7.26 fixed XSS vulnerability (rhbz 1111808)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Kenjiro Nakayama <knakayam@redhat.com> - 0.7.25-3
- update to 0.7.25
- fix spec file.

* Fri May 17 2013 Warren Togami <wtogami@gmail.com> - 0.7.11-3
- systemd service script
- license
