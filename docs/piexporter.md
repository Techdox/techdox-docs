---
title: Deploying PiHole Exporter with Docker Compose
description: This guide provides step-by-step instructions for deploying PiHole Exporter using Docker Compose, including configuring the environment variables and integrating with Prometheus and Grafana for visualization.
---
<a href=\"https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz\" target=\"_blank\">
    <img src=\"https://racknerd.com/banners/728x90.gif\" alt=\"RackNerd Hosting Deals\">
</a>

# Deploying PiHole Exporter with Docker Compose

## Introduction to PiHole Exporter

[PiHole Exporter](https://github.com/eko/pihole-exporter) is a monitoring tool designed to export PiHole metrics for use with Prometheus and Grafana. This guide covers deploying PiHole Exporter using Docker Compose, configuring required environment variables, and integrating it with Prometheus for effective monitoring and visualization.

## Requirements

- PiHole v6 (latest version)
- Prometheus and Grafana installed and configured (Note: Prometheus could also be running via Docker)

## Creating the Docker Compose File

Create a directory for your PiHole Exporter deployment and navigate into it:

```bash
mkdir -p /home/<user>/docker/pihole-exporter
cd /home/<user>/docker/pihole-exporter
```

Replace `<user>` with your system username (e.g., `techdox`).

Create a file named `docker-compose.yml` with the following content:

```yaml
services:
  pihole-exporter:
    image: ekofr/pihole-exporter:latest
    ports:
      - "9617:9617"
    environment:
      PIHOLE_HOSTNAME: "192.168.68.104" # IP address of your PiHole
      PIHOLE_PASSWORD: "password" # PiHole web admin password
```

### Configuration Details

- **`PIHOLE_HOSTNAME`**: IP address or hostname of your PiHole installation.
- **`PIHOLE_PASSWORD`**: Password for your PiHole web interface.

## Deploying PiHole Exporter

Navigate to your deployment directory and run Docker Compose:

```bash
cd /home/<user>/docker/pihole-exporter
docker compose up -d
```

This command pulls the PiHole Exporter image, creates, and starts the container.

## Integrating with Prometheus

To visualize the exported metrics, add PiHole Exporter to your Prometheus scrape jobs by updating your Prometheus configuration:

```yaml
scrape_configs:
  - job_name: 'pihole-exporter'
    static_configs:
      - targets: ['<exporter-host>:9617']
```

Replace `<exporter-host>` with your server’s IP address or hostname where PiHole Exporter is running.

After updating, restart Prometheus to apply changes:

```bash
sudo systemctl restart prometheus
```
or
```bash
docker restart prometheus
```
## Visualizing Data with Grafana

In Grafana, you can import or create a dashboard to visualize PiHole metrics collected by Prometheus. Browse community dashboards or build your own for tailored monitoring.

## Accessing PiHole Exporter

Ensure PiHole Exporter is running by accessing:

```
http://localhost:9617/metrics
```

Replace `localhost` with your server's IP or hostname if accessing remotely.

## Conclusion

By following this guide, you've successfully deployed PiHole Exporter with Docker Compose, integrated it with Prometheus, and are ready to visualize metrics in Grafana.

---

<a href=\"https://www.buymeacoffee.com/techdox\"><img src=\"https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff\" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).