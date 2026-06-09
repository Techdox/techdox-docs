---
title: Self-Hosting Matrix with Docker, Element, and Voice Calls
description: Deploy a private Matrix homeserver with Synapse, Element Web, Element Call, LiveKit, coturn, Nginx Proxy Manager, and Cloudflare Tunnel. Full compose file, all config files, and voice/video setup included.
---

# Self-Hosting Matrix with Docker, Element, and Voice Calls

This guide sets up a full Matrix stack as a self-hosted Discord replacement — rooms, direct messages, file sharing, and voice/video calls — with no open inbound ports on your home router.

The stack runs:

- **Synapse** — Matrix homeserver
- **Postgres** — Synapse database
- **Element Web** — browser client
- **Element Call** — voice and video UI
- **LiveKit** — WebRTC media server for calls
- **LiveKit JWT service** — authentication bridge between Synapse and LiveKit
- **Redis** — LiveKit session state
- **coturn** — TURN/STUN relay for NAT traversal
- **Caddy** — internal hostname dispatcher (inside the stack only)
- **Nginx Proxy Manager** — your existing reverse proxy, the external front door

---

## Architecture

```text
Browser / Matrix client
        │
        │ HTTPS
        ▼
Nginx Proxy Manager
        │
        │ HTTP + Host header
        ▼
Caddy (internal dispatcher on port 18080)
        │
        ├── matrix.example.com      → Synapse :8008
        ├── element.example.com     → Element Web :80
        ├── call.example.com        → Element Call :8080
        ├── livekit.example.com     → LiveKit :7880
        └── livekit-jwt.example.com → LK JWT service :8080

Synapse ──────────────────── Postgres
Element Call → LiveKit → Redis
NAT traversal ────────────── coturn (STUN/TURN)
```

All five domains point at the same Nginx Proxy Manager entry on port 18080. Caddy routes each request to the right container using the `Host` header that NPM passes through.

---

## Voice and Video Limitations

Cloudflare Tunnel proxies HTTPS only. Matrix chat, file uploads, and Element Web all work through the tunnel. Voice and video are different — they use UDP paths that Cloudflare Tunnel cannot carry.

- **Chat, images, rooms:** work publicly via Cloudflare Tunnel
- **Voice and video on LAN or VPN:** work fine
- **Voice and video publicly:** require a VPS running coturn with a real public IP

Do not open UDP ports on your home router. If you need reliable public calls, put coturn on a cheap VPS.

---

## Prerequisites

- Docker and Docker Compose installed on your server
- Nginx Proxy Manager already running on your network
- Five subdomains on your domain (e.g. `matrix.`, `element.`, `call.`, `livekit.`, `livekit-jwt.`)
- Local DNS pointing those domains at your NPM host (Pi-hole, AdGuard Home, or router DNS)
- Cloudflare Tunnel configured for public access (optional — LAN-only works without it)

!!! tip
    Replace every instance of `example.com` in this guide with your actual domain before copying any config.

---

## Step 1: Create the Project Directory

Copy and run as-is:

```bash
mkdir -p /opt/matrix
cd /opt/matrix
mkdir -p caddy synapse coturn livekit element-web element-call postgres
```

---

## Step 2: Create the Environment File

```bash
nano /opt/matrix/.env
```

```env
# Domains — replace example.com with your domain
MATRIX_SERVER_NAME=matrix.example.com
MATRIX_PUBLIC_BASEURL=https://matrix.example.com
ELEMENT_DOMAIN=element.example.com
ELEMENT_CALL_DOMAIN=call.example.com
LIVEKIT_DOMAIN=livekit.example.com
LIVEKIT_JWT_DOMAIN=livekit-jwt.example.com

# Postgres — DB name and user can stay as-is
POSTGRES_DB=synapse
POSTGRES_USER=synapse
POSTGRES_PASSWORD=changeme

# Synapse
SYNAPSE_REGISTRATION_SHARED_SECRET=changeme

# TURN
TURN_SHARED_SECRET=changeme

# LiveKit — key name can stay as-is, secret must be changed
LIVEKIT_API_KEY=matrix_livekit
LIVEKIT_API_SECRET=changeme
```

Generate all four secrets in one go and paste them into the file:

