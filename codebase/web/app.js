// Actionable Digest — UI phía trình duyệt.
// Gọi AI thật qua server nội bộ (POST /api/extract), không bao giờ chạm API key trực tiếp.

const state = {
  messages: [],       // toàn bộ tin nhắn mẫu tải từ /api/demo-messages
  now: '',
  channels: [],        // danh sách channel duy nhất, suy ra từ messages
  selectedChannels: new Set(),
  items: [],           // kết quả items gần nhất từ /api/extract
  dismissed: new Set(),
  edited: {},          // index -> { title, due } sau khi người dùng sửa tay
  typeFilter: 'ALL',
};

function msgById(msgId) {
  return state.messages.find(m => m.msg_id === msgId);
}

async function loadDemoMessages() {
  const res = await fetch('/api/demo-messages');
  const data = await res.json();
  state.messages = data.messages || [];
  state.now = data.now || '';
  state.channels = [...new Set(state.messages.map(m => m.channel))].sort();
  state.selectedChannels = new Set(state.channels);
  renderChannelChips();
  updateChannelSummary();
}

function renderChannelChips() {
  const grid = document.getElementById('channel-grid');
  grid.innerHTML = '';
  state.channels.forEach(ch => {
    const count = state.messages.filter(m => m.channel === ch).length;
    const label = document.createElement('label');
    label.className = 'channel-chip selected';
    label.id = `chip-${ch}`;
    label.innerHTML = `
      <div class="channel-info">
        <span class="channel-name">#${ch}</span>
        <span class="channel-desc">${count} tin nhắn mẫu</span>
      </div>
      <input type="checkbox" class="channel-checkbox" value="${ch}" checked>
    `;
    label.querySelector('input').addEventListener('change', updateChannelFilter);
    grid.appendChild(label);
  });
}

function updateChannelFilter() {
  const checkboxes = document.querySelectorAll('.channel-checkbox');
  const selected = new Set();
  checkboxes.forEach(cb => {
    const chip = document.getElementById(`chip-${cb.value}`);
    if (cb.checked) {
      selected.add(cb.value);
      chip.classList.add('selected');
    } else {
      chip.classList.remove('selected');
    }
  });
  state.selectedChannels = selected;
  updateChannelSummary();
  renderCards();
}

function updateChannelSummary() {
  document.getElementById('active-channel-count').innerText = `${state.selectedChannels.size} kênh`;
  document.getElementById('scan-summary').innerText =
    `Đang duyệt thông báo từ ${state.selectedChannels.size}/${state.channels.length} kênh đã chọn`;
}

