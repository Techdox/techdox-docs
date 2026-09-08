# Cursor regression checks

Run against a served build or immutable preview, with Playwright for Node and Pillow for Python installed:

```sh
BASE_URL=http://127.0.0.1:PORT ARTIFACT_DIR=/tmp/cursor-evidence node scripts/cursor-temporal.cjs
python3 scripts/check-cursor-pixels.py /tmp/cursor-evidence
```

Eight real Chromium screenshots per logo cover dark/light preferences and reduced motion, both shell logos, plus the homepage 404. Pixel differences must stay within the supplied cursor rectangle; reduced motion must remain static and visible. The image element itself is never animated, so computed style on img is not proof of internal SVG behavior. Native picture sources are required because Chromium image SVG media-query inheritance did not reliably follow reduced-motion emulation. Keep evidence outside the repository.
