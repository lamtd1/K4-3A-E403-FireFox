"""Hợp nhất các lượt retry lỗi hạ tầng vào một kết quả eval có thể kiểm toán."""

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT_DIR = Path(__file__).resolve().parents[2]
CODEBASE_DIR = ROOT_DIR / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))

from core.extractor import post_process_evidence  # noqa: E402
from scripts.run_eval import evaluate_case  # noqa: E402


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def criteria_fails(results: List[Dict[str, Any]]) -> Dict[str, int]:
    fields = {
        "C1": "c1_count",
        "C2": "c2_type",
        "C3": "c3_due",
        "C4": "c4_confidence",
        "C5": "c5_evidence",
    }
    return {
        label: sum(not result["metrics"][field] for result in results)
        for label, field in fields.items()
    }


def group_stats(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    stats: Dict[str, Dict[str, int]] = {}
    for result in results:
        group = result["group"]
        stats.setdefault(group, {"total": 0, "passed": 0})
        stats[group]["total"] += 1
        stats[group]["passed"] += int(result["metrics"]["passed"])
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chỉ thay các case lỗi hạ tầng bằng kết quả retry và chấm lại bằng code hiện tại."
    )
    parser.add_argument("--base", required=True, help="Lượt eval đầy đủ ban đầu")
    parser.add_argument("--retry", action="append", default=[], help="File retry một/nhiều case")
    parser.add_argument("--output", required=True, help="File kết quả hợp nhất")
    args = parser.parse_args()

    base_path = ROOT_DIR / args.base
    base = load_json(base_path)
    results_by_id = {result["case_id"]: copy.deepcopy(result) for result in base["results"]}
    retry_audit: List[Dict[str, str]] = []

    for retry_arg in args.retry:
        retry_path = ROOT_DIR / retry_arg
        retry_run = load_json(retry_path)
        retry_model = retry_run.get("metadata", {}).get("model", "unknown")

        for retry_result in retry_run.get("results", []):
            case_id = retry_result["case_id"]
            if case_id not in results_by_id:
                raise ValueError(f"Retry chứa case không có trong base: {case_id}")

            base_result = results_by_id[case_id]
            base_error = (base_result.get("actual") or {}).get("error")
            if not base_error:
                raise ValueError(
                    f"Từ chối thay {case_id}: lượt base không có lỗi hạ tầng; "
                    "không được cherry-pick lỗi nghiệp vụ."
                )

            replacement = copy.deepcopy(retry_result)
            replacement["execution_model"] = retry_model
            replacement["source_run"] = str(retry_path.relative_to(ROOT_DIR))
            replacement["retried_after_error"] = True
            results_by_id[case_id] = replacement
            retry_audit.append(
                {
                    "case_id": case_id,
                    "base_error": str(base_error),
                    "retry_model": retry_model,
                    "retry_file": str(retry_path.relative_to(ROOT_DIR)),
                }
            )

    primary_model = base.get("metadata", {}).get("model", "unknown")
    ordered_results: List[Dict[str, Any]] = []
    for base_result in base["results"]:
        result = results_by_id[base_result["case_id"]]
        result.setdefault("execution_model", primary_model)
        result.setdefault("source_run", str(base_path.relative_to(ROOT_DIR)))
        result.setdefault("retried_after_error", False)

        messages = result.get("input", {}).get("messages", [])
        current_items = result.get("actual", {}).get("items", [])
        actual = {"items": post_process_evidence(current_items, messages)}
        result["actual"] = actual
        result["error"] = None
        result["metrics"] = evaluate_case(
            {"expected": result.get("expected", {}), "input": result.get("input", {})},
            actual,
        )
        ordered_results.append(result)

    passed = sum(result["metrics"]["passed"] for result in ordered_results)
    total = len(ordered_results)
    models_used = sorted({result["execution_model"] for result in ordered_results})
    output = {
        "metadata": {
            "run_type": "consolidated_infrastructure_retries",
            "base_run": str(base_path.relative_to(ROOT_DIR)),
            "primary_model": primary_model,
            "models_used": models_used,
            "total_cases": total,
            "passed_cases": passed,
            "failed_cases": total - passed,
            "pass_rate": round(100 * passed / total, 2) if total else 0.0,
            "group_stats": group_stats(ordered_results),
            "criteria_fails": criteria_fails(ordered_results),
            "retry_policy": "Chỉ thay case mà base actual.error khác null; chấm lại toàn bộ bằng post-process hiện tại.",
            "retry_audit": retry_audit,
        },
        "results": ordered_results,
    }

    output_path = ROOT_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)

    print(f"Kết quả: {passed}/{total} = {output['metadata']['pass_rate']}%")
    print(f"Models: {', '.join(models_used)}")
    print(f"Retry do lỗi hạ tầng: {', '.join(x['case_id'] for x in retry_audit)}")
    print(f"Đã ghi: {output_path}")


if __name__ == "__main__":
    main()
