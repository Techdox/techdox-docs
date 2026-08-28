---
title: Setting Up GlusterFS with Docker Compose
description: Set up GlusterFS on Ubuntu 22.04 to create a replicated, distributed filesystem shared across multiple nodes.
tags:
  - storage
  - networking
  - linux
---

# GlusterFS Setup

## Requirements

GlusterFS is only supported on 64bit systems, so make sure the host machine running GlusterFS and any machines utilising the share is also running on a 64bit system.

This guide is created for Ubuntu 22.04 jammy

## Steps to follow

!!! warning "Run on all systems"
    Run the following commands on all systems that will be utilising the share, as well as the host system.

### Adding Hosts to /etc/hosts

We want to make sure our machines can talk to each other via their host names, this can be done by editing and adding the following.

Edit /etc/hosts

```bash
sudo nano /etc/hosts
```

Add in your IP addresses and Hostnames of your machines that will be using GlusterFS, this is my example on my GlusterFS host machine, but remember to add this to all your nodes that will be using GlusterFS

```text
127.0.0.1 localhost
127.0.1.1 elzim

192.168.68.109  elzim
192.168.68.105  pi4lab01
192.168.68.114  pi4lab02
```

### Installing GlusterFS

Setup the GlusterFS repository. At the time of writing this, GlusterFS-10 is the latest release.

```bash
sudo add-apt-repository ppa:gluster/glusterfs-10
```

Run an apt update to update the repositories.

```bash
sudo apt update
```

Install GlusterFS

```bash
sudo apt install glusterfs-server -y
```

Start and enable GlusterFS

```bash
sudo systemctl start glusterd
sudo systemctl enable glusterd
```

### Peering the Nodes

!!! warning "Host machine only"
    This command is only run on the host machine.

Before running the peering command, make sure you run it under sudo via

```bash
sudo -s
```

The following command will peer all the nodes to the GlusterFS Pool, this is using the hostnames for my environment, make sure to change this to suit yours.

```bash
gluster peer probe pi4lab01; gluster peer probe pi4lab02;
```

Running the below command will show your hosts now connected to the pool.

```bash
sudo gluster pool list
```


### Creating the Gluster Volume

Let's create the directory that will be used for the GlusterFS volume.

!!! note "Run on all nodes"
    This is run on all nodes. You can name "volumes" to anything you like.

```bash
sudo mkdir -p /gluster/volumes
```

Now we can create the volume across the Gluster pool.

!!! warning "Host machine only"
    This is run just on the host.

```bash
sudo gluster volume create staging-gfs replica 3 elzim:/gluster/volumes pi4lab01:/gluster/volumes pi4lab02:/gluster/volumes force
```

Start the volume by running the below command

```bash
sudo gluster volume start staging-gfs
```

To ensure the volume automatically mounts on reboot or other circumstances, follow these steps on all machines:

- - Switch to the root user by running: `sudo -s`.
    - Append the following line to the `/etc/fstab` file using the command:

      ```bash
      echo 'localhost:/staging-gfs /mnt glusterfs defaults,_netdev,noauto,x-systemd.automount,backupvolfile-server=localhost 0 0' >> /etc/fstab
      ```

      !!! warning "Use automount options for fstab entries"
          Use the `noauto,x-systemd.automount` options in your fstab entry. An incorrect fstab entry can prevent your system from booting. Always test with `mount -a` before rebooting.

    - Mount the GlusterFS volume to the `/mnt` directory with the command: `mount.glusterfs localhost:/staging-gfs /mnt`.
    - Set the ownership of the `/mnt` directory and its contents to `root:docker` using: `chown -R root:docker /mnt`.
    - Exit the root user session by running: `exit`.

To verify that the GlusterFS volume is successfully mounted, run the command: `df -h`.

```bash
localhost:/staging-gfs                 15G  4.8G  9.1G  35% /mnt
```

Files created in the **/mnt** directory will now show up in the **/gluster/volumes** directories on every machine.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/Has6lUPdzzY?si=U19sdc177UZiDSKd" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
