<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Setting Up Hoarder with Docker Compose
description: Hoarder is a self-hosted application for managing and organizing content efficiently. This guide explains how to deploy Hoarder using Docker Compose.
---

# Setting Up Hoarder with Docker Compose

## Introduction to Hoarder

Hoarder is a self-hosted application designed to help users manage and organize their content effortlessly. It integrates powerful tools like MeiliSearch and Alpine Chrome to enhance content indexing and browsing. This guide will walk you through the deployment of Hoarder using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed on your system.
- Basic understanding of Docker Compose files.
- A `.env` file with required environment variables.

## Docker Compose Configuration for Hoarder

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  web:
    image: ghcr.io/hoarder-app/hoarder:${HOARDER_VERSION:-release}
    restart: unless-stopped
    volumes:
      - data:/data
    ports:
      - 3000:3000
    env_file:
      - .env
    environment:
      MEILI_ADDR: http://meilisearch:7700
      BROWSER_WEB_URL: http://chrome:9222
      # OPENAI_API_KEY: ...
      DATA_DIR: /data

  chrome:
    image: gcr.io/zenika-hub/alpine-chrome:123
    restart: unless-stopped
    command:
      - --no-sandbox
      - --disable-gpu
      - --disable-dev-shm-usage
      - --remote-debugging-address=0.0.0.0
      - --remote-debugging-port=9222
      - --hide-scrollbars

  meilisearch:
    image: getmeili/meilisearch:v1.11.1
    restart: unless-stopped
    env_file:
      - .env
    environment:
      MEILI_NO_ANALYTICS: "true"
    volumes:
      - meilisearch:/meili_data

volumes:
  meilisearch:
  data:
```

### Environment Variables (`.env`)

```env
HOARDER_VERSION=release
NEXTAUTH_SECRET=YourRandomSecureKey
MEILI_MASTER_KEY=YourMeiliMasterKey
NEXTAUTH_URL=http://yourdomain.com:3000
```

- Replace `YourRandomSecureKey` with a securely generated secret (e.g., using `openssl rand -base64 32`).
- Replace `YourMeiliMasterKey` with a securely generated key for MeiliSearch.
- Update `NEXTAUTH_URL` with your domain or IP address and port.

## Key Components of the Configuration

### Service: `web` (Hoarder)
- **Image**: `ghcr.io/hoarder-app/hoarder:${HOARDER_VERSION:-release}`
- **Ports**: Maps `3000:3000` for accessing Hoarder’s web interface.
- **Environment Variables**:
  - `MEILI_ADDR`: URL of the MeiliSearch service.
  - `BROWSER_WEB_URL`: URL of the Alpine Chrome browser debugging service.
  - `DATA_DIR`: Directory for storing Hoarder’s data.

### Service: `chrome` (Alpine Chrome)
- **Image**: `gcr.io/zenika-hub/alpine-chrome:123`
- **Command**: Configures Chrome for headless operation with remote debugging.

### Service: `meilisearch`
- **Image**: `getmeili/meilisearch:v1.11.1`
- **Environment Variables**:
  - `MEILI_NO_ANALYTICS`: Disables analytics for privacy.

### Volumes
- `meilisearch`: Stores MeiliSearch data persistently.
- `data`: Stores Hoarder’s data persistently.

## Preparing for Deployment

1. **Prepare the `.env` File**: Fill out the `.env` file with secure keys and URLs as described above.
2. **Review Configuration**: Ensure the `docker-compose.yml` and `.env` files are correctly set up for your environment.

## Deploying Hoarder

1. Save the configuration in a `docker-compose.yml` file and create the `.env` file in the same directory.
2. Run the following command to start Hoarder and its dependencies:
   ```bash
   docker compose up -d
   ```
3. Access Hoarder at `http://yourdomain.com:3000` (replace with your actual domain or IP and port).

## Post-Deployment Tips

- **Reverse Proxy**: For improved security and accessibility, consider using a reverse proxy (e.g., Nginx or Traefik) to serve Hoarder over HTTPS.
- **OpenAI API Key**: If you plan to integrate OpenAI features, set the `OPENAI_API_KEY` in the `.env` file.
- **Secure Your Setup**: Use strong passwords and secrets for all environment variables.

## Troubleshooting

- **Service Not Starting**: Check for missing or incorrect values in the `.env` file.
- **Connection Issues**: Verify that the `MEILI_ADDR` and `BROWSER_WEB_URL` are correctly configured and accessible.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>