```bash
for var in POSTGRES_PASSWORD SYNAPSE_REGISTRATION_SHARED_SECRET TURN_SHARED_SECRET LIVEKIT_API_SECRET; do
  echo "$var=$(openssl rand -hex 32)"
done
```

!!! note "What to change"
    - All six domain values — replace `example.com` with your domain
    - Replace all four `changeme` values with the output of the command above
    - `POSTGRES_DB`, `POSTGRES_USER`, and `LIVEKIT_API_KEY` can stay as shown

!!! warning "Keep `.env` private"
    Never commit this file. Add `.env` to `.gitignore` if you version-control this directory.

---

## Step 3: Create `docker-compose.yml`

!!! tip "Copy as-is — one line to change"
    The only thing to edit in this file is the Caddy `ports:` line. Replace `192.168.1.x` with your server's actual LAN IP. Everything else copies unchanged.

```yaml
services:

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    volumes:
      - ./postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  synapse:
    image: matrixdotorg/synapse:latest
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      SYNAPSE_CONFIG_PATH: /data/homeserver.yaml
    volumes:
      - ./synapse:/data
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:8008/health"]
      interval: 30s
      timeout: 10s
      retries: 5

  element-web:
    image: vectorim/element-web:latest
    restart: unless-stopped
    volumes:
      - ./element-web/config.json:/app/config.json:ro
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  livekit:
    image: livekit/livekit-server:latest
    restart: unless-stopped
    depends_on:
      redis:
        condition: service_healthy
    volumes:
      - ./livekit/livekit.yaml:/etc/livekit.yaml:ro
    command: --config /etc/livekit.yaml

  lk-jwt-service:
    image: ghcr.io/element-hq/lk-jwt-service:latest
    restart: unless-stopped
    environment:
      LIVEKIT_URL: ws://livekit:7880
      LIVEKIT_KEY: ${LIVEKIT_API_KEY}
      LIVEKIT_SECRET: ${LIVEKIT_API_SECRET}

  element-call:
    image: ghcr.io/element-hq/element-call:latest
    restart: unless-stopped
    volumes:
      - ./element-call/config.json:/app/config.json:ro

  coturn:
    image: coturn/coturn:latest
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./coturn/turnserver.conf:/etc/coturn/turnserver.conf:ro

  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "192.168.1.x:18080:80"   # ← change this IP to your server's LAN IP
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      synapse:
        condition: service_healthy
      element-web:
        condition: service_healthy

volumes:
  caddy_data:
  caddy_config:
```

---

## Step 4: Configure Caddy

Create `caddy/Caddyfile`:

!!! note "What to change"
    Replace every occurrence of `example.com` with your domain. The structure, ports, and directives copy as-is.

```caddyfile
{
    auto_https off
}

http://matrix.example.com {
    encode zstd gzip

    handle /.well-known/matrix/server {
        header Content-Type application/json
        respond `{"m.server":"matrix.example.com:443"}`
    }

    handle /.well-known/matrix/client {
        header Content-Type application/json
        header Access-Control-Allow-Origin "*"
        respond `{"m.homeserver":{"base_url":"https://matrix.example.com"}}`
    }

    reverse_proxy synapse:8008
}

http://element.example.com {
    encode zstd gzip
    reverse_proxy element-web:80
}

http://call.example.com {
    encode zstd gzip
    reverse_proxy element-call:8080
}

http://livekit.example.com {
    encode zstd gzip
    reverse_proxy livekit:7880
}

http://livekit-jwt.example.com {
    encode zstd gzip
    reverse_proxy lk-jwt-service:8080
}
```

!!! warning "Site labels must include `http://`"
    Without `http://`, Caddy tries to obtain TLS certificates internally and breaks. Keep `auto_https off` and prefix every site block with `http://`.

---

## Step 5: Configure Element Web

Create `element-web/config.json`:

!!! note "What to change"
    Replace `example.com` with your domain. Everything else copies as-is.

```json
{
  "default_server_config": {
    "m.homeserver": {
      "base_url": "https://matrix.example.com",
      "server_name": "matrix.example.com"
    }
  },
  "brand": "Element",
  "show_labs_settings": true,
  "features": {
    "feature_video_rooms": true,
    "feature_element_call_video_rooms": true,
    "feature_group_calls": true
  },
  "element_call": {
    "url": "https://call.example.com",
    "use_exclusively": false
  }
}
```

