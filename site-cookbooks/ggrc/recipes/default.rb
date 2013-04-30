# install all prerequisites for GGRC-Core development within a Vagrant VM.

include_recipe "apt"

package "unzip" do
  action :install
end

package "zip" do
  action :install
end

package "python-virtualenv" do
  action :install
end

package "git" do
  action :install
end

version = node[:ggrc][:app_engine_version]
zipfile = "google_appengine_#{version}.zip"

unless File.exists?("/opt/#{zipfile}")
  remote_file "/opt/#{zipfile}" do
    source "http://googleappengine.googlecode.com/files/#{zipfile}"
    action :create
  end

  execute "Unzip Google App Engine SDK" do
    command "unzip /opt/#{zipfile}"
    cwd "/opt"
    action :run
  end

  execute "Add Google App Engine SDK to the PATH" do
    command "sed -i -e 's/PATH=\"/PATH=\"\\/opt\\/google_appengine:/' /etc/environment"
    action :run
  end
end

directory "/vagrant/src/instance" do
  owner "vagrant"
  group "vagrant"
  action :create
end

execute "Copy development settings to instance directory" do
  command "ln -s /vagrant/src/ggrc/settings/development.py /vagrant/src/instance/settings.cfg"
  user "vagrant"
  group "vagrant"
  creates "/vagrant/src/instance/settings.cfg"
  action :run
end

include_recipe "ggrc::package_env"
include_recipe "ggrc::test_env"

# Attempt to include custom local additions to the environment
begin
  include_recipe "ggrc::local"
rescue Chef::Exceptions::RecipeNotFound
  # Fail silently, since the file is optional
end
