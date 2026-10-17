#!/usr/bin/env python3
"""Static site builder for thefamilygems.com (The Family Gem Shop).

Run:  python3 build.py
Edits: change CONFIG / PAGES below, rerun. Output is written into this folder
(index.html, about/index.html, ...), plus sitemap.xml and robots.txt.

All internal links are RELATIVE ({{root}} token), so the same files work at
https://thefamilygems.com/ and at https://<user>.github.io/familygems-site/.
Only 404.html needs CONFIG["base_path"] (GitHub Pages serves it at any depth).
"""
import json, html, os, datetime, pathlib
import fsite  # direction F (Spectrum Boutique) header/footer + home/Our Story bodies; styles in f.css

ROOT = pathlib.Path(__file__).resolve().parent

CONFIG = {
    "site_name": "The Family Gem Shop",
    "domain": "https://thefamilygems.com",
    # 404.html link base. thefamilygems.com is live (CNAME), so the default is "/".
    # For a github.io project-page preview use FG_BASE=/familygems-site/
    "base_path": os.environ.get("FG_BASE", "/"),
    "etsy": "https://www.etsy.com/shop/TheFamilyGemShop",
    "email": "",            # PLACEHOLDER: business email once it exists (shown on /contact/ when set)
    "updated": "2026-10-16",
    "theme": "#0F4A3A",
}
E = CONFIG["etsy"]

GEM_SVG = ('<svg class="gem" viewBox="0 0 100 92" aria-hidden="true" focusable="false">'
  '<defs><linearGradient id="g{n}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5fd39a"/>'
  '<stop offset=".55" stop-color="#14874f"/><stop offset="1" stop-color="#0b3d26"/></linearGradient></defs>'
  '<path d="M50 88 12 50C0 37 4 14 24 12c12-1 21 6 26 16 5-10 14-17 26-16 20 2 24 25 12 38Z" fill="url(#g{n})"/>'
  '<path d="M50 28 50 88M24 12 50 46 76 12M12 50 50 46 88 50M50 28 32 34 12 50M50 28 68 34 88 50" '
  'stroke="#ffffff" stroke-opacity=".35" stroke-width="1.2" fill="none"/></svg>')

# Styles: f.css (direction F). The old inline CSS was retired on Oct 16, 2026 (backup branch backup/pre-F-20261016).

# Navigation lives in fsite.NAV (Shop, Guides, Our Story -> /about/, FAQ, Contact).

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"

ORG = {"@type": "Organization", "@id": CONFIG["domain"] + "/#org", "name": CONFIG["site_name"],
       "url": CONFIG["domain"] + "/", "logo": CONFIG["domain"] + "/img/logo-512.png", "sameAs": [E]}
WEBSITE = {"@type": "WebSite", "@id": CONFIG["domain"] + "/#website", "name": CONFIG["site_name"],
           "url": CONFIG["domain"] + "/", "publisher": {"@id": CONFIG["domain"] + "/#org"}, "inLanguage": "en-US"}

def crumbs(items):
    """items: [(name, path)] after Home."""
    allitems = [("Home", "")] + items
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": CONFIG["domain"] + "/" + p}
        for i, (n, p) in enumerate(allitems)]}
    lis = "".join(
        (f'<li><a href="{{{{root}}}}{p}">{html.escape(n)}</a></li>' if i < len(allitems) - 1
         else f'<li aria-current="page">{html.escape(n)}</li>')
        for i, (n, p) in enumerate(allitems))
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>', jsonld(ld)

