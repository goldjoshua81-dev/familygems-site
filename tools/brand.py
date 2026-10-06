#!/usr/bin/env python3
"""Regenerate favicon.svg/.ico, apple-touch-icon.png, img/logo-192/512.png and img/og.png.
Run with: /workspace/.venv-pw/bin/python tools/brand.py"""
import pathlib, io
from playwright.sync_api import sync_playwright
import sys; sys.path.append("/usr/local/lib/python3.13/dist-packages")
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
GEM = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 92">'
  '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5fd39a"/>'
  '<stop offset=".55" stop-color="#14874f"/><stop offset="1" stop-color="#0b3d26"/></linearGradient></defs>'
  '<path d="M50 88 12 50C0 37 4 14 24 12c12-1 21 6 26 16 5-10 14-17 26-16 20 2 24 25 12 38Z" fill="url(#g)"/>'
  '<path d="M50 28 50 88M24 12 50 46 76 12M12 50 50 46 88 50M50 28 32 34 12 50M50 28 68 34 88 50" '
  'stroke="#fff" stroke-opacity=".35" stroke-width="1.2" fill="none"/></svg>')
(R / "favicon.svg").write_text(GEM)
ICON = f'<html><body style="margin:0;width:512px;height:512px;background:#fbfaf7;display:grid;place-items:center">' \
       f'<div style="width:400px">{GEM}</div></body></html>'
OG = f'''<html><body style="margin:0;width:1200px;height:630px;background:linear-gradient(150deg,#0f5132,#0a2e1d);
display:flex;align-items:center;gap:60px;padding:0 80px;box-sizing:border-box;font-family:Georgia,serif;color:#fff">
<div style="width:300px;flex:none">{GEM}</div><div><div style="font-size:72px;line-height:1.05;font-weight:700">The Family<br>Gem Shop</div>
<div style="font:400 34px/1.35 system-ui,sans-serif;margin-top:24px;color:#d6efe0">Loose gemstones &amp; heart-cut tsavorite<br>for jewelry that means something</div>
<div style="font:600 26px system-ui,sans-serif;margin-top:28px;color:#9fe0bb">thefamilygems.com</div></div></body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 512, "height": 512})
    pg.set_content(ICON); png = pg.screenshot()
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    im.save(R / "img/logo-512.png", optimize=True)
    im.resize((192, 192), Image.LANCZOS).save(R / "img/logo-192.png", optimize=True)
    im.resize((180, 180), Image.LANCZOS).save(R / "apple-touch-icon.png", optimize=True)
    # transparent-ish favicon: render gem only
    pg2 = b.new_page(viewport={"width": 256, "height": 256})
    pg2.set_content(f'<html><body style="margin:0;background:transparent;width:256px;height:256px;display:grid;place-items:center"><div style="width:240px">{GEM}</div></body></html>')
    fav = Image.open(io.BytesIO(pg2.screenshot(omit_background=True))).convert("RGBA")
    fav.save(R / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    pg3 = b.new_page(viewport={"width": 1200, "height": 630})
    pg3.set_content(OG); og = Image.open(io.BytesIO(pg3.screenshot())).convert("RGB")
    og.save(R / "img/og.png", optimize=True)
    b.close()
print("brand assets written")