```bash
chmod 644 element-web/config.json
```

!!! warning "File permissions matter"
    If `config.json` is mode `600`, the Element Web container restarts in a loop with a permission error. Always run `chmod 644` after creating it.

---

## Step 6: Configure Element Call

Create `element-call/config.json`:

!!! note "What to change"
    Replace `example.com` with your domain. Everything else copies as-is.

```json
{
  "default_server_config": {
    "m.homeserver": {
      "base_url": "https://matrix.example.com",
      "server_name": "matrix.example.com"
    }
  },
  "livekit": {
    "url": "wss://livekit.example.com",
    "jwt_service_url": "https://livekit-jwt.example.com"
  },
  "livekit_service_url": "https://livekit-jwt.example.com",
  "livekit_url": "wss://livekit.example.com"
}
```

```bash
chmod 644 element-call/config.json
```

---

## Step 7: Configure LiveKit

Create `livekit/livekit.yaml`:

!!! note "What to change"
    Only the `keys:` section. Replace `matrix_livekit` with your `LIVEKIT_API_KEY` and the value after the colon with your `LIVEKIT_API_SECRET` from `.env`. Everything else copies as-is.

```yaml
port: 7880
bind_addresses:
  - "0.0.0.0"

rtc:
  tcp_port: 7881
  udp_port: 7882
  use_external_ip: true
  port_range_start: 50000
  port_range_end: 50200

redis:
  address: redis:6379

keys:
  matrix_livekit: your-livekit-api-secret   # ← paste LIVEKIT_API_KEY: LIVEKIT_API_SECRET

logging:
  level: info
```

---

## Step 8: Configure coturn

Create `coturn/turnserver.conf`:

!!! note "What to change"
    - `static-auth-secret` — paste your `TURN_SHARED_SECRET` from `.env`
    - `realm` — your Matrix domain (e.g. `matrix.example.com`)
    - `external-ip`, `listening-ip`, `relay-ip` — your server's LAN IP

```conf
listening-port=3478
fingerprint
use-auth-secret
static-auth-secret=your-turn-shared-secret
realm=matrix.example.com
lt-cred-mech
no-cli
no-tls
no-dtls
mobility
no-multicast-peers
no-loopback-peers
external-ip=192.168.1.x
listening-ip=192.168.1.x
relay-ip=192.168.1.x
min-port=49160
max-port=49200
log-file=stdout
simple-log
```

coturn uses `network_mode: host` in the Compose file so it has direct access to network interfaces for UDP relay. All other settings can stay as shown.

---

## Step 9: Generate and Configure Synapse

### Generate the initial config

```bash
cd /opt/matrix
docker compose run --rm synapse generate
```

This creates `synapse/homeserver.yaml` and a signing key file. Synapse defaults to SQLite and has no TURN or registration config — you need to add those now.

### Edit `synapse/homeserver.yaml`

Open the generated file:

```bash
nano synapse/homeserver.yaml
```

Make the following changes:

---

**1. Switch from SQLite to Postgres**

Find the existing `database:` block (it will reference SQLite) and replace the entire block:

```yaml
database:
  name: psycopg2
  args:
    user: synapse
    password: your-postgres-password   # ← your POSTGRES_PASSWORD from .env
    database: synapse
    host: postgres
    port: 5432
    cp_min: 5
    cp_max: 10
```

---

**2. Add TURN configuration**

This block does not exist in the generated file — add it:

```yaml
turn_uris:
  - "turn:192.168.1.x:3478?transport=udp"   # ← your server's LAN IP
  - "turn:192.168.1.x:3478?transport=tcp"
turn_shared_secret: your-turn-shared-secret  # ← your TURN_SHARED_SECRET from .env
turn_user_lifetime: 86400000
turn_allow_guests: false
```

---

**3. Add the registration shared secret**

Find the existing `registration_shared_secret:` line or add it:

```yaml
registration_shared_secret: your-registration-secret  # ← SYNAPSE_REGISTRATION_SHARED_SECRET from .env
```

---

**4. Enable well-known serving**

Add this line (not in the generated file):

```yaml
serve_server_wellknown: true
```

---

