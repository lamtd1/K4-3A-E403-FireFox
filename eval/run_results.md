# CP3 Run Results — Actionable Digest

Pass rate: 11/20 (55.0%)

| ID | Bucket | Pass | Lý do fail |
|---|---|---|---|
| GS-01 | class1 | ✅ | - |
| GS-02 | class1 | ❌ | Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0) |
| GS-03 | class2 | ✅ | - |
| GS-04 | class2 | ❌ | Không thấy type=TASK trong ['DEADLINE'] |
| GS-05 | class2 | ✅ | - |
| GS-06 | class3 | ✅ | - |
| GS-07 | class3 | ✅ | - |
| GS-08 | class4 | ✅ | - |
| GS-09 | class4 | ✅ | - |
| GS-10 | class4 | ❌ | Lỗi gọi API: Gemini API lỗi 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 33.434292646s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Learn more about Gemini API quotas",
            "url": "https://ai.google.dev/gemini-api/docs/rate-limits"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
        "violations": [
          {
            "quotaMetric": "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
            "quotaDimensions": {
              "location": "global",
              "model": "gemini-3.5-flash"
            },
            "quotaValue": "5"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "33s"
      }
    ]
  }
}
 |
| GS-11 | common | ❌ | Lỗi gọi API: Gemini API lỗi 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 33.150563136s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Learn more about Gemini API quotas",
            "url": "https://ai.google.dev/gemini-api/docs/rate-limits"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
        "violations": [
          {
            "quotaMetric": "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
            "quotaDimensions": {
              "location": "global",
              "model": "gemini-3.5-flash"
            },
            "quotaValue": "5"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "33s"
      }
    ]
  }
}
 |
| GS-12 | common | ✅ | - |
| GS-13 | common | ✅ | - |
| GS-14 | common | ❌ | Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0) |
| GS-15 | common | ❌ | Kỳ vọng NONE (0 card) nhưng có 1 card |
| GS-16 | common | ❌ | Không thấy type=DEADLINE trong ['SCHED'] |
| GS-17 | common | ❌ | Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0) |
| GS-18 | common | ✅ | - |
| GS-19 | edge | ✅ | - |
| GS-20 | edge | ❌ | Lỗi gọi API: Gemini API lỗi 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 34.658110881s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Learn more about Gemini API quotas",
            "url": "https://ai.google.dev/gemini-api/docs/rate-limits"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
        "violations": [
          {
            "quotaMetric": "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
            "quotaDimensions": {
              "location": "global",
              "model": "gemini-3.5-flash"
            },
            "quotaValue": "5"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "34s"
      }
    ]
  }
}
 |

## Phân tích nguyên nhân case sai

**Model đã đổi từ `gemini-2.0-flash` (bị khai tử, 404) sang `gemini-3.5-flash`** (xác nhận có trong danh sách model sống qua endpoint `GET /v1beta/models`, hỗ trợ `generateContent`, và đúng dòng "flash" nhanh/rẻ mà user ưu tiên). Với model thật sự trả lời, pass rate giờ là **11/20 (55%)** — con số này giờ mới thực sự phản ánh chất lượng `codebase/PROMPT.md`, khác hẳn lần chạy trước (2/20, gần như toàn bộ do lỗi hạ tầng 404).

- **GS-02**: Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0). Chẩn đoán: (c)-mở-rộng — không phải prompt sai nội dung, cũng không phải bug trong `grade_case`, mà là **field `text` rỗng** trả về từ Gemini. `gemini-3.5-flash` là model "thinking" (bật suy luận nội bộ mặc định) trong khi request hiện tại (`eval/gemini_client.py::call_gemini`, `codebase/ai-client.js::classifyMessages`) không gửi `generationConfig`/`thinkingConfig` nào — nhiều khả năng toàn bộ ngân sách output bị model dùng cho phần "thinking" ẩn, khiến `candidates[0].content.parts[0].text` rỗng. Đây là một hạn chế tích hợp thật (cần thêm `generationConfig` để tắt/giới hạn thinking), không nằm gọn trong 3 nhóm (a)/(b)/(c) — nên ghi nhận là điểm cần theo dõi riêng ở CP4, không sửa vội trong task này.
- **GS-04**: Không thấy type=TASK trong ['DEADLINE']. Chẩn đoán: (a) lỗi cách viết prompt — `codebase/PROMPT.md` không có quy tắc phân biệt rõ ràng TASK và DEADLINE khi một tin vừa có hành động ("nộp form khảo sát") vừa có cụm giờ tương đối ("trước cuối tuần này"); model hợp lý khi thấy có mốc thời gian liền coi là DEADLINE, nhưng golden set kỳ vọng TASK — cần bổ sung quy tắc phân định ranh giới 2 loại này vào PROMPT.md.
- **GS-10**: Lỗi gọi API: Gemini API lỗi 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 33.434292646s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Learn more about Gemini API quotas",
            "url": "https://ai.google.dev/gemini-api/docs/rate-limits"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
        "violations": [
          {
            "quotaMetric": "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
            "quotaDimensions": {
              "location": "global",
              "model": "gemini-3.5-flash"
            },
            "quotaValue": "5"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "33s"
      }
    ]
  }
}

  Chẩn đoán: không phải prompt, không phải `grade_case`, không phải giới hạn năng lực model — đây là **giới hạn quota free-tier** ("limit: 5, model: gemini-3.5-flash" — 5 request/phút), và `eval/run_eval.py::run_one_case` hiện gọi tuần tự không có backoff/retry khi gặp 429. Đây là một hạn chế vận hành của script eval (thiếu retry/rate-limit handling), nên tách thành cải tiến riêng cho `run_eval.py` (ngoài phạm vi task này), không phải bằng chứng về chất lượng prompt.
