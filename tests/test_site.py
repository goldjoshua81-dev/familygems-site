"""Regression checks for the Nov 7 2026 audit fixes.

Prices, gem facts, photos, and Etsy listing URLs are locked here on purpose.
A failure means the site drifted from the reviewed inventory, not that a new
price should be invented to make the test pass.
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Joshua-locked amounts already on the shop. Do not edit to "fix" a test.
LOCKED_PRICES = {
    "SF-001": 340,
    "SF-202": 260,
    "SF-203": 185,
    "SF-204": 140,
    "SF-205": 165,
    "SF-206": 1200,
    "SF-207": 320,
    "SF-208": 340,
    "SF-209": 725,
    "SF-210": 190,
    "SF-211": 125,
}
# Face photo of Stone 01. The audit must not rewrite image bytes.
STONE01_SHA256 = "c0a0b8b995d8d169bec96251223d3b78dd62100a1aa971216b20be1a66e558ad"


class SiteAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.check_call(["python3", "build.py"], cwd=ROOT)
        cls.inv = json.loads((ROOT / "data" / "inventory.json").read_text())
        cls.shop = (ROOT / "shop" / "index.html").read_text()
        cls.home = (ROOT / "index.html").read_text()
        cls.guides = (ROOT / "guides" / "index.html").read_text()
        cls.css = (ROOT / "f.css").read_text()
        cls.pages = [p.read_text() for p in ROOT.rglob("*.html")]

    def test_locked_prices_unchanged(self):
        got = {s["sku"]: s["price_usd"] for s in self.inv["stones"]}
        self.assertEqual(got, LOCKED_PRICES)
        for sku, price in LOCKED_PRICES.items():
            shown = f"${price:,}" if price >= 1000 else f"${price}"
            self.assertIn(shown, self.shop, sku)
            self.assertEqual(
                next(s for s in self.inv["stones"] if s["sku"] == sku)["status"],
                "available",
            )

    def test_notes_do_not_call_locked_stones_draft(self):
        notes = self.inv["notes"]
        self.assertNotIn("remain draft", notes)
        self.assertNotIn("Price TBD", notes)
        self.assertNotIn("Joshua yes Oct 22", notes)
        self.assertNotIn("Joshua locked", notes)
        self.assertNotIn("parent-verified", notes)
        self.assertIn("185", notes)
        self.assertIn("725", notes)
        self.assertIn("not a live Etsy identity check", notes)

    def test_featured_gem_box_links_to_its_stone(self):
        self.assertIn('<a class="hcard glow" href="./shop/#sf-202"', self.home)
        self.assertIn('id="sf-202"', self.shop)

    def test_wheel_selection_spin_and_fallback(self):
        self.assertEqual(self.home.count('<a class="dot"'), 9)
        self.assertIn('id="wheel-spin"', self.home)
        self.assertIn('id="wheel-reset"', self.home)
        self.assertIn("prefers-reduced-motion", self.home)
        self.assertIn("This is not a giveaway and not a checkout.", self.home)
        self.assertIn('href="./guides/#notes-tourmaline"', self.home)
        self.assertIn('href="./shop/#notes-spinel"', self.home)
        self.assertIn('href="./shop/#notes-zircon"', self.home)
        self.assertIn('href="./guides/tsavorite-garnet-buying-guide/"', self.home)
        self.assertIn('id="notes-tourmaline"', (ROOT / "guides" / "index.html").read_text())
        self.assertIn('id="notes-spinel"', self.shop)
        self.assertIn('id="notes-zircon"', self.shop)
        low = self.home.lower()
        for banned in ("you won", "in stock", "available now", "prize", "repository", "source file"):
            self.assertNotIn(banned, low)
        self.assertIn("https://www.gia.edu/spinel", self.home)
        self.assertIn("https://www.gia.edu/tourmaline", self.home)
        self.assertIn("https://www.gia.edu/zircon", self.home)
        self.assertIn("https://www.gia.edu/garnet", self.home)
        self.assertNotIn("most gem tourmaline", low)
        self.assertIn("This video did not load. The still photo is shown.", self.shop)
        self.assertIn('"sku": "SF-208"', self.home)
        self.assertIn("sf-208-400.jpg", self.home)
        self.assertIn('"sku": "SF-001"', self.home)
        self.assertIn("sf-001-400.jpg", self.home)
        self.assertIn('"sku": "SF-211"', self.home)
        self.assertIn('"sku": "SF-202"', self.home)
        self.assertIn("No sapphire photo is on this site.", self.home)
        self.assertIn("not one gemstone", self.home)
        self.assertIn("my!==token", self.home)

    def test_no_family_lab_link(self):
        blob = "\n".join(self.pages).lower()
        self.assertNotIn("family lab", blob)
        self.assertNotIn("familylab", blob)

    def test_gallery_thumbs_keep_nojs_hrefs(self):
        # Seek and ended are not asserted here. Python http.server 3.12 answers
        # Range with 200 and the whole file, and Chrome then reports seekable [0, 0].
        # That miss is the review server. A range-capable static server (http-server, 206)
        # and the public GitHub host (accept-ranges, 206) both seek these same files.
        # Do not treat a SimpleHTTP seek miss as an application defect.
        self.assertIn('href="../img/stone-01-800.jpg"', self.shop)
        self.assertIn('href="../video/stone-01.mp4"', self.shop)
        self.assertIn('id="sf-207"', self.shop)
        self.assertNotIn("video/sf-207", self.shop)
        self.assertEqual(self.shop.count('class="th"'), 44)
        self.assertEqual(self.shop.count('class="th thv"'), 10)

    def test_specimen_provenance_strings_unchanged(self):
        # Locks the current specimen wording. It does not prove those seller statements.
        import fsite
        expect = {
            "SF-202": ("Madagascar, per the original seller", "No heat, per the original seller"),
            "SF-203": ("Afghanistan, per the original seller", "No heat, per the original seller"),
            "SF-204": ("Afghanistan, per the original seller", "No heat, per the original seller"),
            "SF-205": ("Afghanistan, per the original seller", "No heat, per the original seller"),
            "SF-001": ("Not known (seller label says Kenya)", "Not known"),
            "SF-206": ("Not known (seller label says Kenya)", "Not known"),
            "SF-207": ("Not known", "Not known"),
            "SF-208": ("Not known", "Not known"),
            "SF-209": ("Not known", "Not known"),
            "SF-210": ("Not known", "Not known"),
            "SF-211": ("Not known", "Not known"),
        }
        by = {s["sku"]: dict(s["specs"]) for s in fsite.STONES}
        for sku, (origin, treat) in expect.items():
            self.assertEqual(by[sku]["Origin"], origin, sku)
            self.assertEqual(by[sku]["Treatment"], treat, sku)
            if sku != "SF-206":
                self.assertEqual(by[sku]["Measurements"], "To measure", sku)
        self.assertEqual(by["SF-206"]["Measurements"], "9.63 × 7.72 × 5.28 mm (from the box label)")

    def test_hero_uses_locked_inventory_price(self):
        self.assertIn('<div class="tag t3"><b>$260</b>From my collection</div>', self.home)
        self.assertNotIn("Price TBD", self.home)
        self.assertIn("$260", self.shop)

    # Hardcoded regression fixture. A pass does not open Etsy and is not a live identity check.
    # A signed-in owner reread reconfirmed title, species, carat, and price on all 11,
    # with Add to cart and no sold or unavailable state, shop text "All 11", and no vacation text.
    # That was not a logged-out session. Logged-out availability and checkout are not established.
    # Public SKUs were visible only on SF-204, SF-205, SF-206, and SF-210.
    # The other seven stay mapped by unique variety, carat, and price_usd, not as SKU-certified.
    LISTINGS = {
        "SF-001": "https://www.etsy.com/listing/4601364223",
        "SF-202": "https://www.etsy.com/listing/4601390856",
        "SF-203": "https://www.etsy.com/listing/4601365197",
        "SF-204": "https://www.etsy.com/listing/4601391538",
        "SF-205": "https://www.etsy.com/listing/4601365891",
        "SF-206": "https://www.etsy.com/listing/4601392166",
        "SF-207": "https://www.etsy.com/listing/4601366409",
        "SF-208": "https://www.etsy.com/listing/4601392802",
        "SF-209": "https://www.etsy.com/listing/4601393102",
        "SF-210": "https://www.etsy.com/listing/4601393384",
        "SF-211": "https://www.etsy.com/listing/4601367587",
    }

    def test_no_invented_etsy_listing_links(self):
        got = {s["sku"]: s["etsy_url"] for s in self.inv["stones"]}
        self.assertEqual(got, self.LISTINGS)
        ids = {s["sku"]: s["etsy_listing_id"] for s in self.inv["stones"]}
        self.assertEqual(ids, {sku: int(url.rsplit("/", 1)[-1]) for sku, url in self.LISTINGS.items()})
        blob = "\n".join(self.pages)
        self.assertNotIn("cloudflareinsights", blob)
        self.assertNotIn("googletagmanager", blob)
        self.assertNotIn("Coming soon to Etsy", blob)
        self.assertNotIn("when it goes live", blob.lower())
        self.assertNotIn(">Almost.", (ROOT / "faq" / "index.html").read_text())
        for sku, url in self.LISTINGS.items():
            anchor = sku.lower()
            start = self.shop.find(f'id="{anchor}"')
            self.assertGreater(start, -1, sku)
            nxt = self.shop.find("<article ", start + 10)
            chunk = self.shop[start:nxt if nxt > 0 else None]
            self.assertIn(f'href="{url}" rel="noopener">See it on Etsy</a>', chunk, sku)
            self.assertIn(f'"url":"{url}"', self.shop)
        self.assertEqual(self.shop.count(">See it on Etsy</a>"), 11)

    def test_buying_paths_and_tiles(self):
        faq = (ROOT / "faq" / "index.html").read_text()
        self.assertIn("Browse our gemstone listings on Etsy", faq)
        self.assertIn('href="https://www.etsy.com/shop/TheFamilyGemShop" rel="noopener">TheFamilyGemShop</a>', faq)
        self.assertNotIn("The Etsy shop is open", faq)
        self.assertNotIn("all 11 photographed", faq)
        open_answer = faq.split("Is the shop open yet?", 1)[1].split("</details>", 1)[0]
        self.assertNotIn("Checkout", open_answer)
        self.assertNotIn("all 11", open_answer.lower())
        guide = (ROOT / "guides" / "tsavorite-garnet-buying-guide" / "index.html").read_text()
        self.assertIn(self.LISTINGS["SF-001"], guide)
        self.assertNotIn("Etsy soon", self.shop)
        # Photographed families and the whole collection are links. Coming-soon families are not.
        self.assertEqual(self.home.count("<a class=\"cc"), 5)
        self.assertEqual(self.home.count("<div class=\"cc"), 4)
        self.assertIn('href="./shop/#sf-202"', self.home)
        self.assertIn('href="./shop/"', self.home)
        def opener(heading):
            idx = self.home.find(f">{heading}</h3>")
            self.assertGreater(idx, -1, heading)
            open_at = self.home.rfind('class="cc', 0, idx)
            tag = self.home.rfind("<", 0, open_at)
            return self.home[tag:tag + 4]
        self.assertEqual(opener("Tourmaline"), "<a c")
        self.assertEqual(opener("Sapphire"), "<div")
        self.assertEqual(opener("The Collection"), "<a c")

    def test_mobile_hero_price_is_in_the_card(self):
        self.assertIn('<b class="hprice">$260</b>', self.home)
        self.assertIn(".hcard .hprice{display:none", self.css)
        self.assertIn(".hcard .hprice{display:block", self.css)

    def test_unknown_facts_stay_unknown(self):
        self.assertIn(">Not known</dd>", self.shop)
        self.assertIn('class="unk">Not known (seller label says Kenya)</dd>', self.shop)
        self.assertNotIn("Muzo", self.shop)
        self.assertNotIn("Colombia", self.shop)
        self.assertIn("Muzo emerald from Colombia", (ROOT / "about" / "index.html").read_text())

    def test_guide_notes_are_not_video_cards(self):
        self.assertIn('class="vnote"', self.guides)
        self.assertNotIn('class="vcard"', self.guides)
        self.assertNotIn("mint green tourmaline", self.guides.lower())
        self.assertIn("pink tourmaline", self.guides.lower())
        note = self.css.split(".vnote{", 1)[1].split("}", 1)[0]
        self.assertNotIn("aspect-ratio", note)
        self.assertIn("a.vcard{", self.css)
        self.assertIn('class="vcard"', self.shop)

    def test_announcement_is_a_named_region(self):
        self.assertIn('class="ann" role="region" aria-label="How we describe stones"', self.home)

    def test_mobile_menu_target_size(self):
        self.assertIn(".mnav nav a{min-height:44px;", self.css)

    def test_stone_photo_bytes_unchanged(self):
        digest = hashlib.sha256((ROOT / "img" / "stone-01-800.jpg").read_bytes()).hexdigest()
        self.assertEqual(digest, STONE01_SHA256)
        self.assertNotIn("filter:", self.css.split(".photo img{", 1)[1].split("}", 1)[0])

    def test_listing_url_helper_rejects_non_listings(self):
        import fsite
        self.assertIsNone(fsite.listing_url({"etsy_url": None}))
        self.assertIsNone(fsite.listing_url({"etsy_url": "https://www.etsy.com/shop/TheFamilyGemShop"}))
        self.assertIsNone(fsite.listing_url({"etsy_url": "javascript:alert(1)"}))
        ok = "https://www.etsy.com/listing/1234567890/example-stone"
        self.assertEqual(fsite.listing_url({"etsy_url": ok}), ok)


if __name__ == "__main__":
    unittest.main()
