from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CI = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")


class CiWorkflowTest(unittest.TestCase):
    def test_ci_chay_khi_push_nhanh_fork(self):
        self.assertIn("vietnam-clean", CI)

    def test_co_job_windows(self):
        self.assertIn("windows-python", CI)
        self.assertIn("windows-latest", CI)

    def test_job_windows_chay_pytest(self):
        win_job = CI[CI.index("windows-python"):]
        self.assertIn("runs-on: windows-latest", win_job)
        self.assertIn("python -m pytest -q", win_job)

    def test_job_windows_khong_ep_pythonutf8(self):
        # Muc dich la bat loi locale that: khong duoc set PYTHONUTF8.
        win_job = CI[CI.index("windows-python"):]
        self.assertNotIn("PYTHONUTF8", win_job)


if __name__ == "__main__":
    unittest.main()
