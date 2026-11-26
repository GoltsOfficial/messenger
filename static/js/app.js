/**
 * Messenger frontend
 * POST /auth/register (JSON), POST /auth/login (form)
 * GET /users, GET /users/me
 * GET/POST /chats, GET/POST /chats/{id}/messages
 */

const API = "";

const state = {
  token: localStorage.getItem("token") || null,
  username: localStorage.getItem("username") || null,
  userId: Number(localStorage.getItem("userId")) || null,
  mode: "login",
  chats: [],
  users: [],
  currentChatId: null,
  messages: [],
  pollTimer: null,
};

const $ = (sel) => document.querySelector(sel);

const authScreen = $("#auth-screen");
const appScreen = $("#app-screen");
const authForm = $("#auth-form");
const authError = $("#auth-error");
const authSubmit = $("#auth-submit");
const usernameInput = $("#username");
const passwordInput = $("#password");
const userNameEl = $("#user-name");
const logoutBtn = $("#logout-btn");
const chatList = $("#chat-list");
const chatsEmpty = $("#chats-empty");
const noChat = $("#no-chat");
const chatView = $("#chat-view");
const chatTitle = $("#chat-title");
const messagesEl = $("#messages");
const sendForm = $("#send-form");
const messageInput = $("#message-input");
const newChatBtn = $("#new-chat-btn");
const modal = $("#modal");
const newChatForm = $("#new-chat-form");
const chatNameInput = $("#chat-name");
const usersChecklist = $("#users-checklist");
const modalError = $("#modal-error");
const modalCancel = $("#modal-cancel");

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof URLSearchParams)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }
  if (state.token) {
    headers["Authorization"] = `Bearer ${state.token}`;
  }

  const res = await fetch(`${API}${path}`, { ...options, headers });

  if (res.status === 204) return null;

  let data = null;
  const text = await res.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { detail: text };
    }
  }

  if (!res.ok) {
    const msg =
      (data && (data.detail || data.message)) || `Ошибка ${res.status}`;
    const err = new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
    err.status = res.status;
    throw err;
  }

  return data;
}

function setAuthMode(mode) {
  state.mode = mode;
  document.querySelectorAll(".tab").forEach((t) => {
    t.classList.toggle("active", t.dataset.tab === mode);
  });
  authSubmit.textContent = mode === "login" ? "Войти" : "Зарегистрироваться";
  authError.hidden = true;
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => setAuthMode(tab.dataset.tab));
});

authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  authError.hidden = true;
  authSubmit.disabled = true;

  const username = usernameInput.value.trim();
  const password = passwordInput.value;

  try {
    if (state.mode === "register") {
      await api("/auth/register", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
    }

    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);

    const tokenData = await api("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });

    state.token = tokenData.access_token;
    state.username = username;
    localStorage.setItem("token", state.token);
    localStorage.setItem("username", username);

    const me = await api("/users/me");
    state.userId = me.id;
    localStorage.setItem("userId", String(me.id));

    showApp();
  } catch (err) {
    authError.textContent = err.message || "Ошибка авторизации";
    authError.hidden = false;
  } finally {
    authSubmit.disabled = false;
  }
});

logoutBtn.addEventListener("click", () => {
  stopPolling();
  state.token = null;
  state.username = null;
  state.userId = null;
  state.chats = [];
  state.currentChatId = null;
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  localStorage.removeItem("userId");
  showAuth();
});

async function loadChats() {
  state.chats = await api("/chats");
  renderChats();
}

function renderChats() {
  chatList.innerHTML = "";
  chatsEmpty.hidden = state.chats.length > 0;

  state.chats.forEach((chat) => {
    const li = document.createElement("li");
    li.className = `chat-item${chat.id === state.currentChatId ? " active" : ""}`;
    li.innerHTML = `<div class="chat-item-name"></div>`;
    li.querySelector(".chat-item-name").textContent = chat.name;
    li.addEventListener("click", () => selectChat(chat));
    chatList.appendChild(li);
  });
}

