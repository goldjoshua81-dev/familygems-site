"""F (Spectrum Boutique) design pieces for thefamilygems.com.
Ported from the approved designs-5 F mockups (front page approved Oct 16, 2026, 5:24 PM PT;
Our Story approved 5:21 PM PT). Images live in img/, fonts in fonts/, styles in f.css.
Links use the {{root}} token, which build.py replaces per page.
Rules: Price TBD on stones; Muzo/Colombia only in the personal story; US spelling."""
import math, json, pathlib, itertools
A='{{root}}img/'
# Per-stone color (review fix M1, Joshua Oct 16, 2026 7:23 PM PT: "Full rainbow of collection").
# Each stone has ONE `hue` word -> data/palette.json (built + AA-checked by tools/palette.py) -> CSS variables.
# Emerald/gold/cream stay the brand frame; stone colors drive only glow, bands, tints, chips and panels.
PAL=json.loads((pathlib.Path(__file__).resolve().parent/'data'/'palette.json').read_text())
def svars(s):
    t=PAL[s['hue']]
    return f"--stone:{t['stone']};--stone-ink:{t['ink']};--stone-soft:{t['soft']};--stone-line:{t['line']};--stone-glow:{t['glow']}"
def _de(a,b): return sum((x-y)**2 for x,y in zip(PAL[a['hue']]['lab'],PAL[b['hue']]['lab']))**.5
def color_order(stones):
    """Order so neighbors never share a color family and look as different as possible.
    <=8 stones: best permutation (max of the smallest neighbor gap, then the total). More: greedy farthest-next,
    which scales to ~200 stones (O(n^2)) and keeps the newest stone first."""
    st=list(stones)
    if len(st)<=1: return st
    if len(st)<=8:
        best=None
        for perm in itertools.permutations(st[1:]):
            seq=[st[0],*perm]
            if any(seq[i]['hue']==seq[i+1]['hue'] for i in range(len(seq)-1)): continue
            gaps=[_de(seq[i],seq[i+1]) for i in range(len(seq)-1)]
            key=(min(gaps),sum(gaps))
            if best is None or key>best[0]: best=(key,seq)
        if best: return best[1]
    seq=[st.pop(0)]
    while st:
        cand=[s for s in st if s['hue']!=seq[-1]['hue']] or st
        nxt=max(cand,key=lambda s:_de(s,seq[-1])); st.remove(nxt); seq.append(nxt)
    return seq

COLL=[
 ('showcase','Showcase','#8E1B2C','#C98A95','#8E1B2C','#FBF8F1','#4A0D17','Coming soon'),
 ('collection','The Collection','#0F4A3A','#1C6650','#0F4A3A','#FBF8F1','#082E24','5 stones photographed'),
 ('spinel','Spinel','#B8476A','#A99BD1','#B8476A','#FBF8F1','#5E1F35','Coming soon'),
 ('sapphire','Sapphire','#1F3A7A','#4B4A9E','#1F3A7A','#FBF8F1','#0E1C40','Coming soon'),
 ('garnet','Garnet','#B34528','#0F4A3A','#B34528','#FBF8F1','#5A1F10','1 stone photographed'),
 ('tourmaline','Tourmaline','#3FD0C9','#9FD3C1','#267C78','#1E2A24','#134A47','4 stones photographed'),
 ('aquamarine','Aquamarine','#23708A','#9FD3C1','#23708A','#FBF8F1','#0F3746','Coming soon'),
 ('topaz','Topaz','#D08A2E','#23708A','#996622','#1E2A24','#4A300C','Coming soon'),
 ('other','Other gems','#B8955A','#D9BE87','#886E42','#1E2A24','#3F321C','Coming soon'),
]
CD={c[0]:c for c in COLL}

