from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "sanpra_uiv16"
CSS = PKG / "public" / "css"
FONTS = PKG / "public" / "fonts" / "inter"


class NoExternalFontsTest(unittest.TestCase):
    def test_khong_goi_google_fonts(self):
        bad = []
        for path in list(CSS.glob("*.css")) + list((PKG / "public" / "js").glob("*.js")):
            text = path.read_text(encoding="utf-8")
            if "fonts.googleapis.com" in text or "fonts.gstatic.com" in text:
                bad.append(path.name)
        self.assertEqual(bad, [])

    def test_font_face_tro_file_noi_bo_va_ton_tai(self):
        css = (CSS / "fonts.css").read_text(encoding="utf-8")
        self.assertIn("font-family:'Inter'", css.replace(" ", ""))
        srcs = re.findall(r"url\('([^']+\.woff2)'\)", css)
        self.assertEqual(len(srcs), 2)
        for src in srcs:
            rel = src.removeprefix("/assets/sanpra_uiv16/")
            self.assertTrue((PKG / "public" / rel).is_file(), src)
        self.assertTrue((FONTS / "OFL.txt").is_file())

    def test_van_con_fallback_stack(self):
        desk = (CSS / "sanpra_uiv16.css").read_text(encoding="utf-8")
        login = (CSS / "login.css").read_text(encoding="utf-8")
        for text in (desk, login):
            self.assertIn("'Inter', -apple-system", text)

    def test_khong_con_at_import(self):
        desk = (CSS / "sanpra_uiv16.css").read_text(encoding="utf-8")
        login = (CSS / "login.css").read_text(encoding="utf-8")
        for text in (desk, login):
            self.assertNotIn("@import", text, "con @import (phai self-host font)")


if __name__ == "__main__":
    unittest.main()
