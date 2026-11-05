"""Slice P2-d C — hex -> design tokens.

Guard: khong con hex literal trong fork CSS ngoai block khai bao token
(:root trong sanpra_uiv16.css). Moi mau phai di qua var(--sanpra-c-*).
(AUDIT_UI_FULL 31/10/2026: 237-242 hex cung.)

Giu nguyen GIA TRI (mapping 1-1, khong doi identity) nen contrast giu
nguyen — do lai bang script contrast sau deploy.

Lesson 75: sua asset phai bump ?v= trong hooks.py + cap nhat test ghim.
Lesson 61: assert tren gia tri (count), khong tren tap ten ham.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_DIR = ROOT / "sanpra_uiv16" / "public" / "css"
TOKENS_FILE = ROOT / "sanpra_uiv16" / "public" / "css" / "sanpra_uiv16.css"

TOKEN_RE = re.compile(r"(--sanpra-c-([0-9a-fA-F]{3,6}))\s*:\s*([^;]+);")
USE_RE = re.compile(r"var\((--sanpra-c-[0-9a-fA-F]{3,6})\)")


def _token_block():
    text = TOKENS_FILE.read_text(encoding="utf-8")
    start = text.index(":root")
    end = text.index("}", start)
    return text[start:end]


def strip_comments(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


class HexTokensTest(unittest.TestCase):
    def _literal_count(self):
        n = 0
        for path in sorted(CSS_DIR.rglob("*.css")):
            text = strip_comments(path.read_text(encoding="utf-8"))
            if path == TOKENS_FILE:
                text = re.sub(r":root\s*\{[^}]*\}", "", text, count=1, flags=re.S)
            for m in re.finditer(r"#(?:[0-9a-fA-F]{3}){1,2}\b", text):
                n += 1
        return n

    def test_no_hex_literal_outside_token_block(self):
        """Fail-before tren code cu (~700+). Sau fix: count == 0."""
        n = self._literal_count()
        self.assertEqual(
            n,
            0,
            "Con {} hex literal ngoai block token".format(n),
        )

    def test_token_block_defines_sanpra_color_tokens(self):
        text = TOKENS_FILE.read_text(encoding="utf-8")
        self.assertIn("--sanpra-c-", text, "Thieu token mau --sanpra-c-*")


class TokenValueTest(unittest.TestCase):
    def test_moi_token_mau_co_gia_tri_hex_literal(self):
        decls = TOKEN_RE.findall(_token_block())
        self.assertEqual(len(decls), 242, "so token doi: %d" % len(decls))
        bad = [
            (name, value)
            for name, suffix, value in decls
            if value.strip().lower() != "#" + suffix.lower()
        ]
        self.assertEqual(bad, [], "token tu tro / sai gia tri: %r" % (bad[:10],))

    def test_moi_token_duoc_dung_deu_duoc_khai(self):
        declared = {name for name, _, _ in TOKEN_RE.findall(_token_block())}
        used = set()
        for path in CSS_DIR.rglob("*.css"):
            used |= set(USE_RE.findall(path.read_text(encoding="utf-8")))
        self.assertEqual(sorted(used - declared), [], "token dung nhung chua khai")


if __name__ == "__main__":
    unittest.main()
