# Update pip for the entire system, install any development requirements

execute "Update system pip" do
  command "sudo pip install -U pip"
  user "root"
  group "root"
  cwd "/tmp"
  action :run
end

execute "Install development Python requirements" do
  command "sudo pip install -r /vagrant/src/dev-requirements.txt"
  user "root"
  group "root"
  cwd "/tmp"
  action :run
end