def gem_svg(stroke='currentColor',sw=2.2,cls='gemico'):
    return (f'<svg class="{cls}" viewBox="0 0 100 100" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">'
            '<path d="M32 12h36q20 0 20 20v36q0 20-20 20H32q-20 0-20-20V32q0-20 20-20z"/>'
            '<path d="M38 30h24q8 0 8 8v24q0 8-8 8H38q-8 0-8-8V38q0-8 8-8z"/>'
            '<path d="M18 18L32 32M82 18L68 32M18 82L32 68M82 82L68 68M50 12V30M50 70V88M12 50H30M70 50H88"/></svg>')


# Trust wording APPROVED by Joshua Oct 16, 2026, 7:23 PM PT (replaces "Seller-identified, not guaranteed").
TRUST_LINE=['From my personal collection','GIA-informed descriptions','Photographed honestly, never retouched']
TRUST=[
 ('From my personal collection','Species, weight and origin come from the original seller. Lab reports are shown only when one exists.'),
 ('GIA-informed descriptions','Plain words, checked against GIA-informed facts about each variety.'),
 ('Photographed honestly','Never retouched. Inclusions stay visible; any glow sits behind the photo frame, never on the stone.'),
 ('Unknown says “unknown”','No invented origins, treatments or value claims. Missing facts are marked plainly.'),
]
LORE=[
 ('Why gems matter','Why people have kept, worn and handed down stones for thousands of years, told as stories, not scholarship.','#1F3A7A'),
 ('One family, many minerals','Tourmaline is more than 14 minerals; one of them, elbaite, gives nearly all tourmaline gems (Smithsonian).','#267C78'),
 ('Stories &amp; eras','Famous stones through time, and the human story told again and again in stone.','#8E1B2C'),
]
HUNT_P='Looking for something specific: a colour no one else seems to stock, a shape you’ve only imagined, a stone for a piece that will outlast you? Put me on the hunt. I’ll do my best to find it and deliver.'

def _specs(gem,wt,shape,origin,treat):
    return [('Gemstone',gem),('Weight',wt),('Shape',shape),('Measurements','To measure'),
            ('Clarity','Not graded, inclusions shown as they are'),('Origin',origin),('Treatment',treat)]
def spread_pick(stones,n):
    """Pick n stones that look as different as possible (newest first, then farthest color), then color-order them."""
    st=list(stones); pick=[st.pop(0)]
    while st and len(pick)<n:
        nxt=max(st,key=lambda s:min(_de(s,q) for q in pick)); st.remove(nxt); pick.append(nxt)
    return color_order(pick)

# Facts = listing drafts in familygem/listings/ (approved wording, 7:01 PM PT). hue = palette family (internal word).
STONE01=dict(sku='SF-202',anchor='sf-202',no='Stone 01',title='Green Tourmaline, 5.04 ct',short='Green Tourmaline',ct='5.04 ct',shape='Cushion',hue='forest',coll='tourmaline',
  lead='One stone at a time, from my personal collection. A deep green cushion that throws bright green flashes as it moves; loose and ready for a ring or pendant.',
  photos=['stone-01'],alt='Stone 01, green tourmaline, 5.04 ct cushion',variety='tourmaline-green',
  specs=_specs('Green tourmaline','5.04 ct','Cushion, faceted','Madagascar, per the original seller','No heat, per the original seller'))
SF001=dict(sku='SF-001',anchor='sf-001',no='SF-001',title='Tsavorite Garnet, 1.19 ct',short='Tsavorite Garnet',ct='1.19 ct',shape='Heart',hue='green-vivid',coll='garnet',
  photos=['sf-001'],alt='SF-001, green tsavorite garnet, 1.19 ct heart, in tweezers',variety='tsavorite',
  specs=_specs('Tsavorite garnet','1.19 ct','Heart, faceted','Kenya, per the original seller','Not known'))
STONE02=dict(sku='SF-203',anchor='sf-203',no='Stone 02',title='Pink Tourmaline, 1.42 ct',short='Pink Tourmaline',ct='1.42 ct',shape='Cushion',hue='pink',coll='tourmaline',
  photos=['stone-02'],alt='Stone 02, pink tourmaline, 1.42 ct cushion',variety='tourmaline-pink',
  specs=_specs('Pink tourmaline','1.42 ct','Cushion, faceted','Afghanistan, per the original seller','No heat, per the original seller'))
