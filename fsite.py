"""F (Spectrum Boutique) design pieces for thefamilygems.com.
Ported from the approved designs-5 F mockups (front page approved Oct 16, 2026, 5:24 PM PT;
Our Story approved 5:21 PM PT). Images live in img/, fonts in fonts/, styles in f.css.
Links use the {{root}} token, which build.py replaces per page.
Rules: Price TBD on stones; Muzo/Colombia only in the personal story; US spelling."""
import math
A='{{root}}img/'
G01='rgba(104,150,34,.24)'   # Stone 01 own color (green), <=25% alpha
G02='rgba(224,72,128,.22)'   # Stone 02 own color (pink)

COLL=[
 ('showcase','Showcase','#8E1B2C','#C98A95','#8E1B2C','#FBF8F1','#4A0D17','Photos coming'),
 ('collection','The Collection','#0F4A3A','#1C6650','#0F4A3A','#FBF8F1','#082E24','2 stones photographed'),
 ('spinel','Spinel','#B8476A','#A99BD1','#B8476A','#FBF8F1','#5E1F35','Photos coming'),
 ('sapphire','Sapphire','#1F3A7A','#4B4A9E','#1F3A7A','#FBF8F1','#0E1C40','Photos coming'),
 ('garnet','Garnet','#B34528','#0F4A3A','#B34528','#FBF8F1','#5A1F10','Photos coming'),
 ('tourmaline','Tourmaline','#3FD0C9','#9FD3C1','#267C78','#1E2A24','#134A47','2 stones photographed'),
 ('aquamarine','Aquamarine','#23708A','#9FD3C1','#23708A','#FBF8F1','#0F3746','Photos coming'),
 ('topaz','Topaz','#D08A2E','#23708A','#996622','#1E2A24','#4A300C','Photos coming'),
 ('other','Other gems','#B8955A','#D9BE87','#886E42','#1E2A24','#3F321C','Photos coming'),
]
CD={c[0]:c for c in COLL}

def gem_svg(stroke='currentColor',sw=2.2,cls='gemico'):
    return (f'<svg class="{cls}" viewBox="0 0 100 100" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">'
            '<path d="M32 12h36q20 0 20 20v36q0 20-20 20H32q-20 0-20-20V32q0-20 20-20z"/>'
            '<path d="M38 30h24q8 0 8 8v24q0 8-8 8H38q-8 0-8-8V38q0-8 8-8z"/>'
            '<path d="M18 18L32 32M82 18L68 32M18 82L32 68M82 82L68 68M50 12V30M50 70V88M12 50H30M70 50H88"/></svg>')


TRUST=[
 ('Seller-identified','Not guaranteed. Every stone is identified by us and described from our collection labels.'),
 ('GIA-informed','Descriptions follow GIA-informed language. Lab reports are shown only when one exists.'),
 ('Photographed as it is','Inclusions stay visible. Glow is added to the background only, never to the stone.'),
 ('Unknown says “unknown”','No invented origins, treatments or value claims. Missing facts are marked plainly.'),
]
LORE=[
 ('Why gems matter','Why people have kept, worn and handed down stones for thousands of years, told as stories, not scholarship.','#1F3A7A'),
 ('One family, many minerals','Tourmaline is more than 14 minerals; one of them, elbaite, gives nearly all tourmaline gems (Smithsonian).','#267C78'),
 ('Stories &amp; eras','Famous stones through time, and the human story told again and again in stone.','#8E1B2C'),
]
HUNT_P='Looking for something specific: a colour no one else seems to stock, a shape you’ve only imagined, a stone for a piece that will outlast you? Put me on the hunt. I’ll do my best to find it and deliver.'

STONE01=dict(no='Stone 01',title='Green Tourmaline, 5.04 ct',short='Green Tourmaline',ct='5.04 ct',shape='Cushion',
  lead='One stone at a time, from my personal collection. A deep green cushion that throws bright green flashes as it moves; loose and ready for a ring or pendant.',
  photos=['stone-01'],glow=G01,alt='Stone 01, green tourmaline, 5.04 ct cushion (seller-identified)')
STONE02=dict(no='Stone 02',title='Pink Tourmaline, 1.42 ct',short='Pink Tourmaline',ct='1.42 ct',shape='Cushion',photos=['stone-02'],glow=G02,alt='Stone 02, pink tourmaline, 1.42 ct cushion (seller-identified)')


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
    return f'<span class="chip" style="--bg:{c[3]}33;--fg:{c[4]}"><i style="background:{c[2]}"></i>{txt or c[1]}</span>'

def dots():
    out=''
    for i,c in enumerate(COLL):
        ang=math.radians(-90+i*40); r=45.5
        x=50+r*math.cos(ang); y=50+r*math.sin(ang)
        side='left:28px' if math.cos(ang)>=0.01 else ('right:28px' if math.cos(ang)<-0.01 else 'left:28px')
        out+=f'<div class="dot" style="left:calc({x:.2f}% - 12px);top:calc({y:.2f}% - 12px);background:{c[2]}"><span style="{side};color:{c[4]}">{c[1]}</span></div>'
    return out

def framed(s,cls='fr',i=0):
    return f'<div class="glow" style="--g:{s["glow"]}"><div class="{cls}"><div class="photo"><img src="{A}{s["photos"][i]}-400.jpg" srcset="{A}{s["photos"][i]}-400.jpg 400w, {A}{s["photos"][i]}-800.jpg 800w" sizes="(max-width:820px) 45vw, 300px" width="400" height="400" loading="lazy" decoding="async" alt="{s["alt"]}"></div></div></div>'

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
            f'{gem_svg(cls="gemico wm",sw=4)}<div>{extra if cls=="hero2" else ""}<h3 style="margin-top:{18 if cls=="hero2" else 0}px">{n}</h3><span class="cnt">{st}</span>{strip}</div></div>')

