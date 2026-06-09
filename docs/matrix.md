---
title: Self-Hosting Matrix with Docker, Element, Nginx Proxy Manager, and Cloudflare Tunnel
description: Deploy a private Matrix server with Synapse, Element Web, Element Call, LiveKit, coturn, Nginx Proxy Manager, and Cloudflare Tunnel without opening inbound firewall ports.
---

# Self-Hosting Matrix with Docker, Element, Nginx Proxy Manager, and Cloudflare Tunnel

This guide walks through a Matrix deployment designed to replace a Discord server with a private, self-hosted chat stack.

The setup supports:

- Rooms and spaces
- Direct messages
- Image and file uploads
- Element Web as the browser client
- Foundations for voice and video calls with Element Call, LiveKit, and coturn
- Internal access through a homelab reverse proxy
- Public access through Cloudflare Tunnel
- No open inbound firewall ports

This public version uses example domains and IPs. Replace them with your own values.

## Final Architecture

```text
Browser / Matrix client
        |
        | HTTPS
        v
Nginx Proxy Manager
        |
        | HTTP to internal Matrix dispatcher
        v
192.168.1.50:18080
        |
        v
Caddy inside the Matrix Docker stack
        |
        +-- matrix.example.com       -> Synapse homeserver
        +-- element.example.com      -> Element Web
        +-- call.example.com         -> Element Call
        +-- livekit.example.com      -> LiveKit signalling
        +-- livekit-jwt.example.com  -> LiveKit JWT auth service

Synapse -> Postgres
Element Call -> LiveKit -> Redis
Calls/NAT traversal -> coturn
```

Nginx Proxy Manager is still the front door. Caddy is only used inside the Matrix stack as a small hostname-based dispatcher.

That sounds redundant, but it keeps the Matrix routing logic next to the Matrix Compose file instead of spreading path rules across Nginx Proxy Manager.

## Domains Used

```text
matrix.example.com       Matrix homeserver
element.example.com      Element Web client
call.example.com         Element Call web app
livekit.example.com      LiveKit signalling
livekit-jwt.example.com  LiveKit JWT auth service
```

## Server Used

```text
Matrix Docker host: 192.168.1.50
Matrix stack path:  /opt/matrix
Internal port:      192.168.1.50:18080
```

Replace these values with your own.

## Important Limitation Before You Start

Cloudflare Tunnel works well for HTTPS applications. Matrix chat, images, rooms, login, and federation all use HTTPS, so they can work well through a tunnel.

Voice and video media are different.

TURN/STUN and LiveKit media relay use UDP/TCP media paths that normal Cloudflare Tunnel does not proxy. That means:

- Chat and file uploads can work publicly through Cloudflare Tunnel.
- Voice and video may work well on LAN or VPN.
- Reliable public calls usually need a small public VPS running TURN or LiveKit relay.

Do not open random ports on your home firewall just to make calls work. Use a VPS relay if you need reliable public calls.

## Step 1: Create the Project Directory

```bash
mkdir -p /opt/matrix
cd /opt/matrix
```

Create the subdirectories used by the stack:

```bash
mkdir -p caddy synapse coturn livekit element-web element-call cloudflared
```

## Step 2: Create the Environment File

Create `.env`:

```bash
nano .env
```

Example:

```env
MATRIX_SERVER_NAME=matrix.example.com
MATRIX_PUBLIC_BASEURL=https://matrix.example.com
ELEMENT_DOMAIN=element.example.com
ELEMENT_CALL_DOMAIN=call.example.com
LIVEKIT_DOMAIN=livekit.example.com
LIVEKIT_JWT_DOMAIN=livekit-jwt.example.com
TURN_HOST=192.168.1.50

POSTGRES_DB=synapse
POSTGRES_USER=synapse
POSTGRES_PASSWORD=replace-with-a-long-random-secret
SYNAPSE_REGISTRATION_SHARED_SECRET=replace-with-a-long-random-secret
TURN_SHARED_SECRET=replace-with-a-long-random-secret
LIVEKIT_API_KEY=matrix_replace_this
LIVEKIT_API_SECRET=replace-with-a-long-random-secret
```

Generate secrets with:

```bash
python3 - <<'PY'
import secrets

for name in [
    "POSTGRES_PASSWORD",
    "SYNAPSE_REGISTRATION_SHARED_SECRET",
    "TURN_SHARED_SECRET",
    "LIVEKIT_API_SECRET",
]:
    print(f"{name}={secrets.token_urlsafe(32)}")

print("LIVEKIT_API_KEY=matrix_" + secrets.token_urlsafe(12).replace("-", "_"))
PY
```

Keep `.env` private. Do not publish it.

## Step 3: Create `docker-compose.yml`

This stack runs:

- Postgres
- Synapse
- Element Web
- Redis
- LiveKit
- LiveKit JWT service
- Element Call
- coturn
- Caddy internal dispatcher

