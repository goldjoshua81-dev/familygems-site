#!/usr/bin/env python3
"""Per-stone color palette for The Family Gem Shop (review fix M1, Joshua Oct 16, 2026: "Full rainbow of collection").

One word per stone (`hue` in fsite.STONES) picks a family here. This script derives the CSS tokens for each
family, checks contrast (WCAG AA), and writes data/palette.json, which build.py reads. build.py re-checks and
refuses to build if a stone has no hue or a token pair fails.

Tokens per family (all used through CSS variables, never hard-coded per stone):
  --stone       swatch (bands, dots, hairlines)
  --stone-ink   text/border shade, >= 4.5:1 on white, ivory and on --stone-soft
  --stone-soft  ~10% tint for panels and chips
  --stone-glow  the stone color at <= 25% alpha (glow behind the photo frame only)
  --stone-line  ~35% tint hairline
Family keys are internal names only; public copy uses plain color words (no trade names).
Emerald/gold/cream stay the brand frame (header, buttons, footer, trust bar) and are not in this file.
Run:  python3 tools/palette.py   (rewrites data/palette.json)
"""
import json, colorsys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
# family: (swatch hex, plain public color word)
BASE = {
 'red':        ('#B3243A', 'red'),
 'pink':       ('#D9487A', 'pink'),
 'orange':     ('#E07B2E', 'orange'),
 'peach':      ('#E8A27E', 'peach'),
 'yellow':     ('#E2B93B', 'yellow'),
 'champagne':  ('#C9A46A', 'champagne'),
 'brown':      ('#8A5A3B', 'brown'),
 'forest':     ('#2F6B1E', 'deep green'),
 'green':      ('#3E9B4F', 'green'),
 'green-vivid':('#1FA35A', 'vivid green'),
 'mint':       ('#7FCDB5', 'light bluish green'),
 'teal':       ('#2BA8A0', 'blue-green'),
 'blue':       ('#2E6FB0', 'blue'),
 'violet':     ('#6A5ACD', 'violet'),
 'colorless':  ('#B9C4CF', 'colorless'),
 'black':      ('#3A3D42', 'black'),
}
WHITE, IVORY = '#FFFFFF', '#FBF8F1'

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def hx(c): return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)
def lum(h):
    def f(x): x /= 255; return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h); return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def contrast(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
def mix(a, b, t):  # t of a over b
    A, B = rgb(a), rgb(b); return hx([A[i] * t + B[i] * (1 - t) for i in range(3)])
def lab(h):
    def f(x): x /= 255; return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = [f(v) for v in rgb(h)]
    X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047; Y = 0.2126 * r + 0.7152 * g + 0.0722 * b; Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    g_ = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return (116 * g_(Y) - 16, 500 * (g_(X) - g_(Y)), 200 * (g_(Y) - g_(Z)))

def ink_for(sw, soft):
    """Darken the swatch (keep hue) until it passes 4.5:1 on white, ivory and the soft tint."""
    r, g, b = [v / 255 for v in rgb(sw)]; h, l, s = colorsys.rgb_to_hls(r, g, b)
    while l > 0.02:
        c = hx([v * 255 for v in colorsys.hls_to_rgb(h, l, min(1, s))])
        if min(contrast(c, WHITE), contrast(c, IVORY), contrast(c, soft)) >= 4.5: return c
        l -= 0.01
    return '#1E2A24'

def build():
    out = {}
    for k, (sw, word) in BASE.items():
        soft = mix(sw, WHITE, 0.11)
        ink = ink_for(sw, soft)
        r, g, b = rgb(sw)
        out[k] = {'word': word, 'stone': sw, 'ink': ink, 'soft': soft, 'line': mix(sw, WHITE, 0.35),
                  'glow': f'rgba({r},{g},{b},.22)', 'lab': [round(v, 1) for v in lab(sw)]}
    return out

def check(pal):
    bad = []
    for k, t in pal.items():
        for bg in (WHITE, IVORY, t['soft']):
            c = contrast(t['ink'], bg)
            if c < 4.5: bad.append(f'{k}: ink {t["ink"]} on {bg} = {c:.2f}')
        if float(t['glow'].rsplit(',', 1)[1].rstrip(')')) > 0.25: bad.append(f'{k}: glow alpha > .25')
    return bad

if __name__ == '__main__':
    pal = build(); bad = check(pal)
    if bad: raise SystemExit('palette contrast FAIL:\n' + '\n'.join(bad))
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'palette.json').write_text(json.dumps(pal, indent=1))
    for k, t in pal.items():
        print(f'{k:12s} {t["stone"]} ink {t["ink"]} ({contrast(t["ink"], IVORY):.2f}:1 ivory, {contrast(t["ink"], t["soft"]):.2f}:1 soft) soft {t["soft"]}')
    print('ok,', len(pal), 'families, all AA')
