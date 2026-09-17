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
    try:
        envelope = json.loads(raw_response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Không parse được response bao ngoài của Gemini: {e}")

    try:
        text = envelope["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise ValueError("Response Gemini thiếu candidates[0].content.parts[0].text")

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


def call_gemini(prompt_text, api_key, model="gemini-2.0-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt_text}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Gemini API lỗi {e.code}: {e.read().decode('utf-8')}")
