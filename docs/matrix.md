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
- **Caddy** — internal hostname dispatcher (used inside the stack only)
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
        ├── matrix.example.com    → Synapse :8008
        ├── element.example.com   → Element Web :80
        ├── call.example.com      → Element Call :8080
        ├── livekit.example.com   → LiveKit :7880
        └── livekit-jwt.example.com → LK JWT service :8080

Synapse ──────────────────────── Postgres
Element Call → LiveKit → Redis
NAT traversal ──────────────── coturn (STUN/TURN)
```

Caddy runs inside the Docker stack and routes based on the `Host` header that Nginx Proxy Manager passes through. All five domains point at the same NPM proxy — Caddy figures out where to send each request.

---

## Voice and Video Limitations

Cloudflare Tunnel proxies HTTPS only. Matrix chat, file uploads, and the Element Web UI all work through the tunnel. Voice and video media are different — they use UDP paths that a Cloudflare Tunnel cannot carry.

- **Chat, images, rooms:** work publicly via Cloudflare Tunnel
- **Voice and video on LAN or VPN:** work fine — clients reach coturn/LiveKit directly
- **Voice and video publicly:** require a VPS running coturn or a LiveKit relay with a real public IP

Do not open UDP ports on your home router. If you need reliable public calls, put coturn on a cheap VPS.

---

## Prerequisites

- Docker and Docker Compose installed
- Nginx Proxy Manager running on your network
- Five subdomains created in Cloudflare DNS pointing at your Cloudflare Tunnel (or at your NPM host for LAN-only)
- Local DNS records pointing those same domains at your NPM host (Pi-hole, AdGuard Home, or router DNS)

Replace `example.com` with your actual domain throughout.

---

## Step 1: Create the Project Directory

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
# Domains
MATRIX_SERVER_NAME=matrix.example.com
MATRIX_PUBLIC_BASEURL=https://matrix.example.com
ELEMENT_DOMAIN=element.example.com
ELEMENT_CALL_DOMAIN=call.example.com
LIVEKIT_DOMAIN=livekit.example.com
LIVEKIT_JWT_DOMAIN=livekit-jwt.example.com

# Postgres
POSTGRES_DB=synapse
POSTGRES_USER=synapse
POSTGRES_PASSWORD=changeme

# Synapse
SYNAPSE_REGISTRATION_SHARED_SECRET=changeme

# TURN
TURN_SHARED_SECRET=changeme

# LiveKit
LIVEKIT_API_KEY=matrix_livekit
LIVEKIT_API_SECRET=changeme
```

Generate secure secrets to replace the `changeme` values:

```bash
for var in POSTGRES_PASSWORD SYNAPSE_REGISTRATION_SHARED_SECRET TURN_SHARED_SECRET LIVEKIT_API_SECRET; do
  echo "$var=$(openssl rand -hex 32)"
done
```

!!! warning "Keep `.env` private"
    Never commit this file. Add it to `.gitignore` if you version-control this directory.

---

## Step 3: Create `docker-compose.yml`

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
      - "192.168.1.x:18080:80"
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

!!! note "Replace `192.168.1.x` with your server's LAN IP"
    The `ports` line on Caddy exposes the dispatcher only to your LAN. Nginx Proxy Manager connects to it on port 18080.

---

## Step 4: Configure Caddy

Create `caddy/Caddyfile`:

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
    Without `http://`, Caddy tries to get TLS certificates internally and the stack breaks. Keep `auto_https off` and use `http://` on every site block.

---

## Step 5: Configure Element Web

Create `element-web/config.json`:

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
    If `config.json` is mode `600`, the Element Web container will restart in a loop with a permission error.

---

## Step 6: Configure Element Call

Create `element-call/config.json`:

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

Create `livekit/livekit.yaml`. Paste in the `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` values from your `.env`:

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
  matrix_livekit: your-livekit-api-secret

logging:
  level: info
```

Replace `matrix_livekit` with your `LIVEKIT_API_KEY` value and the secret with your `LIVEKIT_API_SECRET` value.

---

## Step 8: Configure coturn

Create `coturn/turnserver.conf`. Replace `192.168.1.x` with your server's LAN IP and paste in your `TURN_SHARED_SECRET`:

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

coturn runs with `network_mode: host` so it has direct access to the network interface for UDP media relay.

---

## Step 9: Generate and Configure Synapse

### Generate the initial config

```bash
cd /opt/matrix
docker compose run --rm synapse generate
```

This creates `synapse/homeserver.yaml` and a signing key. Synapse defaults to SQLite — you need to switch it to Postgres and add TURN/LiveKit settings.

### Edit `synapse/homeserver.yaml`

Open the generated file and apply these changes:

**Switch database from SQLite to Postgres** — find the `database:` block and replace it:

```yaml
database:
  name: psycopg2
  args:
    user: synapse
    password: your-postgres-password
    database: synapse
    host: postgres
    port: 5432
    cp_min: 5
    cp_max: 10
