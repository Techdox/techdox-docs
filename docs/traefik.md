---
title: Setting Up Traefik with Docker Compose
description: Traefik is a reverse proxy which allows for seamless service communication
---
# Secure Web Services with Traefik and Docker Compose: A Practical Guide

## Introduction

This guide focuses on deploying Traefik as a reverse proxy with Docker Compose, emphasizing the setup of a dedicated network for seamless service communication and automatic HTTPS configuration using Let's Encrypt.

!!! note "Port Forward"

    Make sure you have port 80 and 443 forwarded within your Router
## Setup Overview

1. **Traefik Deployment**: Configure Traefik with Docker Compose, enabling HTTPS through Let's Encrypt.
2. **Dedicated Docker Network**: Establish a network for Traefik and services to facilitate secure and efficient communication.
3. **Example Service Deployment**: Deploy an Nginx service as an example, secured by Traefik with HTTPS.

## Docker Compose Configuration for Traefik

Start with defining Traefik in a `docker-compose.yml` file, specifying the necessary configurations, volumes, and the dedicated network.

### Traefik Docker Compose

```yaml
version: '3'
services:
  reverse-proxy:
    image: traefik:v2.11
    command: --configFile=/etc/traefik/traefik.yml
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik.yml:/etc/traefik/traefik.yml
      - ./acme.json:/acme.json
    networks:
      - traefik

networks:
  traefik:
    external: true
```

**Key Components:**

- **Ports**: Exposes HTTP (80), HTTPS (443), and Traefik Dashboard (8080).
- **Volumes**:
  - Docker socket for container management.
  - `traefik.yml` for Traefik's configuration.
  - `acme.json` for storing SSL certificates.
- **Networks**: Connects Traefik to a dedicated network named `traefik`.

### Creating the Traefik Network

Before deploying, create the network with the Docker CLI:

```bash
docker network create traefik
```

## Traefik Configuration (`traefik.yml`)

The `traefik.yml` configures entry points and SSL certificates through ACME (Let's Encrypt).

### Sample `traefik.yml`

```yaml
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

certificatesResolvers:
  myresolver:
    acme:
      email: your-email@example.com
      storage: acme.json
      httpChallenge:
        entryPoint: web

providers:
  docker:
    exposedByDefault: false
```
### Important Notes:

- **ACME Configuration**: Essential for automatic HTTPS. Traefik will communicate with Let's Encrypt to issue and renew certificates as needed.
- **`email`**: Used by Let's Encrypt for important notifications.
- **`storage`**: Points to `acme.json`, which securely stores your certificates.


## Preparing `acme.json`

Create an empty `acme.json` file with restricted permissions to securely store your SSL certificates:

```bash
touch acme.json
chmod 600 acme.json
```

This step is vital for security, ensuring that your certificates are kept confidential.


## Deploying Traefik

With the configuration files prepared (`traefik.yml` and `acme.json`), and the dedicated network created, deploy Traefik using Docker Compose:

```bash
docker compose up -d
```

## Securing Services with HTTPS: Examples

Deploy an example Nginx service, using Traefik labels to enable HTTPS.

### Docker Compose for Nginx

```yaml
version: '3'
services:
  nginx_test:
    image: nginx
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx.rule=Host(`test.yourdomain.com`)"
      - "traefik.http.routers.nginx.entrypoints=websecure"
      - "traefik.http.routers.nginx.tls=true"
      - "traefik.http.routers.nginx.tls.certresolver=myresolver"
    networks:
      - traefik

networks:
  traefik:
    external: true
```

### Docker Compose for Wordpress

Deploy an example Wordpress service, using Traefik labels to enable HTTPS.

```yaml
services:
  db:
    # We use a mariadb image which supports both amd64 & arm64 architecture
    image: mariadb:10.6.4-focal
    # If you really want to use MySQL, uncomment the following line
    #image: mysql:8.0.27
    command: '--default-authentication-plugin=mysql_native_password'
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=somewordpress
      - MYSQL_DATABASE=wordpress
      - MYSQL_USER=wordpress
      - MYSQL_PASSWORD=wordpress
    networks:
      - traefik
  wordpress:
    image: wordpress:latest
    volumes:
      - wp_data:/var/www/html
    restart: always
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER=wordpress
      - WORDPRESS_DB_PASSWORD=wordpress
      - WORDPRESS_DB_NAME=wordpress
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.wordpress.rule=Host(`wordpress.elitron.xyz`)"
      - "traefik.http.routers.wordpress.entrypoints=websecure"
      - "traefik.http.routers.wordpress.tls=true"
      - "traefik.http.routers.wordpress.tls.certresolver=myresolver"
    networks:
      - traefik

networks:
  traefik:
    external: true

volumes:
  db_data:
  wp_data:
```

**Highlights:**

- **Labels**: Configure routing rules, entry points, and TLS settings specific to the Nginx service.
- **Networks**: Ensures Nginx is on the same network as Traefik for proper routing.

## Deployment Process

1. **Prepare Configuration Files**: Create `traefik.yml` and an empty `acme.json` file with restrictive permissions (`chmod 600 acme.json`).
2. **Deploy Traefik**: Use `docker compose up -d` in the directory containing your Traefik `docker-compose.yml`.
3. **Verify Traefik Operation**: Access the Traefik Dashboard via `http://your-host:8080`.
4. **Deploy Services**: Repeat the deployment process for your services, ensuring they include the appropriate Traefik labels.

This guide provides a structured approach to deploying Traefik with Docker Compose, creating a secure environment for hosting web services with automatic HTTPS configuration.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
