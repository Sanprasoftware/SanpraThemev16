"""S5: moi @frappe.whitelist phai khai methods ro rang; GET khong duoc mutation.

Doc endpoint nhan GET+POST (login fetch() + frappe.call deu dung duoc);
ghi endpoint chi nhan POST (chan CSRF qua GET). Quet bang AST tinh,
khong import frappe. Them guard audit log cho reset_workspace_for_user (S4).
"""

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "sanpra_uiv16"

EXPECTED = {
    "api.py::get_theme_css": ["GET", "POST"],
    "api.py::get_theme_config": ["GET", "POST"],
    "api.py::save_theme_config": ["POST"],
    "api.py::get_branding": ["GET", "POST"],
    "api.py::get_workspaces": ["GET", "POST"],
    "api.py::get_available_languages": ["GET", "POST"],
    "api.py::set_user_language": ["POST"],
    "api.py::reset_workspace_for_user": ["POST"],
    "api.py::set_user_theme": ["POST"],
    "theme_api.py::get_theme_studio_state": ["GET", "POST"],
    "theme_api.py::get_chart_preview": ["GET", "POST"],
    "theme_api.py::preview_theme_css": ["GET", "POST"],
    "theme_api.py::save_theme_draft": ["POST"],
    "theme_api.py::publish_theme_config": ["POST"],
    "theme_api.py::manage_theme_profile": ["POST"],
    "theme_api.py::restore_theme_version": ["POST"],
    "theme_api.py::import_theme_profile": ["POST"],
    "theme_api.py::save_theme_assignments": ["POST"],
    "theme_api.py::save_theme_schedule": ["POST"],
    "theme_api.py::set_user_theme_profile": ["POST"],
    "theme_api.py::get_resolved_theme_runtime": ["GET", "POST"],
    "theme_api.py::clear_theme_cache": ["POST"],
    "sanpra_ui_v16/doctype/theme_settings/theme_settings.py::get_theme_settings": ["GET", "POST"],
    "sanpra_ui_v16/doctype/login_page_settings/login_page_settings.py::fetch_branding": ["GET", "POST"],
}

MUTATIONS = (
    "save_theme_config",
    "set_user_language",
    "reset_workspace_for_user",
    "set_user_theme",
)


def scan():
    found = {}
    for path in PKG.rglob("*.py"):
        # utf-8-sig: boot.py/setup.py co BOM san (khong sua trong dot nay)
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        rel = path.relative_to(PKG).as_posix()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                func = getattr(dec, "func", None)
                if isinstance(dec, ast.Call) and getattr(func, "attr", "") == "whitelist":
                    methods = None
                    for kw in dec.keywords:
                        if kw.arg == "methods":
                            methods = ast.literal_eval(kw.value)
                    found[f"{rel}::{node.name}"] = methods
    return found


class ApiMethodsTest(unittest.TestCase):
    def test_khong_con_whitelist_bare(self):
        bare = sorted(k for k, v in scan().items() if v is None)
        self.assertEqual(bare, [], "whitelist thieu methods=: %r" % (bare,))

    def test_mapping_methods_dung_quy_uoc(self):
        self.assertEqual(scan(), EXPECTED)

    def test_reset_workspace_co_audit_log(self):
        src = (PKG / "api.py").read_text(encoding="utf-8")
        start = src.index("def reset_workspace_for_user")
        body = src[start:]
        nxt = body.find("\n@frappe.whitelist", 1)
        body = body[:nxt] if nxt != -1 else body
        self.assertIn('frappe.logger("sanpra_uiv16")', body)
        self.assertIn("# S4:", body)

    def test_js_khong_fetch_endpoint_ghi(self):
        # fetch() mac dinh GET: khong bao gio duoc goi endpoint mutation.
        # frappe.call (POST) la duong hop le duy nhat.
        js_dir = PKG / "public" / "js"
        hits = []
        for path in js_dir.rglob("*.js"):
            text = path.read_text(encoding="utf-8")
            for name in MUTATIONS:
                if name not in text:
                    continue
                for line_no, line in enumerate(text.splitlines(), 1):
                    if "fetch(" in line and name in line:
                        hits.append(f"{path.name}:{line_no}:{name}")
        self.assertEqual(hits, [])

    def test_js_wiring_mutation_con_nguyen(self):
        # Sau khi khoa POST-only, nut Reset layout / language / theme phai van goi
        # qua frappe.call (POST). Mat wiring = mat chuc nang.
        text = (PKG / "public" / "js" / "sanpra_uiv16.js").read_text(encoding="utf-8")
        for name in ("reset_workspace_for_user", "set_user_language"):
            self.assertIn(name, text, f"mat wiring frappe.call {name}")
        dark = (PKG / "public" / "js" / "dark_mode.js").read_text(encoding="utf-8")
        self.assertIn("sanpra_uiv16.api.set_user_theme", dark)


if __name__ == "__main__":
    unittest.main()
