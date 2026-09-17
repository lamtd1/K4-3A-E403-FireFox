"""Runner đánh giá tự động chất lượng AI theo bộ kiểm thử chuẩn Golden Set.

Thực hiện phần việc của Nguyễn Duy Phong (Đội trưởng) theo CP3_TASKS.md (Mục 3.2):
- Đọc eval/golden_set.json (22 case chuẩn)
- Gọi hàm extract() từ codebase/core/extractor.py cho từng case
- Tự động chấm 5 tiêu chí C1 - C5
- Lưu toàn bộ kết quả thô vào eval/runs/run1_raw.json
- In bảng thống kê chi tiết ra màn hình
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from itertools import permutations
from typing import Dict, Any, List, Tuple

# Đảm bảo in UTF-8 không bị crash charmap trên Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Đảm bảo đường dẫn import hoạt động từ thư mục gốc
ROOT_DIR = Path(__file__).resolve().parent.parent
CODEBASE_DIR = ROOT_DIR / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))

try:
    from core.extractor import extract
    from core.llm_client import get_llm_config
except ImportError as e:
    raise RuntimeError(f"Không thể import module AI từ {CODEBASE_DIR}: {e}")


def get_git_commit_hash() -> str:
    """Lấy commit hash hiện tại của repo git."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


def normalize_due(due_val: Any) -> Any:
    """Chuẩn hóa giá trị due (cắt bớt khoảng trắng, None nếu rỗng)."""
    if due_val is None:
        return None
    s = str(due_val).strip()
    return s if s else None


def check_evidence_quote(actual_items: List[Dict[str, Any]], messages: List[Dict[str, Any]]) -> bool:
    """
    Tiêu chí C5: Kiểm tra quote của mọi item trích xuất có phải chuỗi con trong tin gốc không.
    """
    if not actual_items:
        return True

    msg_map = {str(m.get("msg_id")): str(m.get("content", "")) for m in messages if isinstance(m, dict)}

    for item in actual_items:
        evidence = item.get("evidence") or {}
        msg_id = str(evidence.get("msg_id", "")).strip()
        quote = str(evidence.get("quote", "")).strip()

        if not quote:
            return False
        if msg_id not in msg_map:
            return False
        if quote not in msg_map[msg_id]:
            return False

    return True


