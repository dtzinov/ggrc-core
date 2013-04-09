unless File.exists?("/opt/packages.zip")
  python_virtualenv "/tmp/package_env" do
    interpreter "python2.7"
    action :create
  end

  directory "/tmp/packages" do
    owner "root"
    group "root"
    action :create
  end

  execute "Prepare to build packages.zip using the temporary virtualenv" do
    command "/bin/bash -c '"\
            "source package_env/bin/activate;"\
            "pip install -r /vagrant/src/requirements.txt --target ./packages;"\
            "find packages -name \"*.pyc\" -delete;"\
            "find packages -name \"*.egg-info\" | xargs rm -rf'"
    user "root"
    group "root"
    cwd "/tmp"
    action :run
  end

  execute "Create packages.zip" do
    command "zip -9mrv packages.zip .;"\
            "mv packages.zip /opt/packages.zip"
    user "root"
    group "root"
    creates "/opt/packages.zip"
    cwd "/tmp/packages"
    action :run
  end

  directory "/tmp/packages" do
    recursive true
    action :delete
  end

  python_virtualenv "/tmp/package_env" do
    action :delete
  end
end
