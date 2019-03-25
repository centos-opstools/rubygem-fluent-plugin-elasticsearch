# Manually modified spec file from v1.0.0 release
%global gem_name fluent-plugin-elasticsearch

Name: rubygem-%{gem_name}
Version: 1.17.2
Release: 1%{?dist}
Summary: ElasticSearch output plugin for Fluent event collector
Group: Development/Languages
License: MIT
URL: https://github.com/uken/fluent-plugin-elasticsearch
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby >= 2.0
BuildRequires: fluentd
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(excon)
BuildRequires: rubygem(elasticsearch)
BuildRequires: rubygem(multipart-post)
Requires: fluentd >= 0.12.0
Requires: rubygem(elasticsearch)
Requires: rubygem(excon)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
ElasticSearch output plugin for Fluent event collector.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_instdir}/{.gitignore,.travis.yml,.editorconfig,.coveralls.yml}


# Run the test suite
%check
pushd .%{gem_instdir}
# Disabled on EL due to missing dependencies
%if 0%{?fedora} > 0
testrb2 -Ilib test
%endif
popd

%files
%dir %{gem_instdir}
%{gem_instdir}/ISSUE_TEMPLATE.md
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/PULL_REQUEST_TEMPLATE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/Gemfile
%doc %{gem_instdir}/Gemfile.v0.12
%doc %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/test

%changelog
* Wed Aug 15 2018 Rich Megginson <rmeggins@redhat.com> - 1.17.2-1
- version 0.17.2
- Bug 1489533 - logging-fluentd needs to periodically reconnect to logging-mux or elasticsearch to help balance sessions

* Wed Jun 20 2018 Jeff Cantrill <jcantril@redhat.com> - 1.17.0-1
- version 1.17.0
- Bug 1593297. Fix improper evaluation of bulk index count which
- causes fluent to become wedged when the request/response differ

* Wed May 09 2018 Jeff Cantrill <jcantril@redhat.com> - 1.16.1-1
- version 1.16.1

* Fri Apr 27 2018 Rich Megginson <rmeggins@redhat.com> - 1.15.2-1
- version 1.15.2
- Bug 1541429 logging-fluentd gets wedged in a state where retries do not succeed after bulk index queue full error
- - previous fix caused a regression

* Wed Apr 18 2018 Jeff Cantrill <jcantril@redhat.com> - 1.15.0-1
- version 1.15.0

* Fri Apr 13 2018 Jeff Cantrill <jcantril@redhat.com> - 1.14.0-1
- version 1.14.0

* Tue Feb 27 2018 Rich Megginson <rmeggins@redhat.com> - 1.13.2-1
- version 1.13.2

* Wed Dec 13 2017 Rich Megginson <rmeggins@redhat.com> - 1.13.0-1
- version 1.13.0

* Fri Sep  1 2017 Rich Megginson <rmeggins@redhat.com> - 1.9.5.1-1
- Retry on certain errors from Elasticsearch
-   specifically, better handling for bulk index rejections
- Add support for logstash_prefix_key and logstash_prefix_separator

* Thu Jun 29 2017 Rich Megginson <rmeggins@redhat.com> - 1.9.5-2
- remove requirement on rubygem(elasticsearch) < 1.1

* Thu Jun 29 2017 Rich Megginson <rmeggins@redhat.com> - 1.9.5-1
- version 1.9.5

* Mon Jan  9 2017 Rich Megginson <rmeggins@redhat.com> - 1.9.2-2
- add Gemfile.v0.12

* Mon Jan  9 2017 Rich Megginson <rmeggins@redhat.com> - 1.9.2-1
- Upgrade to upstream version v1.9.2

* Tue Dec 13 2016 Rich Megginson <rmeggins@redhat.com> - 1.9.1-1
- Upgrade to upstream version v1.9.1

* Mon Dec 12 2016 Rich Megginson <rmeggins@redhat.com> - 1.9.0-1
- Upgrade to upstream version v1.9.0

* Fri Nov 04 2016 Rich Megginson <rmeggins@redhat.com> - 1.8.0-1
- Upgrade to upstream version v1.8.0

* Fri Sep 16 2016 Rich Megginson <rmeggins@redhat.com> - 1.7.0-1
- Upgrade to upstream version v1.7.0

* Thu Feb 04 2016 Lukas Vlcek <lvlcek@redhat.com> - 1.3.0-2
- Remove .coveralls.yml file

* Thu Feb 04 2016 Lukas Vlcek <lvlcek@redhat.com> - 1.3.0-1
- Upgrade to upstream version v1.3.0

* Tue Sep 08 2015 Troy Dawson <tdawson@redhat.com> - 1.0.0-2
- Add patch2 for implementing dynamic variables in config

* Wed Sep 02 2015 Troy Dawson <tdawson@redhat.com> - 1.0.0-1
- Update to 1.0.0
- Add patch0 for dynamic index and type
- Add patch1 for passing client configurations to excon

* Tue Feb 17 2015 Graeme Gillies <ggillies@redhat.com> - 0.7.0-1
- Initial package
