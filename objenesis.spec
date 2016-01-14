%global pkg_name objenesis
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.2
Release:        16.5%{?dist}
Summary:        A library for instantiating Java objects
License:        ASL 2.0
URL:            http://objenesis.org/
# svn export http://objenesis.googlecode.com/svn/tags/1_2/ objenesis-1.2
# tar cfJ objenesis-1.2.tar.xz objenesis-1.2
Source0:        %{pkg_name}-%{version}.tar.xz

# Skipping website (requires xsite), this patch is unused atm
#Patch0:         objenesis-website-pom.patch

# Remove deps for test scope (unavailable); fix
# maven-license-plugin groupID to latest version available.
Patch1:         001-objenesis-fix-build.patch
Patch2:         JRockitInstantntiatorCharacters.patch

BuildRequires:  %{?scl_prefix}jpackage-utils
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix_maven}maven-shade-plugin
BuildRequires:  %{?scl_prefix}xpp3-minimal
BuildRequires:  %{?scl_prefix}objectweb-asm
BuildRequires:  %{?scl_prefix_maven}apache-resource-bundles

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
Group:          Documentation
Summary:        Javadoc for %{pkg_name}
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}
#%%patch0 -b .sav0
%patch1 -p1
%patch2 -p2
scl enable %{scl_maven} %{scl} - <<"EOF"
# Enable generation of pom.properties (rhbz#1017850)
%pom_xpath_remove pom:addMavenDescriptor
%pom_remove_plugin com.mycila.maven-license-plugin:maven-license-plugin
%pom_remove_plugin com.keyboardsamurais.maven:maven-timestamp-plugin
%pom_xpath_remove pom:extensions
EOF


%build
scl enable %{scl_maven} %{scl} - <<"EOF"
# tests are skipped because of missing dependency spring-osgi-test
%mvn_build -- -Dyear=2009 -Dmaven.test.skip=true
EOF


%install
scl enable %{scl_maven} %{scl} - <<"EOF"
%mvn_install
EOF

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt


%changelog
* Wed Jan 14 2015 Michal Srb <msrb@redhat.com> - 1.2-16.5
- Fix directory ownership
- Fix BR

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-16.4
- Fix BR

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.2-16.4
- Mass rebuild 2015-01-13

* Fri Jan  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-16.3
- Mass rebuild 2015-01-09

* Wed Jan  7 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-16.2
- Build for rh-java-common SCL

* Tue Jun 3 2014 Alexander Kurtakov <akurtako@redhat.com> 1.2-16.1
- Fix dist macro.

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
