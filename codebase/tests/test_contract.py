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


@pytest.mark.parametrize(
    ("author_role", "expected_reason"),
    [
        ("bot", "Nguồn bot"),
        ("student", "Thông tin từ học viên"),
    ],
)
def test_post_process_evidence_downgrades_untrusted_sources(author_role, expected_reason):
    """Nguồn bot/học viên không được giữ confidence=high dù quote hợp lệ."""
    messages = [
        {
            "msg_id": "M200",
            "author_role": author_role,
            "content": "Hạn nộp là 23:59 ngày 20/09/2026.",
        }
    ]
    items = [
        {
            "type": "DEADLINE",
            "title": "Nộp bài",
            "due": "2026-09-20T23:59",
            "confidence": "high",
            "review_reason": None,
            "evidence": {
                "msg_id": "M200",
                "quote": "Hạn nộp là 23:59 ngày 20/09/2026",
            },
        }
    ]

    processed = post_process_evidence(items, messages)

    assert processed[0]["confidence"] == "low"
    assert expected_reason in processed[0]["review_reason"]


def test_post_process_evidence_clears_reason_for_high_confidence():
    """Item high từ staff phải có review_reason=null theo hợp đồng output."""
    messages = [
        {
            "msg_id": "M201",
            "author_role": "staff",
            "content": "Workshop bắt đầu lúc 20:00 ngày 20/09/2026.",
        }
    ]
    items = [
        {
            "type": "SCHEDULE",
            "title": "Workshop",
            "due": "2026-09-20T20:00",
            "confidence": "high",
            "review_reason": "Lý do thừa từ model",
            "evidence": {
                "msg_id": "M201",
                "quote": "Workshop bắt đầu lúc 20:00 ngày 20/09/2026",
            },
        }
    ]

    processed = post_process_evidence(items, messages)

    assert processed[0]["confidence"] == "high"
    assert processed[0]["review_reason"] is None


def test_post_process_recurring_submission_window_has_no_concrete_due():
    """Khung giờ lặp lại là DEADLINE nhưng không được gắn vào ngày hiện tại."""
    quote = "Khung giờ nộp daily hàng ngày là từ 0h-10h sáng nhé."
    messages = [
        {
            "msg_id": "M202",
            "author_role": "bot",
            "content": quote,
        }
    ]
    items = [
        {
            "type": "TASK",
            "title": "Nộp daily trước 10h",
            "due": "2026-09-14T10:00",
            "confidence": "high",
            "review_reason": None,
            "evidence": {"msg_id": "M202", "quote": quote},
        }
    ]

    processed = post_process_evidence(items, messages)

    assert processed[0]["type"] == "DEADLINE"
    assert processed[0]["due"] is None
    assert processed[0]["confidence"] == "low"


def test_post_process_recurring_staff_window_keeps_high_confidence():
    """Chuẩn hóa type/due không được làm giảm confidence của nguồn staff."""
    quote = "Khung giờ nộp mentor duty: trước 12h00 các buổi mentor duty."
    messages = [
        {
            "msg_id": "M203",
            "author_role": "staff",
            "content": quote,
        }
    ]
    items = [
        {
            "type": "TASK",
            "title": "Nộp mentor duty",
            "due": None,
            "confidence": "high",
            "review_reason": None,
            "evidence": {"msg_id": "M203", "quote": quote},
        }
    ]

    processed = post_process_evidence(items, messages)

    assert processed[0]["type"] == "DEADLINE"
    assert processed[0]["due"] is None
    assert processed[0]["confidence"] == "high"


def test_post_process_infers_next_day_deadline_from_staff_evidence():
    """Mốc '12h hôm sau' được tính từ created_at của chính tin evidence."""
    quote = "Nộp hôm trước miễn trước 12h hôm sau là được nhé"
    messages = [
        {
            "msg_id": "M204",
            "author_role": "staff",
            "created_at": "2026-09-14 16:09",
            "content": quote,
        }
    ]
    items = [
        {
            "type": "DEADLINE",
            "title": "Nộp mentor duty",
            "due": None,
            "confidence": "high",
            "review_reason": None,
            "evidence": {"msg_id": "M204", "quote": quote},
        }
    ]

    processed = post_process_evidence(items, messages)

    assert processed[0]["due"] == "2026-09-15T12:00"


def test_post_process_removes_instruction_task_covered_by_deadline():
    """Một bước trong mục hướng dẫn không thành item riêng cạnh deadline tổng."""
    content = (
        "Gate 1 — Chốt đề tài\n"
        "Deadline 23:59 ngày 20/09/2026\n"
        "\nCách setup AI Log\n"
        "Setup AI Log càng sớm càng tốt"
    )
    messages = [
        {
            "msg_id": "M205",
            "author_role": "bot",
            "created_at": "2026-09-13 21:58",
            "content": content,
        }
    ]
    items = [
        {
            "type": "DEADLINE",
            "title": "Nộp Gate 1",
            "due": "2026-09-20T23:59",
            "confidence": "low",
            "review_reason": "Nguồn bot",
            "evidence": {"msg_id": "M205", "quote": "Deadline 23:59 ngày 20/09/2026"},
        },
        {
            "type": "TASK",
            "title": "Setup AI Log",
            "due": None,
            "confidence": "low",
            "review_reason": "Nguồn bot",
            "evidence": {"msg_id": "M205", "quote": "Setup AI Log càng sớm càng tốt"},
        },
    ]

    processed = post_process_evidence(items, messages)

    assert len(processed) == 1
    assert processed[0]["type"] == "DEADLINE"


def test_extract_garbage_text_returns_empty_items_without_crash(monkeypatch):
    """Task 1.4: Đưa text rác vào không làm chết chương trình, trả {"items": [], "error": ...}"""
    from core.extractor import extract

    # Giả lập LLM trả về text rác không phải JSON ở cả lượt 1 và retry
    monkeypatch.setattr("core.extractor.call_llm", lambda prompt, system_prompt: ("Hoàn toàn là text vô nghĩa không có JSON nào", 50.0))
    monkeypatch.setattr("core.extractor.log_llm_call", lambda **kwargs: None)

    messages = [{"msg_id": "M99", "content": "Tin rác"}]
    res = extract(messages, "2026-09-13 09:00")

    assert isinstance(res, dict)
    assert res.get("items") == []
    assert "error" in res
    assert "Lỗi sau retry" in res["error"]

