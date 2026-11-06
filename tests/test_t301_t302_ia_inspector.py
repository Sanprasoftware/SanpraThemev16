"""T301 (IA 4 nhóm + accordion) + T302 (Inspector flip + mockup Edusuccess).

Fail-before: chạy trên code chưa sửa phải ĐỎ; sau implement phải XANH.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "sanpra_uiv16" / "sanpra_ui_v16" / "page" / "theme_studio" / "theme_studio.js"
CSS = ROOT / "sanpra_uiv16" / "public" / "css" / "theme_studio.css"

EXPECTED_SECTIONS = {
    "colors", "navigation", "controls", "typography", "data", "workspace",
    "features", "branding", "layout", "accessibility", "advanced", "operations",
}


class T301GroupsTest(unittest.TestCase):
    def test_bon_nhom_bao_phu_dung_12_sections(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("theme_studio_groups", js)
        for group in ("foundation", "navigation", "content", "system"):
            self.assertIn(group, js)
        for section in sorted(EXPECTED_SECTIONS):
            self.assertIn(section, js)

    def test_tabs_render_theo_nhom_accordion_co_aria(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("data-group", js)
        self.assertIn("data-group-toggle", js)
        self.assertIn("aria-expanded", js)
        self.assertIn("aria-controls", js)

    def test_bind_co_handler_toggle_nhom_va_nho_trang_thai(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("[data-group-toggle]", js)
        self.assertIn("sts-studio-groups-collapsed", js)

    def test_search_tu_mo_nhom_co_ket_qua(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("_search_controls", js)
        # search phải chạm tới group khi lọc (không giấu kết quả trong nhóm gập)
        self.assertIn("sts-tab-group", js)

    def test_css_co_style_nhom_accordion(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn(".sts-tab-group", css)


class T302InspectorFlipTest(unittest.TestCase):
    def test_nut_flip_va_method_ton_tai(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("data-inspector-flip", js)
        self.assertIn("_flip_inspector", js)

    def test_bind_co_handler_flip(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("[data-inspector-flip]", js)


class T302EdusuccessMockupTest(unittest.TestCase):
    def test_mockup_edusuccess_lam_default(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertIn("EDUSUCCESS_MOCKUP", js)
        self.assertIn("Edusuccess", js)
        self.assertIn("edusuccess.vn", js)

    def test_placeholder_cu_khong_con_lam_default_preview(self):
        js = PAGE.read_text(encoding="utf-8")
        self.assertNotIn("<b data-app-title>Sanpra UI V16</b>", js)
        self.assertNotIn("Good morning, Ayesha", js)
        self.assertNotIn("Northstar Trading", js)
        self.assertNotIn('"Sanpra UI V16"', js)


if __name__ == "__main__":
    unittest.main()
