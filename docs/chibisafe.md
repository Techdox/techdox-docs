---
title: Setting Up Chibisafe with Docker Compose
description: Chibisafe is a file uploader and manager that's easy to use, allowing for the quick and secure sharing of files. It's a self-hosted solution for those who need control over their file-sharing environment.
---

# Setting Up Chibisafe with Docker Compose

## Introduction to Chibisafe

Chibisafe is a file uploader and manager that's easy to use, allowing for the quick and secure sharing of files. It's a self-hosted solution for those who need control over their file-sharing environment.

## Docker Compose Configuration for Chibisafe

This Docker Compose setup deploys Chibisafe in a Docker container, streamlining the process of managing and sharing files securely.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "3.7"

services:
  chibisafe:
    image: chibisafe/chibisafe:latest
    container_name: chibisafe
    volumes:
      - ./database:/home/node/chibisafe/database:rw
      - ./uploads:/home/node/chibisafe/uploads:rw
      - ./logs:/home/node/chibisafe/logs:rw
    ports:
      - 24424:8000
    restart: always
```

##Key Components of the Configuration

### Service: Chibisafe
- **Image**: `chibisafe/chibisafe:latest` is the Docker image used for Chibisafe.
- **Volumes**: 
  - `./database:/home/node/chibisafe/database:rw` stores Chibisafe's database files.
  - `./uploads:/home/node/chibisafe/uploads:rw` stores the uploaded files.
  - `./logs:/home/node/chibisafe/logs:rw` stores logs.
  Each of these folders needs to be created manually before starting the container to avoid permission issues.
- **Ports**: 
  - `24424:8000` maps port 24424 on the host to port 8000 in the container, where Chibisafe's web interface is accessible.
- **Restart Policy**: `always` ensures that Chibisafe restarts automatically after a crash or reboot.

## Preparing for Deployment

1. **Manual Directory Creation**: Before running `docker compose up -d`, manually create the `database`, `uploads`, and `logs` directories within the same directory as your `docker-compose.yml` file. This step is important to prevent permission issues that can arise when these directories are automatically created by Docker, possibly under the root user.
   
2. **Defining the App URL**: If you plan to publish Chibisafe publicly, ensure to define the application URL within Chibisafe's configuration. This step is crucial for proper functionality and access.

## Deploying Chibisafe

1. After manually creating the necessary directories, save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Chibisafe in detached mode.
3. Access Chibisafe by navigating to `http://<host-ip>:24424`.

## Configuring and Using Chibisafe

Post-deployment, dive into Chibisafe's settings to customize your file-sharing environment. Remember, the initial setup like directory creation and app URL definition plays a significant role in the smooth operation of Chibisafe.