# ---------------------------------------------------------------- FAQ data
FAQS = [
    ("Where do I buy your gemstones?",
     f'All purchases happen through our Etsy shop, <a href="{E}" rel="noopener">TheFamilyGemShop</a>. Etsy handles checkout and payment, so you can pay with the methods Etsy supports.'),
    ("Is the shop open yet?",
     f"Almost. {len(fsite.STONES)} stones are photographed and being listed one at a time. Favorite the shop on Etsy to see each stone the day it goes live."),
    ("What is a loose gemstone?",
     "A loose gemstone is a cut and polished stone that is not set in jewelry yet. You or your jeweler choose the setting, metal and design, which makes loose stones popular for custom engagement rings, pendants and heirloom pieces."),
    ("What is tsavorite?",
     'Tsavorite is the green variety of grossular garnet, found in East Africa (Kenya and Tanzania). It rates about 7 to 7.5 on the Mohs hardness scale and is prized for its bright, saturated green. Read our <a href="{{root}}guides/tsavorite-garnet-buying-guide/">tsavorite buying guide</a> to learn more.'),
    ("What is tourmaline?",
     "Not one mineral but a whole family of borosilicates; elbaite gives us most gem tourmaline. It has one of the widest color ranges of any gem, and one crystal can grow pink at the core and green at the rim. Iron makes it green to blue; manganese makes it pink. Hardness 7 to 7.5 (GIA). See the tourmalines in the <a href=\"{{root}}shop/\">shop</a>."),
    ("What details will a listing include?",
     "Each listing is meant to show the gemstone type, carat weight, measurements in millimeters, shape, origin when known, and any known treatment, along with clear photos. If something you need is missing, message us on Etsy before you buy."),
    ("How do I know a loose stone will fit my setting?",
     "Settings are made for a stone's millimeter measurements, not just its carat weight. Share the length, width and depth from the listing with your jeweler before you buy, or ask us on Etsy for exact measurements."),
    ("How do you ship?",
     "Shipping options, costs and delivery estimates are shown on each Etsy listing at checkout. We plan to ship gemstones with tracking and insurance."),
    ("What is your return policy?",
     "Returns and exchanges follow the policy shown on each Etsy listing. Please read it before you buy, and message us on Etsy with any questions."),
    ("How do I contact you?",
     f'The quickest way is Etsy Messages: open <a href="{E}" rel="noopener">our Etsy shop</a> and choose "Message" or "Contact shop owner".'),
]

def faq_html(faqs):
    return "".join(f"<details><summary>{html.escape(q)}</summary><p>{a}</p></details>" for q, a in faqs)

def faq_ld(faqs, root_abs):
    def clean(a):
        return a.replace("{{root}}", root_abs)
    import re
    return jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", clean(a))}}
        for q, a in faqs]})

# ---------------------------------------------------------------- pages
def page_home():
    # Direction F front page, APPROVED by Joshua Oct 16, 2026, 5:24 PM PT (Stone 01 green tourmaline leading).
    ld = jsonld({"@context": "https://schema.org", "@graph": [ORG, WEBSITE]})
    return dict(path="", nav="", main="f",
        title="The Family Gem Shop | Loose Gemstones, One Stone at a Time",
        desc="Loose gemstones from my personal collection, every color, one stone at a time. GIA-informed descriptions. Photographed honestly, never retouched.",
        body=fsite.home_body(), ld=ld, prio="1.0", freq="weekly")

def page_shop():
    # Rebuilt to match home (review M3): all photographed stones, color-ordered cards, per-stone sections in each stone's own color.
    c, cld = crumbs([("Shop", "shop/")])
    return dict(path="shop/", nav="shop/", main="f inner",
        title="Shop Loose Gemstones | The Family Gem Shop",
        desc="Loose gemstones from my personal collection: pink and green tourmaline, tsavorite garnet and more. Plain specs, honest photos. Coming soon to Etsy.",
        body=fsite.shop_body(c, E), ld=cld, prio="0.9", freq="weekly")

def page_about():
    # Our Story (direction F), text + ring photo APPROVED by Joshua Oct 16, 2026, 5:21 PM PT. URL stays /about/.
    c, cld = crumbs([("Our Story", "about/")])
    return dict(path="about/", nav="about/", main="f",
        title="Our Story | The Family Gem Shop",
        desc="How The Family Gem Shop began: an emerald my dad bought when I was three or four, and the family crest it inspired.",
        body=fsite.story_body(), ld=cld, prio="0.6", freq="monthly")

def page_faq():
    c, cld = crumbs([("FAQ", "faq/")])
    body = f"""<div class="wrap">
{fsite.phead("FAQ", "Frequently asked questions", "Straight answers about buying loose gemstones from The Family Gem Shop.", c, lc="#2E6FB0")}
<div class="sheet prose faqs">{faq_html(FAQS)}</div>
</div>
"""
    return dict(path="faq/", nav="faq/", title="FAQ: Buying Loose Gemstones | The Family Gem Shop",
        desc="How buying loose gemstones from The Family Gem Shop works: Etsy checkout, what tsavorite is, fitting a stone to a setting, shipping and returns.",
        body=body, ld=cld + faq_ld(FAQS, CONFIG["domain"] + "/"), prio="0.7", freq="monthly")

