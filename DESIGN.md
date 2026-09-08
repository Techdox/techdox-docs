---
version: alpha
name: Techdox
description: Practical self-hosting, from Nick's own homelab. Dark technical surfaces with a human editorial voice.
colors:
  primary: "#4D8DFF"
  background: "#090C12"
  raised: "#0D121B"
  panel: "#111824"
  soft: "#151E2C"
  text: "#F4F7FB"
  muted: "#9AA8BC"
  bright: "#79AAFF"
  cyan: "#65DCE9"
  success: "#65E6A7"
  caution: "#FFD166"
  line: "#293445"
typography:
  h1:
    fontFamily: Hanken Grotesk
    fontWeight: 800
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.5556
  label:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4286
  editorial:
    fontFamily: Fraunces
    fontWeight: 600
    fontVariation: "'opsz' 72"
rounded:
  panel: 18px
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.panel}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.background}"
  muted-copy:
    backgroundColor: "{colors.background}"
    textColor: "{colors.muted}"
---

## Overview

Canonical working reference derived from the uploaded Techdox-Brand-Kit, not a replacement for its original files. The kit calls itself proposed; Nick requested adoption for techdox.nz, docs.techdox.nz and blog.techdox.nz. Separate products and homelab applications are out of scope.

Tagline: **Build it. Break it. Understand it.**

Use Techdox in prose and the supplied lowercase techdox artwork in logos. Voice: first-person real experience, named tools and results, useful failures, restrained dry humour. Do not turn personal publishing into corporate copy.

Source: `Techdox-Brand-Kit/Techdox-Brand-Guide.pdf`, especially pages 3–7, 11–12; exact exported tokens: `Techdox-Brand-Kit/tokens/techdox.css`.

## Colors

Keep compositions predominantly dark/neutral. Blue drives main emphasis; cyan is secondary technical detail. Green means success and yellow means caution, not decoration. Use dark text on brand-blue buttons; off-white on brand blue fails even the large-text contrast threshold.

The source exports a dark palette only. Retain accessible existing light themes; do not blindly apply dark token values to light surfaces. Document any light-theme semantic adaptation separately rather than claiming the kit defines it.

## Typography

Hanken Grotesk: UI/body, short display headlines at 800 and paragraphs at 400. JetBrains Mono: code, commands, labels and metadata, not body paragraphs. Fraunces 600 belongs to blog/editorial headlines; preserve that distinction.

Use existing matching local webfonts where available; do not replace compact WOFF2 files with larger TTFs without need. Preserve bundled OFL licenses when distributing fonts. Sizes are guide working sizes; retain responsive, readable documentation layouts.

## Layout

Shared identity does not require identical layouts. Homepage introduces Techdox, docs prioritise finding/reading guides, blog retains editorial hierarchy. Preserve content, routes, search, navigation, code copying and mobile controls.

## Shapes

The exported panel radius is 18px; smaller controls may retain fit-for-purpose radii. Prefer restrained panels/rules and original schematic artwork, not glow or decorative status colors.

## Components

Use supplied outlined SVG masters from `logos/` for production, not editable text SVGs from `templates/`. Inspect primary-light.svg and primary-dark.svg against the actual background before use; do not infer suitability from the filename alone.

Full wordmark: minimum 140 CSS px wide, clear space at least half its rendered height on all sides. Below 140px use the ~/ icon. Nick explicitly overrides the kit static-cursor rule for techdox.nz, docs.techdox.nz and blog.techdox.nz: blink only the supplied attached cursor at 1.2s with step timing in web-only SVG derivatives. Keep all paths, fills, transforms, canvas geometry, visible size, clearspace, themed variants and accessible link names unchanged. Never add a second cursor or animate the letters. Reduced motion selects the unchanged static artwork via a native picture source; retain the SVG media-query safeguard too. Original masters, icons, favicons and social artwork remain byte-identical and static. Logo link destinations and accessible names must remain explicit; docs retains a separate docs-home link if the main wordmark links to techdox.nz.

Supply the kit favicon, matching app/touch icons and default social artwork. Preserve article-specific OG images rather than replacing all posts with one generic card. Use `social/blog-og.png` for the blog fallback; don't assume it suits the homepage/docs without inspecting its content.

## Do's and Don'ts

- Do retain the blog serif, accessible light mode, responsive navigation and existing functionality.
- Do compare original assets by checksum and validate desktop/mobile, dark/light, loaded fonts, logo spacing, favicon and OG output.
- Do keep production changes behind existing release workflows; Nick hardware-signs production commits.
- Don't animate the letters, stretch, rotate, outline, glow or recreate the logo with substitute fonts; only the website cursor has an explicit animation override.
- Don't promote the secondary mascot back into the primary logo. No mascot source is included.
- Don't apply this identity to separate products without a new scope decision.

## Storage and provenance

Host: elitron-cloud. Canonical directory: `/home/techdox/brand/techdox/`.
Original archive: `Techdox-Brand-Kit.original.zip`.
SHA-256: `fc044d1bf92ff8c95424b8599b471c6a81bd381baf1e3608021d58e635aa99e9`.
Clean source tree: `Techdox-Brand-Kit/` (83 files; macOS metadata omitted).
Per-file hashes: `archive-inventory.json`.
This is persistent local storage, not a verified off-host backup.
