# Deployment Setup + Commands

## Initial Setup

```bash
# sudo apt update && sudo apt upgrade
sudo apt update

sudo apt install nginx
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw status
systemctl status nginx
```

## Install Repository

```
git clone https://github.com/jchen42703/chinese-translation-api.git
cd chinese-translation-api
docker-compose up -d
```

## Configuring NGINX:

`nano /etc/nginx/sites-available/default`:

```
server {
    server_name chinesetranslationapi.com www.chinesetranslationapi.com;
    listen 80;

    location /api/ {
        proxy_pass http://localhost:5001/api/;
        proxy_http_version 1.1;
    }
    location / {
        proxy_pass http://localhost:3006;
    }
}
```

To test:

```
sudo nginx -t
```

To restart:

```
sudo systemctl restart nginx
```

## Setup SSL

```bash
sudo apt-get install certbot
apt-get install python3-certbot-nginx

# test
sudo certbot --nginx --staging -d chinesetranslationapi.com -d www.chinesetranslationapi.com

# real cert
sudo certbot --nginx -d chinesetranslationapi.com -d www.chinesetranslationapi.com
```

SSL Contrab for renewal:

```
crontab -e

// add this in crontab file; renews if cert will expire in the next 30 days
0 12 * * * /usr/bin/certbot renew --quiet
```
