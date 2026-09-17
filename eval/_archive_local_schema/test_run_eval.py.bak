import io
import json
import unittest
from run_eval import grade_case, write_log_entry


class TestGradeCase(unittest.TestCase):
    def test_none_case_passes_with_zero_cards(self):
        case = {"id": "GS-01", "expected": {"type": "NONE", "count": 0}}
        result = grade_case(case, [])
        self.assertTrue(result["passed"], result["reasons"])

    def test_none_case_fails_if_card_fabricated(self):
        case = {"id": "GS-01", "expected": {"type": "NONE", "count": 0}}
        actual = [{"type": "TASK", "title": "x", "deadline_text": "", "confidence": "low",
                   "quote": "q", "msg_id": "M1", "escalate": False, "reason": "r"}]
        result = grade_case(case, actual)
        self.assertFalse(result["passed"])

    def test_deadline_text_empty_required(self):
        case = {"id": "GS-02", "expected": {"type": "TASK", "deadline_text_empty": True}}
        actual = [{"type": "TASK", "title": "x", "deadline_text": "19:30 16/09",
                   "confidence": "low", "quote": "q", "msg_id": "M72484", "escalate": True, "reason": "r"}]
        result = grade_case(case, actual)
        self.assertFalse(result["passed"])

    def test_deadline_text_empty_passes_when_actually_empty(self):
        case = {"id": "GS-02", "expected": {"type": "TASK", "deadline_text_empty": True}}
        actual = [{"type": "TASK", "title": "x", "deadline_text": "",
                   "confidence": "low", "quote": "q", "msg_id": "M72484", "escalate": True, "reason": "r"}]
        result = grade_case(case, actual)
        self.assertTrue(result["passed"], result["reasons"])

    def test_scope_must_contain_passes(self):
        case = {"id": "GS-08", "expected": {"type": "SCHED", "scope_must_contain": "cụm 1-3"}}
        actual = [{"type": "SCHED", "title": "Di chuyển cụm 1-3 sang E403", "deadline_text": "",
                   "confidence": "high", "quote": "cụm 1-3", "msg_id": "SYN-08", "escalate": False, "reason": "r"}]
        result = grade_case(case, actual)
        self.assertTrue(result["passed"], result["reasons"])

    def test_scope_must_contain_fails_when_missing(self):
        case = {"id": "GS-08", "expected": {"type": "SCHED", "scope_must_contain": "cụm 1-3"}}
        actual = [{"type": "SCHED", "title": "Di chuyển sang E403", "deadline_text": "",
                   "confidence": "high", "quote": "mọi người di chuyển", "msg_id": "SYN-08", "escalate": False, "reason": "r"}]
        result = grade_case(case, actual)
        self.assertFalse(result["passed"])

    def test_count_mismatch_fails(self):
        case = {"id": "GS-09", "expected": {"type": "DEADLINE", "count": 2}}
        actual = [{"type": "DEADLINE", "title": "x", "deadline_text": "22:00 13/09", "confidence": "high",
                   "quote": "q", "msg_id": "M09449", "escalate": False, "reason": "r"}]
        result = grade_case(case, actual)
        self.assertFalse(result["passed"])

    def test_escalate_required_for_none_case(self):
        case = {"id": "GS-14", "expected": {"type": "NONE", "escalate": True}}
        result = grade_case(case, [])
        self.assertTrue(result["passed"], result["reasons"])


class TestWriteLogEntry(unittest.TestCase):
    def test_writes_one_json_line_with_timestamp(self):
        buf = io.StringIO()
        write_log_entry(buf, {"case_id": "GS-01", "prompt": "p", "raw_response": "r"})
        lines = buf.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["case_id"], "GS-01")
        self.assertEqual(entry["prompt"], "p")
        self.assertEqual(entry["raw_response"], "r")
        self.assertIn("timestamp", entry)

    def test_noop_when_log_file_is_none(self):
        # Không được raise dù không truyền log_file (dùng ở nơi không cần ghi log, ví dụ test khác).
        write_log_entry(None, {"case_id": "GS-01"})

    def test_preserves_error_field(self):
        buf = io.StringIO()
        write_log_entry(buf, {"case_id": "GS-02", "prompt": "p", "error": "boom"})
        entry = json.loads(buf.getvalue().splitlines()[0])
        self.assertEqual(entry["error"], "boom")
        self.assertNotIn("raw_response", entry)


if __name__ == "__main__":
    unittest.main()
