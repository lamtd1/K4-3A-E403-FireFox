import unittest
from run_eval import grade_case


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


if __name__ == "__main__":
    unittest.main()
