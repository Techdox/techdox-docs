# Setting Up Synapse Matrix Server with Docker: A Complete Guide

## Introduction to Synapse Matrix Server

Synapse Matrix Server provides a robust platform for secure, decentralized communication. It supports instant messaging, VoIP, and file transfers, making it an excellent choice for individuals and organizations looking for a private communication solution.

## Deployment Steps for Synapse Matrix Server

This guide will walk you through deploying the Synapse Matrix Server using Docker, configuring essential settings, and enabling user registration.

### Docker Compose Setup

1. **Docker Compose File**:

```yaml
version: '3.3'
services:
  synapse:
    container_name: synapse
    image: matrixdotorg/synapse:latest
    restart: always
    ports:
      - 8008:8008
    volumes:
      - ./data:/data
```

2. **Prepare the Data Directory**:
   - Create a `data` directory alongside your `docker-compose.yml`. This prevents Docker from setting it up as owned by `root`, which can complicate file permissions.

3. **Generate Matrix Configuration**:
   - Run the following command to generate the Matrix configuration files. Replace `matrix.elzim.xyz` with your server name:
     ```bash
     docker run -it --rm -v ./data:/data -e SYNAPSE_SERVER_NAME=matrix.elzim.xyz -e SYNAPSE_REPORT_STATS=yes matrixdotorg/synapse:latest generate
     ```

4. **Adjust Ownership of the Data Directory**:
   - Files in the `data` directory may be owned by `root`. Change the ownership to UID 991 with the following command:
     ```bash
     sudo chown -R 991:991 data/
     ```
   - This ensures Synapse can access its configuration and data files.

5. **Enable User Registration**:
   - Edit the `homeserver.yaml` file in the `data` directory:
Let's incorporate the provided `homeserver.yaml` configuration details into the documentation for setting up Synapse Matrix Server using Docker. This includes steps for enabling user registration and configuring reCAPTCHA.

After generating the Synapse configuration files and adjusting file ownership, the next crucial step is to configure your Synapse server to allow user registration and enhance security with reCAPTCHA.

## Editing `homeserver.yaml`

### Sample File

```yaml
# Basic server information
server_name: "your.domain.com"  # The domain name of your Matrix server.
pid_file: /data/homeserver.pid  # Path to the PID file for the Synapse process.

# Networking
listeners:
  - port: 8008
    tls: false
    type: http
    x_forwarded: true  # Enables handling of X-Forwarded-For headers.
    resources:
      - names: [client, federation]
        compress: false

# Database settings
database:
  name: sqlite3
  args:
    database: /data/homeserver.db  # Path to the SQLite database file.

# Logging
log_config: "/data/your.domain.com.log.config"  # Path to the logging configuration file.

# Media storage
media_store_path: /data/media_store  # Where media files are stored on the disk.

# Registration and authentication
registration_shared_secret: "your_secret"  # A secret used to authorize registration requests.
enable_registration: true  # Allows users to register on your server.
enable_registration_captcha: true  # Enables CAPTCHA for registrations.

# reCAPTCHA settings
recaptcha_public_key: "your_public_key"
recaptcha_private_key: "your_private_key"
recaptcha_siteverify_api: "https://www.google.com/recaptcha/api/siteverify"

# Privacy
report_stats: true  # Whether to report anonymous statistics to the Matrix.org project.

# Security
macaroon_secret_key: "your_macaroon_secret"
form_secret: "your_form_secret"
signing_key_path: "/data/your.domain.com.signing.key"  # Path to the server's signing key.

# Federation
trusted_key_servers:
  - server_name: "matrix.org"  # Trusted server for key validation.
```

Locate the `homeserver.yaml` file within the `data` directory you've created and make the following adjustments:

### Basic Server Information
- **`server_name`**: This should be the domain name of your Matrix server. Replace `"your.domain.com"` with your actual domain name.
- **`pid_file`**: Specifies the path to the PID file for the Synapse process. It's set to `/data/homeserver.pid` by default.

### Networking
- The `listeners` configuration allows your server to handle HTTP connections on port `8008` and properly manage `X-Forwarded-For` headers if you're running Synapse behind a reverse proxy.

### Database Settings
- Synapse uses SQLite by default for simplicity, indicated by the `"sqlite3"` `name`. The `database` argument points to the SQLite database file path.

### Logging
- **`log_config`**: Path to the Synapse logging configuration file. Replace `"your.domain.com.log.config"` with the appropriate path, ensuring it matches your domain.

### Media Storage
- **`media_store_path`**: Defines where media files uploaded to the server are stored on disk.

### Registration and Authentication
- **`enable_registration`**: Set to `true` to allow users to register on your server without an invitation.
- **`enable_registration_captcha`**: Set to `true` and configure Google reCAPTCHA to prevent automated spam registrations.

### reCAPTCHA Settings
- **`recaptcha_public_key`** and **`recaptcha_private_key`**: Obtain these from Google's reCAPTCHA admin console by creating a new site with reCAPTCHA v2 ("I'm not a robot" Checkbox). Include your server's domain in the list of authorized domains.
- **`recaptcha_siteverify_api`**: The API URL used to verify the reCAPTCHA response.

## Configuring Google reCAPTCHA

1. Go to [Google reCAPTCHA admin console](https://www.google.com/recaptcha/admin/create) to create a new site.
2. Set the label and choose reCAPTCHA v2 with the "I'm not a robot" Checkbox.
3. Add your server's domain to the list of authorized domains.
4. Copy the site key and secret key into `homeserver.yaml` under `recaptcha_public_key` and `recaptcha_private_key`, respectively.
5. Ensure `enable_registration_captcha: true` is set in your `homeserver.yaml`.

By following these steps, you've configured your Synapse server to allow user registrations while protecting against spam with Google reCAPTCHA. Continue with the deployment by running `docker compose up -d`, and proceed to create a local admin account to start managing your Matrix server.

6. **Creating a Local Admin Account**:
   - Use the following command to create an admin account. Replace `admin` and `testing123@!` with your desired username and password:
     ```bash
     docker exec -it synapse register_new_matrix_user -u admin -p testing123@! -a -c /data/homeserver.yaml http://localhost:8008
     ```

7. **Start Synapse Matrix Server**:
   - With the configuration complete, start your server:
     ```bash
     docker compose up -d
     ```
   - Ensure everything is running smoothly by accessing the server locally.

### Making Your Server Public

For those looking to make their Synapse Matrix Server accessible publicly, setting up a Cloudflare Tunnel is a secure and effective method. Refer to [this video tutorial](https://www.youtube.com/watch?v=gpWo94XXrhU) for a step-by-step guide on deploying Cloudflare Tunnel.

### Connecting with a Matrix Client

Once your server is up and running, you can connect using any Matrix-compatible client, such as Element, by pointing it to your server's URL.

By following these detailed steps, you'll have a fully functional Synapse Matrix Server ready for secure communication across your devices and with others on the Matrix network.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
