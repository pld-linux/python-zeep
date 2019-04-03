# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		zeep
%define		egg_name	zeep
%define		pypi_name	zeep
Summary:	A fast and modern Python SOAP client
Name:		python-%{pypi_name}
Version:	3.3.1
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/zeep/zeep-%{version}.tar.gz
# Source0-md5:	f4c6c94052f7498a4962c72d0e771591
URL:		https://pypi.org/project/zeep/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-cached_property
BuildRequires:	python-defusedxml
BuildRequires:	python-modules
BuildRequires:	python-pretend
BuildRequires:	python-requests-toolbelt
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-cached_property
BuildRequires:	python3-defusedxml
BuildRequires:	python3-modules
BuildRequires:	python3-pretend
BuildRequires:	python3-requests-toolbelt
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Highlights:
- Compatible with Python 2.7, 3.3, 3.4, 3.5, 3.6, 3.7 and PyPy
- Build on top of lxml and requests
- Support for Soap 1.1, Soap 1.2 and HTTP bindings
- Support for WS-Addressing headers
- Support for WSSE (UserNameToken / x.509 signing)
- Support for tornado async transport via gen.coroutine (Python 2.7+)
- Support for asyncio via aiohttp (Python 3.5+)
- Experimental support for XOP messages

%package -n python3-%{pypi_name}
Summary:	A fast and modern Python SOAP client
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}
Highlights:
- Compatible with Python 2.7, 3.3, 3.4, 3.5, 3.6, 3.7 and PyPy
- Build on top of lxml and requests
- Support for Soap 1.1, Soap 1.2 and HTTP bindings
- Support for WS-Addressing headers
- Support for WSSE (UserNameToken / x.509 signing)
- Support for tornado async transport via gen.coroutine (Python 2.7+)
- Support for asyncio via aiohttp (Python 3.5+)
- Experimental support for XOP messages

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES CONTRIBUTORS* README*
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python-%{pypi_name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES CONTRIBUTORS* README*
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{pypi_name}-%{version}
%endif
