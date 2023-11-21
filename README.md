## Description
Jafa is meant to be a reddit-like alternative built with Flask, React, MongoDB with support for docker/docker-compose. 
I plan on adding support for additional databases in the future.

## Development
Follow these steps to get a development environemnt setup.

### Prerequisites 
* Git
* Docker / Docker-Compose

1. Clone the repo.
```bash
git clone https://github.com/timothy1205/jafa
```

2. Navigate to the repo.
```bash
cd jafa
```

3. Setup .env file. Open and modified as desired or leave unmodified for quick defaults.
```bash
cp env.example .env
```

4. Run the development script.
```bash
./scripts/dev.sh
```

Thats it! Docker will build the frontend and backend images from source and start them. 
You may navigate to http://localhost:3000 for the frontend server.
The backend server listens on port `8080` by default and MongoDB server on `27017`


## Production Images
While it is not advised to run this project in a production environment yet, these are the steps to take to set it up. If you decide to do so regardless, then please put it behind a fully configured reverse proxy such as [nginx](https://nginx.org/), [traefik](https://traefik.io/traefik/), or [caddy](https://caddyserver.com/).

1. Clone the repo.
```bash
git clone https://github.com/timothy1205/jafa
```

2. Navigate to the repo.
```bash
cd jafa
```

3. Setup .env file. Open and modified as desired or leave unmodified for quick defaults.
```bash
cp env.example .env
```

4. Start with docker-compose
```bash
docker compose up -d
```
