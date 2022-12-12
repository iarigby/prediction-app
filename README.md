# Breast Cancer prediction application
## Run
```shell
docker run -p 5050:5050 ghcr.io/iarigby/prediction-app:main
```

## Development Environment
### Prerequisites
- Python 3.10
- pipenv - used for managing dependencies, virtual environment and launching run scripts

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

### DevOps
GitHub Actions are set up to automate these processes:
- Build and publish container on pull request or push to main
- Check pull request by running tests 

## Answers to questions
### 1. If you had more time how would you extend the solution?
- Extend error handling, report attributed in data that are out of range
- Improve error messages so that in case of an incomplete data object they api reports exactly 
which attributes are missing.
- Use blueprints to create a more modular configuration for endpoints (instead of using string). 
- Split `api.py` so that swagger and rest of the endpoints are separate and tests do not import swagger.
- Use type based syntax for generating swagger documentation, instead of docstrings. 
I have used swagger in Scala and Typescript but learned about python middleware now, so just went with 
the quick solution

### 2. What other REST endpoints about the model (beside prediction) would be useful
Ones I can think of would be:
- returning the scaled data instead of/along with the prediction
- endpoint which posts the data along with result that will be saved (or immediately used) for training the data,
or the result would be checked against the prediction and ones that are wrong would be stored in some way.

### 3. How would you deploy the whole application into production for real?
Production environment in this case is easy and straightforward. To docker-compose or Kubernetes service file,
just need to add image name and decide which subpath to use on the domain. 
The rest would be managed by reverse proxy, or the port can be exposed.

The front end ui can be in the same network or cluster (that is how I deployed it right now), so that it will communicate with the backend internally vs.
using the public api. In case it is decided that backend should not serve public requests, no modification on the front
end will be necessary

#### Deployment example
- api: [https://exscientia.kernelpanicdisco.dev/api](https://exscientia.kernelpanicdisco.dev/api)
- api docs: [https://exscientia.kernelpanicdisco.dev/api/docs](https://exscientia.kernelpanicdisco.dev/api/docs)
- front end: [https://exscientia.kernelpanicdisco.dev/](https://exscientia.kernelpanicdisco.dev/)
- front end repository: <https://github.com/iarigby/prediction-app-ui>

I did not have time to be as though with front end. I had learned React some time ago so needed to refresh my knowledge, and it was my first time using React with Typescript (I used ts for nodejs projects in the past). I was still able to navigate smoothly and have decent modularity with the components and states.

<details>
<summary>View docker-compose and nginx.conf for backend</summary>
    
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
        # or return the front end path
        return 301 https://exscientia.kernelpanicdisco.dev/api/docs;
    }

    location /api {
        proxy_pass http://docker-webserver/api/;
    }
}
```

</details>