STONE03=dict(sku='SF-204',anchor='sf-204',no='Stone 03',title='Green Tourmaline, 1.26 ct',short='Green Tourmaline',ct='1.26 ct',shape='Cushion',hue='green',coll='tourmaline',
  photos=['stone-03'],alt='Stone 03, crisp green tourmaline, 1.26 ct elongated cushion',variety='tourmaline-green',
  specs=_specs('Green tourmaline','1.26 ct','Elongated cushion, faceted','Afghanistan, per the original seller','No heat, per the original seller'))
STONE04=dict(sku='SF-205',anchor='sf-205',no='Stone 04',title='Light Bluish Green Tourmaline, 1.02 ct',short='Light Bluish Green Tourmaline',ct='1.02 ct',shape='Emerald cut',hue='mint',coll='tourmaline',
  photos=['stone-04'],alt='Stone 04, light bluish green tourmaline, 1.02 ct emerald cut',variety='tourmaline-bluegreen',
  specs=_specs('Light bluish green tourmaline','1.02 ct','Emerald cut, faceted','Afghanistan, per the original seller','No heat, per the original seller'))
STONES=[STONE04,STONE03,SF001,STONE02,STONE01]   # newest first; every photographed stone on the site
for _s in STONES:
    assert _s['hue'] in PAL, f"{_s['sku']}: hue '{_s['hue']}' not in data/palette.json"
    assert _s['sku'] in _s['alt'] or _s['no'] in _s['alt'], _s['sku']
    assert _s['ct'] in _s['alt'], f"{_s['sku']}: alt must name the weight"

# Approved wording (Joshua, Oct 16, 2026, 7:01 PM PT). Variety text copied from familygem/listings/variety-blurbs/ (KB-cited there).
CLOSE='From my personal collection. Species, weight and origin come from the original seller. No lab report. What you see is the real stone, photographed honestly and never retouched.'
VARIETY={'tsavorite':"Green grossular garnet, colored by vanadium and chromium. Campbell Bridges found it in Tanzania in 1967 and in Kenya in 1970; it was named tsavorite in 1973 and reached jewelry buyers in 1974. Rarer than red garnet, because it needs unusual rock chemistry, and most stones are small. Singly refractive, often red through a Chelsea filter, hardness 7 to 7.5. As a species it generally isn't treated; that's about the variety, not any one stone.",
 'tourmaline-green':'Not one mineral but a whole family of borosilicates; elbaite gives us most gem tourmaline, and liddicoatite is named for Richard T. Liddicoat. One of the widest color ranges of any gem: one pegmatite pocket can turn up several colors, and one crystal can grow pink at the core and green at the rim. Iron is what makes it green. Doubly refractive and strongly pleochroic, so the color shifts as you turn it. Hardness 7 to 7.5; mined worldwide, from Brazil to Namibia and Russia (GIA).',
 'tourmaline-bluegreen':'Not one mineral but a whole family of borosilicates; elbaite gives us most gem tourmaline, and liddicoatite is named for Richard T. Liddicoat. One of the widest color ranges of any gem: one pegmatite pocket can turn up several colors, and one crystal can grow pink at the core and green at the rim. Iron is what makes it blue to green. Doubly refractive and strongly pleochroic, so the color shifts as you turn it. Hardness 7 to 7.5; mined worldwide, from Brazil to Namibia and Russia (GIA).',
 'tourmaline-pink':'Not one mineral but a whole family of borosilicates; elbaite gives us most gem tourmaline, and liddicoatite is named for Richard T. Liddicoat. One of the widest color ranges of any gem: one pegmatite pocket can turn up several colors, and one crystal can grow pink at the core and green at the rim. Manganese is what makes it pink. Doubly refractive and strongly pleochroic, so the color shifts as you turn it. Hardness 7 to 7.5; mined worldwide, from Brazil to Namibia and Russia (GIA).'}