def page_contact():
    c, cld = crumbs([("Contact", "contact/")])
    email = (f'<p>Email: <a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></p>' if CONFIG["email"]
             else "<!-- PLACEHOLDER: set CONFIG['email'] once a business inbox exists -->")
    body = f"""<div class="wrap">
{fsite.phead("Contact", "Contact us", "The fastest way to reach me is Etsy Messages.", c, lc="#D08A2E")}
<div class="duo2"><div class="sheet prose">
  <h2>Message me on Etsy</h2>
  <ol>
    <li>Open <a href="{E}" rel="noopener">our Etsy shop</a>.</li>
    <li>Choose <strong>Message</strong> (or <strong>Contact shop owner</strong>).</li>
    <li>Tell us which stone you are asking about and what you need, such as measurements or more photos.</li>
  </ol>
  {email}
  <p>Questions about an existing order? Use the message thread on your Etsy order so all the details stay together.</p>
</div>
<div class="huntc"><div class="label" style="color:var(--golds)">The Hunt</div><h2>Put me on the hunt.</h2><p>{fsite._us(fsite.HUNT_P)}</p><a class="btn rnd white" href="{E}" rel="noopener">Message me on Etsy</a><div class="rg"></div></div></div>
</div>
"""
    return dict(path="contact/", nav="contact/", title="Contact | The Family Gem Shop",
        desc="Questions about a loose gemstone, measurements or an order? Reach The Family Gem Shop through Etsy Messages.",
        body=body, ld=cld, prio="0.5", freq="monthly")

def page_privacy():
    c, cld = crumbs([("Privacy", "privacy/")])
    body = f"""<div class="wrap">
  <!-- DRAFT: plain-English privacy notice, needs Joshua's review. Update it before adding analytics, forms or email signup. -->
{fsite.phead("Privacy", "Privacy policy", "No cookies, no analytics, no forms. Last updated October 5, 2026.", c, lc="#6A5ACD")}
<div class="sheet prose">
  <h2>The short version</h2>
  <p>This website does not use cookies, analytics or advertising trackers, and it has no forms. We do not collect personal information on this site.</p>
  <h2>Hosting</h2>
  <p>This site is hosted on GitHub Pages. Like most web hosts, GitHub may log technical information such as visitors' IP addresses for security and to keep the service running. See GitHub's privacy statement for details.</p>
  <h2>Purchases and messages</h2>
  <p>When you buy from us or message us, that happens on Etsy, and Etsy's privacy policy applies. We use the information Etsy shares with us, such as your name and shipping address, only to fulfill and support your order.</p>
  <h2>Links to other sites</h2>
  <p>Links to Etsy and other websites are governed by those sites' own policies.</p>
  <h2>Changes</h2>
  <p>If we add analytics, an email list or a contact form, we will update this page first.</p>
  <h2>Contact</h2>
  <p>Questions about privacy? Message us through <a href="{E}" rel="noopener">our Etsy shop</a>.</p>
</div>
</div>
"""
    return dict(path="privacy/", nav="", title="Privacy Policy | The Family Gem Shop",
        desc="Privacy policy for thefamilygems.com: no cookies, analytics or forms on this site. Purchases and messages happen on Etsy.",
        body=body, ld=cld, prio="0.3", freq="yearly")

GUIDES = [("tsavorite-garnet-buying-guide/", "Tsavorite garnet buying guide",
           "Color, clarity, cut, size, treatments, heart-shape tips and the questions to ask before buying a loose tsavorite.")]

def page_guides():
    c, cld = crumbs([("Guides", "guides/")])
    s = fsite.SF001
    cards = "".join(
        f'<a class="gcard" href="{{{{root}}}}guides/{p}" style="{fsite.svars(s)}"><div class="gpic">{fsite.framed(s, "fr", 0, "(max-width:820px) 40vw, 200px")}</div>'
        f'<div><div class="label" style="color:var(--stone-ink)">Buying guide</div><h2>{html.escape(t)}</h2><p>{html.escape(d)}</p><span class="link">Read the guide →</span></div></a>'
        for p, t, d in GUIDES)
    body = f"""<div class="wrap">
{fsite.phead("Guides", "Gemstone buying guides", "Plain-English guides to help you choose a loose gemstone with confidence.", c, lc="#187C45")}
<div class="glist">{cards}</div>
<section class="blk"><div class="sh"><div><div class="label" style="color:#C92A61">GIA-informed</div><h2>Variety notes</h2></div><p>The short history and the cool facts, the same notes that sit on every stone.</p></div><div class="vgrid">{fsite.guides_extra()}</div></section>
</div>
"""
    return dict(path="guides/", nav="guides/", title="Gemstone Buying Guides | The Family Gem Shop",
        desc="Plain-English guides to buying loose gemstones: tsavorite color and clarity, heart shapes, settings and questions to ask, plus variety notes.",
        body=body, ld=cld, prio="0.7", freq="weekly")

