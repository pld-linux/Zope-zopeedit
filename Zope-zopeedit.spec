%include	/usr/lib/rpm/macros.python
%define		zope_subname	zopeedit
Summary:	Client-side helper application for ExternalEditor Zope product
Summary(pl):	Aplikacja pomocnicza dla ExternalEditor, produktu Zope
Name:		Zope-%{zope_subname}
Version:	0.7
Release:	2
License:	ZPL 2.0
Group:		Development/Tools
Source0:	http://zope.org/Members/Caseman/ExternalEditor/%{version}/%{zope_subname}-%{version}-src.tgz
# Source0-md5:	87fe890a7f7c2506db16142bc4789b38
URL:		http://zope.org/Members/Caseman/ExternalEditor/
BuildRequires:	python >= 2.2
%pyrequires_eq	python-modules
Requires:	python-tkinter
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Client-side helper application for ExternalEditor Zope product

%description -l pl
Aplikacja kliencka dla ExternalEditor, produktu Zope

%prep
%setup -q -n %{zope_subname}-%{version}-src

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{zope_subname},%{_mandir}/man1,%{_bindir}}

install man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -af {Plugins,%{zope_subname}.py} $RPM_BUILD_ROOT%{_datadir}/%{zope_subname}

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
if ! grep -q zopeedit /etc/mailcap ; then
	echo "application/x-zope-edit; /usr/bin/zopeedit %%s ; test=test -x /usr/bin/zopeedit" >> /etc/mailcap
fi

%postun

%files
%defattr(644,root,root,755)
%doc CHANGES.txt INSTALL-UNIX.txt LICENSE.txt README.txt
%attr(755,root,root) %{_bindir}/%{zope_subname}
%{_datadir}/%{zope_subname}
%{_mandir}/man1/*
