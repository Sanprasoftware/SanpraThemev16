"""Bug #2 (AUDIT_UI-2-ANH-LOI_20261106): tab strip chui duoi page-head / troi khoi side panel.

Do tren staging (Playwright, viewport 1600x900):
- Form page cuon `.main-section`: `.page-head` sticky top:36px z:1010 (h~49, y 36-85),
  `.form-tabs-list` sticky top:48px (var --navbar-height) z:5 (y 48-92) -> chong 37px,
  hit-test giua tab strip trung `.page-head-content`.
- Side panel (`frappe.ui.get_side_panel()`): tab strip `top:auto` (core scroll-listener
  chi bind `.main-section`) -> troi theo noi dung, chui duoi panel header duc roi
  bien mat (tabs top:-42, hit-test NONE).

Fix:
- Form: tab strip bam DUOI page-head da dinh (pattern core `show-navbar` variant).
- Panel: tab strip bam dinh vung cuon panel (top:0).
"""
import re
from pathlib import Path
import unittest

CSS = Path(__file__).resolve().parents[1] / "sanpra_uiv16" / "public" / "css" / "sanpra_uiv16.css"


def _blocks(css):
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css)


class StickyTabsOverlapTest(unittest.TestCase):
    def test_tabs_khong_dinh_o_48px_nua(self):
        css = CSS.read_text(encoding="utf-8")
        bad = [
            sel.strip().replace("\n", " ")[:100]
            for sel, body in _blocks(css)
            if ".form-tabs-list" in sel
            and "sticky" in sel
            and re.search(r"top\s*:\s*48px", body)
            and "page-head-height" not in body
        ]
        self.assertEqual(bad, [], f"tab strip van top:48px -> chui duoi page-head: {bad}")

    def test_tabs_bam_duoi_page_head_da_dinh(self):
        css = CSS.read_text(encoding="utf-8")
        ok = [
            body
            for sel, body in _blocks(css)
            if ".form-tabs-list" in sel and "page-head-height" in body
        ]
        self.assertTrue(ok, "thieu rule tab strip top = toolbar + page-head")
        self.assertTrue(
            any("st-header-height" in b for b in ok),
            "offset phai cong them chieu cao toolbar cua theme",
        )

    def test_side_panel_tabs_bam_dinh_panel(self):
        css = CSS.read_text(encoding="utf-8")
        bodies = [body for sel, body in _blocks(css) if ".side-panel .form-tabs-list" in sel]
        self.assertTrue(bodies, "thieu rule .side-panel .form-tabs-list")
        self.assertTrue(
            any(re.search(r"top\s*:\s*0", b) for b in bodies),
            "tab strip trong panel phai top:0 (bam dinh vung cuon panel)",
        )


if __name__ == "__main__":
    unittest.main()
