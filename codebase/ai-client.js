const CARD_TYPES = ['NONE', 'DEADLINE', 'TASK', 'SCHED'];
const REQUIRED_FIELDS = ['type', 'title', 'deadline_text', 'confidence', 'quote', 'msg_id', 'escalate', 'reason'];

function filterMessagesByChannel(messages, selectedChannels) {
  return messages.filter(m => selectedChannels.includes(m.channel));
}

function buildPrompt(promptTemplate, messages) {
  const messagesBlock = messages.map(m =>
    `[msg_id=${m.msg_id}] [channel=${m.channel}] [author_role=${m.author_role}] [time=${m.created_at_vn}]\n${m.content}`
  ).join('\n---\n');
  return `${promptTemplate}\n\n## TIN NHẮN CẦN PHÂN LOẠI\n${messagesBlock}\n\nTrả lời DUY NHẤT bằng một mảng JSON hợp lệ, không thêm chữ nào khác.`;
}

function parseGeminiResponse(rawResponseText) {
  // Parse phản hồi dạng OpenAI chat-completions: {choices: [{message: {content: "..."}}]}.
  // Chuẩn này dùng chung cho mọi provider OpenAI-compatible (OpenAI, Groq, router nội bộ,
  // Gemini qua endpoint .../v1beta/openai/, v.v.) — không còn khoá riêng vào schema gốc của Gemini.
  let envelope;
  try {
    envelope = JSON.parse(rawResponseText);
  } catch (e) {
    throw new Error(`Không parse được response bao ngoài của model: ${e.message}`);
  }
  const text = envelope && envelope.choices && envelope.choices[0] &&
    envelope.choices[0].message && envelope.choices[0].message.content;
  if (typeof text !== 'string' || text.trim() === '') {
    throw new Error('Model không trả JSON hợp lệ trong text: nội dung rỗng');
  }
  let cards;
  try {
    cards = JSON.parse(text);
  } catch (e) {
    throw new Error(`Model không trả JSON hợp lệ trong text: ${e.message}`);
  }
  if (!Array.isArray(cards)) {
    throw new Error('Model phải trả về một mảng card, kể cả khi rỗng');
  }
  cards.forEach((card, i) => {
    if (typeof card !== 'object' || card === null) {
      throw new Error(`Card #${i} không phải object hợp lệ`);
    }
    for (const field of REQUIRED_FIELDS) {
      if (!(field in card)) {
        throw new Error(`Card #${i} thiếu field bắt buộc "${field}"`);
      }
    }
    if (!CARD_TYPES.includes(card.type)) {
      throw new Error(`Card #${i} có type không hợp lệ: ${card.type}`);
    }
  });
  return cards;
}

async function classifyMessages(messages, apiKey, promptTemplate, baseUrl, model, onLog) {
  // onLog(entry) là cơ chế ghi vết: được gọi với {prompt, rawResponse, ok, status} sau MỌI lệnh
  // gọi (thành công lẫn thất bại) — phục vụ xác minh kỹ thuật trực tiếp trên giao diện demo.
  const prompt = buildPrompt(promptTemplate, messages);
  const url = `${baseUrl.replace(/\/$/, '')}/chat/completions`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [{ role: 'user', content: prompt }],
      stream: false,
    }),
  });
  const rawText = await response.text();
  if (onLog) {
    onLog({ prompt, rawResponse: rawText, ok: response.ok, status: response.status });
  }
  if (!response.ok) {
    throw new Error(`LLM API lỗi ${response.status}: ${rawText}`);
  }
  return parseGeminiResponse(rawText);
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { filterMessagesByChannel, buildPrompt, parseGeminiResponse, classifyMessages, CARD_TYPES };
}
