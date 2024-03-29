%define		zope_subname	zopeedit
Summary:	Client-side helper application for ExternalEditor Zope product
Summary(pl.UTF-8):	Aplikacja kliencka dla produktu Zope ExternalEditor
Name:		Zope-%{zope_subname}
Version:	0.9.3
Release:	1
License:	ZPL 2.0
Group:		Development/Tools
Source0:	http://plope.com/software/ExternalEditor/%{zope_subname}-%{version}-src.tgz
# Source0-md5:	25dbf5438c27266a2a0840834f9bcd36
URL:		http://plope.com/software/ExternalEditor/
BuildRequires:	python
BuildRequires:	rpm-pythonprov
Requires(post,postun):	grep
Requires(postun):	fileutils
%pyrequires_eq	python-modules
Requires:	python-tkinter
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Client-side helper application for ExternalEditor Zope product.

%description -l pl.UTF-8
Aplikacja kliencka dla produktu Zope ExternalEditor.

%prep
%setup -q -n %{zope_subname}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{zope_subname},%{_mandir}/man1,%{_bindir}}

install man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -af {Plugins,version.txt,%{zope_subname}.py} $RPM_BUILD_ROOT%{_datadir}/%{zope_subname}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{zope_subname}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{zope_subname}

cat >$RPM_BUILD_ROOT%{_bindir}/%{zope_subname} <<EOF
#!/bin/sh

exec %{_bindir}/python %{_datadir}/%{zope_subname}/%{zope_subname}.pyo \$*
EOF

# sometimes .py needed
# rm -f $RPM_BUILD_ROOT%{_datadir}/%{zope_subname}/*.py
# rm -f $RPM_BUILD_ROOT%{_datadir}/%{zope_subname}/Plugins/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -qs zopeedit /etc/mailcap ; then
	umask 022
	echo "application/x-zope-edit; /usr/bin/zopeedit %%s ; test=test -x /usr/bin/zopeedit" >> /etc/mailcap
fi

%postun
if [ "$1" = "0" ]; then
	if grep -qs zopeedit /etc/mailcap ; then
		umask 022
		grep -v '^application/x-zope-edit; /usr/bin/zopeedit %%s ; test=test -x /usr/bin/zopeedit$' /etc/mailcap >> /etc/mailcap_new
		mv -f /etc/mailcap_new /etc/mailcap 
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES.txt INSTALL-UNIX.txt README.txt
%attr(755,root,root) %{_bindir}/%{zope_subname}
%{_datadir}/%{zope_subname}
%{_mandir}/man1/*