async function selectChat(chat) {
  state.currentChatId = chat.id;
  chatTitle.textContent = chat.name;
  noChat.hidden = true;
  chatView.hidden = false;
  renderChats();
  await loadMessages();
  startPolling();
  messageInput.focus();
}

async function loadMessages() {
  if (!state.currentChatId) return;
  try {
    state.messages = await api(`/chats/${state.currentChatId}/messages?limit=100`);
    renderMessages();
  } catch (err) {
    if (err.status === 401) {
      logoutBtn.click();
    }
  }
}

function renderMessages() {
  messagesEl.innerHTML = "";
  state.messages.forEach((msg) => {
    const div = document.createElement("div");
    div.className = `message${msg.author_id === state.userId ? " mine" : ""}`;
    const time = new Date(msg.created_at).toLocaleString("ru-RU", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "2-digit",
    });
    div.innerHTML = `
      <div class="message-meta"></div>
      <div class="message-text"></div>
    `;
    div.querySelector(".message-meta").textContent = `#${msg.author_id} · ${time}`;
    div.querySelector(".message-text").textContent = msg.text;
    messagesEl.appendChild(div);
  });
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

sendForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = messageInput.value.trim();
  if (!text || !state.currentChatId) return;

  try {
    const msg = await api(`/chats/${state.currentChatId}/messages`, {
      method: "POST",
      body: JSON.stringify({ text }),
    });
    state.messages.push(msg);
    renderMessages();
    messageInput.value = "";
    messageInput.focus();
  } catch (err) {
    alert(err.message || "Не удалось отправить");
  }
});

function startPolling() {
  stopPolling();
  state.pollTimer = setInterval(loadMessages, 3000);
}

function stopPolling() {
  if (state.pollTimer) {
    clearInterval(state.pollTimer);
    state.pollTimer = null;
  }
}

newChatBtn.addEventListener("click", async () => {
  modalError.hidden = true;
  chatNameInput.value = "";
  usersChecklist.innerHTML = "<p class=\"empty-state small\">Загрузка…</p>";
  modal.hidden = false;

  try {
    state.users = await api("/users");
    usersChecklist.innerHTML = "";
    state.users
      .filter((u) => u.id !== state.userId)
      .forEach((u) => {
        const label = document.createElement("label");
        label.className = "user-check";
        label.innerHTML = `<input type="checkbox" value="${u.id}" /> <span></span>`;
        label.querySelector("span").textContent = u.username;
        usersChecklist.appendChild(label);
      });
    if (!usersChecklist.children.length) {
      usersChecklist.innerHTML =
        "<p class=\"empty-state small\">Нет других пользователей</p>";
    }
  } catch (err) {
    usersChecklist.innerHTML = `<p class="error">${err.message}</p>`;
  }
});

modalCancel.addEventListener("click", () => {
  modal.hidden = true;
});

newChatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  modalError.hidden = true;

  const name = chatNameInput.value.trim();
  const user_ids = [...usersChecklist.querySelectorAll("input:checked")].map(
    (el) => Number(el.value)
  );

  try {
    const chat = await api("/chats", {
      method: "POST",
      body: JSON.stringify({ name, user_ids }),
    });
    modal.hidden = true;
    await loadChats();
    await selectChat(chat);
  } catch (err) {
    modalError.textContent = err.message || "Ошибка создания чата";
    modalError.hidden = false;
  }
});

function showAuth() {
  stopPolling();
  authScreen.removeAttribute("hidden");
  appScreen.setAttribute("hidden", "");
  passwordInput.value = "";
  authError.hidden = true;
}

async function showApp() {
  authScreen.setAttribute("hidden", "");
  appScreen.removeAttribute("hidden");
  userNameEl.textContent = state.username || "";
  noChat.hidden = false;
  chatView.hidden = true;
  try {
    if (!state.userId) {
      const me = await api("/users/me");
      state.userId = me.id;
      state.username = me.username;
      localStorage.setItem("userId", String(me.id));
      localStorage.setItem("username", me.username);
      userNameEl.textContent = me.username;
    }
    await loadChats();
  } catch (err) {
    if (err.status === 401) {
      logoutBtn.click();
    }
  }
}

if (state.token) {
  showApp();
} else {
  showAuth();
}
