---
title: Setting Up PrivateBin with Docker Compose
description: PrivateBin is a secure, minimalist, open-source online pastebin where the server has zero knowledge of pasted data. It allows you to share sensitive information securely and anonymously.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Setting Up PrivateBin with Docker Compose

## Introduction to PrivateBin

PrivateBin is a secure, minimalist, open-source online pastebin where the server has zero knowledge of pasted data. It allows you to share sensitive information securely and anonymously.

!!! note

    **PrivateBin must run via HTTPS**

## Docker Compose Configuration for PrivateBin

This Docker Compose setup deploys PrivateBin using the `privatebin/nginx-fpm-alpine` image in a Docker container, ensuring a secure environment for sharing texts and files.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  privatebin:
    image: privatebin/nginx-fpm-alpine
    restart: always
    read_only: true
    user: "1000:1000"  # Run the container with the UID:GID of your Docker user
    ports:
      - "8082:8080"
    volumes:
      - ./privatebin-data:/srv/data
```

## Key Components of the Configuration

### Service: PrivateBin
- **Image**: `privatebin/nginx-fpm-alpine` is the Docker image used for PrivateBin.
- **Restart Policy**: `always` ensures that the PrivateBin service restarts automatically after a crash or reboot.
- **Read Only**: `read_only: true` enhances security by making the root filesystem read-only.
- **User**: `user: "1000:1000"` specifies the UID and GID for running the container, enhancing security by avoiding running as root.
- **Ports**: 
  - `8082:8080` maps port 8082 on the host to port 8080 in the container, where PrivateBin's web interface is accessible.
- **Volumes**: 
  - `./privatebin-data:/srv/data` provides persistent storage for PrivateBin's data.

## Deploying PrivateBin

1. **Create a Directory for PrivateBin Data**:  
   It's important to manually create a directory for your PrivateBin data before running the Docker Compose command. If you allow Docker to create the directory automatically, it might be created with root ownership, leading to permission issues, especially if Docker is not being run as root. This can cause PrivateBin to not function correctly due to insufficient permissions.
     ```shell
     mkdir -p ./privatebin-data
     ```
!!! note

    **Ensure the directory has the correct permissions by setting the user ID (UID) and group ID (GID) to match the service's configured `user: "1000:1000"` setting.**

2. **Save Docker Compose Configuration**:  
   Save the Docker Compose configuration in a `docker-compose.yml` file within your project directory.

3. **Start PrivateBin**:  
   Run `docker compose up -d` to start PrivateBin in detached mode.

4. **Access PrivateBin**:  
Access PrivateBin by navigating to `http://<host-ip>:8082`.

By following these steps and ensuring the data directory has the correct permissions, you can avoid potential issues and ensure PrivateBin functions correctly.

## Understanding the PrivateBin Data Directory

After setting up PrivateBin, various files and directories within the `privatebin-data` directory play crucial roles in the application's functionality and security. Here's a breakdown of these components:

### `salt.php`

- **Purpose**: Contains the server salt used by PrivateBin.
- **Functionality**: A salt is a random piece of data used as an additional input to a one-way function that hashes data, passwords, or passphrases. In the context of PrivateBin, it enhances security by ensuring that encrypted data stored on the server cannot be decrypted without the correct salt, which is known only to the client.

### `traffic_limiter.php` and `purge_limiter.php`

- **Purpose**: These files are instrumental in limiting the rate of traffic and purging operations to the server.
- **Functionality**:
  - **`traffic_limiter.php`**: Contains data or logic to track and limit the amount of data traffic (e.g., paste creation and retrieval) to avoid denial of service attacks or excessive load.
  - **`purge_limiter.php`**: Tracks the purge operations to prevent mass deletion of data, which could also impact server performance.

### `d7` (directory)

- **Purpose**: Part of the storage structure used by PrivateBin to organize encrypted paste files.
- **Functionality**: PrivateBin typically stores pastes as files on the server, organizing them into directories like `d7` to optimize file system performance and management.

## Managing the PrivateBin Data Directory

It's important to regularly back up and monitor the contents of the `privatebin-data` directory to ensure data integrity and application security. Proper management of this directory supports the overall health of your PrivateBin deployment.


## Configuring and Using PrivateBin

After deployment, PrivateBin is ready to use with minimal configuration required. Access the web interface to start sharing texts and files securely.


<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