```

**Add TURN configuration** — add this block (not present in the generated file):

```yaml
turn_uris:
  - "turn:192.168.1.x:3478?transport=udp"
  - "turn:192.168.1.x:3478?transport=tcp"
turn_shared_secret: your-turn-shared-secret
turn_user_lifetime: 86400000
turn_allow_guests: false
```

Replace `192.168.1.x` with your server's LAN IP and fill in your `TURN_SHARED_SECRET`.

**Add registration shared secret** — find or add:

```yaml
registration_shared_secret: your-synapse-registration-shared-secret
```

**Enable well-known serving** — add:

```yaml
serve_server_wellknown: true
```

**Disable public registration** (users are created manually):

```yaml
enable_registration: false
```

**Set correct paths** — these should already be set by the generator, but verify:

```yaml
media_store_path: /data/media_store
log_config: "/data/matrix.example.com.log.config"
signing_key_path: "/data/matrix.example.com.signing.key"
```

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

Expected:

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

If anything is unhealthy, check its logs:

```bash
docker compose logs synapse
docker compose logs caddy
docker compose logs element-web
```

---

## Step 11: Add Nginx Proxy Manager Hosts

Create a proxy host in NPM for each of the five domains. All five point at the same backend:

| Field | Value |
|-------|-------|
| Scheme | `http` |
| Forward Hostname / IP | `192.168.1.x` (your server LAN IP) |
| Forward Port | `18080` |
| Websockets Support | Enabled |
| Block Common Exploits | Enabled |
| SSL | Your existing cert or request new |

Nginx Proxy Manager forwards the `Host` header by default — Caddy uses this to route each request to the right service.

---

## Step 12: DNS

### Local / LAN access

Add local DNS overrides (Pi-hole, AdGuard Home, or router DNS) pointing all five domains at your NPM host:

```
matrix.example.com      → NPM IP
element.example.com     → NPM IP
call.example.com        → NPM IP
livekit.example.com     → NPM IP
livekit-jwt.example.com → NPM IP
```

### Public access via Cloudflare Tunnel

In the Cloudflare Zero Trust dashboard, add public hostnames for all five domains routing to:

- If `cloudflared` runs on the same host as the stack: `http://localhost:18080`
- If `cloudflared` runs elsewhere on the LAN: `http://192.168.1.x:18080`

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

You'll be prompted for a password. Add more users (without `-a` for non-admin):

```bash
docker compose exec synapse register_new_matrix_user \
  -u username \
  --no-admin \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

---

## Step 14: Log In

Open `https://element.example.com` in your browser.

On the login screen, set the homeserver to `matrix.example.com` if it isn't already, then log in with the admin account you just created.

---

## Verification

```bash
# Matrix API responding
curl https://matrix.example.com/_matrix/client/versions

# Federation well-known
curl https://matrix.example.com/.well-known/matrix/server

# Element Web config loading
curl https://element.example.com/config.json

# Element Call loading
curl -I https://call.example.com/
```

---

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Synapse won't start | Database not ready | Check `docker compose logs postgres` — wait for healthy |
| Synapse starts but crashes | homeserver.yaml still using SQLite | Update `database:` block to use psycopg2 |
| Element Web restarts in a loop | `config.json` permission denied | Run `chmod 644 element-web/config.json` |
| Caddy gives connection resets | Missing `http://` in Caddyfile | Add `http://` prefix to all site blocks |
| 502 from NPM | Caddy not running or wrong port | Check `docker compose ps caddy` and confirm port 18080 |
| Calls don't connect on LAN | TURN not reachable | Check coturn is running, confirm LAN IP in `turnserver.conf` |
| Calls fail publicly | Expected — Cloudflare Tunnel can't carry UDP | Use a VPS with coturn for public calls |
| Can't register users | `registration_shared_secret` mismatch | Must match between `homeserver.yaml` and the register command |

---

## Keeping Up to Date

```bash
cd /opt/matrix
docker compose pull
docker compose up -d
```

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
