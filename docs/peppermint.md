---
title: Setting Up Peppermint with Docker Compose
description: Peppermint is a self-hosted ticketing and knowledge base solution. This guide explains how to deploy Peppermint using Docker Compose.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Setting Up Peppermint with Docker Compose

## Introduction to Peppermint

Peppermint is a self-hosted application designed to streamline support ticketing and knowledge management, providing a simple, efficient solution for customer support teams. This guide details how to set up Peppermint using Docker Compose for easy deployment.

## Prerequisites

- Docker and Docker Compose installed on your system.
- Basic familiarity with Docker Compose configurations.

## Docker Compose Configuration for Peppermint

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  peppermint_postgres:
    container_name: peppermint_postgres
    image: postgres:latest
    restart: always
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: peppermint
      POSTGRES_PASSWORD: securepassword
      POSTGRES_DB: peppermint

  peppermint:
    container_name: peppermint
    image: pepperlabs/peppermint:latest
    ports:
      - 3000:3000
      - 5003:5003
    restart: always
    depends_on:
      - peppermint_postgres
    environment:
      DB_USERNAME: "peppermint"
      DB_PASSWORD: "securepassword"
      DB_HOST: "peppermint_postgres"
      SECRET: "YourSecureSecretKey"

volumes:
  pgdata:
```

### Environment Variables Explained

- **POSTGRES_USER**: Database username (set securely).
- **POSTGRES_PASSWORD**: Secure password for the PostgreSQL database.
- **POSTGRES_DB**: Database name used by Peppermint.
- **DB_USERNAME/DB_PASSWORD/DB_HOST**: Connection details for Peppermint to communicate with PostgreSQL.
- **SECRET**: Secure key used by Peppermint for encryption and security purposes. Generate a strong random key.

## Deployment Steps

### Step 1: Prepare Your Docker Compose File

- Create a directory for Peppermint deployment.
- Save the provided `docker-compose.yml` file within this directory.

### Step 2: Customize Your Environment Variables

- Replace `securepassword` and `YourSecureSecretKey` with securely generated credentials.

### Step 3: Deploy Peppermint

Run the following command in your deployment directory to start the containers:

```bash
docker compose up -d
```

## Accessing Peppermint

- Once running, Peppermint will be accessible via:

```
http://yourdomain.com:3000
```

Replace `yourdomain.com` with your actual domain name or IP address.

## Post-Deployment Recommendations

- **Secure Your Deployment**: Implement HTTPS using a reverse proxy like Nginx or Traefik for secure, encrypted communication.
- **Regular Backups**: Ensure regular backups of your database (`pgdata` volume) to avoid data loss.

## Troubleshooting Common Issues

- **Database Connection Issues**: Confirm database credentials (`DB_USERNAME`, `DB_PASSWORD`, and `DB_HOST`) match in both the PostgreSQL and Peppermint configurations.
- **Containers Not Starting**: Verify volume permissions and environment variable configurations are correct.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

