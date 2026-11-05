"""Release 2.6.1 follow-up: brand wrap + audit log level + contrast + toolbar retry.

Fail-before tren 2.6.0. Sau fix: PASS + full suite xanh.
"""

import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "sanpra_uiv16"
SIDEBAR_CSS = PKG / "public" / "css" / "sidebar.css"
DESK_CSS = PKG / "public" / "css" / "sanpra_uiv16.css"
DESK_JS = PKG / "public" / "js" / "sanpra_uiv16.js"


def _block(text, selector):
    start = text.index(selector)
    end = text.index("}", start)
    return text[start:end]


class BrandWrapTest(unittest.TestCase):
    def test_ten_cong_ty_xuong_dong_du(self):
        css = SIDEBAR_CSS.read_text(encoding="utf-8")
        block = _block(css, ".st-company-name {")
        self.assertIn("white-space: normal", block)
        self.assertNotIn("text-overflow: ellipsis", block)

    def test_header_chua_dong_cao(self):
        css = SIDEBAR_CSS.read_text(encoding="utf-8")
        block = _block(css, "\n#st-company-header {")
        self.assertIn("min-height", block)
        self.assertNotIn("\n  height: 56px", block)


class Contrast261Test(unittest.TestCase):
    def test_clock_dat_aa(self):
        css = DESK_CSS.read_text(encoding="utf-8")
        block = _block(css, "\n#st-tb-clock {")
        self.assertIn("rgba(255,255,255,0.6)", block)

    def test_rail_label_dat_aa(self):
        css = SIDEBAR_CSS.read_text(encoding="utf-8")
        block = _block(css, "#st-icon-rail .st-rail-module-label {")
        self.assertIn("var(--sanpra-c-4b5563)", block)


class ToolbarRetryTest(unittest.TestCase):
    def test_co_retry_sau_boot(self):
        js = DESK_JS.read_text(encoding="utf-8")
        self.assertRegex(js, r"setTimeout\(function \(\) \{\s*try \{\s*onDeskReady\(\)")


if __name__ == "__main__":
    unittest.main()
