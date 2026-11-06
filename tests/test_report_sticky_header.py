"""Bug #1 (AUDIT_UI-2-ANH-LOI_20261106): header datatable sticky sai offset.

Fail-before: `.dt-header` mang `top: 36px` (offset của page-toolbar) trong khi nó
nằm TRONG scroll-container noi bo `.dt-scrollable` cua frappe-datatable ->
phu dung ~1 dong body (fixture A/B: mat ROW-1, STT bat dau tu 2).
Fix dung: datatable header `top: 0`; giu `top: 36px` cho `.list-row-head`
(page scroll duoi toolbar co dinh).
"""

from pathlib import Path
import re
import unittest

CSS = Path(__file__).resolve().parents[1] / "sanpra_uiv16" / "public" / "css" / "sanpra_uiv16.css"


def _blocks(css: str):
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css)


def _has_36px_top(body: str) -> bool:
    # Bat ca literal `top: 36px` lan var-fallback `top: var(--st-header-height, 36px)`.
    return re.search(r"top\s*:[^;]*36px", body) is not None


class ReportStickyHeaderTest(unittest.TestCase):
    def test_dt_header_khong_top_36px(self):
        css = CSS.read_text(encoding="utf-8")
        bad = [
            sel.strip()
            for sel, body in _blocks(css)
            if ".dt-header" in sel and _has_36px_top(body)
        ]
        self.assertEqual(bad, [], f"dt-header van sticky top:36px (che 1 dong): {bad}")

    def test_dt_header_sticky_sat_dinh_scrollport(self):
        css = CSS.read_text(encoding="utf-8")
        bodies = [body for sel, body in _blocks(css) if ".datatable .dt-header" in sel]
        self.assertTrue(bodies, "mat block .datatable .dt-header")
        self.assertTrue(
            any(re.search(r"top\s*:\s*0(px)?\b", b) for b in bodies),
            "dt-header phai sticky top:0 trong scroll-container noi bo",
        )

    def test_list_row_head_giu_top_36px(self):
        css = CSS.read_text(encoding="utf-8")
        bodies = [body for sel, body in _blocks(css) if ".list-row-head" in sel]
        self.assertTrue(bodies, "mat block .list-row-head")
        self.assertTrue(
            any(_has_36px_top(b) for b in bodies),
            "list-row-head page-level phai giu top:36px duoi toolbar",
        )


if __name__ == "__main__":
    unittest.main()
