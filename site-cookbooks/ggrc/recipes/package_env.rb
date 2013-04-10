# Create the packages.zip for use in GAE SDK or other environment.

packages_zip = "/vagrant/src/packages.zip"
reqs = "/vagrant/src/requirements.txt"
reqs_md5 = reqs + ".md5"

if not File.exists?(packages_zip) or \
   not File.exists?(reqs_md5) or \
   not system("md5sum --status --strict -c #{reqs_md5}")
  if File.exists?(packages_zip)
    file packages_zip do
      action :delete
    end
  end

  if File.exists?(reqs_md5)
    file reqs_md5 do
      action :delete
    end
  end

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
    command "zip -9mrv #{packages_zip} .;"\
            "mv packages.zip #{packages_zip};"\
            "chown vagrant:vagrant #{packages_zip}"
    user "root"
    group "root"
    creates packages_zip
    cwd "/tmp/packages"
    action :run
  end

  execute "Store the md5sum of requirements.txt" do
    command "md5sum #{reqs} > #{reqs_md5}"
    user "vagrant"
    group "vagrant"
    creates reqs_md5
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
