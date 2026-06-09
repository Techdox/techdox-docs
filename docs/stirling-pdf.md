---
title: Setting Up Stirling PDF with Docker Compose
description: Stirling PDF is a self-hosted PDF toolbox for merging, splitting, compressing, converting, OCRing, signing, and editing PDFs from your own server.
---

# Setting Up Stirling PDF with Docker Compose

## Introduction to Stirling PDF

Stirling PDF is a self-hosted web app for working with PDF files. It gives you a browser-based toolbox for common PDF jobs without uploading private documents to random online PDF sites.

You can use it to:

- Merge and split PDFs
- Compress large PDFs
- Convert images, Office documents, and other files to PDF
- Convert PDFs to images
- OCR scanned documents
- Rotate, crop, reorder, and remove pages
- Add or remove passwords
- Sign PDFs
- Clean up PDF metadata
- Use the Stirling PDF desktop app with a self-hosted backend

This is a good fit for homelabs because PDF tools are useful, but the files are often sensitive: bank statements, invoices, contracts, receipts, medical documents, and house paperwork.

!!! warning
    Treat uploaded PDFs as sensitive. Keep Stirling PDF on a trusted network, enable login if other people can reach it, and do not expose it directly to the public internet without authentication and HTTPS.

---

## Prerequisites

Before starting, make sure you have:

- Docker installed
- Docker Compose installed
- A server or VM to host the container
- A local folder where the Stirling PDF config and logs will live

This guide uses port `8090` on the host. Change it if that port is already in use.

---

## Docker Compose Configuration for Stirling PDF

Create a project directory:

```bash
mkdir -p /opt/stirling-pdf
cd /opt/stirling-pdf
mkdir -p trainingData extraConfigs customFiles logs pipeline
```

Create an environment file for the initial admin account:

```bash
nano .env
```

Add the following values:

```env
STIRLING_ADMIN_USER=admin
STIRLING_ADMIN_PASSWORD=change-this-password
```

Generate a stronger password if you want one quickly:

```bash
openssl rand -base64 32
```

!!! warning "Keep `.env` private"
    The `.env` file contains the initial admin password. Do not commit it to Git or share it publicly.

---

## Docker Compose File (`docker-compose.yml`)

Create the Compose file:

```bash
nano docker-compose.yml
```

Paste the following:

```yaml
services:
  stirling-pdf:
    image: stirlingtools/stirling-pdf:latest
    container_name: stirling-pdf
    restart: unless-stopped
    ports:
      - "8090:8080"
    volumes:
      - ./trainingData:/usr/share/tessdata
      - ./extraConfigs:/configs
      - ./customFiles:/customFiles
      - ./logs:/logs
      - ./pipeline:/pipeline
    environment:
      SECURITY_ENABLELOGIN: "true"
      DOCKER_ENABLE_SECURITY: "true"
      DISABLE_ADDITIONAL_FEATURES: "false"
      SECURITY_INITIALLOGIN_USERNAME: "${STIRLING_ADMIN_USER}"
      SECURITY_INITIALLOGIN_PASSWORD: "${STIRLING_ADMIN_PASSWORD}"
      LANGS: "en_GB,en_US"
      SYSTEM_DEFAULTLOCALE: "en-GB"
```

!!! note "Login and desktop app support"
    Login is enabled in this example. The Stirling PDF desktop app expects an authenticated backend, so keeping login enabled is the safer default if you plan to connect the desktop app to your self-hosted server.

---

## Key Components of the Configuration

| Setting | Purpose |
| --- | --- |
| `8090:8080` | Exposes Stirling PDF on port `8090` of the host |
| `./extraConfigs:/configs` | Stores settings, database, generated keys, and app configuration |
| `./trainingData:/usr/share/tessdata` | Optional OCR language data location |
| `./customFiles:/customFiles` | Custom static files and branding |
| `./logs:/logs` | Application logs |
| `./pipeline:/pipeline` | Watched folders and automation pipeline files |
| `SECURITY_ENABLELOGIN=true` | Enables user login and admin features |
| `DISABLE_ADDITIONAL_FEATURES=false` | Keeps the additional/login-enabled feature set available |
| `SECURITY_INITIALLOGIN_*` | Sets the initial admin username and password |

