from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
GITIGNORE = (ROOT / ".gitignore").read_text(encoding="utf-8")


class PackagingMetadataTest(unittest.TestCase):
    def test_repository_tro_dung_fork(self):
        self.assertIn('Repository = "https://github.com/vietdungiitb/SanpraThemev16"', TEXT)

    def test_frappe_floor_la_16(self):
        self.assertIn('frappe = ">=16.0.0,<17.0.0"', TEXT)

    def test_co_license_mit(self):
        self.assertIn('license = { text = "MIT" }', TEXT)

    def test_gitignore_bo_pytest_cache(self):
        self.assertIn(".pytest_cache/", GITIGNORE)


if __name__ == "__main__":
    unittest.main()