def page_tsavorite():
    path = "guides/tsavorite-garnet-buying-guide/"
    c, cld = crumbs([("Guides", "guides/"), ("Tsavorite garnet buying guide", path)])
    title = "Tsavorite Garnet Buying Guide: Color, Clarity & Heart Cuts"
    desc = "How to buy a loose tsavorite garnet: what good color looks like, clarity, cut and size, treatments, heart-shape tips and questions to ask a seller."
    art = jsonld({"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
        "datePublished": "2026-10-05", "dateModified": CONFIG["updated"],
        "author": {"@id": CONFIG["domain"] + "/#org"}, "publisher": ORG,
        "image": CONFIG["domain"] + "/img/og.png", "mainEntityOfPage": CONFIG["domain"] + "/" + path, "inLanguage": "en-US"})
    s = fsite.SF001
    body = f"""<div class="wrap">
{fsite.phead("Buying guide", "Tsavorite garnet buying guide", "Tsavorite is a bright green garnet and an easy one to fall for. Here is what to look for before you buy a loose tsavorite, especially a heart-shaped one.", c, '<p class="pub">Published October 5, 2026 · updated October 16, 2026 · The Family Gem Shop</p>', lc="#187C45")}
<article class="sheet prose guide" style="{fsite.svars(s)}">

  <h2>What is tsavorite?</h2>
  <p>Tsavorite is the green variety of <strong>grossular garnet</strong>. Its color comes from trace amounts of vanadium and chromium. Geologist Campbell Bridges found it in Tanzania in 1967 and in Kenya in 1970, near Tsavo National Park, which gave the stone its name. It was <strong>named tsavorite in 1973</strong> and <strong>reached jewelry buyers in 1974</strong>.</p>

  <h2>Color matters most</h2>
  <p>The most valued tsavorites are a vivid, saturated green, often with a slightly bluish undertone. Stones that lean yellowish look closer to peridot, and stones that are too dark can look almost black in dim light. When you compare photos, look for:</p>
  <ul>
    <li>Strong, even green across the face of the stone.</li>
    <li>A medium to medium-dark tone, not so dark that the stone loses its sparkle.</li>
    <li>Photos or video in daylight as well as under studio lights.</li>
  </ul>

  <h2>Clarity</h2>
  <p>Tsavorite is usually cleaner than emerald. Many good stones are <em>eye-clean</em>, meaning you cannot see inclusions without magnification. Tiny needles or crystals under a loupe are normal for tsavorite, and honest photos should show them.</p>

  <h2>Cut and size</h2>
  <p>A well-cut stone returns light evenly instead of showing a dark or washed-out center. Tsavorite usually forms as small crystals, so clean stones above a carat or two are scarce and cost noticeably more per carat. A stone around one carat is already a substantial size for this gem.</p>

  <h2>Treatments</h2>
  <p>As a species, tsavorite generally isn't treated, which is part of its appeal. That's a fact about the variety, not a promise about any one stone. Still, ask the seller to state the treatment status in writing. For higher-value stones, a report from an independent gemological lab adds confidence.</p>

  <h2>Buying a heart-shaped tsavorite</h2>
  <p>Heart shapes are a classic fit for engagement rings, anniversary pieces and pendants. A few extra checks help:</p>
  <ul>
    <li><strong>Symmetry:</strong> both lobes should be the same size, with a clear, centered cleft.</li>
    <li><strong>Proportions:</strong> length and width close to equal give the classic heart outline. Longer or wider hearts are a matter of taste.</li>
    <li><strong>Protect the point:</strong> ask your jeweler about a V-prong or bezel at the tip, the most exposed part of the stone.</li>
    <li><strong>Measurements:</strong> the setting is built for the stone's millimeters, so get exact length, width and depth before you order a mount.</li>
  </ul>

  <h2>Questions to ask any seller</h2>
  <ol>
    <li>What is the exact carat weight and the measurements in millimeters?</li>
    <li>Where is the stone from?</li>
    <li>Has it been treated in any way?</li>
    <li>Can I see a video in daylight?</li>
    <li>Is there a lab report, and what is the return policy?</li>
  </ol>

  <h2>Caring for tsavorite</h2>
  <p>At about 7 to 7.5 on the Mohs scale, tsavorite is suitable for everyday jewelry with reasonable care. Clean it with warm soapy water and a soft brush, and skip ultrasonic or steam cleaners unless your jeweler confirms the stone has no fractures.</p>

  <div class="note"><p><strong>Looking for a tsavorite?</strong> See the <a href="{{{{root}}}}shop/#sf-001">1.19 ct tsavorite heart</a> in the shop, or <a href="{E}" rel="noopener">favorite us on Etsy</a> to see it when it goes live.</p></div>
</article>
</div>
"""
    return dict(path=path, nav="guides/", title=title, desc=desc, body=body, ld=cld + art,
                prio="0.8", freq="monthly", ogtype="article")

