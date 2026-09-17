import pytest
from core.extractor import clean_and_parse_json, post_process_evidence


def test_clean_and_parse_json_standard():
    raw = """
    {
      "items": [
        {
          "type": "SCHEDULE",
          "title": "Workshop 02",
          "due": "2026-09-13T20:00",
          "confidence": "high",
          "evidence": {"msg_id": "M1", "quote": "20:00 tối nay"}
        }
      ]
    }
    """
    res = clean_and_parse_json(raw)
    assert "items" in res
    assert len(res["items"]) == 1
    assert res["items"][0]["type"] == "SCHEDULE"


def test_clean_and_parse_json_with_markdown_fences():
    raw = """
    Dưới đây là kết quả trích xuất:
    ```json
    {
      "items": []
    }
    ```
    Hy vọng giúp ích cho bạn!
    """
    res = clean_and_parse_json(raw)
    assert res == {"items": []}


def test_clean_and_parse_json_invalid_raises():
    with pytest.raises(Exception):
        clean_and_parse_json("Đây là text rác hoàn toàn không có JSON")


def test_post_process_evidence_valid_quote():
    messages = [
        {
            "msg_id": "M100",
            "content": "Hạn chót nộp bài là 23:59 ngày mai nhé các bạn."
        }
    ]
    items = [
        {
            "type": "DEADLINE",
            "title": "Nộp bài",
            "due": "2026-09-14T23:59",
            "confidence": "high",
            "review_reason": None,
            "evidence": {
                "msg_id": "M100",
                "quote": "23:59 ngày mai"
            }
        }
    ]

    processed = post_process_evidence(items, messages)
    assert len(processed) == 1
    # Quote có trong content -> giữ nguyên high
    assert processed[0]["confidence"] == "high"
    assert processed[0]["review_reason"] is None


def test_post_process_evidence_hallucinated_quote_downgrades():
    """Task 1.5: Nếu quote không có trong content -> hạ confidence về low, gán review_reason"""
    messages = [
        {
            "msg_id": "M100",
            "content": "Thông báo ngắn: hôm nay không có bài tập."
        }
    ]
    items = [
        {
            "type": "DEADLINE",
            "title": "Nộp bài giả tưởng",
            "due": "2026-09-14T23:59",
            "confidence": "high",
            "review_reason": None,
            "evidence": {
                "msg_id": "M100",
                "quote": "Bắt buộc nộp trước 12h đêm nay"  # Quote bịa hoàn toàn
            }
        }
    ]

    processed = post_process_evidence(items, messages)
    assert len(processed) == 1
    assert processed[0]["confidence"] == "low"
    assert "Không tìm thấy trích dẫn trong tin gốc" in processed[0]["review_reason"]


def test_post_process_evidence_nonexistent_msg_id():
    """Task 1.5: Nếu msg_id không tồn tại trong danh sách messages -> hạ confidence về low"""
    messages = [
        {
            "msg_id": "M100",
            "content": "Nội dung tin 100."
        }
    ]
    items = [
        {
            "type": "TASK",
            "title": "Task ảo",
            "due": None,
            "confidence": "high",
            "review_reason": None,
            "evidence": {
                "msg_id": "M999",  # ID không tồn tại
                "quote": "Nội dung"
            }
        }
    ]

    processed = post_process_evidence(items, messages)
    assert len(processed) == 1
    assert processed[0]["confidence"] == "low"
    assert "Không tìm thấy trích dẫn trong tin gốc" in processed[0]["review_reason"]


def test_extract_garbage_text_returns_empty_items_without_crash(monkeypatch):
    """Task 1.4: Đưa text rác vào không làm chết chương trình, trả {"items": [], "error": ...}"""
    from core.extractor import extract

    # Giả lập LLM trả về text rác không phải JSON ở cả lượt 1 và retry
    monkeypatch.setattr("core.extractor.call_llm", lambda prompt, system_prompt: ("Hoàn toàn là text vô nghĩa không có JSON nào", 50.0))

    messages = [{"msg_id": "M99", "content": "Tin rác"}]
    res = extract(messages, "2026-09-13 09:00")

    assert isinstance(res, dict)
    assert res.get("items") == []
    assert "error" in res
    assert "Lỗi sau retry" in res["error"]

