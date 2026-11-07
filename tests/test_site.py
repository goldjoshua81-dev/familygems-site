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

    def test_no_invented_etsy_listing_links(self):
        for stone in self.inv["stones"]:
            self.assertIsNone(stone["etsy_url"], stone["sku"])
            self.assertIsNone(stone["etsy_listing_id"], stone["sku"])
        blob = "\n".join(self.pages)
        self.assertNotIn("etsy.com/listing", blob)
        self.assertNotIn("cloudflareinsights", blob)
        self.assertNotIn("googletagmanager", blob)
        self.assertEqual(blob.count("Coming soon to Etsy"), 11)

    def test_unknown_facts_stay_unknown(self):
        for sku in ("SF-207", "SF-208", "SF-209", "SF-210", "SF-211"):
            self.assertIn(f"ETSY LISTING SLOT ({sku})", self.shop)
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
