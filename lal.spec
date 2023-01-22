# TODO: bconds for boinc, cuda
Summary:	LALSuite - various gravitational wave data analysis routines
Summary(pl.UTF-8):	LALSuite - różne procedury do analizy danych fal grawitacyjnych
Name:		lal
Version:	7.2.4
Release:	2
License:	GPL v2
Group:		Applications/Science
Source0:	http://software.igwn.org/lscsoft/source/lalsuite/%{name}-%{version}.tar.xz
# Source0-md5:	14994c1e60f71409e3765ece76adb021
Patch0:		%{name}-env.patch
Patch1:		no-simd.patch
Patch2:		%{name}-swig.patch
Patch3:		%{name}-octave.patch
URL:		https://wiki.ligo.org/Computing/LALSuite
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	fftw3-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	hdf5-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel >= 2:6
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-numpy-devel >= 1:1.7
# 3.0.11 for octave 4.0, 3.0.12 for octave 4.2, 4.0.2 for octave 4.4, 4.1.0 for octave 6
BuildRequires:	swig >= 4.1.0
BuildRequires:	swig-python >= 3.0.11
BuildRequires:	tar >= 1:1.22
BuildRequires:	texlive-dvips
BuildRequires:	texlive-format-pdflatex
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	gsl >= 1.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LALSuite is comprised of various gravitational wave data analysis
routines written in C following the ISO/IEC 9899:1999 standard, more
commonly referred to as C99.

%description -l pl.UTF-8
LALSuite składa się z różnych procedur do analizy danych fal
grawitacyjnych, napisanych w C zgodnie ze standardem ISO/IEC
9899:1999, bardziej znanym jako C99.

%package devel
Summary:	Header files for LAL core libraries
Summary(pl.UTF-8):	Pliki nagłówkowe podstawowych bibliotek LAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fftw3-devel
Requires:	fftw3-single-devel
Requires:	gsl-devel >= 1.13
Requires:	zlib-devel

%description devel
Header files for LAL core libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe podstawowych bibliotek LAL.

%package static
Summary:	Static LAL core libraries
Summary(pl.UTF-8):	Statyczne podstawowe biblioteki LAL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LAL core libraries.

%description static -l pl.UTF-8
Statyczne podstawowe biblioteki LAL.

%package -n octave-lal
Summary:	Octave LAL interface
Summary(pl.UTF-8):	Interfejs Octave do bibliotek LAL
Group:		Applications/Math
Requires:	%{name} = %{version}-%{release}
Requires:	octave

%description -n octave-lal
Octave LAL interface.

%description -n octave-lal -l pl.UTF-8
Interfejs Octave do bibliotek LAL.

%package -n python3-lal
Summary:	LAL Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do bibliotek LAL
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-modules >= 1:3.5
Requires:	python3-numpy >= 1:1.7
Obsoletes:	python-lal < 7

%description -n python3-lal
LAL Python bindings.

%description -n python3-lal -l pl.UTF-8
Wiązania Pythona do bibliotek LAL.

%prep
%setup -q
%patch0 -p1
%ifarch %{ix86}
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I gnuscripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	ac_cv_path_GIT=no-you-dont \
	--disable-silent-rules \
	--enable-swig
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Fix undefined variable genereted by configure
%{__sed} -i -e 's/\${PYTHON_EXEC_PREFIX}/\${prefix}/' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblal*.la

install -d $RPM_BUILD_ROOT/etc/shrc.d
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/*sh $RPM_BUILD_ROOT/etc/shrc.d

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%{_sysconfdir}/shrc.d/lal-user-env.csh
%{_sysconfdir}/shrc.d/lal-user-env.fish
%{_sysconfdir}/shrc.d/lal-user-env.sh
%attr(755,root,root) %{_bindir}/lal_cache
%attr(755,root,root) %{_bindir}/lal_fftw_wisdom
%attr(755,root,root) %{_bindir}/lal_fftwf_wisdom
%attr(755,root,root) %{_bindir}/lal_path2cache
%attr(755,root,root) %{_bindir}/lal_searchsum2cache
%attr(755,root,root) %{_bindir}/lal_simd_detect
%attr(755,root,root) %{_bindir}/lal_tconvert
%attr(755,root,root) %{_bindir}/lal_version
%attr(755,root,root) %{_libdir}/liblal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblal.so.20
%attr(755,root,root) %{_libdir}/liblalsupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblalsupport.so.14
%{_mandir}/man1/lal_cache.1*
%{_mandir}/man1/lal_fftw_wisdom.1*
%{_mandir}/man1/lal_fftwf_wisdom.1*
%{_mandir}/man1/lal_path2cache.1*
%{_mandir}/man1/lal_searchsum2cache.1*
%{_mandir}/man1/lal_simd_detect.1*
%{_mandir}/man1/lal_tconvert.1*
%{_mandir}/man1/lal_version.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblal.so
%attr(755,root,root) %{_libdir}/liblalsupport.so
%{_includedir}/lal
%{_pkgconfigdir}/lal.pc
%{_pkgconfigdir}/lalsupport.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblal.a
%{_libdir}/liblalsupport.a

%files -n octave-lal
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/octave/*/site/oct/*/lal.oct

%files -n python3-lal
%defattr(644,root,root,755)
%dir %{py3_sitedir}/lal
%attr(755,root,root) %{py3_sitedir}/lal/_lal.so
%{py3_sitedir}/lal/*.py
%{py3_sitedir}/lal/__pycache__
%dir %{py3_sitedir}/lal/utils
%{py3_sitedir}/lal/utils/*.py
%{py3_sitedir}/lal/utils/__pycache__