The key binding for Nginx Proxy Manager is the internal Caddy port:

```yaml
ports:
  - "192.168.1.50:18080:80"
```

That exposes the Matrix dispatcher to the LAN, not directly to the public internet.

In this deployment, the active Compose file is:

```text
/opt/matrix/docker-compose.yml
```

For sharing publicly, do not include your `.env` values.

## Step 4: Configure the Internal Caddy Dispatcher

Create:

```text
/opt/matrix/caddy/Caddyfile
```

Because Nginx Proxy Manager sends plain HTTP to this internal service, the Caddy site labels must explicitly use `http://`.

Example:

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

If you forget `http://`, Caddy may try to listen on HTTPS/443 internally and local HTTP checks can fail with connection resets.

## Step 5: Configure Element Web

Create:

```text
/opt/matrix/element-web/config.json
```

Minimal example:

```json
{
  "default_server_config": {
    "m.homeserver": {
      "base_url": "https://matrix.example.com",
      "server_name": "matrix.example.com"
    }
  },
  "brand": "My Matrix",
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

Make it readable by the container:

```bash
chmod 644 element-web/config.json
```

If this file is mode `600`, Element Web can restart in a loop with a permission error.

## Step 6: Configure Element Call

Create:

```text
/opt/matrix/element-call/config.json
```

Example:

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

Make it readable:

```bash
chmod 644 element-call/config.json
```

## Step 7: Configure LiveKit

Create:

```text
/opt/matrix/livekit/livekit.yaml
```

Example:

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
  your-livekit-api-key: your-livekit-api-secret
logging:
  level: info
```

`use_external_ip: true` matters when LiveKit is running in Docker.

## Step 8: Configure coturn

Create:

```text
/opt/matrix/coturn/turnserver.conf
```

Example:

```conf
listening-port=3478
fingerprint
use-auth-secret
lt-cred-mech
no-cli
no-tls
no-dtls
mobility
no-multicast-peers
no-loopback-peers
external-ip=192.168.1.50
listening-ip=192.168.1.50
relay-ip=192.168.1.50
min-port=49160
max-port=49200
log-file=stdout
simple-log
```

The Compose stack passes the shared secret and realm into coturn from `.env`.

## Step 9: Generate and Patch Synapse Config

Synapse generates its own initial config. Generate it first:

```bash
cd /opt/matrix
docker compose run --rm synapse generate
```

Then patch `synapse/homeserver.yaml` so it uses:

- Postgres instead of SQLite
- `/data/media_store`
- `/data/<server>.signing.key`
- `/data/<server>.log.config`
- `report_stats: false`
- `registration_shared_secret`
- TURN settings
- `serve_server_wellknown: true`

In this deployment, a small Python patcher was used:

```text
/opt/matrix/patch_synapse.py
```

One gotcha: Synapse-generated files are owned by UID 991. If your patcher runs as your normal user, temporarily change ownership, patch the files, then restore ownership:

```bash
docker run --rm -v "$PWD/synapse:/data" alpine:3.20 chown -R "$(id -u):$(id -g)" /data
python3 patch_synapse.py
docker run --rm -v "$PWD/synapse:/data" alpine:3.20 chown -R 991:991 /data
```

## Step 10: Start the Stack

```bash
cd /opt/matrix
docker compose up -d
```

Check status:

```bash
docker compose ps
```

Expected result:

```text
postgres       running / healthy
synapse        running / healthy
element-web    running / healthy
caddy          running
coturn         running
redis          running
livekit        running
lk-jwt-service running
element-call   running
```

## Step 11: Add Nginx Proxy Manager Hosts

In Nginx Proxy Manager, create one proxy host for each domain.

All of them point to the same internal target:

```text
Scheme: http
Forward Hostname / IP: 192.168.1.50
Forward Port: 18080
Websockets Support: enabled
Block Common Exploits: enabled
SSL: enabled with your normal certificate setup
```

Create these Nginx Proxy Manager proxy hosts:

```text
matrix.example.com       -> http://192.168.1.50:18080
element.example.com      -> http://192.168.1.50:18080
call.example.com         -> http://192.168.1.50:18080
livekit.example.com      -> http://192.168.1.50:18080
livekit-jwt.example.com  -> http://192.168.1.50:18080
```

Nginx Proxy Manager preserves the Host header by default. That is important because Caddy uses the hostname to route to the correct internal service.

## Step 12: Configure DNS

For local LAN access, point these names at your Nginx Proxy Manager host:

```text
matrix.example.com
element.example.com
call.example.com
livekit.example.com
livekit-jwt.example.com
```

In a homelab, this might mean Pi-hole, AdGuard Home, Unbound overrides, or router DNS records pointing these names to your Nginx Proxy Manager host.

