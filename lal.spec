Summary:	LALSuite is comprised of various gravitational wave data analysis routines
Name:		lal
Version:	6.15.0
Release:	2
License:	GPL v2
Group:		Applications/Science
Source0:	https://www.lsc-group.phys.uwm.edu/daswg/download/software/source/lalsuite/%{name}-%{version}.tar.gz
# Source0-md5:	67fb4647b08f9ba2b9c4e561daf6e3e5
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

%package -n python-lal
Summary:	LAL Python bindings
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description  -n python-lal
LAL Python bindings.

%prep
%setup -q

%build
%configure \
	ac_cv_path_GIT=no-you-dont
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/shrc.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/*sh $RPM_BUILD_ROOT/etc/shrc.d

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%{_sysconfdir}/shrc.d/lal-user-env.*
%attr(755,root,root) %{_bindir}/lal-simd-detect
%attr(755,root,root) %{_bindir}/lal-version
%attr(755,root,root) %{_libdir}/liblal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblal.so.11
%attr(755,root,root) %{_libdir}/liblalsupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblalsupport.so.7

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc
%dir %{_includedir}/lal
%{_includedir}/lal/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-lal
%defattr(644,root,root,755)
%dir %{py_sitedir}/lal
%{py_sitedir}/lal/*.py[co]
%dir %{py_sitedir}/lal/spectrum
%{py_sitedir}/lal/spectrum/*.py[co]
%dir %{py_sitedir}/lal/utils
%{py_sitedir}/lal/utils/*.py[co]
