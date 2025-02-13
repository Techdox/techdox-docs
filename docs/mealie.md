---
title: Deploying Mealie with Docker Compose
description: Mealie is a self-hosted recipe manager and meal planner that allows you to organize your recipes, create meal plans, and store yo>Mealie is a self-hosted recipe manager and meal planner that allows you to organize your recipes, create meal plans, and store yo>Mealie is a self-hosted recipe manager and meal planner that allows you to organize your recipes, create meal plans, and store yo>
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Deploying Mealie with Docker Compose

## Introduction to Mealie

Mealie is a self-hosted recipe manager and meal planner that allows you to organize your recipes, create meal plans, and store your favorite recipes in one convenient location. This guide details deploying Mealie using Docker Compose, including configuration settings for optimized performance.

## Docker Compose Configuration for Mealie

Here's how to set up Mealie using Docker Compose, explaining each component of the configuration.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v1.6.0  # Specifies the Mealie Docker image and version.
    container_name: mealie                      # Names the container for easier management.
    restart: always                              # Ensures the container restarts automatically unless stopped.
    ports:
      - "9925:9000"                             # Maps port 9925 on the host to port 9000 in the container.
    deploy:
      resources:
        limits:
          memory: 1000M                         # Limits the container to use a maximum of 1000M of memory.
    volumes:
      - mealie-data:/app/data/                  # Persists data in a named volume.
    environment:
      - ALLOW_SIGNUP=true                       # Allows new user signups on the Mealie instance.
      - PUID=1000                               # Sets the user ID for the container.
      - PGID=1000                               # Sets the group ID for the container.
      - TZ=America/Anchorage                    # Sets the timezone for the container.
      - MAX_WORKERS=1                           # Limits the number of workers to 1.
      - WEB_CONCURRENCY=1                       # Sets the concurrency level for web workers.
      - BASE_URL=https://mealie.yourdomain.com  # The base URL where Mealie is accessed.

volumes:
  mealie-data:                                  # Declares a named volume for persisting application data.
```

### Explanation of Key Components

- **Image**: Specifies the specific version of Mealie to be used, ensuring consistency and compatibility.
- **Ports**: Maps the host port to the container port where Mealie is accessible. Port `9000` is the default for Mealie, and it's mapped to `9925` on the host for external access.
- **Memory Limit**: Restricts the amount of memory the container can use, important for environments with limited resources.
- **Volumes**: Uses a Docker volume (`mealie-data`) to store persistent data like recipes and configuration settings. This is crucial for maintaining data across container restarts or updates.
- **Environment Variables**: Configures various aspects of the application, such as user permissions, system environment, and operational parameters.

## Preparing for Deployment

Ensure that the volume exists or Docker will create it at runtime:

```bash
docker volume create mealie-data
```

This command prepares a dedicated storage space for Mealie's data, avoiding data loss during updates or restarts.

## Deployment

To deploy Mealie, navigate to the directory containing your `docker-compose.yml` and run:

```bash
docker compose up -d
```

This command starts the Mealie service in detached mode, running in the background.

## Accessing Mealie

After deployment, Mealie will be accessible at `https://mealie.yourdomain.com` or `http://<your-server-ip>:9925` based on your `BASE_URL` and port configuration. This setup ensures that Mealie is ready for recipe management and meal planning, all from your self-hosted environment.

## Conclusion

Deploying Mealie with Docker Compose allows for straightforward setup and management of a self-hosted recipe manager. The configuration ensures optimal use of system resources while providing robust data persistence and easy accessibility.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
