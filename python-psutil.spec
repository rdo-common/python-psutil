%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global short_name psutil

Name:           python-psutil
Version:        0.1.2
Release:        4%{?dist}
Summary:        A process utilities module for Python

Group:          Development/Languages
License:        BSD
URL:            http://psutil.googlecode.com/
Source0:        http://psutil.googlecode.com/files/%{short_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python2-tools
BuildRequires:  python3-devel
%endif

%description
psutil is a module providing an interface for retrieving information on running
processes and system utilization (CPU, memory) in a portable way by using
Python, implementing many functionalities offered by tools like ps, top and
Windows task manager.


%if 0%{?with_python3}
%package -n python3-psutil
Summary:        A process utilities module for Python 3
Group:          Development/Languages

%description -n python3-psutil
psutil is a module providing an interface for retrieving information on running
processes and system utilization (CPU, memory) in a portable way by using Python
3, implementing many functionalities offered by tools like ps, top and Windows
task manager.
%endif


%prep
%setup -q -n %{short_name}-%{version}

# Remove shebangs
pushd psutil
for file in _psbsd.py _pslinux.py _psmswindows.py _psosx.py _psutil.py; do
  sed -i.orig -e 1d $file && \
  touch -r $file.orig $file && \
  rm $file.orig
done
popd

# Remove DOS line endings
for file in HISTORY LICENSE README; do
  sed 's|\r||g' $file > $file.new && \
  touch -r $file $file.new && \
  mv $file.new $file
done

chmod a-x docs/class_diagram.png

rm docs/.DS_Store


%if 0%{?with_python3}
cp -rp . %{py3dir}
pushd %{py3dir}
2to3 --nobackups --write .
popd
%endif


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
%endif


%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
  --skip-build \
  --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install \
  --skip-build \
  --root $RPM_BUILD_ROOT
popd
%endif

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc HISTORY LICENSE README docs
%{python_sitelib}/%{short_name}
%{python_sitelib}/*.egg-info


%if 0%{?with_python3}
%files -n python3-psutil
%defattr(-,root,root,-)
%doc HISTORY LICENSE README docs
%{python3_sitelib}/%{short_name}
%{python3_sitelib}/*.egg-info
%endif


%changelog
* Sat Feb 20 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-4
- Change python-utils BuildRequires for python2-utils

* Sat Feb 20 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-3
- Add python3 subpackage

* Thu Jan 14 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-2
- Drop no-shebang patch for a sed command
- Drop test suite from %%doc tag

* Fri Jan  8 2010 ELMORABITY Mohamed <melmorabity@fedoraproject.org> 0.1.2-1
- Initial RPM release
