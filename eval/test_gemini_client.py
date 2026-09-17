import json
import unittest
from gemini_client import filter_messages_by_channel, build_prompt, parse_response


class TestFilterMessagesByChannel(unittest.TestCase):
    def test_keeps_only_selected_channels(self):
        messages = [
            {"msg_id": "M1", "channel": "general", "content": "a"},
            {"msg_id": "M2", "channel": "random", "content": "b"},
        ]
        result = filter_messages_by_channel(messages, ["general"])
        self.assertEqual([m["msg_id"] for m in result], ["M1"])

    def test_empty_selection_returns_empty(self):
        messages = [{"msg_id": "M1", "channel": "general", "content": "a"}]
        self.assertEqual(filter_messages_by_channel(messages, []), [])


class TestBuildPrompt(unittest.TestCase):
    def test_embeds_fields_and_instruction(self):
        prompt = build_prompt("RULES", [{
            "msg_id": "M1", "channel": "general", "author_role": "hoc_vien",
            "created_at_vn": "2026-09-12 10:00", "content": "Hạn nộp Lab02",
        }])
        self.assertIn("RULES", prompt)
        self.assertIn("msg_id=M1", prompt)
        self.assertIn("Hạn nộp Lab02", prompt)
        self.assertIn("mảng JSON", prompt)


class TestParseResponse(unittest.TestCase):
    def _wrap(self, cards):
        return json.dumps({"choices": [{"message": {"content": json.dumps(cards)}}]})

    def test_extracts_valid_cards(self):
        raw = self._wrap([{
            "type": "TASK", "title": "x", "deadline_text": "", "confidence": "high",
            "quote": "q", "msg_id": "M1", "escalate": False, "reason": "r",
        }])
        cards = parse_response(raw)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["type"], "TASK")

    def test_empty_array_is_valid(self):
        raw = self._wrap([])
        self.assertEqual(parse_response(raw), [])

    def test_raises_on_missing_field(self):
        raw = self._wrap([{"type": "TASK"}])
        with self.assertRaisesRegex(ValueError, "thiếu field"):
            parse_response(raw)

    def test_raises_on_invalid_type(self):
        raw = self._wrap([{
            "type": "BOGUS", "title": "x", "deadline_text": "", "confidence": "high",
            "quote": "q", "msg_id": "M1", "escalate": False, "reason": "r",
        }])
        with self.assertRaisesRegex(ValueError, "type không hợp lệ"):
            parse_response(raw)

    def test_raises_on_non_json_envelope(self):
        with self.assertRaisesRegex(ValueError, "bao ngoài"):
            parse_response("not json")

    def test_raises_on_non_array_text(self):
        raw = json.dumps({"choices": [{"message": {"content": json.dumps({"type": "TASK"})}}]})
        with self.assertRaisesRegex(ValueError, "mảng card"):
            parse_response(raw)

    def test_raises_on_empty_content(self):
        raw = json.dumps({"choices": [{"message": {"content": ""}}]})
        with self.assertRaisesRegex(ValueError, "rỗng"):
            parse_response(raw)


if __name__ == "__main__":
    unittest.main()