STORY_SHORT=("When I was three or four, my dad bought a crisp apple-green Muzo emerald from Colombia, set in a 14k gold tension ring "
 "with gold nuggets down the sides. It hooked me for life. That emerald crowns our crest, and the diamond below it stands for the whole family.")
# LONG story: Joshua's exact text, APPROVED Oct 16, 2026, 5:21 PM PT (pass 8). Short story APPROVED 5:24 PM PT. Do not edit without his yes.
STORY_LONG_P=[
 "One of my earliest memories is a jewelry shop in Napa. I sat wide-eyed as the jeweler laid out four emeralds and handed my dad a loupe. I was straining to see, so my dad passed it to me, and one emerald pulled me straight in. The light bounced around inside it, throwing a color you can’t explain. It just has to be seen. That crisp apple-green Muzo emerald from Colombia became a 14k gold tension ring with gold nuggets down the sides.",
 "Later, in Elk Grove, my dad and the local jeweler would talk about the amazing gems that had just come in: watermelon tourmaline, sapphire, alexandrite, black opal from Australia. Those talks stuck with me.",
 "Every stone in my collection has its own story of how it came to me. Now each one is moving to its new home for the next part of its journey.",
 "That emerald crowns our crest. The diamond below it stands for the whole family."]
STORY_LONG=" ".join(STORY_LONG_P)
PULL="A color you can’t explain. It just has to be seen."
# Personal story photo only (Joshua's dad's ring). Muzo/Colombia applies to this ring story, never to any stone for sale.
RING_IMG=A+'our-story-ring-'; RING_SM=A+'our-story-ring-'
RING_CAP="My dad’s emerald, the one that started it all."
RING_NOTE="Phone photo, cleaned up for light, color and background."


def _ring():
    stops=[f'{c[2]} {max(i*40-14,0)}deg {i*40+14}deg' for i,c in enumerate(COLL)]
    return 'conic-gradient(from 0deg,'+','.join(stops)+f',{COLL[0][2]} 346deg)'
RING=_ring()
SPEC='linear-gradient(90deg,#0F4A3A,#3FD0C9,#23708A,#1F3A7A,#4B4A9E,#A99BD1,#B8476A,#8E1B2C,#B34528,#D08A2E,#B8955A)'


def chip(c,txt=None):
    return f'<span class="chip" style="--bg:{c[2]}1c;--fg:{c[4]}"><i style="background:{c[2]}"></i>{txt or c[1]}</span>'

def dots():
    out=''
    for i,c in enumerate(COLL):
        ang=math.radians(-90+i*40); r=45.5
        x=50+r*math.cos(ang); y=50+r*math.sin(ang)
        side='left:28px' if math.cos(ang)>=0.01 else ('right:28px' if math.cos(ang)<-0.01 else 'left:28px')
        out+=f'<div class="dot" style="left:calc({x:.2f}% - 12px);top:calc({y:.2f}% - 12px);background:{c[2]}"><span style="{side};color:{c[4]}">{c[1]}</span></div>'
    return out

def framed(s,cls='fr',i=0,sizes='(max-width:820px) 45vw, 300px'):
    return f'<div class="glow" style="{svars(s)}"><div class="{cls}"><div class="photo"><img src="{A}{s["photos"][i]}-400.jpg" srcset="{A}{s["photos"][i]}-400.jpg 400w, {A}{s["photos"][i]}-800.jpg 800w" sizes="{sizes}" width="400" height="400" loading="lazy" decoding="async" alt="{s["alt"]}"></div></div></div>'

