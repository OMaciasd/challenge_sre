Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provision "file",
    source: "./docker-compose.yml",
    destination: "/home/vagrant/docker-compose.yml"

  config.vm.provision "file",
    source: "./src/Dockerfile",
    destination: "/home/vagrant/flask_app/Dockerfile"

  config.vm.provision "file",
    source: "./requirements.txt",
    destination: "/home/vagrant/flask_app/requirements.txt"

  config.vm.provision "file",
    source: "./infrastructure/main.tf",
    destination: "/home/vagrant/terraform/main.tf"

  config.vm.provision "file",
    source: "./scripts/init_terraform.sh",
    destination: "/home/vagrant/init_terraform.sh"

  # Otras configuraciones y provisionamiento
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo apt-get install -y terraform
    bash /home/vagrant/init_terraform.sh
  SHELL
end
