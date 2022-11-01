
# https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9
# Don't need yum to install docker anymore
# sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
# sudo yum install docker -y
# sudo systemctl enable docker.service
# sudo systemctl start docker.service
sudo docker pull public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
sudo docker run -d -e ENV_TYPE="production" -e DEPLOY_TYPE="server" -e NUM_WORKERS=1 --name translation_server_container_deploy -p 5001:5001 public.ecr.aws/h1c6y7g8/chinese-translation-api:latest
