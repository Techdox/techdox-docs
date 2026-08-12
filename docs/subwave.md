---
title: Build a Personal Radio Station with SUB/WAVE and Docker Compose
description: Turn your own music library into a continuous, self-hosted radio station with scheduled shows, optional AI DJ links, and standard or lossless streams.
---

# Build a Personal Radio Station with SUB/WAVE and Docker Compose

[SUB/WAVE](https://github.com/perminder-klair/subwave) turns an existing music library into a continuous personal radio station. It is radio rather than a playlist: everyone tuned in hears the same broadcast at the same time.

It can schedule shows through the day, use music metadata to keep a show in a particular musical lane, accept requests, and optionally add an AI DJ for short links between tracks. It does **not** provide or generate a music catalogue. The library is yours.

This guide uses [Navidrome](https://www.navidrome.org/) as the music-library server and Docker Compose for the station. It is a practical starting point. Check the [official SUB/WAVE setup guide](https://www.getsubwave.com/setup) and [operator manual](https://www.getsubwave.com/manual) for current upstream options.

!!! warning
    Owning music files does not automatically give you public broadcasting rights. Keep a personal station private unless you have checked the licensing requirements where you live.

## What you are building

```text
Music files
    ↓
Navidrome catalogue
    ↓
SUB/WAVE
  ├─ shows, schedules and optional DJ links
  ├─ transitions and broadcast mixing
  └─ MP3 and optional lossless streams
    ↓
Browser, phone, radio app or audio client
```

There are only two core ideas:

- **Navidrome** indexes your music and presents it as a Subsonic-compatible library.
- **SUB/WAVE** chooses tracks, runs the schedule, mixes the broadcast, and serves the player.

## Prerequisites

You need:

- A Linux server or NAS running Docker Engine and Docker Compose.
- A music library you are permitted to use.
- Enough storage for application data and analysis cache.
- A strong password for the SUB/WAVE admin area.
- An optional LLM provider, such as OpenAI, Anthropic or Ollama, if you want AI DJ links, natural-language requests, or AI-assisted library enrichment.

For the first run, keep it on your LAN or VPN. Add a reverse proxy and HTTPS later if you need a friendly hostname or remote access.

## Create the project

Create folders for persistent data:

```bash
mkdir -p ~/subwave/{state,navidrome}
cd ~/subwave
```

Create `.env`:

```env
ADMIN_USER=admin
ADMIN_PASS=replace-this-with-a-long-random-password
SITE_URL=http://192.168.1.50:7700
STATE_DIR=./state
TZ=Pacific/Auckland
```

Replace `192.168.1.50` with your server's LAN address or hostname. If you later use HTTPS, update `SITE_URL` to the final URL and recreate the stack.

!!! tip
    Generate the password rather than making one up:

    ```bash
    openssl rand -hex 24
    ```

## Docker Compose configuration

Create `docker-compose.yml`:

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    restart: unless-stopped
    user: "1000:1000"
    environment:
      ND_MUSICFOLDER: /music
      ND_DATAFOLDER: /data
      ND_SCANSCHEDULE: 1h
      ND_LOGLEVEL: info
    volumes:
      - ./navidrome:/data
      # Change the host path to your music library.
      # Keep it read-only so the station cannot alter your files.
      - /srv/music:/music:ro
    ports:
      - "4533:4533"

  subwave:
    image: ghcr.io/perminder-klair/subwave-aio:latest
    container_name: subwave
    restart: unless-stopped
    env_file: .env
    environment:
      NAVIDROME_URL: http://navidrome:4533
    volumes:
      - ./state:/var/sub-wave
    ports:
      - "7700:7700"
    depends_on:
      - navidrome
```

Change this line to the real path to your music:

```yaml
- /srv/music:/music:ro
```

For example, use `/mnt/media/music` for a mounted NAS share or `/srv/media/music` for local storage.

!!! warning
    The `user: "1000:1000"` value must be able to read your music and write to `./navidrome`. Run `id` on the host and change it if your NAS uses different ownership.

## Start and configure the station

Start the containers:

```bash
docker compose up -d
```

Check their status and recent logs:

```bash
docker compose ps
docker compose logs --tail=100 subwave
```

Open these URLs:

| Service | URL | Purpose |
|---|---|---|
| SUB/WAVE onboarding | `http://<server-ip>:7700/onboarding` | Connect your library and configure the station. |
| SUB/WAVE player | `http://<server-ip>:7700` | Listen to the station. |
| Navidrome | `http://<server-ip>:4533` | Confirm the music library indexed correctly. |

Complete the SUB/WAVE onboarding wizard. It connects to Navidrome and lets you choose optional LLM, text-to-speech, DJ persona, and station settings.

## Do you need AI tagging?

No. A well-tagged library can run genre-filtered shows without AI.

SUB/WAVE can use standard metadata already embedded in your files:

- artist, album and title
- genre
- year
- existing playlists

Optional enrichment helps, but it is an upgrade rather than a requirement:

| Feature | Uses AI? | Why it is useful |
|---|---:|---|
| Genre-filtered shows using file tags | No | Keeps a morning, hip-hop, rock, or evening show on format. |
| BPM, musical key, loudness and ending analysis | No | Helps pacing and more natural transitions. |
| Last.fm tags | No, but needs an optional API key | Adds community genre and style context. |
| Mood and energy tagging | Usually | Gives a mixed library richer programming rules. |
| AI DJ links and requests | Yes | Creates short spoken links and handles plain-language requests. |
| Audio fingerprints / “sounds-like” matching | No LLM, but heavier local processing | Finds tracks that sound similar, not merely similarly tagged. |

Start with existing tags. Good tags and sensible show rules matter more than turning every AI setting on.

## Build shows that make musical sense

Tags are raw material. They do not automatically turn a shuffled library into a good station.

Create shows around **genre families**, then use strict filters when you want a clear format:

| Show | Example musical lane |
|---|---|
| First Light | Indie, mellow rock, folk-pop, R&B and low-energy electronic. |
| Open Stacks | A broad daytime mix: alternative, rock, hip-hop, rap, pop and electronic. |
| Golden Hour | Warm, melodic rock, pop, R&B and singer-songwriter material. |
| Night Shift | Hip-hop, R&B, rap, electronic and alternative at a lower late-night energy. |
| Weekend Workbench | Higher-energy rock, hip-hop, metal, dance and electronic. |

Avoid creating an hour for every raw genre label. Small pools get repetitive quickly. Combining compatible styles gives the station enough room to space artists out and create better transitions.

!!! note
    A personal library is not an unlimited streaming catalogue. Treat SUB/WAVE as something you programme with your own taste, not as a magic replacement for every music service.

## Optional audio analysis

SUB/WAVE's default analyzer can calculate BPM, key, loudness, and track endings. That analysis is local and does not need an AI provider.

The optional heavy analyzer adds CLAP audio fingerprints, also called **sounds-like** matching. It needs more CPU and memory, so get the basic station working first.

For the standard split-container deployment, add this to `.env`:

```env
ANALYZER_HEAVY=1
```

Then recreate the stack:

```bash
docker compose up -d
```

For the all-in-one image used in this guide, consult the current [official operator manual](https://www.getsubwave.com/manual) before changing images or enabling heavy processing. Those details move faster than a static guide should pretend otherwise.

## Reverse proxy and security notes

For LAN-only use, the direct port is enough:

```text
http://<server-ip>:7700
```

For a friendly hostname or remote access, place SUB/WAVE behind Nginx Proxy Manager, Caddy, or Traefik.

- Proxy SUB/WAVE's HTTP port, `7700`.
- Enable WebSockets.
- Use HTTPS beyond a trusted LAN or VPN.
- Protect the player and streams with SUB/WAVE private-station mode, proxy authentication, or both.
- Do not expose Navidrome directly unless you have separately secured it.
- Do not accidentally make a station public. A working URL and legal broadcasting rights are very different achievements.

## Updating

Back up the `state` and `navidrome` directories first. They hold station configuration, schedules, personas, and library data.

Then update the containers:

```bash
cd ~/subwave
docker compose pull
docker compose up -d
```

Verify the station afterwards:

```bash
docker compose ps
docker compose logs --tail=100 subwave
```

## Troubleshooting

### SUB/WAVE cannot find music

1. Open Navidrome and confirm albums appear there first.
2. Check the music mount path in `docker-compose.yml`.
3. Confirm the directory is readable by the configured container user.
4. Review Navidrome logs:

    ```bash
    docker compose logs --tail=100 navidrome
    ```

### The station still sounds random

Review the show filters in the SUB/WAVE admin area. Soft preferences allow fallback tracks when a matching pool is thin. Use strict genre filters for format-led shows, while keeping each pool large enough to avoid repetition.

### AI features do not work

The station can still broadcast without them. For AI DJ links, requests, or AI-assisted tagging, check **Admin → LLM**, save the provider configuration, and run the built-in key test before starting a large tagging job.

### Audio analysis uses too many resources

Pause analysis or run it during quiet periods. BPM/key analysis is relatively modest. The optional audio-fingerprint and vocal-analysis features require substantially more CPU and memory.

## Official resources

- [SUB/WAVE project site](https://www.getsubwave.com/)
- [Official setup walkthrough](https://www.getsubwave.com/setup)
- [Official operator manual](https://www.getsubwave.com/manual)
- [SUB/WAVE source on GitHub](https://github.com/perminder-klair/subwave)
- [Navidrome documentation](https://www.navidrome.org/docs/)

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
