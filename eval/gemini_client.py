import json
import urllib.request
import urllib.error

CARD_TYPES = {"NONE", "DEADLINE", "TASK", "SCHED"}
REQUIRED_FIELDS = ["type", "title", "deadline_text", "confidence", "quote", "msg_id", "escalate", "reason"]


def filter_messages_by_channel(messages, selected_channels):
    return [m for m in messages if m["channel"] in selected_channels]


def build_prompt(prompt_template, messages):
    blocks = []
    for m in messages:
        blocks.append(
            f"[msg_id={m['msg_id']}] [channel={m['channel']}] "
            f"[author_role={m['author_role']}] [time={m['created_at_vn']}]\n{m['content']}"
        )
    messages_block = "\n---\n".join(blocks)
    return (
        f"{prompt_template}\n\n## TIN NHẮN CẦN PHÂN LOẠI\n{messages_block}\n\n"
        "Trả lời DUY NHẤT bằng một mảng JSON hợp lệ, không thêm chữ nào khác."
    )


def parse_response(raw_response_text):
    """Parse phản hồi dạng OpenAI chat-completions: {"choices": [{"message": {"content": "..."}}]}.
    Chuẩn này dùng chung cho mọi provider OpenAI-compatible (OpenAI, Groq, router nội bộ, Gemini
    qua endpoint .../v1beta/openai/, v.v.) — không còn khoá riêng vào schema gốc của Gemini."""
    try:
        envelope = json.loads(raw_response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Không parse được response bao ngoài của model: {e}")

    try:
        text = envelope["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise ValueError("Response thiếu choices[0].message.content")

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Model không trả JSON hợp lệ trong text: nội dung rỗng")

    try:
        cards = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model không trả JSON hợp lệ trong text: {e}")

    if not isinstance(cards, list):
        raise ValueError("Model phải trả về một mảng card, kể cả khi rỗng")

    for i, card in enumerate(cards):
        for field in REQUIRED_FIELDS:
            if field not in card:
                raise ValueError(f'Card #{i} thiếu field bắt buộc "{field}"')
        if card["type"] not in CARD_TYPES:
            raise ValueError(f"Card #{i} có type không hợp lệ: {card['type']}")

    return cards


def call_llm(prompt_text, api_key, base_url, model):
    """Gọi bất kỳ endpoint nào tương thích chuẩn OpenAI chat-completions
    (POST {base_url}/chat/completions, header Authorization: Bearer <key>).
    base_url không có dấu "/" ở cuối, ví dụ: "https://api.openai.com/v1" hoặc
    "http://localhost:20128/v1"."""
    url = f"{base_url.rstrip('/')}/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt_text}],
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"LLM API lỗi {e.code}: {e.read().decode('utf-8')}")
