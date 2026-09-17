import json
import os
import unittest

HERE = os.path.dirname(__file__)


class TestGoldenSetStructure(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(HERE, "golden_set.json"), encoding="utf-8") as f:
            self.cases = json.load(f)

    def test_has_20_cases(self):
        self.assertEqual(len(self.cases), 20)

    def test_ids_are_unique(self):
        ids = [c["id"] for c in self.cases]
        self.assertEqual(len(ids), len(set(ids)))

    def test_at_least_two_per_class_bucket(self):
        buckets = ["class1", "class2", "class3", "class4"]
        counts = {b: 0 for b in buckets}
        for c in self.cases:
            if c["bucket"] in counts:
                counts[c["bucket"]] += 1
        for b in buckets:
            self.assertGreaterEqual(counts[b], 2, f"Lớp {b} phải có ít nhất 2 case, hiện có {counts[b]}")

    def test_common_bucket_in_range(self):
        n = sum(1 for c in self.cases if c["bucket"] == "common")
        self.assertGreaterEqual(n, 8)
        self.assertLessEqual(n, 10)

    def test_edge_bucket_in_range(self):
        n = sum(1 for c in self.cases if c["bucket"] == "edge")
        self.assertGreaterEqual(n, 2)
        self.assertLessEqual(n, 4)

    def test_at_least_10_real_sourced(self):
        n = sum(1 for c in self.cases if c.get("source") == "real")
        self.assertGreaterEqual(n, 10, f"Cần ≥10 case từ dữ liệu thật, hiện có {n}")

    def test_every_case_has_expected_block(self):
        for c in self.cases:
            self.assertIn("expected", c, f"{c['id']} thiếu 'expected'")


if __name__ == "__main__":
    unittest.main()
