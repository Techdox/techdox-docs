---
title: Setting Up Docmost with Docker Compose
description: Docmost is a self-hosted document collaboration and management platform. This guide will help you set up Docmost using Docker Compose for a seamless and secure deployment.
---

# Setting Up Docmost with Docker Compose

## Introduction to Docmost

Docmost is a self-hosted document collaboration and management platform that provides a secure and efficient way to work on and manage your documents. With Docker Compose, deploying and managing Docmost becomes straightforward.

## Docker Compose Configuration for Docmost

This Docker Compose setup includes Docmost, a PostgreSQL database, and Redis, allowing you to run Docmost in a containerized environment.

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  docmost:
    image: docmost/docmost:latest
    depends_on:
      - db
      - redis
    environment:
      APP_URL: 'http://localhost:3090'
      APP_SECRET: '<APP SECRET>'
      DATABASE_URL: 'postgresql://docmost:STRONG_DB_PASSWORD@db:5432/docmost?schema=public'
      REDIS_URL: 'redis://redis:6379'
    ports:
      - "3090:3000"
    restart: unless-stopped
    volumes:
      - docmost:/app/data/storage

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: docmost
      POSTGRES_USER: docmost
      POSTGRES_PASSWORD: STRONG_DB_PASSWORD
    restart: unless-stopped
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7.2-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  docmost:
  db_data:
  redis_data:
```

## Key Components of the Configuration

### Service: Docmost
- **Image**: `docmost/docmost:latest` is the official Docker image for Docmost.
- **Environment Variables**:
  - `APP_URL`: Replace with your domain or local IP/port (e.g., `https://docmost.example.com`).
  - `APP_SECRET`: A secure key generated with `openssl rand -hex 32`, replace with your own key.
  - `DATABASE_URL`: Connection string for the PostgreSQL database.
  - `REDIS_URL`: Connection string for Redis.
- **Ports**: `3090:3000` maps port 3090 on the host to port 3000 in the container for accessing Docmost's web interface.
- **Volumes**: 
  - `docmost:/app/data/storage` stores Docmost's data.

### Service: PostgreSQL
- **Environment Variables**:
  - `POSTGRES_DB`: Name of the database for Docmost.
  - `POSTGRES_USER`: Database username.
  - `POSTGRES_PASSWORD`: Database password (replace `STRONG_DB_PASSWORD` with a secure password).
- **Volumes**:
  - `db_data:/var/lib/postgresql/data` stores PostgreSQL data persistently.

### Service: Redis
- **Volumes**:
  - `redis_data:/data` stores Redis data persistently.

## Preparing for Deployment

1. **Generate a Secure App Secret**: Run `openssl rand -hex 32` to generate a secure value for `APP_SECRET`. Ensure this value is set; leaving it empty will cause deployment to fail.
   
2. **Set the App URL**: Replace `APP_URL` with your chosen domain (e.g., `https://docmost.example.com`) or local IP and port. Using a reverse proxy, even for local setups, is recommended for security and accessibility.

3. **Directory and Volume Preparation**: Docker volumes (`docmost`, `db_data`, `redis_data`) are automatically managed by Docker but ensure the hosting environment has sufficient storage.

## Deploying Docmost

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Docmost and its dependencies in detached mode.
3. Access Docmost at `http://localhost:3090` (or your configured domain).

## Configuring and Using Docmost

After deployment:
- Customize settings via the Docmost web interface to suit your environment.
- For a public deployment, ensure SSL is configured using a reverse proxy like Nginx or Traefik.

## Troubleshooting Tips

- **Database Connection Issues**: Verify that `DATABASE_URL` matches the PostgreSQL configuration.
- **Redis Connection Issues**: Ensure Redis is running and the `REDIS_URL` is correctly defined.
- **Permission Issues**: Ensure Docker has the necessary permissions to create and manage volumes.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise a PR on [GitHub](https://github.com/Techdox/techdox-docs).
