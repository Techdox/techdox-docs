# Local social-card fonts (Material 9.5.26)

`mkdocs.yml` points the existing social plugin's supported `cache_dir` here and sets `cards_layout_options.font_family: Hanken Grotesk`. The plugin resolves `fonts/Hanken Grotesk/{Regular,Bold}.ttf` locally before considering a Google Fonts download. Keep these fonts tracked; generated card PNGs in this directory are ignored. Nothing here is a browser webfont: existing `docs/fonts/*.woff2` files are unchanged.

The static faces were instantiated with fontTools 4.60.1 from the supplied kit's `fonts/HankenGrotesk.ttf`, SHA-256 `813b3f8fa0965405669a89b38e51bbefd95eef6b8e20d1cb2d8c10cce062662f`. Only the variable weight axis was pinned; glyph coverage was retained. `Regular.ttf` is 400; `Bold.ttf` is the kit's display weight 800 (the filename is Material's lookup key). The supplied OFL license accompanies them.

Reproduction, in a temporary tooling environment with fontTools 4.60.1 (not a runtime/build dependency):

```python
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
for style, weight in [('Regular', 400), ('Bold', 800)]:
    font = TTFont('/path/to/Techdox-Brand-Kit/fonts/HankenGrotesk.ttf', recalcTimestamp=False)
    instantiateVariableFont(font, {'wght': weight}, inplace=True)
    font.save(f'fonts/Hanken Grotesk/{style}.ttf')
```

Expected SHA-256:
- Regular.ttf: `0a4cb26adfce0ba2d7a9fb9f1458f03bddef3e4dc915e7c5b7982a9c879cb095`
- Bold.ttf: `e2e24b5626761a850ad71cb0e8836deaa62fd8c73e2e86bfe97a5b6e284fa7e8`

Version this directory and update the config when changing identity or fonts: Material 9.5 caches cards by text only. The built-brand regression compares actual title pixels against explicitly loaded local Hanken, preventing both Roboto fallback and stale cards. A cold social-card build was exercised with Docker `--network none`; the existing RSS plugin logs a non-fatal remote-image lookup, but font rendering succeeds entirely offline.
