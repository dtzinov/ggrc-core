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

include_recipe "ggrc::package_env"

# Attempt to include custom local additions to the environment
begin
  include_recipe "ggrc::local"
rescue Chef::Exceptions::RecipeNotFound
  # Fail silently, since the file is optional
end
