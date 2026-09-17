import json
import os
import sys
from gemini_client import build_prompt, call_gemini, parse_response, filter_messages_by_channel

PROMPT_TEXT = open(os.path.join(os.path.dirname(__file__), "..", "codebase", "PROMPT.md"), encoding="utf-8").read()
# ĐỒNG BỘ TAY: nội dung này phải khớp codebase/PROMPT.md dùng trong ai-client.js — sửa 1 chỗ phải sửa chỗ kia (spec-cp3.md §7).


def grade_case(case, actual_cards):
    expected = case["expected"]
    reasons = []

    if "count" in expected and len(actual_cards) != expected["count"]:
        reasons.append(f"Kỳ vọng {expected['count']} card, thực tế {len(actual_cards)}")

    if expected.get("type") == "NONE":
        if len(actual_cards) != 0:
            reasons.append(f"Kỳ vọng NONE (0 card) nhưng có {len(actual_cards)} card")
    elif "type" in expected and actual_cards:
        types_found = [c["type"] for c in actual_cards]
        if expected["type"] not in types_found:
            reasons.append(f"Không thấy type={expected['type']} trong {types_found}")

    if expected.get("escalate") is True and expected.get("type") != "NONE":
        if not any(c.get("escalate") for c in actual_cards):
            reasons.append("Kỳ vọng escalate=true nhưng không card nào escalate")

    if expected.get("confidence") and actual_cards:
        confidences = [c.get("confidence") for c in actual_cards]
        if expected["confidence"] not in confidences:
            reasons.append(f"Kỳ vọng confidence={expected['confidence']}, thực tế {confidences}")

    if expected.get("deadline_text_empty") and actual_cards:
        non_empty = [c for c in actual_cards if c.get("deadline_text")]
        if non_empty:
            reasons.append(f"Kỳ vọng deadline_text rỗng (không bịa giờ) nhưng có {[c['deadline_text'] for c in non_empty]}")

    if expected.get("scope_must_contain") and actual_cards:
        needle = expected["scope_must_contain"]
        if not any(needle in (c.get("title", "") + c.get("quote", "")) for c in actual_cards):
            reasons.append(f'Kỳ vọng giữ phạm vi "{needle}" trong title/quote nhưng không thấy')

    if expected.get("priority_source_channel") and actual_cards:
        wanted = expected["priority_source_channel"]
        if not any(wanted in c.get("quote", "") or wanted in c.get("reason", "") for c in actual_cards):
            reasons.append(f'Kỳ vọng ưu tiên nguồn "{wanted}" nhưng không thấy nhắc trong quote/reason')

    return {"id": case["id"], "passed": len(reasons) == 0, "reasons": reasons}


def run_one_case(case, api_key):
    messages = filter_messages_by_channel(case["messages"], case["selected_channels"])
    if case.get("filter_only") or not messages:
        return []
    prompt = build_prompt(PROMPT_TEXT, messages)
    try:
        raw = call_gemini(prompt, api_key)
        return parse_response(raw)
    except (ValueError, RuntimeError) as e:
        return {"__error__": str(e)}


def write_results_md(golden_set, graded, out_path):
    total = len(graded)
    passed = sum(1 for g in graded if g["passed"])
    lines = [
        "# CP3 Run Results — Actionable Digest",
        "",
        f"Pass rate: {passed}/{total} ({passed/total*100:.1f}%)",
        "",
        "| ID | Bucket | Pass | Lý do fail |",
        "|---|---|---|---|",
    ]
    case_by_id = {c["id"]: c for c in golden_set}
    for g in graded:
        c = case_by_id[g["id"]]
        status = "✅" if g["passed"] else "❌"
        reasons = "; ".join(g["reasons"]) if g["reasons"] else "-"
        lines.append(f"| {g['id']} | {c['bucket']} | {status} | {reasons} |")
    lines.append("")
    lines.append("## Phân tích nguyên nhân case sai")
    lines.append("")
    for g in graded:
        if not g["passed"]:
            lines.append(f"- **{g['id']}**: {'; '.join(g['reasons'])}")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Thiếu biến môi trường GEMINI_API_KEY", file=sys.stderr)
        sys.exit(1)

    golden_set_path = os.path.join(os.path.dirname(__file__), "golden_set.json")
    with open(golden_set_path, encoding="utf-8") as f:
        golden_set = json.load(f)

    graded = []
    for case in golden_set:
        actual = run_one_case(case, api_key)
        if isinstance(actual, dict) and "__error__" in actual:
            graded.append({"id": case["id"], "passed": False, "reasons": [f"Lỗi gọi API: {actual['__error__']}"]})
            continue
        graded.append(grade_case(case, actual))

    out_path = os.path.join(os.path.dirname(__file__), "run_results.md")
    write_results_md(golden_set, graded, out_path)
    passed = sum(1 for g in graded if g["passed"])
    print(f"Đã ghi kết quả vào {out_path} — {passed}/{len(graded)} case đạt")


if __name__ == "__main__":
    main()
