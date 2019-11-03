# TODO: bconds for boinc, cuda
Summary:	LALSuite - various gravitational wave data analysis routines
Summary(pl.UTF-8):	LALSuite - różne procedury do analizy danych fal grawitacyjnych
Name:		lal
Version:	6.20.2
Release:	1
License:	GPL v2
Group:		Applications/Science
Source0:	http://software.ligo.org/lscsoft/source/lalsuite/%{name}-%{version}.tar.xz
# Source0-md5:	621c8c8758b4bd3d2cbd66727394329e
Patch0:		%{name}-env.patch
Patch1:		no-simd.patch
URL:		https://wiki.ligo.org/DASWG/LALSuite
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	fftw3-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	hdf5-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel >= 2:3.2.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-numpy-devel >= 1.7
# 2.0.12 for octave 3.2, 3.0.7 for octave 4.0, 3.0.12 for octave 4.2
BuildRequires:	swig >= 3.0.12
BuildRequires:	swig-python >= 2.0.12
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

%package -n python-lal
Summary:	LAL Python bindings
Summary(pl.UTF-8):	Wiązania Pythona do bibliotek LAL
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules >= 1:2.6
Requires:	python-numpy >= 1:1.7

%description -n python-lal
LAL Python bindings.

%description -n python-lal -l pl.UTF-8
Wiązania Pythona do bibliotek LAL.

%prep
%setup -q
%patch0 -p1
%ifarch %{ix86}
%patch1 -p1
%endif

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
%attr(755,root,root) %{_bindir}/lal_simd_detect
%attr(755,root,root) %{_bindir}/lal_version
%attr(755,root,root) %{_libdir}/liblal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblal.so.17
%attr(755,root,root) %{_libdir}/liblalsupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblalsupport.so.12

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

%files -n python-lal
%defattr(644,root,root,755)
%dir %{py_sitedir}/lal
%attr(755,root,root) %{py_sitedir}/lal/_lal.so
%{py_sitedir}/lal/*.py[co]
%dir %{py_sitedir}/lal/spectrum
%{py_sitedir}/lal/spectrum/*.py[co]
%dir %{py_sitedir}/lal/utils
%{py_sitedir}/lal/utils/*.py[co]