---

## Deploying Stirling PDF

Start the container:

```bash
docker compose pull
docker compose up -d
```

Check that it is running:

```bash
docker compose ps
```

Check the health endpoint:

```bash
curl http://localhost:8090/api/v1/info/status
```

A healthy response looks like this:

```json
{"version":"2.11.0","status":"UP"}
```

The version number may be different depending on when you deploy it.

---

## Accessing Stirling PDF

Open a browser and go to:

```text
http://<server-ip>:8090
```

Log in with the admin credentials from your `.env` file.

After logging in, change the password in the account settings.

!!! tip
    If you only use this on your LAN or VPN, a local IP address is fine. If you want a nicer URL, put it behind a reverse proxy such as Nginx Proxy Manager and use an internal hostname like `pdf.example.com`.

---

## Connecting the Stirling PDF Desktop App

Stirling PDF also has a desktop app that can connect to your self-hosted server.

Use the full server URL:

```text
http://<server-ip>:8090
```

If the app says login is not enabled, confirm your Compose file has:

```yaml
SECURITY_ENABLELOGIN: "true"
DISABLE_ADDITIONAL_FEATURES: "false"
```

Then restart the container:

```bash
docker compose restart
```

If you are using a reverse proxy, make sure the desktop app points to the backend server URL, not a separate frontend-only URL.

---

## Reverse Proxy Notes

If you put Stirling PDF behind Nginx Proxy Manager, Caddy, Traefik, or another reverse proxy, proxy the hostname to:

```text
http://<server-ip>:8090
```

For Nginx Proxy Manager, create a Proxy Host with:

| Field | Value |
| --- | --- |
| Scheme | `http` |
| Forward Hostname / IP | `<server-ip>` |
| Forward Port | `8090` |
| Websockets Support | Optional |
| Block Common Exploits | Enabled |

!!! warning "Do not publish it casually"
    Stirling PDF processes uploaded files. If you expose it outside your LAN/VPN, use HTTPS, strong passwords, and preferably additional access controls such as VPN, SSO, or an allowlist.

---

## Running Without Login

If you only run Stirling PDF on a trusted LAN and want a no-login web UI, you can disable login:

```yaml
SECURITY_ENABLELOGIN: "false"
DISABLE_ADDITIONAL_FEATURES: "false"
```

Restart the container after changing the setting:

```bash
docker compose restart
```

!!! note
    The desktop app may require login to be enabled when connecting to a self-hosted backend. If you plan to use the desktop app, keep login enabled.

---

## Updating Stirling PDF

Update the container with:

```bash
cd /opt/stirling-pdf
docker compose pull
docker compose up -d
```

Check the logs if it does not start correctly:

```bash
docker compose logs -f stirling-pdf
```

---

## Backing Up Stirling PDF

Back up the project directory, especially:

```text
/opt/stirling-pdf/extraConfigs
/opt/stirling-pdf/.env
```

The `extraConfigs` directory contains the app database, generated keys, settings, and backup files.

!!! warning
    Keep `.env` private. It contains credentials.

---

## Troubleshooting

### Browser works, but the desktop app cannot connect

Check the backend health endpoint from the same machine running the desktop app:

```text
http://<server-ip>:8090/api/v1/info/status
```

If that does not return a JSON status response, the desktop app cannot reach the backend either.

### Desktop app says login is not enabled

Enable login:

```yaml
SECURITY_ENABLELOGIN: "true"
DISABLE_ADDITIONAL_FEATURES: "false"
```

Then restart the container:

```bash
docker compose restart
```

### The web UI returns `401 Unauthorized`

That usually means login is enabled. Open the normal web URL and sign in:

```text
http://<server-ip>:8090
```

### Large uploads fail behind a reverse proxy

Increase the maximum upload size in your reverse proxy. Stirling PDF can handle large files, but the proxy may reject the upload first.

---

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
