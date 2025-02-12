<a href="https://my.racknerd.com/aff.php?aff=5792ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Setting Up Node Exporter
description: The Node Exporter is a project that is maintained through the Prometheus project. 
---

# Setting Up Node Exporter

## Download Node Exporter

Begin by downloading Node Exporter using the wget command:

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
```

Note: Ensure you are using the latest version of Node Exporter and the correct architecture build for your server. The provided link is for amd64. For the latest releases, check here - [Prometheus Node Exporter Releases](https://github.com/prometheus/node_exporter/releases)


## Extract the Contents

After downloading, extract the contents with the following command:

```bash
tar xvf node_exporter-1.7.0.linux-amd64.tar.gz
```

## Move the Node Exporter Binary

Change to the directory and move the node_exporter binary to /usr/local/bin:

```bash
cd node_exporter-1.7.0.linux-amd64
``` 

```bash
sudo cp node_exporter /usr/local/bin
```

Then, clean up by removing the downloaded tar file and its directory:

```bash
rm -rf ./node_exporter-1.7.0.linux-amd64
```

## Create a Node Exporter User

Create a dedicated user for running Node Exporter:

```bash
sudo useradd --no-create-home --shell /bin/false node_exporter
```

Assign ownership permissions of the node_exporter binary to this user:

```bash
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

## Configure the Service

To ensure Node Exporter automatically starts on server reboot, configure the systemd service:

```bash
sudo nano /etc/systemd/system/node_exporter.service
```

Then, paste the following configuration:
```bash
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
Save and exit the editor.

## Enable and Start the Service

Reload the systemd daemon:

```bash
sudo systemctl daemon-reload
```

Enable the Node Exporter service:

```bash
sudo systemctl enable node_exporter
```

Start the service:

```bash
sudo systemctl start node_exporter
```

To confirm the service is running properly, check its status:

```bash
sudo systemctl status node_exporter.service
```

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