**5. Disable public registration**

Find and set (or add):

```yaml
enable_registration: false
```

---

**6. Verify these paths are correct** (the generator sets them, but double-check):

```yaml
media_store_path: /data/media_store
log_config: "/data/matrix.example.com.log.config"
signing_key_path: "/data/matrix.example.com.signing.key"
```

!!! tip
    The `log_config` and `signing_key_path` filenames include your server name. If you used a different domain during `generate`, they'll already reflect that — just confirm they point to `/data/`.

---

## Step 10: Start the Stack

```bash
cd /opt/matrix
docker compose up -d
```

Check all containers are running:

```bash
docker compose ps
```

Expected output:

```
NAME             STATUS
postgres         running (healthy)
synapse          running (healthy)
element-web      running (healthy)
redis            running (healthy)
livekit          running
lk-jwt-service   running
element-call     running
coturn           running
caddy            running
```

If anything is unhealthy, check its logs before continuing:

```bash
docker compose logs synapse
docker compose logs caddy
docker compose logs element-web
```

---

## Step 11: Add Nginx Proxy Manager Hosts

Create one proxy host for each of the five domains. All five use the **same backend settings**:

| Field | Value |
|-------|-------|
| Scheme | `http` |
| Forward Hostname / IP | Your server's LAN IP |
| Forward Port | `18080` |
| Websockets Support | ✅ Enabled |
| Block Common Exploits | ✅ Enabled |
| SSL | Request a new certificate or use an existing one |

NPM passes the `Host` header through by default — Caddy uses it to route each request to the correct container.

---

## Step 12: Configure DNS

### LAN access (required)

Add local DNS records pointing all five domains at your NPM host IP (not your server IP — your NPM host IP):

```
matrix.example.com      → NPM host IP
element.example.com     → NPM host IP
call.example.com        → NPM host IP
livekit.example.com     → NPM host IP
livekit-jwt.example.com → NPM host IP
```

Use Pi-hole local DNS records, AdGuard Home rewrites, or your router's DNS overrides.

### Public access via Cloudflare Tunnel

In Cloudflare Zero Trust → Access → Tunnels, add a public hostname for each domain pointing to:

- `http://localhost:18080` — if `cloudflared` runs on the same host as the stack
- `http://192.168.1.x:18080` — if `cloudflared` runs elsewhere on the LAN

---

## Step 13: Create the First Admin Account

```bash
cd /opt/matrix
docker compose exec synapse register_new_matrix_user \
  -u admin \
  -a \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

You'll be prompted for a password. To add regular (non-admin) users:

```bash
docker compose exec synapse register_new_matrix_user \
  -u username \
  --no-admin \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

---

## Step 14: Log In

Open `https://element.example.com` in your browser. On the login screen confirm the homeserver is set to `matrix.example.com`, then sign in with the admin account you just created.

---

## Verification

```bash
# Matrix API responding
curl https://matrix.example.com/_matrix/client/versions

# Federation well-known
curl https://matrix.example.com/.well-known/matrix/server
# Should return: {"m.server":"matrix.example.com:443"}

# Element Web config reachable
curl https://element.example.com/config.json

# Element Call reachable
curl -I https://call.example.com/
```

---

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Synapse won't start | Postgres not ready yet | Check `docker compose logs postgres` — wait for healthy |
| Synapse starts then crashes | `homeserver.yaml` still on SQLite | Replace the `database:` block with the psycopg2 config above |
| Element Web restarts in a loop | `config.json` permissions | Run `chmod 644 element-web/config.json` |
| Caddy connection resets | Missing `http://` in Caddyfile | Prefix every site block with `http://` |
| 502 Bad Gateway from NPM | Wrong IP or port | Confirm Caddy is running and NPM is pointing at the right LAN IP:18080 |
| Calls don't connect on LAN | coturn not reachable | Check coturn is running; confirm LAN IP in `turnserver.conf` |
| Calls fail publicly | Cloudflare Tunnel can't carry UDP | Use a VPS with coturn for reliable public calls |
| User registration fails | Secret mismatch | `registration_shared_secret` in `homeserver.yaml` must match `.env` |

---

## Keeping Up to Date

```bash
cd /opt/matrix
docker compose pull
docker compose up -d
```

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
