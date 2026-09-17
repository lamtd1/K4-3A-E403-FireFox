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
  let envelope;
  try {
    envelope = JSON.parse(rawResponseText);
  } catch (e) {
    throw new Error(`Không parse được response bao ngoài của Gemini: ${e.message}`);
  }
  const text = envelope && envelope.candidates && envelope.candidates[0] &&
    envelope.candidates[0].content && envelope.candidates[0].content.parts &&
    envelope.candidates[0].content.parts[0] && envelope.candidates[0].content.parts[0].text;
  if (typeof text !== 'string') {
    throw new Error('Response Gemini thiếu candidates[0].content.parts[0].text');
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

async function classifyMessages(messages, apiKey, promptTemplate) {
  const prompt = buildPrompt(promptTemplate, messages);
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=${apiKey}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
  });
  const rawText = await response.text();
  if (!response.ok) {
    throw new Error(`Gemini API lỗi ${response.status}: ${rawText}`);
  }
  return parseGeminiResponse(rawText);
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { filterMessagesByChannel, buildPrompt, parseGeminiResponse, classifyMessages, CARD_TYPES };
}