def pcard(s=None,coll='tourmaline'):
    c=CD[coll]
    if s:
        pic=f'<div class="pic" style="--tint:radial-gradient(circle at 50% 45%,{c[3]}44,{c[3]}14 70%)">{framed(s)}</div>'
        meta=f'<div class="row">{chip(c)}<span class="no">{s["no"]}</span></div><h3>{s["short"]}</h3><div class="sub">{s["ct"]} · {s["shape"]}</div><div class="row" style="margin-top:10px"><span class="pr">Price TBD</span></div>'
    else:
        pic=f'<div class="pic" style="--tint:linear-gradient(160deg,{c[3]}55,{c[2]}2a)"><div class="ph" style="color:{c[4]}">{gem_svg()}<span>Photos coming</span></div></div>'
        meta=f'<div class="row">{chip(c)}</div><h3>Photos coming</h3><div class="sub">Next stone from the collection</div><div class="row" style="margin-top:10px"><span class="pr" style="color:var(--muted)">Price TBD</span></div>'
    return f'<div class="pc"><div class="band" style="background:linear-gradient(90deg,{c[2]},{c[3]})"></div>{pic}<div class="meta">{meta}</div></div>'

LEGEND='<div class="legend"><span><i class="gem-e"></i><b>Emerald</b> · where it started</span><span><i class="gem-d"></i><b>Diamond</b> · the whole family</span></div>'


def home_body():
    s1=STONE01
    order=[('tourmaline','hero2'),('sapphire',''),('spinel',''),('garnet',''),('aquamarine',''),('topaz',''),('other',''),('showcase',''),('collection','')]
    cards=''.join(cc(CD[k],cls) for k,cls in order)
    tcol=[('#0F4A3A','#EEF6F2'),('#1F3A7A','#EEF1FA'),('#B34528','#FBF0EA'),('#4B4A9E','#F3F1FA')]
    lcol=[('#1F3A7A','#EEF1FA'),('#267C78','#EAF7F6'),('#8E1B2C','#FBEDEF')]
    body=f'''<div class="wrap">
<section class="hero"><div class="in"><div><span class="pill" style="--c:#3FD0C9"><i></i>New: two tourmalines photographed</span>
<h1>Every colour, <span class="sw">one stone</span> at a time.</h1>
<p class="lede">Hand-picked loose gemstones from our family collection, sorted by colour. Each stone is photographed as it is, described in plain words and seller-identified, never guaranteed.</p>
<div class="ctas"><a class="btn pri rnd" href="{{{{root}}}}shop/">Shop the collection</a><a class="btn out rnd" href="{{{{root}}}}contact/">Put me on the hunt</a></div>
<div class="minitrust"><span>Seller-identified</span><span>Inclusions shown</span><span>Unknowns marked</span></div></div>
<div class="wheel"><div class="ring"></div><div class="ring2"></div>{dots()}
<div class="hcard glow" style="--g:{s1['glow']}"><div class="photo"><img src="{A}stone-01-800.jpg" srcset="{A}stone-01-400.jpg 400w, {A}stone-01-800.jpg 800w" sizes="(max-width:820px) 176px, 300px" width="800" height="800" fetchpriority="high" alt="{s1['alt']}"></div><div class="lab"><span class="nm2">Green Tourmaline</span>{chip(CD['tourmaline'],'Stone 01')}</div></div>
<div class="tag t1"><b>5.04 ct</b>Cushion · faceted</div>
<div class="tag t2">Tourmaline colours<div class="dr"><i style="background:#2F6B1E"></i><i style="background:#D9487A"></i><i style="background:#3FD0C9"></i><i style="background:#2E6FB0"></i></div></div>
<div class="tag t3"><b>Price TBD</b>Seller-identified</div></div></div>
<div class="chips">{"".join(chip(c) for c in COLL)}</div></section>
<section class="blk"><div class="sh"><div><div class="label" style="color:#B34528">Shop by gem</div><h2>Pick a colour</h2></div><p>Nine collections, nine colours. Tourmaline has real photos today; the rest fill in as each stone is photographed.</p></div><div class="cg">{cards}</div></section>
<section class="blk"><div class="sh"><div><div class="label" style="color:#B8476A">Just photographed</div><h2>Fresh from the collection</h2></div><a class="more" style="--uc:#B8476A" href="{{{{root}}}}shop/">View the shop →</a></div><div class="pg">{pcard(s1)}{pcard(STONE02)}{pcard(None,'sapphire')}{pcard(None,'spinel')}</div></section>
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


ANN='<div class="ann" role="note"><span style="--c:#3FD0C9">Seller-identified, not guaranteed</span><span style="--c:#D9BE87">GIA-informed descriptions</span><span style="--c:#B8476A">Photographed as it is</span></div>'
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
            f'<div class="copy">&copy; 2026 The Family Gem Shop · Seller-identified stones, described honestly. Loose gemstones, sold on Etsy.</div></footer>')

# US spelling (Joshua, Oct 16)
_US=[('Colourless','Colorless'),('colourless','colorless'),('Colour','Color'),('colour','color')]
def _us(h):
    for a,b in _US: h=h.replace(a,b)
    return h
