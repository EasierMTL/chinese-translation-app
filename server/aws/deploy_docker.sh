#!/bin/bash
sudo apt update
# Install docker
sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
sudo apt -y install docker-ce

git clone https://github.com/jchen42703/chinese-translation-api.git chinese
cd ~/chinese/server
# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

sudo docker build -t chinese_translation_server .

# Regular
sudo docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" -e NUM_WORKERS=8 --name translation_server_container_deploy -p 5001:5001 chinese_translation_server

# Quantized
# sudo docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" -e NUM_WORKERS=8 MODEL_TYPE="quantized_dynamic" --name translation_server_container_deploy -p 5001:5001 chinese_translation_server