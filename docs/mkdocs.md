---
title: Setting Up MkDocs with Docker Compose
description: MkDocs is a static site generator that's geared towards project documentation. With the Material theme, it provides a sleek, responsive, and user-friendly interface for your documentation projects.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Setting Up MkDocs with Docker Compose

## Introduction to MkDocs

MkDocs is a static site generator that's geared towards project documentation. With the Material theme, it provides a sleek, responsive, and user-friendly interface for your documentation projects.

## Docker Compose Configuration for MkDocs

This Docker Compose setup deploys MkDocs with the Material theme in a Docker container, allowing you to easily manage and preview your project documentation.

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  mkdocs:
    image: squidfunk/mkdocs-material
    ports:
      - "8005:8000"
    volumes:
      - ./mkdocs-data:/docs
    stdin_open: true
    tty: true
```

## Key Components of the Configuration
### Service: MkDocs
- **Image**: `squidfunk/mkdocs-material` is the Docker image used for MkDocs with the Material theme.
- **Ports**: 
  - `8005:8000` maps port 8005 on the host to port 8000 in the container, where MkDocs's web interface is accessible.
- **Volumes**: 
  - `./mkdocs-data:/docs`: Maps a dedicated `mkdocs-data` subdirectory to `/docs` inside the container. This keeps your documentation files separate from the `docker-compose.yml`, which prevents the container from crashing due to unexpected files at the project root.
- **Interactive Mode**: `stdin_open: true` and `tty: true` allow interactive processes, which is useful for live reloading during documentation development.

## Deploying MkDocs

To deploy MkDocs with Docker Compose, follow these steps:

1. **Create a New Directory**:
   - Create a directory on your host system for the MkDocs stack (e.g. `mkdocs`).

2. **Docker Compose File**:
   - Inside that directory, create a `docker-compose.yml` file with the configuration above.

3. **Create the Data Directory and Docs Folder**:
   - Inside the `mkdocs` directory, create the `mkdocs-data` subdirectory and a `docs` folder inside it:

     ```bash
     mkdir -p mkdocs-data/docs
     ```

   Your directory structure should look like this:

   ```
   mkdocs/
   ├── docker-compose.yml
   └── mkdocs-data/
       ├── docs/
       └── mkdocs.yml
   ```

4. **Create MkDocs Configuration File**:
   - Inside `mkdocs-data/`, create a file named `mkdocs.yml` with the following base structure:

    ```yaml
    site_name: My Docs

    nav:
      - Home: index.md
      - About: about.md

    theme:
      name: 'material'
    ```

5. **Start the MkDocs Container**:
   - Run `docker compose up -d` from within the `mkdocs` directory.

6. **Access MkDocs**:
   - Once the container is running, navigate to `http://<host-ip>:8005` to view your site.

By following these steps, you will have a fully functional MkDocs site running in a Docker container, which you can access and edit as needed.


## Example MkDocs Configuration (`mkdocs.yml`)

This example demonstrates how to configure an MkDocs site with subpages, plugins, and additional features.

```yaml
site_name: Techdox Docs
nav:
  - Home: index.md
  - About: about.md
  - Docker Containers:
      - Overview: docker-containers.md
      - Adguard: adguard.md
      # Additional Docker container pages...
  - Networking:
      - Overview: networking-overview.md
      - GlusterFS: glusterfs.md
  # Additional sections...

theme:
  name: material
  logo: path/to/logo.png

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  # Additional Markdown extensions...
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.superfences
  # More pymdownx extensions...
```
## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/K2RDsWgwDTU?si=sQkLDP4fI0JdhBzX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
