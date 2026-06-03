---
title: Deploying Speedtest Tracker with Docker Compose
description: Speedtest Tracker is a self-hosted internet performance tracking application that runs speedtest checks against Ookla's Speedtest service.
---

## Deployment of Speedtest Tracker

This section guides you through the setup of Speedtest Tracker using Docker Compose. Speedtest Tracker runs scheduled speed tests and provides a web-based interface to view the results.

!!!note
    Offical Docs - [Speedtest Tracker Documentation](https://docs.speedtest-tracker.dev)

### Docker Compose Configuration

Here's the Docker Compose file necessary for deploying the Speedtest Tracker service. Save this configuration as `docker-compose.yml` in your project directory.

```yaml
version: '3.8'
services:
  speedtest-tracker:
    container_name: speedtest-tracker
    image: lscr.io/linuxserver/speedtest-tracker:latest
    ports:
      - '8072:80'   # Maps port 80 inside the container to port 8072 on the host for HTTP access.
      - '8472:443'  # Maps port 443 inside the container to port 8472 on the host for HTTPS access.
    environment:
      - PUID=1000  # Sets the user ID the service will run as.
      - PGID=1000  # Sets the group ID the service will run as.
      - APP_KEY=base64:s5xs13....  # Application key for Laravel framework security. Generate a App Key here - https://speedtest-tracker.dev
      - APP_URL=https://speedtest.yoursite/localIP.com  # Public URL where the Speedtest Tracker will be accessible.
      - DB_CONNECTION=sqlite  # Uses SQLite as the database.
      - SPEEDTEST_SCHEDULE="0 */3 * * *"  # Cron schedule, runs every 3 hours.
      - DISPLAY_TIMEZONE=Pacific/Auckland  # Sets the timezone for displaying data in the UI.
    volumes:
      - ./data:/config  # Mounts the directory for persistent data.
      - ./ssl-keys:/config/keys  # Mounts the directory for SSL keys.
    restart: unless-stopped  # Ensures the container restarts unless it is explicitly stopped.
```

### Deployment Instructions

1. **Prepare the Environment**:
   Ensure Docker and Docker Compose are installed on your host machine.

2. **Create a Docker Compose File**:
   Create a new file named `docker-compose.yml` and copy the above content into this file.

3. **Prepare Data and SSL Directories**:
   Create the `data` and `ssl-keys` directories in the same directory as your `docker-compose.yml`. This ensures proper permissions and data persistence.

4. **Start the Container**:
   Navigate to the directory containing your `docker-compose.yml` and run the following command to start Speedtest Tracker:
   ```bash
   docker compose up -d
   ```
   This command will start the Speedtest Tracker in detached mode, allowing it to run in the background.

5. **Access the Web Interface**:
   Once the container is running, access the Speedtest Tracker web interface by navigating to `http://localhost:8072` or `https://localhost:8472` depending on your setup.

```bash
default login
Username: admin@example.com
Password: password
```

### Additional Notes

- Make sure the ports in the `docker-compose.yml` do not conflict with other services on your host.
- Adjust the `SPEEDTEST_SCHEDULE` environment variable to change the frequency of speed tests as needed.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
