"""AdSense auto-ads safety and static build regression guards."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class AdSenseSetupTests(unittest.TestCase):
    def test_generated_assets_match_the_sources(self):
        for name in ("app.js", "analytics.js"):
            self.assertEqual((ROOT / "assets" / name).read_bytes(), (ROOT / "docs/assets" / name).read_bytes())

    def test_auto_ads_only_after_route_and_privacy_checks(self):
        code = (ROOT / "assets/app.js").read_text()
        self.assertIn("ca-pub-9723666081819297", code)
        self.assertIn("pagead2.googlesyndication.com/pagead/js/adsbygoogle.js", code)
        self.assertIn("interactiveOrPolicy", code)
        for category in ("tools", "maps", "dungeons", "skills", "search", "privacy"):
            self.assertIn(category + r"\/", code)
        self.assertIn("globalPrivacyControl", code)
        self.assertIn("ad_storage:'denied'", code)

    def test_ga_consent_never_overwrites_advertising_cmp(self):
        code = (ROOT / "assets/analytics.js").read_text()
        self.assertIn("const defaults = {analytics_storage:'denied'};", code)

    def test_manual_ad_slots_remain_disabled(self):
        import json
        config = json.loads((ROOT / "site.json").read_text())
        self.assertFalse(config["adsense"]["enabled"])
        self.assertFalse(config["adsense"]["consent_reviewed"])

if __name__ == "__main__":
    unittest.main()
