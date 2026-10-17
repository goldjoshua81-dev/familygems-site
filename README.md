# thefamilygems.com

Static website for The Family Gem Shop (loose gemstones, sold on Etsy).

- Edit `CONFIG` / page functions in `build.py`, then run `python3 build.py` (rebuilds every page, `sitemap.xml`, `robots.txt`, `site.webmanifest`).
- `FG_BASE=/ python3 build.py` once the custom domain is live (only affects `404.html` links; everything else uses relative links).
- Brand assets: `tools/brand.py` (favicons, logo PNGs, `img/og.png`).
- No JavaScript, no cookies, no third-party requests. Plain HTML + one first-party stylesheet.
- Design: direction F (Spectrum Boutique). `f.css` (styles), `fsite.py` (header, footer, front page and Our Story bodies), `fonts/` (self-hosted Inter + Cormorant Garamond woff2 subsets, OFL), `img/` (crest, stone and Our Story photos, pre-sized 400/800/1600).
- Build with `python3 build.py` (404 links default to `/` for thefamilygems.com; use `FG_BASE=/familygems-site/` only for a github.io preview).
