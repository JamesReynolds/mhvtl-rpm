$script = <<-SCRIPT
sudo yum install -y epel-release
sudo yum install -y /vagrant/mhvtl*.rpm
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.provision "shell", inline: $script
end
