"""Build the frozen CP3 golden set from the private Discord CSV export.

The generated JSON is self-contained. The CSV is only used to copy source
messages verbatim and must not be committed.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


# File này nằm ở codebase/scripts/build_golden_set.py -> lùi 2 cấp mới ra thư mục gốc repo.
ROOT = Path(__file__).resolve().parent.parent.parent
CSV_PATH = ROOT / "k4_messages.csv"
OUTPUT_PATH = ROOT / "eval" / "golden_set.json"

STAFF_AUTHORS = {"D3694", "D9617", "D8938"}


def expected_item(item_type: str, due: str | None, confidence: str) -> dict:
    return {"type": item_type, "due": due, "confidence": confidence}


CASES = [
    {
        "id": "G01",
        "group": "L1_source",
        "source": "real:M72484,M28485",
        "description": "Hỏi hạn Lab02 nhưng bot xác nhận không có ngày giờ trong dữ liệu",
        "now": "2026-09-12 23:55",
        "message_ids": ["M72484", "M28485"],
        "expected": [],
        "rationale": "Không có nguồn chính thức nêu hạn; không được tự bịa deadline.",
    },
    {
        "id": "G02",
        "group": "L1_source",
        "source": "real:M57630",
        "description": "Bot nêu giờ thường lệ nhưng không có ngày cụ thể",
        "now": "2026-09-12 12:52",
        "message_ids": ["M57630"],
        "expected": [expected_item("DEADLINE", None, "low")],
        "rationale": "Có quy tắc 23:59 nhưng thiếu ngày và nguồn chỉ là bot, nên due=null và confidence=low.",
    },
    {
        "id": "G03",
        "group": "L1_source",
        "source": "real:M40677,M00595",
        "description": "Học viên tự nhắc giờ hạn và bot không xác nhận được quy định",
        "now": "2026-09-13 01:28",
        "message_ids": ["M40677", "M00595"],
        "expected": [],
        "rationale": "Đây là câu hỏi xử lý ngoại lệ; không có thông báo chính thức tạo việc mới.",
    },
    {
        "id": "G04",
        "group": "L2_ambiguous",
        "source": "real:M80655,M58634",
        "description": "Hai lịch mâu thuẫn và một học viên khuyên dùng lịch UPDATED",
        "now": "2026-09-13 09:13",
        "message_ids": ["M80655", "M58634"],
        "expected": [expected_item("SCHEDULE", None, "low")],
        "rationale": "Có quyết định chọn lịch nhưng không có ngày giờ và chưa được nguồn chính thức xác nhận.",
    },
    {
        "id": "G05",
        "group": "L2_ambiguous",
        "source": "real:M33002",
        "description": "Học viên hỏi hạn tìm đồng đội nhưng không có câu trả lời",
        "now": "2026-09-13 12:02",
        "message_ids": ["M33002"],
        "expected": [],
        "rationale": "Câu hỏi không cung cấp mốc hạn và không phải thông báo hành động.",
    },
    {
        "id": "G06",
        "group": "L2_ambiguous",
        "source": "synthetic",
        "description": "Lời nhắc có hành động nhưng không rõ bài và không có hạn",
        "now": "2026-09-14 09:00",
        "messages": [
            {
                "msg_id": "SYN001",
                "channel": "channel_general",
                "author_role": "student",
                "created_at": "2026-09-14 08:58",
                "content": "Mọi người nhớ nộp bài nha, hình như sắp hết hạn rồi đó.",
            }
        ],
        "expected": [expected_item("TASK", None, "low")],
        "rationale": "Có lời nhắc thực hiện nhưng tên bài và thời hạn đều mơ hồ.",
    },
    {
        "id": "G07",
        "group": "L3_out_of_scope",
        "source": "real:M88027",
        "description": "Học viên xin gia hạn bài Lab2",
        "now": "2026-09-13 00:09",
        "message_ids": ["M88027"],
        "expected": [],
        "rationale": "AI không có thẩm quyền gia hạn và câu hỏi không tạo việc mới.",
    },
    {
        "id": "G08",
        "group": "L3_out_of_scope",
        "source": "real:M85253",
        "description": "Hỏi phòng gym gần khu học",
        "now": "2026-09-13 15:39",
        "message_ids": ["M85253"],
        "expected": [],
        "rationale": "Ngoài phạm vi học tập và phối hợp công việc K4.",
    },
    {
        "id": "G09",
        "group": "L4_domain",
        "source": "real:M09449",
        "description": "Một thông báo chính thức chứa mốc công bố và hạn đăng ký đề tài",
        "now": "2026-09-13 21:50",
        "message_ids": ["M09449"],
        "expected": [
            expected_item("SCHEDULE", "2026-09-13T22:00", "high"),
            expected_item("DEADLINE", "2026-09-20T23:59", "high"),
        ],
        "rationale": "Hai mốc có mục đích khác nhau phải được tách thành hai item.",
    },
    {
        "id": "G10",
        "group": "L4_domain",
        "source": "real:M78917",
        "description": "Hai quy định hạn lặp lại cho daily standup và mentor duty",
        "now": "2026-09-14 15:47",
        "message_ids": ["M78917"],
        "expected": [
            expected_item("DEADLINE", None, "high"),
            expected_item("DEADLINE", None, "high"),
        ],
        "rationale": "Có giờ lặp lại nhưng không gắn ngày cụ thể, nên cả hai due đều null.",
    },
    {
        "id": "G11",
        "group": "common",
        "source": "real:M21817",
        "description": "Thông báo Workshop 02 có ngày giờ và nền tảng rõ ràng",
        "now": "2026-09-13 09:00",
        "message_ids": ["M21817"],
        "expected": [expected_item("SCHEDULE", "2026-09-13T20:00", "high")],
        "rationale": "Thông báo chính thức, có thời gian và Zoom rõ ràng.",
    },
    {
        "id": "G12",
        "group": "common",
        "source": "real:M16114",
        "description": "Lab Coach yêu cầu kiểm tra và cài CVAT trước buổi lab",
        "now": "2026-09-13 11:22",
        "message_ids": ["M16114"],
        "expected": [expected_item("TASK", None, "high")],
        "rationale": "Nhiệm vụ chính thức nhưng không có giờ chót đủ chính xác để điền due.",
    },
    {
        "id": "G13",
        "group": "common",
        "source": "real:M47011",
        "description": "Lab Coach yêu cầu đổi tên Discord theo cú pháp",
        "now": "2026-09-12 09:41",
        "message_ids": ["M47011"],
        "expected": [expected_item("TASK", None, "high")],
        "rationale": "Nhiệm vụ rõ ràng từ Lab Coach, không nêu hạn.",
    },
    {
        "id": "G14",
        "group": "common",
        "source": "real:M49744",
        "description": "Thông báo hoàn tất onboarding và ghép đội trước hạn",
        "now": "2026-09-12 18:03",
        "message_ids": ["M49744"],
        "expected": [expected_item("DEADLINE", "2026-09-13T21:00", "high")],
        "rationale": "Các bước onboarding hợp thành một deliverable có hạn chính thức duy nhất.",
    },
    {
        "id": "G15",
        "group": "common",
        "source": "real:M31002",
        "description": "BTC nhắc vào lại đúng link mời để hệ thống nhận diện",
        "now": "2026-09-12 18:19",
        "message_ids": ["M31002"],
        "expected": [expected_item("TASK", None, "high")],
        "rationale": "Có hành động cụ thể từ BTC nhưng không nêu hạn.",
    },
    {
        "id": "G16",
        "group": "common",
        "source": "real:M14573",
        "description": "BTC yêu cầu kiểm tra hồ sơ Phoenix khớp tài khoản Discord",
        "now": "2026-09-13 20:38",
        "message_ids": ["M14573"],
        "expected": [expected_item("TASK", None, "high")],
        "rationale": "Hành động kiểm tra tài khoản rõ ràng từ BTC, không có hạn.",
    },
    {
        "id": "G17",
        "group": "common",
        "source": "real:M23868",
        "description": "BTC hướng dẫn đổi tài khoản Discord trong hồ sơ Phoenix",
        "now": "2026-09-13 20:45",
        "message_ids": ["M23868"],
        "expected": [expected_item("TASK", None, "high")],
        "rationale": "Hướng dẫn xử lý tài khoản là nhiệm vụ cụ thể, không có hạn.",
    },
    {
        "id": "G18",
        "group": "common",
        "source": "real:M01982",
        "description": "Bot hiển thị Gate 1 với deadline tuyệt đối và deliverables",
        "now": "2026-09-13 21:59",
        "message_ids": ["M01982"],
        "expected": [expected_item("DEADLINE", "2026-09-20T23:59", "low")],
        "rationale": "Mốc giờ rõ nhưng nguồn là bot; người dùng vẫn cần đối chiếu nguồn chính thức.",
    },
    {
        "id": "G19",
        "group": "common",
        "source": "real:M45316,M79177",
        "description": "BTC xác nhận hạn mentor duty là trước 12h hôm sau",
        "now": "2026-09-14 16:10",
        "message_ids": ["M45316", "M79177"],
        "expected": [expected_item("DEADLINE", "2026-09-15T12:00", "high")],
        "rationale": "Câu trả lời chính thức xác nhận mốc tương đối, quy đổi theo ngày gửi.",
    },
    {
        "id": "G20",
        "group": "rare",
        "source": "real:M47011,M12505",
        "description": "Cùng thông báo đổi tên được đăng ở hai channel",
        "now": "2026-09-12 09:42",
        "message_ids": ["M47011", "M12505"],
        "expected": [expected_item("TASK", None, "high")],
        "rationale": "Hai nội dung giống hệt nhau phải được gộp thành một việc.",
    },
    {
        "id": "G21",
        "group": "rare",
        "source": "real:M71036,M01313",
        "description": "Hai câu trả lời bot trùng nhau về hạn daily standup",
        "now": "2026-09-14 09:08",
        "message_ids": ["M71036", "M01313"],
        "expected": [expected_item("DEADLINE", None, "low")],
        "rationale": "Gộp nội dung lặp; thiếu ngày cụ thể và nguồn bot nên due=null, confidence=low.",
    },
    {
        "id": "G22",
        "group": "rare",
        "source": "real:M82237",
        "description": "Bài đăng chỉ cung cấp recording Workshop đã diễn ra",
        "now": "2026-09-13 14:48",
        "message_ids": ["M82237"],
        "expected": [],
        "rationale": "Tài nguyên xem lại không phải task, deadline hay lịch sắp tới.",
    },
]


def load_messages() -> dict[str, dict]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["msg_id"]: row for row in csv.DictReader(handle)}


def author_role(row: dict) -> str:
    if row["is_bot"].strip().lower() == "true" or row["author"] == "BOT":
        return "bot"
    if row["author"] in STAFF_AUTHORS:
        return "staff"
    return "student"


def normalize_message(row: dict) -> dict:
    return {
        "msg_id": row["msg_id"],
        "channel": row["channel"],
        "author_role": author_role(row),
        "created_at": row["created_at_vn"],
        "content": row["content"],
    }


def build() -> list[dict]:
    source_messages = load_messages()
    output = []
    for case in CASES:
        if "messages" in case:
            messages = case["messages"]
        else:
            missing = [msg_id for msg_id in case["message_ids"] if msg_id not in source_messages]
            if missing:
                raise KeyError(f"{case['id']} references missing messages: {missing}")
            messages = [normalize_message(source_messages[msg_id]) for msg_id in case["message_ids"]]

        output.append(
            {
                "id": case["id"],
                "group": case["group"],
                "source": case["source"],
                "description": case["description"],
                "input": {"now": case["now"], "messages": messages},
                "expected": {"items": case["expected"]},
                "label_rationale": case["rationale"],
            }
        )
    return output


def validate(cases: list[dict]) -> None:
    expected_groups = {
        "L1_source": 3,
        "L2_ambiguous": 3,
        "L3_out_of_scope": 2,
        "L4_domain": 2,
        "common": 9,
        "rare": 3,
    }
    actual_groups = {group: 0 for group in expected_groups}
    ids = set()
    real_cases = 0

    for case in cases:
        if case["id"] in ids:
            raise ValueError(f"Duplicate case id: {case['id']}")
        ids.add(case["id"])
        actual_groups[case["group"]] += 1
        real_cases += case["source"].startswith("real:")

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", case["input"]["now"]):
            raise ValueError(f"Invalid now timestamp in {case['id']}")

        if case["source"].startswith("real:"):
            declared_ids = case["source"].removeprefix("real:").split(",")
            actual_ids = [message["msg_id"] for message in case["input"]["messages"]]
            if declared_ids != actual_ids:
                raise ValueError(
                    f"Source ids do not match input messages in {case['id']}: "
                    f"{declared_ids} != {actual_ids}"
                )

        messages_by_id = {message["msg_id"]: message for message in case["input"]["messages"]}
        for message in messages_by_id.values():
            if message["author_role"] not in {"staff", "student", "bot"}:
                raise ValueError(f"Invalid author_role in {case['id']}")
            if not message["content"]:
                raise ValueError(f"Empty content in {case['id']}")

        for item in case["expected"]["items"]:
            if item["type"] not in {"DEADLINE", "TASK", "SCHEDULE"}:
                raise ValueError(f"Invalid type in {case['id']}")
            if item["confidence"] not in {"high", "low"}:
                raise ValueError(f"Invalid confidence in {case['id']}")
            if item["due"] is not None and not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", item["due"]
            ):
                raise ValueError(f"Invalid due timestamp in {case['id']}")

    if len(cases) != 22:
        raise ValueError(f"Expected 22 cases, found {len(cases)}")
    if actual_groups != expected_groups:
        raise ValueError(f"Wrong group distribution: {actual_groups}")
    if real_cases < 14:
        raise ValueError(f"Expected at least 14 real cases, found {real_cases}")


if __name__ == "__main__":
    golden_set = build()
    validate(golden_set)
    OUTPUT_PATH.write_text(
        json.dumps(golden_set, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(golden_set)} cases to {OUTPUT_PATH}")
