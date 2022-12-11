# Breast Cancer prediction application
## Run
```shell
docker run -p 5050:5050 ghcr.io/iarigby/prediction-app:main
```

## Development Environment
### Prerequisites
- Python 3.9
- pipenv - used for managin dependencies, virtual environment and launching run scripts

### Installation
After cloning the repository, execute command
```sh
pipenv install
```

### Run
Project contains `.run` directory with build configurations for PyCharm. For command line, use:

```sh
pipenv run app
pipenv run tests
```

## Deployment example
You can view API documentation of active deployment on [https://exscientia.kernelpanicdisco.dev/api/docs](https://exscientia.kernelpanicdisco.dev/api/).

<details>
<summary>View docker-compose and nginx.conf</summary>
    
```yaml
version: '3'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    restart: always
    volumes:
      - ./nginx/conf/:/etc/nginx/conf.d/:ro
      - ./certbot/www:/var/www/certbot/:ro
      - ./certbot/conf/:/etc/nginx/ssl/:ro
  certbot:
    image: certbot/certbot:latest
    volumes:
      - ./certbot/www/:/var/www/certbot/:rw
      - ./certbot/conf/:/etc/letsencrypt/:rw
  webserver:
    image: ghcr.io/iarigby/prediction-app:pr-3
    ports:
      - "5050:5050"
    environment:
      - "SCRIPT_NAME=/api"
```

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name exscientia.kernelpanicdisco.dev www.exscientia.kernelpanicdisco.dev;
    server_tokens off;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://exscientia.kernelpanicdisco.dev$request_uri;
    }
}

upstream docker-webserver {
    server webserver:5050;
}

server {
    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;

    server_name exscientia.kernelpanicdisco.dev;

    ssl_certificate /etc/nginx/ssl/live/exscientia.kernelpanicdisco.dev/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/exscientia.kernelpanicdisco.dev/privkey.pem;
   
    location / {
    return 301 https://exscientia.kernelpanicdisco.dev/api/docs;
    }

    location /api {
        proxy_pass http://docker-webserver/api/;
    }
    location /docs {
        proxy_pass http://docker-webserver/api/;
    }
}
```

</details>
