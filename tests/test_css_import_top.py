"""CSS @import phai o dau stylesheet (console warning F-UI-1).

Test thuan (doc file), chay tren staging host: python3 -m pytest.
Fail-before: do tren base (@import dong 259, sau ~258 dong CSS).
Browser bo qua @import khong o dau stylesheet -> font Inter co the khong tai.
"""

import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DESK_CSS = ROOT / "sanpra_uiv16" / "public" / "css" / "sanpra_uiv16.css"
HOOKS = ROOT / "sanpra_uiv16" / "hooks.py"


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


class CssImportTopTest(unittest.TestCase):
    def test_import_truoc_moi_rule(self):
        css = DESK_CSS.read_text(encoding="utf-8")
        idx = css.find("@import")
        self.assertNotEqual(idx, -1, "mat @import Inter trong CSS")
        head = strip_comments(css[:idx])
        self.assertNotIn("{", head, "con rule CSS dung truoc @import (browser se bo qua @import)")

    def test_bump_v78(self):
        hooks = HOOKS.read_text(encoding="utf-8")
        self.assertRegex(hooks, r"sanpra_uiv16\.css\?v=\d+")


if __name__ == "__main__":
    unittest.main()

