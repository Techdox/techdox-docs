---
title: AdGuard - Docker Setup
description: AdGuard is a comprehensive, customizable network software that blocks ads, trackers, and malicious websites. It enhances user privacy and improves browsing speed and security.
---
# AdGuard - Docker Setup

## Setting Up AdGuard with Docker

### Introduction to AdGuard
AdGuard is a comprehensive, customizable network software that blocks ads, trackers, and malicious websites. It enhances user privacy and improves browsing speed and security.

### Docker Command Configuration for AdGuard
To install and run AdGuard using Docker, you can use the following command. This command sets up AdGuard Home, a network-wide software for blocking ads & tracking.

### Docker Run Command

```bash
docker run --name adguardhome \
    --restart unless-stopped \
    -v /home/techdox/elzim-docker/adguard/workdir:/opt/adguardhome/work \
    -v /home/techdox/elzim-docker/adguard/confdir:/opt/adguardhome/conf \
    -p 192.168.68.110:53:53/tcp -p 192.168.68.110:53:53/udp \
    -p 80:80/tcp -p 443:443/tcp -p 443:443/udp -p 3000:3000/tcp \
    -p 853:853/tcp \
    -p 784:784/udp -p 853:853/udp -p 8853:8853/udp \
    -p 5443:5443/tcp -p 5443:5443/udp \
    -d adguard/adguardhome
```

#### Breakdown of Docker Command
- `docker run`: This command is used to run a new container.
- `--name adguardhome`: Sets the name of the container to `adguardhome`.
- `--restart unless-stopped`: Ensures the container restarts automatically unless it has been explicitly stopped.
- `-v /home/techdox/elzim-docker/adguard/workdir:/opt/adguardhome/work`: Mounts the local directory `/home/techdox/elzim-docker/adguard/workdir` to the container's `/opt/adguardhome/work` directory. This is used for AdGuard's working files.
- `-v /home/techdox/elzim-docker/adguard/confdir:/opt/adguardhome/conf`: Mounts the local directory `/home/techdox/elzim-docker/adguard/confdir` to the container's `/opt/adguardhome/conf` directory. This is used for AdGuard's configuration files.
- `-p 192.168.68.110:53:53/tcp -p 192.168.68.110:53:53/udp`: Maps both TCP and UDP port 53 from the host (at IP `192.168.68.110`) to port 53 in the container. This is typically used for DNS.
- `-p 80:80/tcp -p 443:443/tcp -p 443:443/udp -p 3000:3000/tcp`: Maps various ports for HTTP (80), HTTPS (443), and other services (3000) from the host to the container.
- `-p 853:853/tcp`: Maps TCP port 853 (commonly used for DNS over TLS) from the host to the container.
- `-p 784:784/udp -p 853:853/udp -p 8853:8853/udp`: Maps additional UDP ports which can be used for various secure DNS services from the host to the container.
- `-p 5443:5443/tcp -p 5443:5443/udp`: Maps TCP and UDP port 5443, which can be used for specific secure web services, from the host to the container.
- `-d adguard/adguardhome`: Specifies the Docker image to use (`adguard/adguardhome`) and runs the container in detached mode.

## Note
- On line 5, a hardcoded IP address of the server is used due to a conflict with a broadcast address. Change the IP address and the volume directory to match your local server setup.

## Docker Hub Link
- [AdGuard Home on Docker Hub](https://hub.docker.com/r/adguard/adguardhome)

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/a3rej5UVvKo?si=-wik4SQoF-A-WGEt" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
