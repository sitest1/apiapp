#! /bin/bash
#Instalando dependencias
reset
sudo apt update
sudo apt install python3-pip python3-mysqldb curl python-is-python3 mariadb-client-* -y
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
sudo apt install docker-ce -y
sudo systemctl start docker
sudo groupadd docker
sudo usermod -aG docker ${USER}
#sudo echo "127.0.0.1	mysql.d.local" >> /etc/hosts
#echo 'alias docker-compose="sudo docker-compose"' >> ~/.bashrc
#source ~/.bashrc



#su -s ${USER}


python3 -m pip install --upgrade pip
python3 -m pip install requests jwcrypto pymysql flask flask-sqlalchemy flask-restful flask-marshmallow hvac
python3 -m pip install -U flask-sqlalchemy marshmallow-sqlalchemy

#Instalar docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
alias python=python3
alias docker-compose="sudo docker-compose"
python vault_start.py