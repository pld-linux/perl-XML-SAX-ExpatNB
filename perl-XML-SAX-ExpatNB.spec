#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%define		pdir	XML
%define		pnam	SAX-ExpatNB
Summary:	XML::SAX::ExpatNB - non-blocking filehandle oriented XML::SAX parser
Summary(pl.UTF-8):	XML::SAX::ExpatNB - nieblokujący zorientowany na uchwyty plików analizator XML::SAX
Name:		perl-XML-SAX-ExpatNB
Version:	0.01
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	335735a0408272ba20addba8e7005bcc
URL:		http://search.cpan.org/dist/XML-SAX-ExpatNB/
BuildRequires:	perl-XML-NamespaceSupport >= 0.03
BuildRequires:	perl-XML-Parser >= 2.27
BuildRequires:	perl-XML-SAX >= 0.03
BuildRequires:	perl(XML::SAX::Base) >= 1.00
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Test-Distribution
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an non blocking implementation of a SAX2 driver sitting on top
of Expat (XML::Parser).

%description -l pl.UTF-8
To jest nieblokujaca implementacja sterownika SAX2 w oparciu o moduł
Expat (XML::Parser).

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->add_parser(q(XML::SAX::ExpatNB))->save_parsers()"

%postun
if [ "$1" = "0" ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::SAX::ExpatNB))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
%{perl_vendorlib}/XML/SAX/ExpatNB.pm
%{_mandir}/man3/*
