# -*- coding: utf-8 -*-
"""Kiểm tra vi.csv của sanpra_uiv16 có đủ 93 thuật ngữ Slice 3 + cấu trúc 2 cột."""
from __future__ import annotations

import csv
import unittest
from pathlib import Path

VI_CSV = Path(__file__).resolve().parent.parent / "translations" / "vi.csv"

REQUIRED_COUNT = 137
SAMPLES = {
    "Accent Color": "Màu nhấn",
    "Login Feature Card": "Thẻ tính năng trang đăng nhập",
    "Theme Settings": "Cài đặt giao diện",
    "Theme Preference": "Tùy chọn giao diện",
}


def load_vi_csv() -> dict:
    result = {}
    with open(VI_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            source = row[0].strip()
            vi = row[1].strip()
            if source and source not in result:
                result[source] = vi
    return result


class TestSanpraViCsv(unittest.TestCase):
    def test_vi_csv_ton_tai(self) -> None:
        self.assertTrue(VI_CSV.exists())

    def test_du_so_muc(self) -> None:
        catalog = load_vi_csv()
        self.assertEqual(len(catalog), REQUIRED_COUNT, f"entries={len(catalog)}")

    def test_mau_co_dung_ban_dich(self) -> None:
        catalog = load_vi_csv()
        for source, vi in SAMPLES.items():
            self.assertEqual(catalog.get(source, ""), vi, f"sai bản dịch: {source}")

    def test_2_cot_khong_header(self) -> None:
        with open(VI_CSV, encoding="utf-8-sig", newline="") as f:
            first = next(csv.reader(f))
        self.assertEqual(len(first), 2, f"dòng đầu phải 2 cột, got {len(first)}")


if __name__ == "__main__":
    unittest.main()