def evaluate_case(case: Dict[str, Any], actual: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chấm điểm 1 test case theo 5 tiêu chí C1 - C5 trong CP3_TASKS.md Mục 0.3.
    """
    expected_items = case.get("expected", {}).get("items", [])
    actual_items = actual.get("items", [])
    messages = case.get("input", {}).get("messages", [])

    n_exp = len(expected_items)
    n_act = len(actual_items)

    # C1: Đúng số lượng việc
    c1 = (n_act == n_exp)

    # C5: Có căn cứ
    c5 = check_evidence_quote(actual_items, messages)

    # Nếu cả 2 đều rỗng -> C1..C5 đều đạt
    if n_exp == 0 and n_act == 0:
        return {
            "c1_count": True,
            "c2_type": True,
            "c3_due": True,
            "c4_confidence": True,
            "c5_evidence": True,
            "passed": True,
            "failure_reasons": []
        }

    # Nếu số lượng khác nhau:
    if n_exp != n_act:
        failure_reasons = [f"C1 Fail: số lượng item thực tế ({n_act}) != kỳ vọng ({n_exp})"]
        # Vẫn thử tìm matching tốt nhất để ghi nhận lỗi các tiêu chí khác
        c2 = False
        c3 = False
        c4 = False
        return {
            "c1_count": False,
            "c2_type": c2,
            "c3_due": c3,
            "c4_confidence": c4,
            "c5_evidence": c5,
            "passed": False,
            "failure_reasons": failure_reasons
        }

    # Trường hợp cùng số lượng items (n_act == n_exp > 0):
    # Tìm hoán vị tối ưu khớp các trường type, due, confidence
    best_c2 = False
    best_c3 = False
    best_c4 = False
    best_match_score = -1
    best_permutation_errors = []

    for perm in permutations(actual_items):
        perm_c2 = True
        perm_c3 = True
        perm_c4 = True
        errs = []

        for act_it, exp_it in zip(perm, expected_items):
            act_type = act_it.get("type")
            exp_type = exp_it.get("type")
            if act_type != exp_type:
                perm_c2 = False
                errs.append(f"C2: type '{act_type}' != '{exp_type}'")

            act_due = normalize_due(act_it.get("due"))
            exp_due = normalize_due(exp_it.get("due"))
            if act_due != exp_due:
                perm_c3 = False
                errs.append(f"C3: due '{act_due}' != '{exp_due}'")

            act_conf = act_it.get("confidence")
            exp_conf = exp_it.get("confidence")
            if act_conf != exp_conf:
                perm_c4 = False
                errs.append(f"C4: confidence '{act_conf}' != '{exp_conf}'")

        score = (1 if perm_c2 else 0) + (1 if perm_c3 else 0) + (1 if perm_c4 else 0)
        if score > best_match_score:
            best_match_score = score
            best_c2 = perm_c2
            best_c3 = perm_c3
            best_c4 = perm_c4
            best_permutation_errors = errs

    if not c5:
        best_permutation_errors.append("C5 Fail: trích dẫn quote không nằm trong nội dung tin gốc")

    passed = c1 and best_c2 and best_c3 and best_c4 and c5

    return {
        "c1_count": c1,
        "c2_type": best_c2,
        "c3_due": best_c3,
        "c4_confidence": best_c4,
        "c5_evidence": c5,
        "passed": passed,
        "failure_reasons": best_permutation_errors
    }


def main():
    parser = argparse.ArgumentParser(description="Runner eval chất lượng Actionable Digest")
    parser.add_argument("--golden-set", default="eval/golden_set.json", help="Đường dẫn file golden set")
    parser.add_argument("--output", default="eval/runs/run1_raw.json", help="Đường dẫn file kết quả raw")
    parser.add_argument("--case-id", default=None, help="Chạy riêng 1 case (ví dụ G01)")
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn số case chạy")
    parser.add_argument("--delay", type=float, default=0.5, help="Độ trễ giữa các lượt gọi (giây)")
    args = parser.parse_args()

    golden_path = ROOT_DIR / args.golden_set
    if not golden_path.exists():
        print(f"Lỗi: Không tìm thấy file golden set tại {golden_path}")
        sys.exit(1)

    with open(golden_path, "r", encoding="utf-8") as f:
        all_cases = json.load(f)

    if args.case_id:
        all_cases = [c for c in all_cases if c.get("id") == args.case_id]
        if not all_cases:
            print(f"Lỗi: Không tìm thấy case có id '{args.case_id}'")
            sys.exit(1)

    if args.limit:
        all_cases = all_cases[:args.limit]

    config = get_llm_config()
    provider = config.get("provider", "unknown")
    model = config.get("model", "unknown")
    commit_hash = get_git_commit_hash()
    start_run_time = time.strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 80)
    print(" BẮT ĐẦU CHẠY EVALUATION — ACTIONABLE DIGEST")
    print("=" * 80)
    print(f" Thời điểm bắt đầu : {start_run_time}")
    print(f" Provider / Model  : {provider} / {model}")
    print(f" Commit prompt     : {commit_hash}")
    print(f" Tổng số test case : {len(all_cases)}")
    print("-" * 80)

    results = []
    passed_total = 0
    start_perf = time.perf_counter()

    for idx, case in enumerate(all_cases, start=1):
        case_id = case.get("id")
        group = case.get("group")
        desc = case.get("description", "")
        input_data = case.get("input", {})
        messages = input_data.get("messages", [])
        now = input_data.get("now", "2026-09-13 09:00")

        print(f"[{idx:02d}/{len(all_cases):02d}] Case {case_id} ({group}): {desc[:40]}...", end=" ", flush=True)

        case_start = time.perf_counter()
        actual_output = {}
        err_msg = None

        try:
            actual_output = extract(messages, now)
        except Exception as ex:
            err_msg = str(ex)
            actual_output = {"items": [], "error": err_msg}

        case_latency_ms = round((time.perf_counter() - case_start) * 1000, 2)
        eval_metrics = evaluate_case(case, actual_output)

        is_passed = eval_metrics["passed"]
        if is_passed:
            passed_total += 1
            status_str = "PASSED [✓]"
        else:
            status_str = "FAILED [✗]"

        c_str = f"C1:{1 if eval_metrics['c1_count'] else 0} " \
                f"C2:{1 if eval_metrics['c2_type'] else 0} " \
                f"C3:{1 if eval_metrics['c3_due'] else 0} " \
                f"C4:{1 if eval_metrics['c4_confidence'] else 0} " \
                f"C5:{1 if eval_metrics['c5_evidence'] else 0}"

        print(f"{status_str} ({c_str}) - {case_latency_ms}ms")

        record = {
            "case_id": case_id,
            "group": group,
            "source": case.get("source"),
            "description": desc,
            "input": input_data,
            "expected": case.get("expected"),
            "actual": actual_output,
            "metrics": eval_metrics,
            "latency_ms": case_latency_ms,
            "error": err_msg
        }
        results.append(record)

        if args.delay > 0 and idx < len(all_cases):
            time.sleep(args.delay)

    total_time = round(time.perf_counter() - start_perf, 2)
    pass_rate = round((passed_total / len(all_cases)) * 100, 2) if all_cases else 0.0

    # Gom nhóm thống kê theo group
    group_stats: Dict[str, Dict[str, int]] = {}
    for r in results:
        g = r["group"]
        if g not in group_stats:
            group_stats[g] = {"total": 0, "passed": 0}
        group_stats[g]["total"] += 1
        if r["metrics"]["passed"]:
            group_stats[g]["passed"] += 1

    # Thống kê vi phạm từng tiêu chí C1 - C5
    criteria_fails = {"C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0}
    for r in results:
        m = r["metrics"]
        if not m["c1_count"]:
            criteria_fails["C1"] += 1
        if not m["c2_type"]:
            criteria_fails["C2"] += 1
        if not m["c3_due"]:
            criteria_fails["C3"] += 1
        if not m["c4_confidence"]:
            criteria_fails["C4"] += 1
        if not m["c5_evidence"]:
            criteria_fails["C5"] += 1

    # In báo cáo console
    print("=" * 80)
    print(" KẾT QUẢ TỔNG QUAN")
    print("=" * 80)
    print(f" Tổng số case : {len(all_cases)}")
    print(f" Số case ĐẠT  : {passed_total}")
    print(f" Số case TRƯỢT: {len(all_cases) - passed_total}")
    print(f" Tỷ lệ Đạt    : {pass_rate}%")
    print(f" Tổng thời gian chạy: {total_time}s")
    print("-" * 80)

    print(" KẾT QUẢ THEO NHÓM:")
    for g, s in group_stats.items():
        g_pct = round((s['passed'] / s['total']) * 100, 1) if s['total'] else 0.0
        print(f"  - {g:18s}: {s['passed']}/{s['total']} đạt ({g_pct}%)")
    print("-" * 80)

    print(" SỐ CASE TRƯỢT THEO TIÊU CHÍ:")
    for c, cnt in criteria_fails.items():
        print(f"  - {c}: {cnt} case vi phạm")
    print("=" * 80)

    # Lưu kết quả ra file json
    output_path = ROOT_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary_data = {
        "metadata": {
            "run_timestamp": start_run_time,
            "provider": provider,
            "model": model,
            "commit_hash": commit_hash,
            "total_cases": len(all_cases),
            "passed_cases": passed_total,
            "failed_cases": len(all_cases) - passed_total,
            "pass_rate": pass_rate,
            "total_duration_sec": total_time,
            "group_stats": group_stats,
            "criteria_fails": criteria_fails
        },
        "results": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu toàn bộ kết quả raw vào: {output_path}")


if __name__ == "__main__":
    main()
