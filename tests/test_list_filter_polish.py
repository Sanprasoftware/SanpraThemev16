"""List filter bar (page-form) polish: input + nut ≈ phai ghep thanh 1 cum.

Fail-before: khong co rule scope .list-page-form/.standard-filter-section nao
ghep input-group; input bi vien hop tach roi + hang thua khoang trang.
Sau fix: presence guard cho 4 cum rule + full suite xanh.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "sanpra_uiv16" / "public" / "css" / "sanpra_uiv16.css"


class ListFilterPolishTest(unittest.TestCase):
    def _css(self):
        return CSS.read_text(encoding="utf-8")

    def test_filter_section_co_rule_gon_hang(self):
        css = self._css()
        self.assertIn(".list-page-form .standard-filter-section", css)

    def test_input_group_duoc_ghep_thanh_cum(self):
        css = self._css()
        self.assertIn(".list-page-form .standard-filter-section .input-group .form-control", css)
        self.assertIn("border-top-right-radius: 0", css)

    def test_nut_match_type_khop_input(self):
        css = self._css()
        self.assertIn("match-type-dropdown-btn", css)

    def test_hang_filter_sort_gon(self):
        css = self._css()
        self.assertIn(".list-page-form .filter-section", css)


if __name__ == "__main__":
    unittest.main()
