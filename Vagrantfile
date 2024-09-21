Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/noble64"

  config.vm.network "forwarded_port", guest: 80, host: 8081
  config.vm.network "forwarded_port", guest: 22, host: 2222
  config.vm.network "public_network", bridge: "Ethernet"

  config.vm.boot_timeout = 1200

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "8096"
    vb.cpus = 8
  end

  config.vm.synced_folder "src", "/home/vagrant/src", type: "rsync"
  config.vm.synced_folder "infrastructure/terraform", "/home/vagrant/terraform", type: "rsync"

  config.vm.provision "shell", path: "infrastructure/scripts/basic_setup.sh"
  config.vm.provision "shell", path: "infrastructure/scripts/post-provision.sh"
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive

    sleep 5
    sudo apt-get update
    sudo apt-get install -y curl apt-transport-https gnupg conntrack jq unzip docker.io python3 python3-pip python3.12-venv gcc \
    python3-dev build-essential || { echo 'Error installing packages'; exit 1; }

    sudo apt-get upgrade -y
    sudo apt-get dist-upgrade -y

    sudo apt-get autoremove -y
    sudo update-grub
    export FLASK_APP=main.py

    TERRAFORM_VERSION=$(curl -s https://checkpoint-api.hashicorp.com/v1/check/terraform | jq -r .current_version)
    curl -LO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
    sudo unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker vagrant
    sudo chmod 666 /var/run/docker.sock
    sudo -u vagrant newgrp docker

    sudo curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    minikube start --driver=docker

    sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo chmod +x kubectl
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

    echo 'source <(kubectl completion bash)' >>~/.bashrc
    echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
    echo 'alias kubectl="kubectl"' >> /home/vagrant/.bashrc
    source ~/.bashrc

    mkdir -p /home/vagrant/.ssh
    chmod 700 /home/vagrant/.ssh
    touch /home/vagrant/.ssh/authorized_keys
    chmod 600 /home/vagrant/.ssh/authorized_keys
    echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDW+bmu6+wkiIgNqVatz5VzRJBpLEItFtufXLAtYIAiuy7GBJ1Mu17reXW1eFrkPLgyt+n8MAXQHb9ZddFIlAdcW+dHsZmFc6+enZfxoXUxQ4j5BeHGGTRvuF5yNIhAWwvnp/uTRF77+brMabH86nTIJpPtDWfDxZas/tcrNVN7R0ARVfflKz37u2pCRrackJI3fqkppwP0Oat84tUlXR2K/R/V86i/b3YPzKV2rm0xZE7IWE2KmcF/QggZQb735o07umV6dPKglYS7llJye8aciNKrfgJ63HQZO2oIj+svEjm0gPs7oSKIWpQMp95MWm7eh+ghrSt3/mSalrzoTE3eID94/xuqT/9UjrumIBMKoqysu4OPitKKESY5wXK3uoNgDAjVZs9HS9tWjRRCZe/cm64r0ZnlPUIYgqy3Tqj/kZzZiSUjCFi/OpFSgFwcbjNNKnQBvEcVynEzt1OSHtIXIMPZUQ3345pvyEHMAQMbtcIzDh6h7O+00Frfnt1lvLNXb6lryfThjSGwdvryDBSVqGreYTTZShpFIRMTEDCNpvQ79Y2LN+YCEArBkpSLau/ZJj6fzXr0nVRE6SliQ5V7hcDh+vZRSu7UzMjNerqG7eP0A4r3UEzI6Go7JnoNJwigpgfiJLwKtqLi6Gevsf/uskww0wysj4bC3cpwUkjHvw== omaciasnarvaez@gmail.com" >> /home/vagrant/.ssh/authorized_keys
    chown -R vagrant:vagrant /home/vagrant/.ssh

    sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
    sudo systemctl restart ssh

    rsync -av /vagrant/scripts /vagrant/nginx /vagrant/terraform /home/vagrant/
    find /home/vagrant/scripts /home/vagrant/nginx /home/vagrant/terraform -type f -exec chmod +x {} \;

    #echo "@reboot vagrant /home/vagrant/scripts/post-provision.sh" | sudo tee -a /etc/crontab
    #sudo /home/vagrant/scripts/init_terraform.sh

  SHELL

end