For public access, create Cloudflare Tunnel public hostnames for the same domains and route them either to Nginx Proxy Manager or directly to the Matrix dispatcher, depending on where your tunnel runs.

If `cloudflared` runs on the Matrix host:

```text
http://localhost:18080
```

If `cloudflared` runs elsewhere on the LAN:

```text
http://192.168.1.50:18080
```

## Step 13: Verify Locally

From the Matrix host:

```bash
cd /opt/matrix
curl -H 'Host: matrix.example.com' http://192.168.1.50:18080/_matrix/client/versions
curl -H 'Host: matrix.example.com' http://192.168.1.50:18080/.well-known/matrix/server
curl -H 'Host: element.example.com' http://192.168.1.50:18080/config.json
curl -I -H 'Host: call.example.com' http://192.168.1.50:18080/
```

Expected:

- Matrix versions returns JSON.
- `.well-known/matrix/server` returns `{"m.server":"matrix.example.com:443"}`.
- Element config returns JSON.
- Element Call returns HTTP 200.

## Step 14: Create the First Admin Account

Keep public registration disabled. Create users manually.

Interactive admin creation:

```bash
cd /opt/matrix
docker compose exec synapse register_new_matrix_user \
  -u adminuser \
  -a \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

It will prompt for a password.

If you need to create the admin non-interactively, place a temporary password file inside the mounted Synapse data directory:

```bash
cd /opt/matrix
umask 077
python3 - <<'PY'
from pathlib import Path
import secrets

Path("synapse/admin-temp-password.txt").write_text(secrets.token_urlsafe(24) + "\n")
PY

docker run --rm -v "$PWD/synapse:/data" alpine:3.20 chown -R 991:991 /data

docker compose exec -T synapse register_new_matrix_user \
  -u adminuser \
  --password-file /data/admin-temp-password.txt \
  -a \
  --exists-ok \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

After logging in, delete the temporary password file:

```bash
rm /opt/matrix/synapse/admin-temp-password.txt
```

## Step 15: Log In

Open:

```text
https://element.example.com
```

Use:

```text
Homeserver: matrix.example.com
Username: adminuser
Password: the password you created
```

## Step 16: Create Normal Users

Run this from the Matrix host:

```bash
cd /opt/matrix
docker compose exec synapse register_new_matrix_user \
  -u someuser \
  --no-admin \
  -c /data/homeserver.yaml \
  http://localhost:8008
```

## Troubleshooting Notes

### Element Login Screen Loads, but the User Creation Command Says Synapse Is Not Running

First check that you are running the command from the server and from the Compose project directory:

```bash
cd /opt/matrix
docker compose ps
```

If Element loads, Synapse is probably running. The usual issue is running `docker compose exec` from the wrong directory or on a different machine.

### Element Web Container Restarts Repeatedly

Check logs:

```bash
docker logs matrix_element_web
```

If you see a permission error reading `/app/config.json`, fix file permissions:

```bash
chmod 644 /opt/matrix/element-web/config.json
docker compose restart element-web
```

### Caddy Gives Connection Resets on Local HTTP Checks

Make sure Caddy site labels include `http://`, for example:

```caddyfile
http://matrix.example.com {
    reverse_proxy synapse:8008
}
```

Do not use bare `matrix.example.com` for this internal HTTP-only dispatcher.

### Synapse Fails with `/media_store` Permission Denied

Make sure `homeserver.yaml` includes:

```yaml
media_store_path: /data/media_store
```

Also make sure these paths are under `/data`:

```yaml
log_config: "/data/matrix.example.com.log.config"
signing_key_path: "/data/matrix.example.com.signing.key"
```

### Calls Work Locally but Not Publicly

This is expected unless you have public UDP, TURN, or LiveKit relay access.

Cloudflare Tunnel does not proxy the UDP media path. Use a small VPS relay for reliable public voice and video.

## Operational Commands

```bash
cd /opt/matrix

docker compose ps
docker compose logs -f synapse
docker compose logs -f caddy
docker compose logs -f element-web
docker compose restart synapse
docker compose pull
docker compose up -d
```

## Security Notes

- Keep `.env` private.
- Leave public registration disabled unless you are intentionally opening signups.
- Prefer manual account creation for a private Discord replacement.
- Do not expose your home firewall directly to the internet.
- Use Cloudflare Tunnel or a proper reverse proxy path.
- For public voice and video, prefer a VPS relay over opening home UDP ports.

## What Was Verified in This Deployment

- Docker Compose config parsed successfully.
- All containers started.
- Synapse became healthy.
- Element Web became healthy.
- Matrix client API returned versions JSON.
- Matrix `.well-known` returned the correct federation response.
- Element Web config was reachable through the internal dispatcher.
- Element Call returned HTTP 200.
- Login screen loaded through Nginx Proxy Manager from a Mac on the same LAN.
- First admin user was created server-side.

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
