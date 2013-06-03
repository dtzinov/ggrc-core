#
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:
#
# install all prerequisites for GGRC-Core development within a Vagrant VM.

base_dir = '/vagrant/'
opt_dir = "#{base_dir}opt/"
src_dir = "#{base_dir}src/"

include_recipe "apt"

apt_packages = %w(unzip zip make python-virtualenv fabric python-mysqldb python-imaging git sqlite3)

apt_packages.each do |package_name|
  package package_name do
    action :install
  end
end

# Create default directories
directories = %w(/vagrant-dev /vagrant-dev/opt /vagrant-dev/tmp /vagrant/tmp)

directories.each do |directory_name|
  directory directory_name do
    owner "vagrant"
    group "vagrant"
    action :create
  end
end

# Initialize development virtual environment
# ..
#   mkdir -p /vagrant-dev/opt
#   chown vagrant:vagrant /vagrant-dev/opt
#   virtualenv /vagrant-dev/opt/dev_virtualenv
python_virtualenv "/vagrant-dev/opt/dev_virtualenv" do
  interpreter "python2.7"
  owner "vagrant"
  group "vagrant"
  action :create
end

execute "Prepare dev virtualenv" do
  command "/bin/bash -c '"\
          "source /vagrant-dev/opt/dev_virtualenv/bin/activate;"\
          "pip install -U pip;"\
          "pip install -r /vagrant/src/dev-requirements.txt;"\
          "pip install --no-deps -r /vagrant/src/requirements.txt'"
  user "vagrant"
  group "vagrant"
  action :run
end

# `compass` gem is required for building CSS assets
# ..
#   sudo gem install compass --version '= 0.12.2'
gem_package "compass" do
  version "0.12.2"
  action :install
end

execute "Run Makefile for first time" do
  command "/bin/bash -c '"\
          "cd /vagrant; make appengine DEV_PREFIX=/vagrant-dev'"
  user "vagrant"
  group "vagrant"
  action :run
end

# Helper to add sections to files wrapped in "# BEGIN" and "# END"

def add_file_section(path, identifier, content)
  puts "Handling #{identifier} for #{path}"

  require 'digest/md5'

  digest = Digest::MD5.hexdigest(content)
  data = File.read(path)
  begin_line = "# BEGIN #{identifier}"
  end_line = "# END #{identifier}"

  # Check for line with matching md5
  if data.grep(/#{begin_line} #{digest}/).empty?
    # Remove old additions
    data = data.gsub(/\s*#{begin_line}.*#{end_line}\s?[0-9a-f]*\s*/m, '')

    # Add new additions
    data << "\n"
    data << "\n#{begin_line} #{digest}\n"
    data << content
    data << "\n#{end_line} #{digest}\n"
    data << "\n"

    file = File.open(path, 'w')
    file.write(data)
    file.close
  end
end

add_file_section("/home/vagrant/.bashrc", "init_env", <<-END)
export DEV_PREFIX=/vagrant-dev

[ -n "$PS1" ] &&
  echo "Initializing environment" &&
  cd /vagrant &&
  source /vagrant/bin/init_env
END

# Update development virtualenv with requirements and dev-requirements


# Attempt to include custom local additions to the environment
begin
  include_recipe "ggrc::local"
rescue Chef::Exceptions::RecipeNotFound
  # Fail silently, since the file is optional
end

include_recipe "mysql"
include_recipe "mysql::server"
include_recipe "database::mysql"
mysql_database 'ggrcdev' do
  connection ({
    :host => "localhost", :username => 'root', :password => 'root' })
  action :create
end

mysql_database 'ggrcdevtest' do
  connection ({
    :host => "localhost", :username => 'root', :password => 'root' })
  action :create
end