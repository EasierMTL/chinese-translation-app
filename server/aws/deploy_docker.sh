#!/bin/bash
git clone https://github.com/jchen42703/chinese-translation-api.git chinese
cd ~/chinese/server
docker build -t chinese_translation_server .
docker run -e ENV_TYPE="production" -e DEPLOY_TYPE="server" --name translation_server_container_deploy -p 80:5001 chinese_translation_server