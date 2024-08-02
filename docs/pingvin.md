# Deploying Pingvin Share with Docker Compose

## Introduction to Pingvin Share

Pingvin Share is a lightweight file sharing service, making it easy to host and share files through a simple and intuitive web interface. This guide will walk you through setting up Pingvin Share on your server using Docker Compose.

## Docker Compose Configuration

### Docker Compose File (`docker-compose.yml`)

Here's the Docker Compose configuration for deploying Pingvin Share:

```yaml
version: '3.8'
services:
  pingvin-share:
    image: stonith404/pingvin-share
    restart: unless-stopped
    ports:
      - 3000:3000  # Exposes Pingvin Share on port 3000 of the host machine.
    volumes:
      - "./data:/opt/app/backend/data"  # Maps the host directory './data' to the container's data storage.
      - "./data/images:/opt/app/frontend/public/img"  # Specific path for image storage within the same data directory.
```

### Configuration Details

- **Ports**: The service is made available on port 3000 of the host, allowing you to access Pingvin Share via `http://your-host-ip:3000`.
- **Volumes**:
  - `./data:/opt/app/backend/data`: This volume mounts a host directory to the container where Pingvin Share stores its data files.
  - `./data/images:/opt/app/frontend/public/img`: This maps a subdirectory of the same host directory specifically for storing images used by the Pingvin Share frontend.

## Preparing Volume Directories

Before deploying the service, it's essential to create the necessary directories on the host machine. This prevents Docker from automatically creating them with `root` ownership, which could lead to permission issues.

### Creating Directories

Run the following commands in the terminal to create the directories with the appropriate permissions:

```bash
mkdir -p ./data/images
```

- **`mkdir -p ./data/images`**: Creates the `data` directory and the `images` subdirectory.

## Deployment

Once the directories are prepared, you can deploy Pingvin Share using Docker Compose:

```bash
docker compose up -d
```

This command starts the Pingvin Share service in detached mode, running in the background.

## Accessing Pingvin Share

After deployment, Pingvin Share will be accessible via `http://your-host-ip:3000`. You can start uploading and sharing files immediately through its web interface.

## Conclusion

Setting up Pingvin Share with Docker Compose is straightforward, provided the necessary directories are prepared in advance to avoid permission issues. This setup allows you to host a private file sharing service, enhancing your control over file distribution and access within your network.
