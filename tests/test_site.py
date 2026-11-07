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
        self.assertIn("185", notes)
        self.assertIn("725", notes)

    def test_hero_uses_locked_inventory_price(self):
        self.assertIn('<div class="tag t3"><b>$260</b>From my collection</div>', self.home)
        self.assertNotIn("Price TBD", self.home)
        self.assertIn("$260", self.shop)

    # Parent-verified Nov 7 2026. SKU-less rows matched by unique variety + carat + locked price.
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
        self.assertIn("The Etsy shop is open", faq)
        self.assertIn("Checkout and payment stay on Etsy", faq)
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