def cc(c,cls=''):
    k,n,b,acc,txt,lab,dark,st=c
    light=k in('tourmaline','topaz','other')
    bg=f'background:radial-gradient(ellipse 75% 85% at 100% 0%,{acc}{"cc" if light else "aa"},transparent 60%),linear-gradient(150deg,{b},{txt if light else dark});--sh:{b}'
    extra=''
    if k=='tourmaline':
        extra=(f'<div class="ph2"><div>{framed(STONE01)}<small>Stone 01 · <em>5.04 ct</em></small></div>'
               f'<div>{framed(STONE02)}<small>Stone 02 · <em>1.42 ct</em></small></div></div>')
    strip=f'<div class="chipstrip"><i style="background:{acc}"></i><i style="background:{b}"></i><i style="background:{dark}"></i></div>'
    return (f'<div class="cc {cls}" style="{bg}"><div style="display:flex;justify-content:space-between;align-items:start">{gem_svg()}</div>'
            f'{gem_svg(cls="gemico wm",sw=4)}<div>{extra if cls=="hero2" else ""}<h3 style="margin-top:{18 if cls=="hero2" else 0}px">{n}</h3><span class="cnt{" soon" if st=="Coming soon" else ""}">{st}</span>{strip}</div></div>')

def pcard(s,href=None):
    """Stone card. Color = the stone's own palette family (CSS vars); chip = its collection.
    Links to the stone's section on /shop/ (no /stones/ URLs until Joshua says yes)."""
    c=CD[s['coll']]
    href=href or f'{{{{root}}}}shop/#{s["anchor"]}'
    pic=f'<div class="pic">{framed(s)}</div>'
    meta=(f'<div class="row">{chip(c)}<span class="no">{s["no"]}</span></div><h3>{s["short"]}</h3><div class="sub">{s["ct"]} · {s["shape"]}</div>'
          f'<div class="row" style="margin-top:10px"><span class="soonchip">Coming soon · Price TBD</span><span class="go" aria-hidden="true">→</span></div>')
    return f'<a class="pc" href="{href}" style="{svars(s)}"><div class="band"></div>{pic}<div class="meta">{meta}</div></a>'

LEGEND='<div class="legend"><span><i class="gem-e"></i><b>Emerald</b> · where it started</span><span><i class="gem-d"></i><b>Diamond</b> · the whole family</span></div>'


