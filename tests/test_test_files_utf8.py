from pathlib import Path
import re
import unittest

TESTS = Path(__file__).resolve().parent
BARE_READ = re.compile(r"read_text\(\s*\)")


class TestFilesUtf8Test(unittest.TestCase):
    def test_moi_read_text_deu_khai_encoding(self):
        bad = []
        for path in TESTS.glob("*.py"):
            for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if BARE_READ.search(line):
                    bad.append(f"{path.name}:{no}")
        self.assertEqual(bad, [], "thieu encoding utf-8: %r" % (bad,))

    def test_khong_ghim_so_version_asset(self):
        pin = re.compile(r"\?v=\d+\"")
        bad = []
        for path in TESTS.glob("*.py"):
            for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if pin.search(line):
                    bad.append(f"{path.name}:{no}")
        self.assertEqual(bad, [], "ghim cung so ?v= (dung regex \\d+): %r" % (bad,))


if __name__ == "__main__":
    unittest.main()
