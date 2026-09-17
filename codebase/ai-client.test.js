const test = require('node:test');
const assert = require('node:assert/strict');
const { filterMessagesByChannel, buildPrompt, parseGeminiResponse } = require('./ai-client.js');

test('filterMessagesByChannel keeps only selected channels', () => {
  const messages = [
    { msg_id: 'M1', channel: 'general', content: 'a' },
    { msg_id: 'M2', channel: 'random', content: 'b' },
  ];
  const result = filterMessagesByChannel(messages, ['general']);
  assert.deepEqual(result.map(m => m.msg_id), ['M1']);
});

test('buildPrompt embeds message fields and instructs JSON-only output', () => {
  const prompt = buildPrompt('RULES', [{
    msg_id: 'M1', channel: 'general', author_role: 'hoc_vien',
    created_at_vn: '2026-09-12 10:00', content: 'Hạn nộp Lab02',
  }]);
  assert.ok(prompt.includes('RULES'));
  assert.ok(prompt.includes('msg_id=M1'));
  assert.ok(prompt.includes('Hạn nộp Lab02'));
  assert.ok(prompt.includes('mảng JSON'));
});

test('parseGeminiResponse extracts and validates cards array', () => {
  const raw = JSON.stringify({
    candidates: [{ content: { parts: [{ text: JSON.stringify([
      { type: 'TASK', title: 'x', deadline_text: '', confidence: 'high', quote: 'q', msg_id: 'M1', escalate: false, reason: 'r' }
    ]) }] } }]
  });
  const cards = parseGeminiResponse(raw);
  assert.equal(cards.length, 1);
  assert.equal(cards[0].type, 'TASK');
});

test('parseGeminiResponse accepts empty array', () => {
  const raw = JSON.stringify({ candidates: [{ content: { parts: [{ text: '[]' }] } }] });
  assert.deepEqual(parseGeminiResponse(raw), []);
});

test('parseGeminiResponse throws on missing field', () => {
  const raw = JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify([{ type: 'TASK' }]) }] } }] });
  assert.throws(() => parseGeminiResponse(raw), /thiếu field/);
});

test('parseGeminiResponse throws on invalid type', () => {
  const raw = JSON.stringify({
    candidates: [{ content: { parts: [{ text: JSON.stringify([
      { type: 'BOGUS', title: 'x', deadline_text: '', confidence: 'high', quote: 'q', msg_id: 'M1', escalate: false, reason: 'r' }
    ]) }] } }]
  });
  assert.throws(() => parseGeminiResponse(raw), /type không hợp lệ/);
});
