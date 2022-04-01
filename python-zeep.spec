# Conditional build:
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		zeep
%define		egg_name	zeep
%define		pypi_name	zeep
Summary:	A fast and modern Python SOAP client
Name:		python-%{pypi_name}
Version:	3.4.0
Release:	5
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/zeep/zeep-%{version}.tar.gz
# Source0-md5:	70f1b5bc7c35173a69bfea4f5ffa77e7
URL:		https://pypi.org/project/zeep/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-cached_property
BuildRequires:	python-defusedxml
BuildRequires:	python-modules
BuildRequires:	python-requests-toolbelt
BuildRequires:	python-setuptools
BuildRequires:	python-isodate >= 0.5.4
BuildRequires:	python-attrs >= 17.2.0
BuildRequires:	python-pretend >= 1.0.8
BuildRequires:	python-pyflakes >= 1.5.0
BuildRequires:	python-pycodestyle >= 2.0.0
BuildRequires:	python-mccabe >= 0.6.0
BuildRequires:	python-configparser
BuildRequires:	python-tornado
%if %{with tests}
BuildRequires:	python-flake8-imports >= 0.1.1
BuildRequires:	python-flake8-debugger >= 1.4.0
BuildRequires:	python-flake8-blind-except >= 0.1.1
BuildRequires:	python-flake8 >= 3.3.0
BuildRequires:	python-isort >= 4.2.15
BuildRequires:	python-freezegun >= 0.3.8
BuildRequires:	python-pretend
BuildRequires:	python-pytest >= 3.1.3
BuildRequires:	python-pytest-cov >= 2.5.1
BuildRequires:	python-pytest-tornado >= 0.4.5
BuildRequires:	python-requests_mock >= 0.7.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cached_property
BuildRequires:	python3-defusedxml
BuildRequires:	python3-modules
BuildRequires:	python3-requests-toolbelt
BuildRequires:	python3-setuptools
BuildRequires:	python3-isodate >= 0.5.4
BuildRequires:	python3-attrs >= 17.2.0
BuildRequires:	python3-pretend >= 1.0.8
BuildRequires:	python3-pyflakes >= 1.5.0
BuildRequires:	python3-pycodestyle >= 2.0.0
BuildRequires:	python3-mccabe >= 0.6.0
BuildRequires:	python3-tornado
%if %{with tests}
BuildRequires:	python3-flake8-imports >= 0.1.1
BuildRequires:	python3-flake8-debugger >= 1.4.0
BuildRequires:	python3-flake8-blind-except >= 0.1.1
BuildRequires:	python3-flake8 >= 3.3.0
BuildRequires:	python3-isort >= 4.2.15
BuildRequires:	python3-freezegun >= 0.3.8
BuildRequires:	python3-pretend
BuildRequires:	python3-pytest >= 3.1.3
BuildRequires:	python3-pytest-cov >= 2.5.1
BuildRequires:	python3-pytest-tornado >= 0.4.5
BuildRequires:	python3-requests_mock >= 0.7.0
%endif
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
