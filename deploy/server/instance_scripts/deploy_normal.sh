
#!/bin/bash -xe

# Specified through CLI: terraform apply -var used_quantized=1
export USE_QUANTIZED="%s"
# DEBUG: echo $USE_QUANTIZED

# https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9
# Don't need yum to install docker anymore
# sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start

# Setup nginx
sudo amazon-linux-extras install -y nginx1
# Don't use default nginx conf: /etc/nginx/conf.d/default.conf
# Relies on /etc/nginx/nginx.conf
echo "http {
    server {
        listen 80;
        access_log /var/log/nginx/deploy.log;

        location /api/ {
            proxy_pass http://localhost:5001/api/;
            proxy_http_version 1.1;
        }
    }
}

events {
    worker_connections  4096;  ## Default: 1024
}" | sudo tee /etc/nginx/nginx.conf
sudo systemctl start nginx

# sudo yum install docker -y
# sudo systemctl enable docker.service
# sudo systemctl start docker.service
# https://awstip.com/to-set-up-docker-container-inside-ec2-instance-with-terraform-3af5d53e54ba

sudo docker pull public.ecr.aws/h1c6y7g8/chinese-translation-api:latest

if [[ -z "${USE_QUANTIZED}" ]]; then
  echo "Using regular model..."
  sudo docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" -e NUM_WORKERS=2 --name translation_server_container_deploy -p 5001:5001 public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
else
  echo "Using quantized model..."
  sudo docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" -e NUM_WORKERS=2 -e MODEL_TYPE="quantized_dynamic" --name translation_server_container_deploy -p 5001:5001 public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
fi
