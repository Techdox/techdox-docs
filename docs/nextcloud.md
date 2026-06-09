---
title: Setting Up Nextcloud with Docker Compose
description: Nextcloud is an open-source, self-hosted file share and collaboration platform. It provides a secure and private alternative to cloud-based storage services.
---

# Setting Up Nextcloud with Docker Compose

## Introduction to Nextcloud

Nextcloud is an open-source, self-hosted file share and collaboration platform. It provides a secure and private alternative to cloud-based storage services.

## Docker Compose Configuration for Nextcloud

This setup includes Nextcloud and a MariaDB database, ensuring an isolated and manageable environment.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '2'

volumes:
  nextcloud:
  db:

services:
  db:
    image: mariadb:10.6
    restart: always
    command: --transaction-isolation=READ-COMMITTED --log-bin=binlog --binlog-format=ROW
    volumes:
      - db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=<ENTER PASSWORD HERE>
      - MYSQL_PASSWORD=<ENTER PASSWORD HERE>
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  app:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
    volumes:
      - nextcloud:/var/www/html
    environment:
      - MYSQL_PASSWORD=<ENTER PASSWORD HERE>
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_HOST=db
```

## Key Components of the Configuration

### Volumes
- `nextcloud`: Stores Nextcloud's data.
- `db`: Stores the MariaDB database files.

### Services
#### `db`
- **Image**: `mariadb:10.6`
- **Restart**: Always ensures the container restarts after a crash or reboot.
- **Command**: Configures MariaDB for optimal use with Nextcloud.
- **Volumes**: Maps `db` volume to MariaDB data directory.
- **Environment Variables**: Set the MySQL root and Nextcloud user passwords, database, and user.

#### `app`
- **Image**: `nextcloud`
- **Restart**: Always ensures the container restarts after a crash or reboot.
- **Ports**: Maps port 8080 of the host to port 80 of the container.
- **Links**: Connects to the `db` service.
- **Volumes**: Maps `nextcloud` volume to Nextcloud's HTML directory.
- **Environment Variables**: Set the database details for Nextcloud to connect to MariaDB.

## Deploying Nextcloud

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Replace `<ENTER PASSWORD HERE>` with your chosen passwords.
3. Run `docker compose up -d` to start Nextcloud in detached mode.
4. Access Nextcloud via `http://<host-ip>:8080`.

## Configuring and Using Nextcloud

After deployment, configure your Nextcloud instance through its web interface. This includes admin account setup, storage management, and app configurations.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/1NXI15cQa8k?si=BVOFk712q5014U9U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
