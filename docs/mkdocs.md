---
title: Setting Up MkDocs with Docker Compose
description: MkDocs is a static site generator that's geared towards project documentation. With the Material theme, it provides a sleek, responsive, and user-friendly interface for your documentation projects.
---

# Setting Up MkDocs with Docker Compose

## Introduction to MkDocs

MkDocs is a static site generator that's geared towards project documentation. With the Material theme, it provides a sleek, responsive, and user-friendly interface for your documentation projects.

## Docker Compose Configuration for MkDocs

This Docker Compose setup deploys MkDocs with the Material theme in a Docker container, allowing you to easily manage and preview your project documentation.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3'
services:
  mkdocs:
    image: squidfunk/mkdocs-material
    ports:
      - "8005:8000"
    volumes:
      - ./:/docs
    stdin_open: true
    tty: true
```

## Key Components of the Configuration
### Service: MkDocs
- **Image**: `squidfunk/mkdocs-material` is the Docker image used for MkDocs with the Material theme.
- **Ports**: 
  - `8005:8000` maps port 8005 on the host to port 8000 in the container, where MkDocs's web interface is accessible.
- **Volumes**: 
  - `./:/docs`: Maps the current directory (project documentation) to the `/docs` directory in the container.
- **Interactive Mode**: `stdin_open: true` and `tty: true` allow interactive processes, which is useful for live reloading during documentation development.

## Deploying MkDocs

To deploy MkDocs with Docker Compose, follow these steps:

1. **Create a New Directory**:
   - Create a new directory on your host system for your MkDocs container. You can name it `mkdocs` or any other name of your choice.

2. **Docker Compose File**:
   - Inside this new directory, create a `docker-compose.yml` file.
   - Save the following Docker Compose configuration into this file:

    ```yaml
    version: '3'
    services:
      mkdocs:
        image: squidfunk/mkdocs-material
        ports:
          - "8005:8000"
        volumes:
          - ./:/docs
        stdin_open: true
        tty: true
    ```

3. **Create Documentation Directory**:
   - Within the `mkdocs` directory, create another directory called `docs`. This will hold all your documentation files.

4. **Create MkDocs Configuration File**:
   - In the root of your `mkdocs` directory, create a file named `mkdocs.yml`.
   - Add the following base structure to the `mkdocs.yml` file:

    ```yaml
    site_name: Techdox Doc

    nav:
      - Home: index.md
      - About: about.md

    theme:
      name: 'material'
    ```

    - Feel free to customize the `site_name`, navigation (`nav`), and other configurations as needed.

5. **Start the MkDocs Container**:
   - Run `docker compose up -d` from within the `mkdocs` directory. This command starts the MkDocs container in detached mode.

6. **Access MkDocs**:
   - Once the container is running, access your MkDocs site by navigating to `http://<host-ip>:8005`.
   - You should see your MkDocs site with the Material theme, ready for further customization and document addition.

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
