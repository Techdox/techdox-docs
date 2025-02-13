---
title: Deploying Firefly III with Docker Compose
description: Firefly III is a free and open-source personal finance manager. This guide provides steps for deploying Firefly III using Docker Compose, including important notes on configuring environment variables, setting up cron jobs, and handling optional configurations.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Deploying Firefly III with Docker Compose

## Introduction to Firefly III

[Firefly III](https://www.firefly-iii.org/) is a free and open-source personal finance manager designed to help you keep track of your expenses, income, budgets, and more. It offers a user-friendly interface and a rich set of features that make managing your finances easier and more efficient. This guide provides detailed instructions on how to deploy Firefly III using Docker Compose, including important notes on setting up environment variables, persistent storage, and scheduled tasks.

## Docker Compose Configuration for Firefly III

Below is the Docker Compose file used to deploy Firefly III, along with explanations of the key components involved.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  app:
    image: fireflyiii/core:latest            # Uses the latest Firefly III Docker image.
    container_name: firefly_iii_app          # Names the container for easier management.
    hostname: app                            # Sets the hostname inside the container.
    restart: always                          # Restarts the container automatically on failure.
    volumes:
      - firefly_iii_upload:/var/www/html/storage/upload  # Stores uploaded files persistently.
    env_file:
      - .env                                 # Loads environment variables from .env file.
    networks:
      - firefly_iii                          # Connects to the specified Docker network.
    ports:
      - "8051:8080"                          # Exposes Firefly III on port 8051.
    depends_on:
      - db                                   # Ensures the database service starts before the app.

  db:
    image: mariadb:lts                       # Uses the latest stable MariaDB image.
    container_name: firefly_iii_db           # Names the container for easier management.
    hostname: db                             # Sets the hostname inside the container.
    restart: always                          # Restarts the container automatically on failure.
    env_file:
      - .db.env                              # Loads environment variables from .db.env file.
    networks:
      - firefly_iii                          # Connects to the specified Docker network.
    volumes:
      - firefly_iii_db:/var/lib/mysql        # Stores database data persistently.

  cron:
    image: alpine                            # Uses a lightweight Alpine Linux image.
    container_name: firefly_iii_cron         # Names the container for easier management.
    restart: always                          # Restarts the container automatically on failure.
    command: >
      sh -c "echo '0 3 * * * wget -qO- http://app:8080/api/v1/cron/YOUR_32_CHAR_CRON_TOKEN' | crontab - && crond -f -L /dev/stdout"
    networks:
      - firefly_iii                          # Connects to the specified Docker network.

volumes:
  firefly_iii_upload:
  firefly_iii_db:

networks:
  firefly_iii:
    driver: bridge
```

### Explanation of Key Components

#### **Services**

- **app**: Runs the Firefly III application.
  - **Image**: Uses the `fireflyiii/core:latest` Docker image.
  - **Ports**: Maps port `8051` on the host to port `8080` in the container, making Firefly III accessible via `http://<your-server-ip>:8051`.
  - **Volumes**:
    - **`firefly_iii_upload:/var/www/html/storage/upload`**: Stores uploaded files persistently.
  - **Environment Variables**: Loaded from the `.env` file.
  - **Depends On**: Waits for the `db` service to be ready before starting.

- **db**: Runs the MariaDB database.
  - **Image**: Uses the `mariadb:lts` Docker image.
  - **Volumes**:
    - **`firefly_iii_db:/var/lib/mysql`**: Stores database files persistently.
  - **Environment Variables**: Loaded from the `.db.env` file.

- **cron**: Sets up a cron job to run scheduled tasks in Firefly III.
  - **Image**: Uses the `alpine` image for a lightweight container.
  - **Command**: Schedules a cron job to trigger Firefly III's scheduled tasks API endpoint.
    > **Important**: Replace `YOUR_32_CHAR_CRON_TOKEN` with your actual `STATIC_CRON_TOKEN` value.

#### **Volumes**

- **firefly_iii_upload**: Stores uploaded files such as attachments.
- **firefly_iii_db**: Stores MariaDB database files.

#### **Networks**

- **firefly_iii**: A custom bridge network that allows the containers to communicate.

### Environment Variables

Firefly III relies on environment variables for configuration. These variables are stored in two files: `.env` for the application and `.db.env` for the database. Both files contain required and optional settings.

#### `.db.env` File for MariaDB

Create a `.db.env` file with the following content:

```ini
# MariaDB Environment Variables

MYSQL_RANDOM_ROOT_PASSWORD=yes            # Generates a random root password.
MYSQL_USER=firefly                        # The database username.
MYSQL_PASSWORD=YOUR_DB_PASSWORD           # The database user's password.
MYSQL_DATABASE=firefly                    # The name of the Firefly III database.
```

> **Note**:
>
> - Replace `YOUR_DB_PASSWORD` with a strong password.
> - **Do not leave any values empty unless specified as optional**.

#### `.env` File for Firefly III Application

Create a `.env` file in the same directory as your `docker-compose.yml` with the following content:

```ini
# Firefly III Application Environment Variables

APP_ENV=production
APP_DEBUG=false
SITE_OWNER=your_email@example.com          # Replace with your email address.
APP_KEY=YOUR_APP_KEY                       # Generate using 'php artisan key:generate --show' inside the app container.
DEFAULT_LANGUAGE=en_US
DEFAULT_LOCALE=equal
TZ=Your/Timezone                           # Replace with your timezone, e.g., 'America/New_York'.
TRUSTED_PROXIES=*
LOG_CHANNEL=stack
APP_LOG_LEVEL=notice
AUDIT_LOG_LEVEL=emergency
DB_CONNECTION=mysql
DB_HOST=db
DB_PORT=3306
DB_DATABASE=firefly
DB_USERNAME=firefly
DB_PASSWORD=YOUR_DB_PASSWORD               # Must match the password in .db.env.
STATIC_CRON_TOKEN=YOUR_32_CHAR_CRON_TOKEN  # A 32-character token for securing cron jobs.
APP_URL=http://localhost:8051              # The URL where Firefly III will be accessible.

# Optional Mail Configuration
MAIL_MAILER=log
MAIL_HOST=null
MAIL_PORT=2525
MAIL_FROM=changeme@example.com
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_SENDMAIL_COMMAND=

# Optional Redis Configuration
REDIS_SCHEME=tcp
REDIS_PATH=
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_USERNAME=
REDIS_PASSWORD=
REDIS_DB="0"
REDIS_CACHE_DB="1"

# Optional Cache and Session Drivers
CACHE_DRIVER=file
SESSION_DRIVER=file

# Optional Cookie Settings
COOKIE_PATH="/"
COOKIE_DOMAIN=
COOKIE_SECURE=false
COOKIE_SAMESITE=lax

# Other Optional Settings
ENABLE_EXTERNAL_MAP=false
ENABLE_EXCHANGE_RATES=false
ENABLE_EXTERNAL_RATES=false
MAP_DEFAULT_LAT=51.983333
MAP_DEFAULT_LONG=5.916667
MAP_DEFAULT_ZOOM=6
VALID_URL_PROTOCOLS=https
AUTHENTICATION_GUARD=web
CUSTOM_LOGOUT_URL=
DISABLE_FRAME_HEADER=false
DISABLE_CSP_HEADER=false
ALLOW_WEBHOOKS=false
FIREFLY_III_LAYOUT=v1
```

> **Notes**:
>
> - **APP_KEY**: Generate a secure application key by running:
>
>   ```bash
>   docker compose exec app php artisan key:generate --show
>   ```
>
>   Copy the generated key and paste it as the value of `APP_KEY`.
>
> - **DB_PASSWORD**: Ensure this matches the `MYSQL_PASSWORD` in your `.db.env` file.
> - **STATIC_CRON_TOKEN**: Generate a 32-character token using a command like `openssl rand -hex 16` and replace `YOUR_32_CHAR_CRON_TOKEN` with it.
> - **SITE_OWNER**: Replace with your actual email address.
> - **TZ**: Set to your local timezone (e.g., `America/New_York`).
>
> **Optional Values**:
>
> - Empty values in the configuration are optional and can be filled if needed.
> - For example, if you wish to configure Redis, fill in the `REDIS_*` variables.
> - Similarly, mail configurations and other optional settings can be adjusted based on your requirements.

### Setting Up the Cron Service

The `cron` service schedules a daily task to trigger Firefly III's scheduled jobs. To set this up:

1. **Generate a Static Cron Token**: This token must be exactly 32 characters long. You can generate one using:

   ```bash
   openssl rand -hex 16
   ```

2. **Update the `.env` File**: Add the `STATIC_CRON_TOKEN` to your `.env` file as shown above.

3. **Update the `docker-compose.yml` File**: Replace `YOUR_32_CHAR_CRON_TOKEN` in the `cron` service command with your actual `STATIC_CRON_TOKEN`.

   ```yaml
   command: >
     sh -c "echo '0 3 * * * wget -qO- http://app:8080/api/v1/cron/YOUR_32_CHAR_CRON_TOKEN' | crontab - && crond -f -L /dev/stdout"
   ```

   > **Note**: Ensure that `YOUR_32_CHAR_CRON_TOKEN` matches the `STATIC_CRON_TOKEN` in your `.env` file.

## Deployment

To deploy Firefly III, follow these steps:

1. **Create Necessary Files**: Ensure that you have created the `.env` and `.db.env` files with the appropriate content and secure values. Include all variables, even optional ones, leaving them empty if you do not wish to set them now.

2. **Initialize Volumes**: Docker will create the volumes `firefly_iii_upload` and `firefly_iii_db` automatically.

3. **Start the Services**: Navigate to the directory containing your `docker-compose.yml` file and run:

   ```bash
   docker compose up -d
   ```

   This command will start all the services in detached mode.

4. **Generate the Application Key**: If you haven't generated the `APP_KEY` yet, run:

   ```bash
   docker compose exec app php artisan key:generate --show
   ```

   Copy the output and paste it into the `APP_KEY` field in your `.env` file. Then, restart the app service:

   ```bash
   docker compose restart app
   ```

5. **Verify the Deployment**: Check the logs to ensure all services are running correctly:

   ```bash
   docker compose logs -f
   ```

## Accessing Firefly III

Once the deployment is complete, you can access Firefly III by navigating to:

```
http://<your-server-ip>:8051
```

Follow the on-screen instructions to complete the setup.

## Conclusion

By following this guide, you have successfully deployed Firefly III using Docker Compose. You now have a powerful personal finance manager up and running, with persistent storage and scheduled tasks configured. Remember to secure all sensitive information and consider filling in optional configurations as needed to enhance your Firefly III experience.

---

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