def home_body():
    s1=STONE01
    order=[('tourmaline','hero2'),('sapphire',''),('spinel',''),('garnet',''),('aquamarine',''),('topaz',''),('other',''),('showcase',''),('collection','')]
    cards=''.join(cc(CD[k],cls) for k,cls in order)
    tcol=[('#0F4A3A','#EEF6F2'),('#1F3A7A','#EEF1FA'),('#B34528','#FBF0EA'),('#4B4A9E','#F3F1FA')]
    lcol=[('#1F3A7A','#EEF1FA'),('#267C78','#EAF7F6'),('#8E1B2C','#FBEDEF')]
    body=f'''<div class="wrap">
<section class="hero"><div class="in"><div><span class="pill" style="--c:#D9487A"><i></i>New: {len(STONES)} stones photographed</span>
<h1>Every colour, <span class="sw">one stone</span> at a time.</h1>
<p class="lede">Hand-picked loose gemstones from my personal collection, sorted by colour. Each one is photographed honestly, never retouched, and described in plain words.</p>
<div class="ctas"><a class="btn pri rnd" href="{{{{root}}}}shop/">Shop the collection</a><a class="btn out rnd" href="{{{{root}}}}contact/">Put me on the hunt</a></div>
<div class="minitrust"><span>Personal collection</span><span>Inclusions shown</span><span>Never retouched</span></div></div>
<div class="wheel"><div class="ring"></div><div class="ring2"></div>{dots()}
<div class="hcard glow" style="{svars(s1)}"><div class="photo"><img src="{A}stone-01-800.jpg" srcset="{A}stone-01-400.jpg 400w, {A}stone-01-800.jpg 800w" sizes="(max-width:820px) 176px, 300px" width="800" height="800" fetchpriority="high" alt="{s1['alt']}"></div><div class="lab"><span class="nm2">Green Tourmaline</span>{chip(CD['tourmaline'],'Stone 01')}</div></div>
<div class="tag t1"><b>5.04 ct</b>Cushion · faceted</div>
<div class="tag t2">Tourmaline colours<div class="dr"><i style="background:#2F6B1E"></i><i style="background:#D9487A"></i><i style="background:#3FD0C9"></i><i style="background:#2E6FB0"></i></div></div>
<div class="tag t3"><b>Price TBD</b>From my collection</div></div></div>
<div class="chips">{"".join(chip(c) for c in COLL)}</div></section>
<section class="blk"><div class="sh"><div><div class="label" style="color:#B34528">Shop by gem</div><h2>Pick a colour</h2></div><p>Nine collections, nine colours. Tourmaline and garnet have real photos today; the rest fill in as each stone is photographed.</p></div><div class="cg">{cards}</div></section>
<section class="blk"><div class="sh"><div><div class="label" style="color:#B8476A">Just photographed</div><h2>Fresh from the collection</h2></div><a class="more" style="--uc:#B8476A" href="{{{{root}}}}shop/">View the shop →</a></div><div class="pg">{"".join(pcard(s) for s in color_order([x for x in STONES if x is not STONE01])[:4])}</div></section>
<section class="blk"><div class="ls"><div class="crest"><img src="{A}crest-280.jpg" width="280" height="280" loading="lazy" alt="The Family Gem Shop crest: FG with an emerald above and a diamond below"></div>
<div class="txt"><div class="halo"></div><div class="label" style="color:#1C6650">Our crest</div><h2>The emerald that <em>started it all</em></h2><p>{STORY_SHORT}</p><div class="ringnote"><div class="rf"><img src="{RING_SM}400.jpg" width="400" height="250" loading="lazy" alt="My dad’s 14k gold tension ring with a green emerald"></div><span>{RING_CAP}</span></div>{LEGEND}<a class="link" href="{{{{root}}}}about/">Read Our Story →</a></div></div></section>
<section class="blk"><div class="sh"><div><div class="label" style="color:#1F3A7A">How we describe stones</div><h2>No surprises</h2></div><p>The same four promises on every stone page.</p></div>
<div class="tg">{"".join(f'<div class="tc" style="--bg:{bg};--c:{c}"><div class="ic">{gem_svg()}</div><h4>{h}</h4><p>{p}</p></div>' for (h,p),(c,bg) in zip(TRUST,tcol))}</div></section>
<section class="blk"><div class="duo"><div class="huntc"><div class="label" style="color:var(--golds)">The Hunt</div><h2>Put me on the hunt.</h2><p>{HUNT_P}</p><a class="btn rnd white" href="{{{{root}}}}contact/">Start a hunt</a><div class="rg"></div></div>
<div class="lg">{"".join(f'<div class="lc" style="--bg:{bg};--c:{c}">{gem_svg()}<div><h3>{t}</h3><p>{p}</p></div></div>' for (t,p,_),(c,bg) in zip(LORE,lcol))}</div></div></section>
</div>'''
    return _us(body)

def story_body():
    body=f'''<div class="wrap">
<section class="shero"><div class="rg"></div><img class="cr" src="{A}crest-280.jpg" width="210" height="210" alt="The Family Gem Shop crest: FG with an emerald above and a diamond below">
<div class="ft l"><i class="gem-e"></i><div><b>The emerald</b>Where it started</div></div><div class="ft r"><i class="gem-d"></i><div><b>The diamond</b>The whole family</div></div><span class="pill" style="--c:#46C38A"><i></i>Our Story</span>
<h1>Gems are in my <em>veins.</em></h1><div class="sub">Where The Family Gem Shop began</div><div class="sp2"></div></section>
<section class="sbody ed"><div class="side"><figure class="ringfig"><div class="rf"><img src="{RING_IMG}800.jpg" srcset="{RING_IMG}400.jpg 400w, {RING_IMG}800.jpg 800w, {RING_IMG}1600.jpg 1600w" sizes="(max-width:820px) 92vw, 440px" width="800" height="500" loading="lazy" decoding="async" alt="My dad’s 14k gold tension ring: a green emerald held in the tension head, gold nuggets along the sides"></div><figcaption>{RING_CAP}<small>{RING_NOTE}</small></figcaption></figure>
<div class="legendcard slim"><div class="row"><i class="gem-e"></i><div><b>The emerald, on top</b><span>Where it started: the emerald my dad bought when I was three or four.</span></div></div>
<div class="row"><i class="gem-d"></i><div><b>The diamond, below</b><span>The whole family.</span></div></div></div></div>
<div class="txt"><div class="label">Our crest</div><h2>The emerald that started it all</h2><div class="rule" style="margin-left:0"><i></i></div>
<p class="long lede">{STORY_LONG_P[0]}</p>
<blockquote class="pq"><q>{PULL}</q><span>The first emerald</span></blockquote>
<p class="long">{STORY_LONG_P[1]}</p><p class="long">{STORY_LONG_P[2]}</p><p class="long close">{STORY_LONG_P[3]}</p><div class="sig">— Josh</div></div></section>
</div>'''
    return _us(body)


