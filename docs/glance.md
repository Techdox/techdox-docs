---
title: Deploying Glance with Docker Compose
description: Glance is a customizable dashboard application that aggregates content from various sources. This guide provides steps for deploying Glance using Docker Compose, including setting up the `glance.yml` configuration file and configuring environment settings.
---

# Deploying Glance with Docker Compose

## Introduction to Glance

[Glance](https://github.com/glanceapp/glance) is a flexible, open-source dashboard application that allows users to aggregate content from diverse sources in a customizable format. Whether you're interested in integrating RSS feeds, tracking stocks, or viewing weather updates, Glance makes it easy to consolidate and view information on a single dashboard. This guide provides a step-by-step approach to deploying Glance using Docker Compose.

## Docker Compose Configuration for Glance

Below is the Docker Compose file used to deploy Glance, along with explanations of key components.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  glance:
    image: glanceapp/glance                       # Uses the official Glance Docker image.
    container_name: glance                        # Assigns a custom container name for easy management.
    volumes:
      - ./glance.yml:/app/glance.yml              # Mounts the glance.yml configuration file.
      - /etc/timezone:/etc/timezone:ro            # Ensures container timezone sync.
      - /etc/localtime:/etc/localtime:ro          # Ensures container localtime sync.
    ports:
      - 8280:8080                                 # Exposes Glance on port 8280.
    restart: unless-stopped                       # Restarts container unless manually stopped.
```
## Explanation of Key Components

### Service

	•	glance: Runs the Glance application.
	•	Image: Pulls the latest glanceapp/glance image from Docker Hub.
	•	Ports: Maps port 8280 on the host to port 8080 in the container, making Glance accessible via http://<your-server-ip>:8280.
	•	Volumes:
	•	./glance.yml:/app/glance.yml: Mounts the local glance.yml file, containing Glance’s configuration settings.
	•	/etc/timezone:/etc/timezone:ro: Syncs the container timezone with the host.
	•	/etc/localtime:/etc/localtime:ro: Syncs the container’s local time with the host’s local time.

## Glance Configuration File

The Glance dashboard is configured using the glance.yml file. This file must be created before deploying the container. Below is an example configuration file that users can customize.

## Example glance.yml File
```yaml
pages:
  - name: Home
    columns:
      - size: small
        widgets:
          - type: calendar

          - type: rss
            limit: 10
            collapse-after: 3
            cache: 3h
            feeds:
              - url: https://ciechanow.ski/atom.xml
              - url: https://www.joshwcomeau.com/rss.xml
                title: Josh Comeau
              - url: https://samwho.dev/rss.xml
              - url: https://awesomekling.github.io/feed.xml
              - url: https://ishadeed.com/feed.xml
                title: Ahmad Shadeed

          - type: twitch-channels
            channels:
              - theprimeagen
              - cohhcarnage
              - christitustech
              - blurbs
              - asmongold
              - jembawls

      - size: full
        widgets:
          - type: hacker-news

          - type: videos
            channels:
              - UCXJ4jKAvMMg56WGhqrZHFgw # Techdox

          - type: reddit
            subreddit: selfhosted

      - size: small
        widgets:
          - type: weather
            location: Christchurch, New Zealand

          - type: markets
            markets:
              - symbol: SPY
                name: S&P 500
              - symbol: BTC-USD
                name: Bitcoin
              - symbol: NVDA
                name: NVIDIA
              - symbol: AAPL
                name: Apple
              - symbol: MSFT
                name: Microsoft
              - symbol: GOOGL
                name: Google
              - symbol: AMD
                name: AMD
              - symbol: RDDT
```
	Note:
		•	Customize the glance.yml file based on your preferences.
	•	Widgets are organized under pages and columns with options for size and type.

Deployment Steps

To deploy Glance, follow these steps:
1.	Create the glance.yml Configuration File: Ensure you have created the glance.yml file as shown above or modified it with your desired widgets and settings.
2.	Run Docker Compose: In the directory containing your docker-compose.yml file, start the Glance service with:
```bash 
docker compose up -d
```
This command will start the Glance container in detached mode.

3.	Verify Deployment: Check that the Glance service is running by accessing:

```bash 
http://<your-server-ip>:8280
```


4.	Restarting the Service: After making changes to glance.yml, restart the container for changes to take effect:
```bash
docker compose restart glance
```


## Conclusion

By following this guide, you have successfully deployed Glance using Docker Compose with a custom configuration file. You can now enjoy a centralized dashboard with various integrations to enhance your productivity.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>