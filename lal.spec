Summary:	LALSuite is comprised of various gravitational wave data analysis routines
Name:		lal
Version:	6.4.1
Release:	0.1
License:	GPL v2
Group:		Applications/Science
Source0:	https://www.lsc-group.phys.uwm.edu/daswg/download/software/source/lalsuite/%{name}-%{version}.tar.gz
# Source0-md5:	254f2e33bee014fc4916769ad5a8dc81
URL:		https://www.lsc-group.phys.uwm.edu/daswg/projects/lalsuite.html
BuildRequires:	fftw3-common-devel
BuildRequires:	gsl-devel
BuildRequires:	metaio-devel
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	texlive-dvips
BuildRequires:	texlive-format-pdflatex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LALSuite is comprised of various gravitational wave data analysis
routines written in C following the ISO/IEC 9899:1999 standard, more
commonly referred to as C99.

%package devel
Summary:	Development files for LAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fftw3-devel
Requires:	fftw3-single-devel
Requires:	zlib-devel

%description devel
Development files for LAL.

%package static
Summary:	Static LAL library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LAL library.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/shrc.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/*sh $RPM_BUILD_ROOT/etc/shrc.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%{_sysconfdir}/shrc.d/lal-user-env.*
%attr(755,root,root) %{_bindir}/lal-version
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lal-config
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc
%dir %{_includedir}/lal
%{_includedir}/lal/*
%{_mandir}/man*/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
