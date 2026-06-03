---
title: Deploying Tududi with Docker Compose  
description: Tududi is a lightweight, open-source task management tool. This guide provides step-by-step instructions for deploying Tududi using Docker Compose, including setting up the required directory, creating a `docker-compose.yml` file, and configuring the environment variables for secure and seamless operation.  
---

# Deploying Tududi with Docker Compose  

## Introduction to Tududi  

[Tududi](https://github.com/chrisvel/tududi) is a simple, yet powerful task management tool designed for personal or small team use. This guide walks you through deploying Tududi using Docker Compose, creating the required directory structure, configuring environment variables, and setting up the `docker-compose.yml` file for deployment.  

## Directory Setup  

To avoid permission conflicts, you need to create a directory for storing Tududi's database before deployment. Replace `<user>` with your actual system username.  

```bash
mkdir -p /home/<user>/docker/tududi/tududi_db
cd /home/<user>/docker/tududi
```

For example, if your username is `techdox`:  

```bash
mkdir -p /home/techdox/docker/tududi/tududi_db
cd /home/techdox/docker/tududi
```

## Creating the `docker-compose.yml` File  

Create a file named `docker-compose.yml` in the `tududi` directory with the following content:  

```yaml
services:
  tududi:
    image: 'chrisvel/tududi:latest'
    ports:
      - '9292:9292'
    volumes:
      - './tududi_db:/usr/src/app/tududi_db'
    environment:
      - TUDUDI_INTERNAL_SSL_ENABLED=false
      - TUDUDI_SESSION_SECRET=2456... <change me>
      - TUDUDI_USER_PASSWORD=mysecurepassword
      - TUDUDI_USER_EMAIL=myemail@example.com
```

### Key Configuration Details  

- **`TUDUDI_INTERNAL_SSL_ENABLED`**: Set to `false` unless you have SSL enabled internally.  
- **`TUDUDI_SESSION_SECRET`**: A secure session secret used for encrypting session data. Generate this using:  
  ```bash
  openssl rand -hex 64
  ```  
- **`TUDUDI_USER_PASSWORD`**: The password for the default user account. Replace with a strong, unique password.  
- **`TUDUDI_USER_EMAIL`**: The email address for the default user account.  

### Permissions  

Ensure the `tududi_db` directory is created before starting the deployment to avoid permission issues.  

## Deploying Tududi  

1. **Navigate to the Tududi Directory**:  
   ```bash
   cd /home/<user>/docker/tududi
   ```

2. **Run Docker Compose**:  
   ```bash
   docker compose up -d
   ```  

   This will pull the Tududi image, create the container, and start the service.  

## Accessing Tududi  

Once the deployment is complete, Tududi will be accessible via your browser at:  
[http://localhost:9292](http://localhost:9292)  

Replace `localhost` with your server's IP or hostname if running Tududi on a remote machine.  

## Conclusion  

By following this guide, you have successfully deployed Tududi using Docker Compose. You can now log in with the email and password specified in the environment variables to start managing your tasks.  

---

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>  

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