ANN='<div class="ann" role="note">'+''.join(f'<span style="--c:{c}">{w}</span>' for w,c in zip(TRUST_LINE,('#D9487A','#D9BE87','#3FD0C9')))+'</div>'
NAV=[('shop/','Shop'),('guides/','Guides'),('about/','Our Story'),('faq/','FAQ'),('contact/','Contact')]
ABOUT_SHORT='The Family Gem Shop: personal-collection gems, listed one stone at a time. Put me on the hunt when you need what no one else can find.'

def brand():
    return '<a class="brand" href="{{root}}"><img src="{{root}}img/crest-128.jpg" width="50" height="50" alt=""><span class="nm">The Family Gem Shop</span></a>'

def header(active=''):
    links=''.join(f'<a href="{{{{root}}}}{h}"'+(' class="on" aria-current="page"' if h==active else '')+f'>{n}</a>' for h,n in NAV)
    return (f'<a class="skip" href="#main">Skip to content</a><div class="spec-line"></div>{ANN}<header>{brand()}'
            f'<nav class="nav" aria-label="Main">{links}</nav>'
            f'<div class="hd-r"><a class="ask" href="{{{{root}}}}contact/">Put me on the hunt</a>'
            f'<details class="mnav"><summary><b aria-hidden="true"></b>Menu</summary><nav aria-label="Mobile">{links}</nav></details></div></header>')

def footer(etsy):
    fl=[('shop/','Shop'),('about/','Our Story'),('guides/','Guides'),('faq/','FAQ'),('contact/','Contact'),('privacy/','Privacy')]
    links=''.join(f'<a href="{{{{root}}}}{h}">{n}</a>' for h,n in fl)+f'<a href="{etsy}" rel="noopener">Etsy shop</a>'
    return (f'<footer><div class="spec-line"></div><div class="fg"><div>{brand()}<p>{ABOUT_SHORT}</p></div>'
            f'<nav class="fl" aria-label="Footer">{links}</nav></div>'
            f'<div class="copy">&copy; 2026 The Family Gem Shop · {" · ".join(TRUST_LINE)}. Loose gemstones, sold on Etsy.</div></footer>')

# US spelling (Joshua, Oct 16)
_US=[('Colourless','Colorless'),('colourless','colorless'),('Colour','Color'),('colour','color')]
def _us(h):
    for a,b in _US: h=h.replace(a,b)
    return h


# ---------------------------------------------------------------- shop + inner pages (review fixes, Oct 16, 2026 7:23 PM PT)
VNAME={'tsavorite':'tsavorite','tourmaline-green':'tourmaline','tourmaline-pink':'tourmaline','tourmaline-bluegreen':'tourmaline'}

def chiprow():
    return f'<div class="chips">{"".join(chip(c) for c in COLL)}</div>'

