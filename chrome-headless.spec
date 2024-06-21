Name:          chrome-headless
Version:       1.0.0
Release:       8%{?dist}
License:       MIT 
Group:         Unspecified
Summary:       Runs Google Chrome in headless mode for remote debugging.

Source1: chrome-headless.service
Source2: chrome-headless.sysconf

#Requires:      dejavu-sans-fonts  
#Requires:      dejavu-sans-mono-fonts  
#Requires:      dejavu-serif-fonts  
#Requires:      urw-fonts  
Requires:      google-chrome >= 120
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

BuildRequires: systemd

%description
Runs Google Chrome in headless mode for remote debugging or HTML->PDF generation

%build

%install
%{__install} -Dp -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/chrome-headless.service
%{__install} -Dp -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/chrome-headless
%{__install} -dp $RPM_BUILD_ROOT/usr/share/chrome-headless

%pre -p /bin/sh
getent group chrome-headless > /dev/null || groupadd -r chrome-headless
getent passwd chrome-headless >/dev/null || \
  useradd -r -g chrome-headless -d /usr/share/chrome-headless -s /sbin/nologin \
  -c "Used for chrome headless" chrome-headless
exit 0

%post -p /bin/sh
if [ $1 -eq 1 ] ; then 
  systemctl preset chrome-headless.service >/dev/null 2>&1 || : 
fi

%preun -p /bin/sh
if [ $1 -eq 0 ] ; then 
  systemctl --no-reload disable chrome-headless.service > /dev/null 2>&1 || : 
  systemctl stop chrome-headless.service > /dev/null 2>&1 || : 
fi

%postun -p /bin/sh
systemctl daemon-reload >/dev/null 2>&1 || :


%files
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/sysconfig/chrome-headless
%attr(0644, root, root) %{_unitdir}/chrome-headless.service
%dir %attr(0750, chrome-headless, chrome-headless) /usr/share/chrome-headless

%changelog
* Wed May 8 2024 Nathanael Noblet <nathanael@gnat.ca> - 1.0.0-8
- Recreated srpm from rpms
