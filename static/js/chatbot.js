// ============================================================
// chatbot.js — Floating Chatbot Widget
// ============================================================

const chatToggle  = document.getElementById('chatToggle');
const chatToggleIcon = document.getElementById('chatToggleIcon');
const chatWindow  = document.getElementById('chatWindow');
const chatClose   = document.getElementById('chatClose');
const chatMessages = document.getElementById('chatMessages');
const chatInput   = document.getElementById('chatInput');
const chatSend    = document.getElementById('chatSend');
const suggestions = document.getElementById('suggestions');

let history = [];        // [{role:'user'|'assistant', content:'...'}]
let isOpen  = false;

// ── Toggle open/close ─────────────────────────────────────────
function openChat() {
  chatWindow.style.display = 'flex';
  chatToggleIcon.textContent = '✕';
  isOpen = true;
  chatInput.focus();
}
function closeChat() {
  chatWindow.style.display = 'none';
  chatToggleIcon.textContent = '💬';
  isOpen = false;
}

chatToggle.addEventListener('click', () => isOpen ? closeChat() : openChat());
chatClose.addEventListener('click', closeChat);

// Keyboard shortcut: Ctrl+/
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === '/') { e.preventDefault(); isOpen ? closeChat() : openChat(); }
});

// ── Send message ──────────────────────────────────────────────
chatSend.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});

async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  chatInput.value = '';
  hideSuggestions();
  appendMessage('user', text);
  history.push({ role: 'user', content: text });

  // Typing indicator
  const typingEl = appendTyping();

  try {
    const res  = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, history })
    });
    const data = await res.json();
    typingEl.remove();

    const reply = data.reply || 'Sorry, I could not process that.';
    appendMessage('bot', reply);
    history.push({ role: 'assistant', content: reply });

    // Keep history to last 20 messages to avoid large payloads
    if (history.length > 20) history = history.slice(-20);

  } catch (err) {
    typingEl.remove();
    appendMessage('bot', '⚠️ Connection error. Please check your internet and try again.');
  }
}

// Suggestion chips
function sendSuggestion(btn) {
  chatInput.value = btn.textContent;
  sendMessage();
}

function hideSuggestions() {
  if (suggestions) suggestions.style.display = 'none';
}

// ── DOM helpers ───────────────────────────────────────────────
function appendMessage(role, text) {
  const wrap = document.createElement('div');
  wrap.className = `chat-msg ${role}`;

  // Simple markdown: **bold**, bullet lines starting with -
  const formatted = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n- /g, '<br>• ')
    .replace(/\n/g, '<br>');

  wrap.innerHTML = `
    ${role === 'bot' ? '<span class="msg-avatar">🌿</span>' : ''}
    <div class="msg-bubble">${formatted}</div>
  `;
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return wrap;
}

function appendTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'chat-msg bot chat-typing';
  wrap.innerHTML = `
    <span class="msg-avatar">🌿</span>
    <div class="msg-bubble">Thinking…</div>
  `;
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return wrap;
}
