const test = require('node:test');
const assert = require('node:assert/strict');
const { filterMessagesByChannel, buildPrompt, parseGeminiResponse, classifyMessages } = require('./ai-client.js');

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
    choices: [{ message: { content: JSON.stringify([
      { type: 'TASK', title: 'x', deadline_text: '', confidence: 'high', quote: 'q', msg_id: 'M1', escalate: false, reason: 'r' }
    ]) } }]
  });
  const cards = parseGeminiResponse(raw);
  assert.equal(cards.length, 1);
  assert.equal(cards[0].type, 'TASK');
});

test('parseGeminiResponse accepts empty array', () => {
  const raw = JSON.stringify({ choices: [{ message: { content: '[]' } }] });
  assert.deepEqual(parseGeminiResponse(raw), []);
});

test('parseGeminiResponse throws on missing field', () => {
  const raw = JSON.stringify({ choices: [{ message: { content: JSON.stringify([{ type: 'TASK' }]) } }] });
  assert.throws(() => parseGeminiResponse(raw), /thiếu field/);
});

test('parseGeminiResponse throws on invalid type', () => {
  const raw = JSON.stringify({
    choices: [{ message: { content: JSON.stringify([
      { type: 'BOGUS', title: 'x', deadline_text: '', confidence: 'high', quote: 'q', msg_id: 'M1', escalate: false, reason: 'r' }
    ]) } }]
  });
  assert.throws(() => parseGeminiResponse(raw), /type không hợp lệ/);
});

test('parseGeminiResponse throws on empty content', () => {
  const raw = JSON.stringify({ choices: [{ message: { content: '' } }] });
  assert.throws(() => parseGeminiResponse(raw), /rỗng/);
});

test('classifyMessages invokes onLog with prompt and raw response on success', async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => ({
    ok: true,
    status: 200,
    text: async () => JSON.stringify({ choices: [{ message: { content: '[]' } }] }),
  });
  try {
    const logs = [];
    const cards = await classifyMessages([], 'key', 'RULES', 'http://x/v1', 'model', (entry) => logs.push(entry));
    assert.deepEqual(cards, []);
    assert.equal(logs.length, 1);
    assert.ok(logs[0].prompt.includes('RULES'));
    assert.ok(logs[0].rawResponse.includes('choices'));
    assert.equal(logs[0].ok, true);
    assert.equal(logs[0].status, 200);
  } finally {
    global.fetch = originalFetch;
  }
});

test('classifyMessages invokes onLog even when the API call fails', async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => ({ ok: false, status: 500, text: async () => 'boom' });
  try {
    const logs = [];
    await assert.rejects(
      () => classifyMessages([], 'key', 'RULES', 'http://x/v1', 'model', (entry) => logs.push(entry)),
      /LLM API lỗi 500/
    );
    assert.equal(logs.length, 1);
    assert.equal(logs[0].ok, false);
    assert.equal(logs[0].status, 500);
    assert.equal(logs[0].rawResponse, 'boom');
  } finally {
    global.fetch = originalFetch;
  }
});

test('classifyMessages works without onLog (backward compatible)', async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => ({
    ok: true,
    status: 200,
    text: async () => JSON.stringify({ choices: [{ message: { content: '[]' } }] }),
  });
  try {
    const cards = await classifyMessages([], 'key', 'RULES', 'http://x/v1', 'model');
    assert.deepEqual(cards, []);
  } finally {
    global.fetch = originalFetch;
  }
});