- **GS-11**: Lỗi gọi API: Gemini API lỗi 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 33.150563136s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Learn more about Gemini API quotas",
            "url": "https://ai.google.dev/gemini-api/docs/rate-limits"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
        "violations": [
          {
            "quotaMetric": "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
            "quotaDimensions": {
              "location": "global",
              "model": "gemini-3.5-flash"
            },
            "quotaValue": "5"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "33s"
      }
    ]
  }
}

  Chẩn đoán: cùng nguyên nhân như GS-10 — quota free-tier 5 request/phút bị vượt do gọi tuần tự không backoff trong `run_eval.py`, không liên quan prompt hay `grade_case`.
- **GS-14**: Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0). Chẩn đoán: cùng nguyên nhân với GS-02 — `text` rỗng, nghi do model "thinking" `gemini-3.5-flash` không được cấu hình `generationConfig`/`thinkingConfig` trong `eval/gemini_client.py`/`codebase/ai-client.js`; không phải lỗi nội dung prompt.
- **GS-15**: Kỳ vọng NONE (0 card) nhưng có 1 card. Chẩn đoán: (a) mâu thuẫn trong `codebase/PROMPT.md` — Quy tắc 3 vừa yêu cầu "không tạo card" vừa yêu cầu "đặt `escalate=true`", nhưng schema JSON chỉ có field `escalate` bên trong một *card*; model không có cách nào set escalate mà không tạo card, nên đã tạo 1 card để mang cờ `escalate=true`, vi phạm kỳ vọng "0 card" của golden set. Cần sửa PROMPT.md để làm rõ: hoặc vẫn tạo 1 card mang `escalate=true` (và cập nhật golden set/`grade_case` cho khớp), hoặc định nghĩa lại cách hệ thống nhận biết escalate khi không có card nào.
- **GS-16**: Không thấy type=DEADLINE trong ['SCHED']. Chẩn đoán: (a) lỗi cách viết prompt — `codebase/PROMPT.md` mô tả SCHED chỉ như "Đổi lịch-phòng" nhưng không định nghĩa rõ trường hợp tin công bố *ngày bắt đầu áp dụng một chính sách* (ở đây là ngày bắt đầu ghi nhận XP daily standup) thuộc DEADLINE hay SCHED; model chọn SCHED có thể hợp lý theo cách đọc "công bố áp dụng từ ngày X" nhưng golden set kỳ vọng DEADLINE — cần bổ sung ranh giới rõ hơn giữa DEADLINE và SCHED trong PROMPT.md.
- **GS-17**: Lỗi gọi API: Model không trả JSON hợp lệ trong text: Expecting value: line 1 column 1 (char 0). Chẩn đoán: cùng nguyên nhân với GS-02/GS-14 — `text` rỗng do thiếu cấu hình thinking cho model mới, không phải lỗi prompt hay `grade_case`.
- **GS-20**: Lỗi gọi API: Gemini API lỗi 429: {
  "error": {
    "code": 429,
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 34.658110881s.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Learn more about Gemini API quotas",
            "url": "https://ai.google.dev/gemini-api/docs/rate-limits"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.QuotaFailure",
        "violations": [
          {
            "quotaMetric": "generativelanguage.googleapis.com/generate_content_free_tier_requests",
            "quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier",
            "quotaDimensions": {
              "location": "global",
              "model": "gemini-3.5-flash"
            },
            "quotaValue": "5"
          }
        ]
      },
      {
        "@type": "type.googleapis.com/google.rpc.RetryInfo",
        "retryDelay": "34s"
      }
    ]
  }
}

  Chẩn đoán: cùng nguyên nhân như GS-10/GS-11 — quota free-tier 5 request/phút bị vượt, không liên quan prompt hay `grade_case`.

**Tóm tắt phân loại 9 case fail:** 3/9 (GS-10, GS-11, GS-20) là lỗi hạ tầng/quota (429, ngoài tầm kiểm soát của prompt); 3/9 (GS-02, GS-14, GS-17) là `text` rỗng nghi do thiếu cấu hình `thinkingConfig` cho model "thinking" mới (vấn đề tích hợp client, không phải nội dung prompt); 3/9 (GS-04, GS-15, GS-16) là vấn đề thật của `codebase/PROMPT.md` — thiếu ranh giới rõ giữa TASK/DEADLINE, mâu thuẫn nội tại ở quy tắc escalate+NONE, và thiếu ranh giới DEADLINE/SCHED cho tin "ngày bắt đầu áp dụng". Khuyến nghị follow-up (ngoài phạm vi task này): (1) thêm `generationConfig` phù hợp cho model thinking trong `eval/gemini_client.py` và `codebase/ai-client.js`; (2) thêm retry/backoff cho lỗi 429 trong `run_eval.py`; (3) sửa PROMPT.md để làm rõ ranh giới TASK/DEADLINE, DEADLINE/SCHED, và cách biểu diễn escalate khi không có card — mỗi thay đổi nên là một commit riêng có thể theo dõi, rồi chạy lại golden set.