def page_404():
    picks = fsite.spread_pick(fsite.STONES, 3)
    body = f"""<div class="wrap">
{fsite.phead("404", "Page not found", "Sorry, that page does not exist or has moved. Try one of these stones instead.", "", '<div class="ctas"><a class="btn pri rnd" href="{{root}}">Go to the home page</a><a class="btn out rnd" href="{{root}}shop/">Shop the collection</a></div>', lc="#C92A61")}
<div class="pg pg3">{"".join(fsite.pcard(s) for s in picks)}</div>
</div>
"""
    return dict(path="404.html", nav="", main="f inner", title="Page Not Found | The Family Gem Shop",
        desc="This page could not be found. Visit The Family Gem Shop home page or our Etsy shop.",
        body=body, ld="", noindex=True)

PAGES = [page_home(), page_shop(), page_guides(), page_tsavorite(), page_about(), page_faq(), page_contact(), page_privacy(), page_404()]

# ---------------------------------------------------------------- render
def render(p):
    path = p["path"]
    if path == "404.html":
        root = CONFIG["base_path"]
    else:
        depth = path.count("/")
        root = "./" if depth == 0 else "../" * depth
    canonical = CONFIG["domain"] + "/" + ("" if path == "404.html" else path)
    og_img = CONFIG["domain"] + "/img/og.png"
    t, d = html.escape(p["title"]), html.escape(p["desc"])
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else '<meta name="robots" content="index,follow,max-image-preview:large">'
    canon = "" if p.get("noindex") else f'<link rel="canonical" href="{canonical}">'
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}
{canon}
<meta name="theme-color" content="{CONFIG['theme']}">
<link rel="icon" href="{{{{root}}}}favicon.ico" sizes="32x32">
<link rel="icon" href="{{{{root}}}}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{{{root}}}}apple-touch-icon.png">
<link rel="manifest" href="{{{{root}}}}site.webmanifest">
<meta property="og:type" content="{p.get('ogtype', 'website')}">
<meta property="og:site_name" content="{CONFIG['site_name']}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The Family Gem Shop crest with four stones from the collection">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{og_img}">
<link rel="preload" href="{{{{root}}}}fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{{{root}}}}fonts/cormorant-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{{{root}}}}f.css">
{p['ld']}
</head>
<body>
{fsite.header(p.get("nav", ""))}
<main id="main" class="{p.get('main', 'std')}">
{p['body']}
</main>
{fsite.footer(E)}
</body>
</html>
"""
    doc = doc.replace("{{root}}", root)
    out = ROOT / (path if path.endswith(".html") else path + "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return out

def main():
    for p in PAGES:
        render(p)
    urls = "".join(
        f"<url><loc>{CONFIG['domain']}/{p['path']}</loc><lastmod>{CONFIG['updated']}</lastmod>"
        f"<changefreq>{p['freq']}</changefreq><priority>{p['prio']}</priority></url>\n"
        for p in PAGES if not p.get("noindex"))
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {CONFIG['domain']}/sitemap.xml\n")
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": CONFIG["site_name"], "short_name": "Family Gem Shop", "start_url": ".", "display": "standalone",
        "background_color": "#FBF8F1", "theme_color": CONFIG["theme"],
        "icons": [{"src": "img/logo-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "img/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    (ROOT / ".nojekyll").write_text("")
    print("built", len(PAGES), "pages; base_path for 404 =", CONFIG["base_path"])

if __name__ == "__main__":
    main()
