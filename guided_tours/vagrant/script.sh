#!/bin/bash

sudo apt-get install -y make

sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -

sudo apt-get install -y nodejs

sudo npm install -g npx

mkdir -p ~src/client/public/content/audio
mkdir -p ~src/client/public/content/images

docker run -d -p 6379:6379 --name aredis redis
docker run --name apostgres -d -p 5432:5432 -e POSTGRES_PASSWORD=PLEASE_CHANGE_ME postgres
# docker run --name amysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=PLEASE_CHANGE_ME -d mysql:5.7

# install python 3.6
sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install -y python3.6

# install and create python virtual environments
sudo apt install -y virtualenv
virtualenv -p /usr/bin/python3.6 ~/src/proxy/venv && source ~/src/proxy/venv/bin/activate && pip install -r ~/src/proxy/requirements.txt && deactivate
virtualenv -p /usr/bin/python3.6 ~/src/api/venv && source ~/src/api/venv/bin/activate && pip install -r ~/src/api/requirements.txt && deactivate

# build api docker container
cd ~/src/api/ && docker-compose build --no-cache
