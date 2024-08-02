---
title: Setting Up PhotoPrism with Docker Compose
description: Learn how to deploy PhotoPrism using Docker Compose to easily manage your photo collections with powerful AI capabilities.
---

## PhotoPrism Docker Compose Setup

This configuration sets up PhotoPrism, a personal photo management solution. It includes important notes on memory requirements, security considerations for public deployments, and advanced configuration options.

### Docker Compose Configuration

Below is the Docker Compose file you will need. Copy this into a `docker-compose.yml` file in your project directory:

```yaml
version: '3.9'
services:
  photoprism:
    image: photoprism/photoprism:latest
    ports:
      - '2342:2342' # Port mapping Host:Container for HTTP access
    environment:
      PHOTOPRISM_ADMIN_USER: "admin"  # Admin username for initial setup
      PHOTOPRISM_ADMIN_PASSWORD: "insecure"  # Initial admin password, change this!
      PHOTOPRISM_SITE_URL: "http://localhost:2342/"  # Public URL for your instance
      # Other environmental variables as per your configuration needs
    volumes:
      - "./photos:/photoprism/originals"  # Path to your photos
      - "./storage:/photoprism/storage"  # Persistent storage for thumbnails, database
    depends_on:
      - mariadb  # Ensure that the database is started first

  mariadb:
    image: mariadb:10.5  # Recommended MariaDB version
    environment:
      MYSQL_ROOT_PASSWORD: "database_password"  # Root password for MariaDB
      MYSQL_DATABASE: "photoprism"  # Database name for PhotoPrism
      MYSQL_USER: "photoprism"  # Database user for PhotoPrism
      MYSQL_PASSWORD: "database_password"  # Password for the PhotoPrism database user
    volumes:
      - "./database:/var/lib/mysql"  # Persistent storage for the database
```

### Configuration Notes

- **Memory Management**: PhotoPrism should run on a server with at least 4 GB of RAM and sufficient swap space to handle large files and intensive processes without crashing.
- **Security**: If deploying publicly, ensure that PhotoPrism is behind an HTTPS reverse proxy like Traefik or Caddy to secure your data and credentials.
- **Database**: Using MariaDB provides better performance than SQLite and is recommended for production environments.
- **Environment Variables**: Customize the environment variables according to your needs. For detailed configuration options, visit [PhotoPrism Configuration Options](https://docs.photoprism.app/getting-started/config-options/).

### Deployment Instructions

1. **Prepare Your Environment**: Make sure Docker and Docker Compose are installed on your host.
2. **Configure Volumes**: Create directories for photos and database if they do not already exist to ensure data persistence.
3. **Launch PhotoPrism**:
   Navigate to the directory containing your `docker-compose.yml` file and run:
   ```bash
   docker compose up -d
   ```
This command starts PhotoPrism in detached mode, running in the background.

4. **Access PhotoPrism**: Once the services are up and running, you can access PhotoPrism through http://localhost:2342 or the domain you have configured.

