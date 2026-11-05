from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "sanpra_uiv16" / "public"
FORBIDDEN = ("injectPoweredBy", "st-powered-by", "Powered by <strong>Sanpra")


class NoVendorBadgeTest(unittest.TestCase):
    def test_public_assets_khong_con_badge_vendor(self):
        hits = []
        for path in PUBLIC.rglob("*"):
            if path.suffix not in {".js", ".css", ".html"}:
                continue
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN:
                if token in text:
                    hits.append(f"{path.relative_to(ROOT)}: {token}")
        self.assertEqual(hits, [], "con badge vendor trong asset public: %r" % (hits,))


if __name__ == "__main__":
    unittest.main()
