# thefamilygems.com

Static website for The Family Gem Shop (loose gemstones, sold on Etsy).

- Edit `CONFIG` / page functions in `build.py`, then run `python3 build.py` (rebuilds every page, `sitemap.xml`, `robots.txt`, `site.webmanifest`).
- `FG_BASE=/ python3 build.py` once the custom domain is live (only affects `404.html` links; everything else uses relative links).
- Brand assets: `tools/brand.py` (favicons, logo PNGs, `img/og.png`).
- No JavaScript, no cookies, no third-party requests. Plain HTML + inline CSS.