def phead(label,h1,lead,crumbs='',extra='',lc='#B8476A'):
    """F page header for inner pages: white stage with multi-color micro-glows + spectrum hairline."""
    return (f'<section class="phead">{crumbs}<div class="label" style="color:{lc}">{label}</div><h1>{h1}</h1>'
            f'<p class="lead">{lead}</p>{extra}<div class="sp3"></div></section>')

def stone_detail(s,etsy):
    c=CD[s['coll']]
    rows=''.join(f'<dt>{k}</dt><dd{" class=unk" if v in ("To measure","Not known") else ""}>{v}</dd>' for k,v in s['specs'])
    v=VNAME[s['variety']]
    return f'''<article class="sd" id="{s['anchor']}" style="{svars(s)}">
<div class="sdp">{framed(s,'fr',0,'(max-width:820px) 88vw, 400px')}</div>
<div class="sdt"><div class="row">{chip(c)}<span class="no">{s['no'] if s['no']==s['sku'] else s['no']+' · '+s['sku']}</span></div>
<h2>{s['title']}</h2>
<dl class="spec2">{rows}<dt>Price</dt><dd>Price TBD</dd></dl>
<p class="closenote">{CLOSE}</p>
<div class="vbox"><h3>About {v}</h3><p>{VARIETY[s['variety']]}</p></div>
<div class="sdcta"><span class="soonchip">Coming soon to Etsy</span><a class="btn out rnd" href="{etsy}" rel="noopener">Favorite the shop on Etsy</a></div></div>
</article>'''

def shop_body(crumbs,etsy):
    order=color_order(STONES)
    lead=('Every stone here is from my personal collection, photographed honestly and never retouched. '
          'They list on Etsy one at a time, where checkout, payment and tracking are handled for you.')
    extra=(f'<div class="ctas"><a class="btn pri rnd" href="{etsy}" rel="noopener">Favorite the shop on Etsy</a>'
           f'<a class="btn out rnd" href="{{{{root}}}}contact/">Put me on the hunt</a></div>{chiprow()}')
    cards=''.join(pcard(s,href=f'#{s["anchor"]}') for s in order)
    details=''.join(stone_detail(s,etsy) for s in order)
    steps=[('Find your stone','Check the photos, weight, shape and specs. Measurements in mm come before each listing goes live.','#2E6FB0'),
           ('Ask anything','Message me on Etsy before you buy: more photos, a video, exact size.','#D9487A'),
           ('Check out on Etsy','Etsy handles payment. Shipping and returns are shown on each listing.','#D08A2E'),
           ('Set it or keep it','Take it to your jeweler, or keep it in your collection.','#6A5ACD')]
    how=''.join(f'<div class="tc" style="--bg:{c}14;--c:{c}"><div class="ic">{gem_svg()}</div><h4>{h}</h4><p>{p}</p></div>' for h,p,c in steps)
    body=f'''<div class="wrap">
{phead('The shop','Shop loose gemstones',lead,crumbs,extra)}
<section class="blk"><div class="sh"><div><div class="label" style="color:#2E6FB0">{len(STONES)} stones photographed</div><h2>The collection so far</h2></div><p>Each card jumps to that stone’s specs and story. New colors are added as each stone is photographed.</p></div><div class="pg pg5">{cards}</div></section>
<section class="blk sds" aria-label="Stone details">{details}</section>
<section class="blk"><div class="sh"><div><div class="label" style="color:#A95719">How buying works</div><h2>Four easy steps</h2></div><p>Favorite the shop on Etsy to see each stone the day it lists.</p></div><div class="tg">{how}</div></section>
</div>'''
    return _us(body)

def guides_extra():
    """Variety notes for /guides/ (same KB-cited text as the stone sections)."""
    cards=[(SF001,'Tsavorite','tsavorite'),(STONE02,'Tourmaline','tourmaline-pink')]
    return ''.join(f'<div class="vcard" style="{svars(s)}"><div class="label" style="color:var(--stone-ink)">Variety notes</div><h3>About {n.lower()}</h3><p>{VARIETY[k]}</p></div>' for s,n,k in cards)
