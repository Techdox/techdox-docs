---
title: Setting Up Joplin with Docker Compose
description: Joplin Server is a self-hosted sync server for Joplin notes, allowing you to sync across multiple devices securely and privately.
---

# Setting Up Joplin Server with Docker Compose

## Introduction to Joplin Server

Joplin Server acts as a self-hosted synchronization server for Joplin notes. It allows you to synchronize your notes across multiple devices securely and privately.

## Docker Compose Configuration for Joplin Server

This Docker Compose setup deploys Joplin Server along with a PostgreSQL database, ensuring a robust and isolated environment for your notes.

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
    db:
        image: postgres:16
        volumes:
            - ./data/postgres:/var/lib/postgresql/data
        ports:
            - "5432:5432"
        restart: unless-stopped
        environment:
            - POSTGRES_PASSWORD=testing123
            - POSTGRES_USER=joplin
            - POSTGRES_DB=joplindb
    app:
        image: joplin/server:latest
        depends_on:
            - db
        ports:
            - "22300:22300"
        restart: unless-stopped
        environment:
            - APP_PORT=22300
            - APP_BASE_URL=http://192.168.68.105:22300
            - DB_CLIENT=pg
            - POSTGRES_PASSWORD=testing123
            - POSTGRES_DATABASE=joplindb
            - POSTGRES_USER=joplin
            - POSTGRES_PORT=5432
            - POSTGRES_HOST=db
```

!!! warning "Update APP_BASE_URL"
    The `APP_BASE_URL` is set to the author's private server IP. **Replace `192.168.68.105:22300` with your own server's IP or hostname**, e.g. `http://YOUR_SERVER_IP:22300`. Using the wrong URL causes "invalid origin" errors on all clients.

!!! warning "Change the database password"
    The password `testing123` appears in two places in this compose file (both the `joplin` and `db` service blocks). **Replace it with a strong, unique password in both locations before deploying.**

!!! warning "Database port exposed to host"
    Port 5432 is mapped to the host, making the PostgreSQL database directly accessible on your network. Remove the `ports:` block from the `db` service if you don't need direct database access from outside Docker.

## Key Components of the Configuration

### Services:

- **db (PostgreSQL)**: Stores Joplin Server data.
  - **Ports**: Exposes PostgreSQL on port `5432`.
  - **Environment**: Configures the database credentials and database name.

- **app (Joplin Server)**: The main Joplin Server application.
  - **Ports**: Exposes Joplin Server on port `22300`.
  - **Environment**: Configures the application to communicate with the PostgreSQL database.

### Initial Login Credentials

- **Username**: `admin@localhost`
- **Password**: `admin`

These are the default login credentials for Joplin Server upon the first run. It's strongly recommended to change these credentials after your initial login to ensure the security of your instance.

## Deployment Instructions

1. **Prepare Environment**:
   - Create a directory named `data` on your host to ensure data persistence for PostgreSQL.
   - Ensure your `.env` file or Docker Compose environment variables are correctly set.

2. **Launch Services**:
   - Use Docker Compose to start the services:
     ```bash
     docker compose up -d
     ```
   - After startup, Joplin Server will be accessible at the `APP_BASE_URL` you've configured, e.g., `http://192.168.68.105:22300`.

!!! warning "Using a Reverse Proxy or Cloudflare?"
    If you are exposing Joplin Server via a reverse proxy (Nginx Proxy Manager, Traefik) or Cloudflare, you **must** update `APP_BASE_URL` to your public domain — for example:

    ```yaml
    - APP_BASE_URL=https://joplin.yourdomain.com
    ```

    Joplin Server uses `APP_BASE_URL` to validate the origin of incoming requests. If the URL doesn't match the host your clients connect to, you will get an **"invalid origin"** error. Make sure the value uses the correct scheme (`https://` when TLS is terminated by the proxy) and does **not** include a trailing slash.

## Initial Setup and Synchronization Configuration

After successfully deploying Joplin Server and logging in with the default credentials (`admin@localhost` / `admin`), it's important to secure your instance and configure your Joplin applications (desktop, mobile) to synchronize with your self-hosted server.

### Secure Your Joplin Server Instance

1. **Change Admin Credentials**: Navigate to the settings through the Joplin Server web interface. Update the admin username and password to secure your Joplin Server instance.

### Configure Synchronization in Joplin Applications

To synchronize your Joplin notes across devices using your self-hosted Joplin Server:

1. **Open Joplin Application Settings**: On each Joplin application (desktop or mobile), go to the settings or configuration section.

2. **Select Synchronization Target**:
    - Find the **Synchronization** settings.
    - Under **Synchronization target**, select **Joplin Server** from the dropdown menu.

3. **Enter Server URL**:
    - In the **URL** field, enter your Joplin Server's URL, which is the `APP_BASE_URL` you set in your Docker Compose file (e.g., `http://192.168.68.105:22300`).

4. **Input Credentials**:
    - Enter the username and password you have set for your Joplin Server admin account.

5. **Apply Changes**: Click **Apply**, **OK**, or similar to save your synchronization settings.

6. **Initiate Synchronization**: Use the synchronize button or feature within your Joplin application to start syncing your notes with your self-hosted Joplin Server.

By following these steps, you will have configured your Joplin applications to synchronize with your self-hosted Joplin Server, ensuring that your notes are up-to-date across all your devices. This setup provides a private and secure way to manage and sync your notes.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
