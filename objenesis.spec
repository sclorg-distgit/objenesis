%{?scl:%scl_package objenesis}
%{!?scl:%global pkg_name %{name}}

# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        A library for instantiating Java objects
Name:           %{?scl_prefix}objenesis
Version:        2.1
Release:        7.2%{?dist}
License:        ASL 2.0
URL:            http://objenesis.org/
Source0:        https://github.com/easymock/%{pkg_name}/archive/%{version}.tar.gz

Patch1:         0001-Fix-build-with-current-jar-plugin.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-shade-plugin)
# xmvn-builddep misses this:
BuildRequires:  %{?scl_prefix}mvn(org.apache:apache-jar-resource-bundle)

BuildArch:      noarch

%description
Objenesis is a small Java library that serves one purpose: to instantiate 
a new object of a particular class.
Java supports dynamic instantiation of classes using Class.newInstance(); 
however, this only works if the class has an appropriate constructor. There 
are many times when a class cannot be instantiated this way, such as when 
the class contains constructors that require arguments, that have side effects,
and/or that throw exceptions. As a result, it is common to see restrictions 
in libraries stating that classes must require a default constructor. 
Objenesis aims to overcome these restrictions by bypassing the constructor 
on object instantiation. Needing to instantiate an object without calling 
the constructor is a fairly specialized task, however there are certain cases 
when this is useful:
* Serialization, Remoting and Persistence - Objects need to be instantiated 
  and restored to a specific state, without invoking code.
* Proxies, AOP Libraries and Mock Objects - Classes can be sub-classed without 
  needing to worry about the super() constructor.
* Container Frameworks - Objects can be dynamically instantiated in 
  non-standard ways.

%package javadoc
Summary:        Javadoc for %{pkg_name}
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q

%patch1 -p1

# Enable generation of pom.properties (rhbz#1017850)
%pom_xpath_remove pom:addMavenDescriptor

%pom_remove_plugin :maven-timestamp-plugin
%pom_remove_plugin :maven-license-plugin
%pom_xpath_remove "pom:dependency[pom:scope='test']" tck

%pom_xpath_remove pom:build/pom:extensions

%build
# tests are skipped because of missing dependency spring-osgi-test
%mvn_build -- -Dyear=2009 -Dmaven.test.skip=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Jun 23 2017 Michael Simacek <msimacek@redhat.com> - 2.1-7.2
- Fix incorrect release bump

* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 2.1-7.1
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 2.1-7%{dist}
- Automated package import and SCL-ization

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-6
- Add missing BR on apache-resource-bundles

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.1-5
- Remove wagon extension

* Fri Jun 03 2016 Michael Simacek <msimacek@redhat.com> - 2.1-4
- Fix build with current maven-jar-plugin

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Michal Srb <msrb@redhat.com> - 2.1-1
- Update to 2.1

* Tue Feb  3 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-18
- Add missing BR on maven-wagon-ssh-external
- Resolves: rhbz#1106608

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-16
- Enable generation of pom.properties
- Resolves: rhbz#1017850

* Sun Sep 08 2013 Mat Booth <fedora@matbooth.co.uk> - 1.2-15
- Update for latest guidelines, rhbz #992389

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-12
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Guido Grazioli <guido.grazioli@gmail.com> 1.2-10
- Update to current Java packaging guidelines
- Remove maven-eclipse-plugin BR

* Mon Feb 20 2012 Jiri Vanek <jvanek@redhat.com> 1.2-9
- Added patch2 - JRockitInstantntiatorCharacters.patch to fix unmappable characters
- Added build requires  apache-resource-bundles and  maven-remote-resources-plugin

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 09 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-7
- Improve project description

* Thu Feb 24 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-6
- Build with mvn-rpmbuild
- Fix License
- Comment on skipped tests

* Fri Feb 04 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-5
- Build with maven 3

* Sun Jan 23 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-4
- Drop buildroot and %%clean section
- Drop use of maven2-settings.xml and jpp-depmap.xml
- Install unversioned jars
- Clean up of needed patch and mvn-jpp execution

* Tue Jan 18 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-3
- Fix build in rawhide

* Sat Dec 04 2010 Guido Grazioli <guido.grazioli@gmail.com> 1.2-2
- Fix build in rawhide
- Update to new Java Packaging Guidelines

* Mon May 10 2010 Guido Grazioli <guido.grazioli@gmail.com> 1.2-1
- Update to 1.2

* Thu May 06 2010 Guido Grazioli <guido.grazioli@gmail.com> 1.0-1
- Import from JPackage 

* Fri Feb 27 2009 Ralph Apel <r.apel at r-apel.de> 0:1.0-2.jpp5
- BR xpp3-minimal and fix depmap accordingly
- Disown poms and fragments dirs

* Wed Jun 18 2008 Ralph Apel <r.apel at r-apel.de> 0:1.0-1.jpp5
- First release
