%global debug_package %{nil}

Name:		 prometheus
Version: 3.3.1
Release: 1%{?dist}
Summary: The Prometheus monitoring system and time series database.
License: ASL 2.0
URL:     https://prometheus.io
Provides: prometheus

Source0: https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
%if 0%{?fedora} >= 19
BuildRequires: systemd-rpm-macros
%endif
Requires(pre): shadow-utils

%description

Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

%prep
%setup -q -n prometheus-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 prometheus %{buildroot}%{_bindir}/prometheus
install -D -m 755 promtool %{buildroot}%{_bindir}/promtool
install -D -m 644 prometheus.yml %{buildroot}%{_sysconfdir}/prometheus/prometheus.yml
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/prometheus.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/prometheus

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post prometheus.service

%preun
%systemd_preun prometheus.service

%postun
%systemd_postun prometheus.service

%files
%defattr(-,root,root,-)
%{_bindir}/prometheus
%{_bindir}/promtool
%config(noreplace) %{_sysconfdir}/prometheus/prometheus.yml
#%{_datarootdir}/prometheus
%{_unitdir}/prometheus.service
%config(noreplace) %{_sysconfdir}/default/prometheus
