
#!/bin/bash -xe

# https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9
# Don't need yum to install docker anymore
# sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo amazon-linux-extras install -y nginx1
sudo service start nginx
echo "server {
    listen 80;
    access_log /var/log/nginx/deploy.log;

    location /api/ {
        proxy_pass http://localhost:5001/api/;
        proxy_http_version 1.1;
    }
}" > /etc/nginx/conf.d/default.conf

# sudo yum install docker -y
# sudo systemctl enable docker.service
# sudo systemctl start docker.service
# https://awstip.com/to-set-up-docker-container-inside-ec2-instance-with-terraform-3af5d53e54ba
sudo docker pull public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
sudo docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" -e NUM_WORKERS=1 --name translation_server_container_deploy -p 5001:5001 public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