function toggleChannelPanel() {
  const panel = document.getElementById('channel-panel');
  panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function filterType(type, btnElement) {
  state.typeFilter = type;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btnElement.classList.add('active');
  renderCards();
}

function cardTypeToBadgeClass(type) {
  return { DEADLINE: 'badge-deadline', TASK: 'badge-task', SCHEDULE: 'badge-sched' }[type] || 'badge-task';
}

function cardTypeToLabel(type) {
  return { DEADLINE: '🚨 Deadline', TASK: '📋 Task', SCHEDULE: '📍 Đổi Phòng / Địa điểm' }[type] || type;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str == null ? '' : String(str);
  return div.innerHTML;
}

function visibleItemsForFilter() {
  return state.items
    .map((item, index) => ({ item, index }))
    .filter(({ item, index }) => {
      if (state.dismissed.has(index)) return false;
      const msg = msgById(item.evidence && item.evidence.msg_id);
      const channel = msg ? msg.channel : '';
      if (!state.selectedChannels.has(channel)) return false;
      if (state.typeFilter !== 'ALL' && item.type !== state.typeFilter) return false;
      return true;
    });
}

function renderCards() {
  const wrapper = document.getElementById('ai-cards');
  wrapper.innerHTML = '';
  const visible = visibleItemsForFilter();

  visible.forEach(({ item, index }) => {
    const overrides = state.edited[index] || {};
    const title = overrides.title !== undefined ? overrides.title : item.title;
    const due = overrides.due !== undefined ? overrides.due : item.due;
    const msg = msgById(item.evidence && item.evidence.msg_id);
    const channel = msg ? msg.channel : '';

    const el = document.createElement('div');
    el.className = 'action-card';
    el.id = `card-${index}`;
    el.dataset.channel = channel;
    el.dataset.type = item.type;

    const confClass = item.confidence === 'high' ? 'conf-high' : 'conf-low';
    const confLabel = item.confidence === 'high' ? '✓ Độ tin cậy cao' : '⚠️ Cần kiểm tra lại';
    const dueLabel = due ? escapeHtml(due) : 'Chưa xác định';
    const locationLine = item.location
      ? `<div class="meta-time"><span>📍</span><span>${escapeHtml(item.location)}</span></div>` : '';
    const reviewLine = item.review_reason
      ? `<div class="review-reason">⚠️ ${escapeHtml(item.review_reason)}</div>` : '';

    el.innerHTML = `
      <div class="card-top">
        <div class="tags-group">
          <span class="badge-type ${cardTypeToBadgeClass(item.type)}">${escapeHtml(cardTypeToLabel(item.type))}</span>
          <span class="badge-confidence ${confClass}">${confLabel}</span>
        </div>
        <div class="channel-source"><span>#${escapeHtml(channel)}</span></div>
      </div>
      <div class="card-content">
        <h3 id="title-${index}">${escapeHtml(title)}</h3>
        <div class="meta-time"><span>⏰ Hạn:</span><span class="highlight" id="due-${index}">${dueLabel}</span></div>
        ${locationLine}
        ${reviewLine}
        <div class="source-box">
          <div class="source-label"><span>Căn cứ xác minh — msg_id: ${escapeHtml(item.evidence && item.evidence.msg_id)}</span></div>
          <div class="source-quote">"${escapeHtml(item.evidence && item.evidence.quote)}"</div>
        </div>
        <div class="edit-inline" id="edit-box-${index}">
          <div class="edit-inputs">
            <input type="text" class="edit-input" id="input-title-${index}" value="${escapeHtml(title)}">
            <input type="text" class="edit-input" id="input-due-${index}" value="${escapeHtml(due || '')}">
          </div>
          <button class="btn btn-confirm" style="padding: 4px 10px; font-size: 11px;" onclick="saveEdit(${index})">Lưu thay đổi</button>
        </div>
      </div>
      <div class="card-actions">
        <div class="action-feedback" id="feedback-${index}">✓ Đã xác nhận & thêm vào lịch</div>
        <div class="btn-group" id="actions-${index}">
          <button class="btn btn-confirm" onclick="verifyCard(${index})">✓ Xác nhận vào Lịch</button>
          <button class="btn btn-edit" onclick="toggleEdit(${index})">✎ Sửa</button>
          <button class="btn btn-dismiss" onclick="dismissCard(${index})">✕ Bỏ qua</button>
        </div>
      </div>
    `;
    wrapper.appendChild(el);
  });

  document.getElementById('empty-state').style.display =
    (state.items.length > 0 && visible.length === 0) ? 'block' : 'none';
  updateTabCounts();
}

function updateTabCounts() {
  const all = state.items
    .map((item, index) => ({ item, index }))
    .filter(({ index }) => !state.dismissed.has(index))
    .filter(({ item }) => {
      const msg = msgById(item.evidence && item.evidence.msg_id);
      return state.selectedChannels.has(msg ? msg.channel : '');
    });

  document.getElementById('count-all').innerText = all.length;
  document.getElementById('count-dl').innerText = all.filter(({ item }) => item.type === 'DEADLINE').length;
  document.getElementById('count-sched').innerText = all.filter(({ item }) => item.type === 'SCHEDULE').length;
  document.getElementById('count-task').innerText = all.filter(({ item }) => item.type === 'TASK').length;
}

// Bug đã biết #1 (CP3_TASKS.md 4.6a): xác nhận phải dùng giá trị ĐÃ SỬA, đọc trực tiếp
// từ DOM hiện tại thay vì baked-in tại thời điểm render.
function verifyCard(index) {
  const card = document.getElementById(`card-${index}`);
  const feedback = document.getElementById(`feedback-${index}`);
  const actions = document.getElementById(`actions-${index}`);
  const title = document.getElementById(`title-${index}`).innerText;
  const due = document.getElementById(`due-${index}`).innerText;

  card.classList.add('status-verified');
  feedback.style.display = 'flex';
  actions.style.display = 'none';

  addEventToTimeline(title, due);
}

function dismissCard(index) {
  state.dismissed.add(index);
  renderCards();
}

function toggleEdit(index) {
  document.getElementById(`edit-box-${index}`).classList.toggle('active');
}

function saveEdit(index) {
  const title = document.getElementById(`input-title-${index}`).value;
  const due = document.getElementById(`input-due-${index}`).value;
  state.edited[index] = { title, due };
  document.getElementById(`title-${index}`).innerText = title;
  document.getElementById(`due-${index}`).innerText = due || 'Chưa xác định';
  toggleEdit(index);
}

function openCalendarModal() {
  document.getElementById('calendar-modal').classList.add('active');
}

function closeCalendarModal() {
  document.getElementById('calendar-modal').classList.remove('active');
}

function handleModalBgClick(event) {
  if (event.target.id === 'calendar-modal') closeCalendarModal();
}

function addEventToTimeline(title, time) {
  const timeline = document.getElementById('timeline-list');
  const newItem = document.createElement('div');
  newItem.className = 'timeline-item';
  newItem.innerHTML = `
    <div class="timeline-dot"></div>
    <div class="timeline-content">
      <div class="timeline-time">${escapeHtml(time)} (Vừa xác nhận)</div>
      <div class="timeline-title">${escapeHtml(title)}</div>
      <div class="timeline-desc">Đã được người dùng phê duyệt từ bản tin Discord.</div>
    </div>
  `;
  timeline.insertBefore(newItem, timeline.firstChild);
}

function logTechCall(entry) {
  const panel = document.getElementById('tech-log-content');
  const time = new Date().toLocaleTimeString('vi-VN');
  const statusLine = entry.ok === false ? `❌ HTTP ${entry.status}` : `✅ HTTP ${entry.status}`;
  panel.textContent = `[${time}] ${statusLine}\n\n${JSON.stringify(entry.body, null, 2)}`;
  document.getElementById('tech-log-panel').open = true;
}

function showError(message) {
  const banner = document.getElementById('error-banner');
  banner.textContent = `⚠️ ${message}`;
  banner.style.display = 'block';
}

function hideError() {
  document.getElementById('error-banner').style.display = 'none';
}

async function runScan() {
  const status = document.getElementById('scan-status');
  const loading = document.getElementById('loading-state');
  const emptyState = document.getElementById('empty-state');
  hideError();

  const messages = state.messages.filter(m => state.selectedChannels.has(m.channel));
  if (messages.length === 0) {
    state.items = [];
    document.getElementById('ai-cards').innerHTML = '';
    emptyState.style.display = 'block';
    status.textContent = 'Không có tin nào trong các kênh đã chọn — chưa gọi AI.';
    updateTabCounts();
    return;
  }

  document.getElementById('btn-scan').disabled = true;
  loading.style.display = 'block';
  emptyState.style.display = 'none';
  document.getElementById('ai-cards').innerHTML = '';
  status.textContent = 'Đang gọi AI…';

  try {
    const res = await fetch('/api/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ now: state.now, messages }),
    });
    const body = await res.json();
    logTechCall({ ok: res.ok, status: res.status, body });

    if (!res.ok || body.error) {
      throw new Error(body.error || `HTTP ${res.status}`);
    }

    state.items = body.items || [];
    state.dismissed = new Set();
    state.edited = {};
    status.textContent = `Xong — ${state.items.length} việc cần làm từ ${messages.length} tin.`;
    renderCards();
  } catch (e) {
    showError(`Lỗi gọi AI: ${e.message}`);
    status.textContent = 'Gọi AI thất bại.';
    emptyState.style.display = 'block';
  } finally {
    loading.style.display = 'none';
    document.getElementById('btn-scan').disabled = false;
  }
}

loadDemoMessages();
