const chatWindow = document.getElementById('chat-window');
const chatBackdrop = document.getElementById('chat-backdrop');
const iconOpen = document.getElementById('chat-icon-open');
const iconClose = document.getElementById('chat-icon-close');
const chatNotif = document.getElementById('chat-notif');
let isOpen = false;

function toggleChat() {
  isOpen ? closeChat() : openChat();
}

function openChat() {
  isOpen = true;
  // Hide teaser pop when chat opens
  const teaser = document.getElementById('chat-teaser');
  if (teaser) teaser.style.display = 'none';

  chatWindow.classList.add('open');
  chatBackdrop.style.display = 'block';
  iconOpen.style.display = 'none';
  iconClose.style.display = '';
  chatNotif.style.display = 'none';
}

function closeChat() {
  isOpen = false;
  chatWindow.classList.remove('open');
  chatBackdrop.style.display = 'none';
  iconOpen.style.display = '';
  iconClose.style.display = 'none';
}

function addMsg(html, isUser) {
  const msgs = document.getElementById('chat-messages');
  const d = document.createElement('div');
  d.style.cssText = 'opacity:0;transform:translateY(8px);transition:opacity .25s,transform .25s;';

  if (isUser) {
    d.style.cssText += 'display:flex;justify-content:flex-end;';
    d.innerHTML = `<div style="background:var(--g);color:#fff;border-radius:16px 16px 4px 16px;padding:9px 12px;font-size:.81rem;line-height:1.55;max-width:220px;">${html}</div>`;
  } else {
    d.style.cssText += 'display:flex;gap:8px;align-items:flex-end;';
    d.innerHTML = `
      <div class="bot-av-wrap">
        <div class="bot-av">🤖</div>
        <span class="bot-av-wave">👋</span>
      </div>
      <div style="background:#fff;border:1px solid var(--bd);border-radius:16px 16px 16px 4px;padding:9px 12px;font-size:.81rem;color:var(--tx);line-height:1.55;max-width:220px;box-shadow:0 1px 3px rgba(0,0,0,.06);">${html}</div>`;
  }

  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
  requestAnimationFrame(() => {
    d.style.opacity = '1';
    d.style.transform = 'translateY(0)';
  });
}

function addTyping() {
  const msgs = document.getElementById('chat-messages');
  const d = document.createElement('div');
  d.id = 'typing-indicator';
  d.style.cssText = 'display:flex;gap:8px;align-items:flex-end;opacity:0;transform:translateY(8px);transition:opacity .2s,transform .2s;';
  d.innerHTML = `
    <div class="bot-av-wrap">
      <div class="bot-av">🤖</div>
    </div>
    <div style="background:#fff;border:1px solid var(--bd);border-radius:16px 16px 16px 4px;padding:10px 14px;display:flex;gap:5px;align-items:center;box-shadow:0 1px 3px rgba(0,0,0,.06);">
      <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
    </div>`;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
  requestAnimationFrame(() => {
    d.style.opacity = '1';
    d.style.transform = 'translateY(0)';
  });
}

function sendQuick(q) {
  document.getElementById('chat-input').value = q;
  sendMsg();
}

async function sendMsg() {
  const input = document.getElementById('chat-input');
  const message = input.value.trim();
  if (!message) return;

  addMsg(message, true);
  input.value = '';
  addTyping();

  try {
    const response = await fetch('/chatbot/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    document.getElementById('typing-indicator')?.remove();
    addMsg(data.reply, false);
  } catch (e) {
    document.getElementById('typing-indicator')?.remove();
    addMsg('Server error. Please try again.', false);
  }
}

function getCookie(name) {
  let value = null;
  if (document.cookie) {
    document.cookie.split(';').forEach(c => {
      c = c.trim();
      if (c.startsWith(name + '=')) value = decodeURIComponent(c.slice(name.length + 1));
    });
  }
  return value;
}

// Auto-hide teaser after 6 seconds
setTimeout(() => {
  const teaser = document.getElementById('chat-teaser');
  if (teaser) {
    teaser.style.transition = 'opacity .4s, transform .4s';
    teaser.style.opacity = '0';
    teaser.style.transform = 'translateY(8px) scale(.96)';
    setTimeout(() => teaser.style.display = 'none', 400);
  }
}, 6000);