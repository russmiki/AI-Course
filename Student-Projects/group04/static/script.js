const ws = new WebSocket("ws://127.0.0.1:8000/ws");
let pendingFile = null;
let titleGenerated = false;

function showTyping() {
    document.getElementById("typingIndicator").style.display = "flex";
}
function hideTyping() {
    document.getElementById("typingIndicator").style.display = "none";
}

ws.onmessage = (e) => {
    const msg = JSON.parse(e.data);
    hideTyping();

    if (msg.type === "chats") loadChats(msg.data);

    if (msg.type === "chat" || msg.type === "chat_switched") {
        const box = document.getElementById("messages");
        box.innerHTML = "";
        if (msg.messages) {
            msg.messages.forEach(m => addMessage(m.role, m.content, m.file));
            box.scrollTop = box.scrollHeight;
        }
        titleGenerated = !!msg.smart_title;
    }

    if (msg.type === "new_message") {
        addMessage(msg.role || "bot", msg.content, msg.file);
    }
};

ws.onopen = () => send({action: "get_chats"});

function send(data) {
    ws.send(JSON.stringify(data));
}

function loadChats(chats) {
    const list = document.getElementById("chatList");
    list.innerHTML = "";
    chats.forEach((c, i) => {
        const div = document.createElement("div");
        div.className = "chat-item";
        div.dataset.index = i;

        const btn = document.createElement("button");
        btn.className = "chat-btn";
        btn.textContent = c.smart_title || c.title || "چت جدید";

        btn.onclick = () => {
            titleGenerated = !!c.smart_title;
            send({action: "switch_chat", index: i});
        };

        div.oncontextmenu = (e) => {
            e.preventDefault();
            showContextMenu(e, i);
        };

        div.appendChild(btn);
        list.appendChild(div);
    });
}

function showContextMenu(e, index) {
    const oldMenu = document.getElementById("contextMenu");
    if (oldMenu) oldMenu.remove();

    const menu = document.createElement("div");
    menu.id = "contextMenu";
    menu.className = "context-menu";
    menu.style.top = `${e.clientY}px`;
    menu.style.left = `${e.clientX}px`;

    const deleteOption = document.createElement("button");
    deleteOption.textContent = "حذف این چت";
    deleteOption.onclick = () => {
        if (confirm("این چت حذف بشه؟")) {
            send({action: "delete_chat", index: index});
        }
        menu.remove();
    };

    menu.appendChild(deleteOption);
    document.body.appendChild(menu);

    const closeMenu = (ev) => {
        if (!menu.contains(ev.target)) {
            menu.remove();
            document.removeEventListener("click", closeMenu);
        }
    };
    setTimeout(() => document.addEventListener("click", closeMenu), 100);
}

function addMessage(role, content, file = null) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    let html = `<strong>${role === 'user' ? 'شما' : 'مربی'}:</strong> `;

    if (file) {
        html += `<div class="file-name">📎 ${file.filename}</div>`;
    }

    html += (content || "").replace(/\n/g, '<br>');
    div.innerHTML = html;
    document.getElementById("messages").appendChild(div);
    div.scrollIntoView({behavior: "smooth"});
}

document.getElementById("messages").addEventListener("click", e => {
    if (e.target.tagName === "IMG") {
        document.getElementById("modalImage").src = e.target.src;
        document.getElementById("imageModal").classList.add("active");
    }
});

function closeModal() {
    document.getElementById("imageModal").classList.remove("active");
}

document.getElementById("fileInput").addEventListener("change", e => {
    const file = e.target.files[0];
    if (!file) return;
    pendingFile = file;
    showPreview(file);
});

function showPreview(file) {
    const preview = document.getElementById("filePreview");
    preview.innerHTML = "";
    const div = document.createElement("div");
    div.style.position = "relative";
    div.style.display = "inline-block";
    div.style.margin = "8px";

    const el = file.type.startsWith("image/") ? document.createElement("img") : document.createElement("video");
    const url = URL.createObjectURL(file);
    el.src = url;
    el.style.maxHeight = "200px";
    el.style.borderRadius = "16px";
    el.style.boxShadow = "0 4px 20px rgba(0,0,0,0.5)";
    if (file.type.startsWith("video/")) el.controls = true;

    div.appendChild(el);
    pendingFile.tempUrl = url;

    const removeBtn = document.createElement("button");
    removeBtn.textContent = "×";
    removeBtn.className = "remove-preview";
    removeBtn.onclick = () => {
        URL.revokeObjectURL(url);
        preview.innerHTML = "";
        pendingFile = null;
        document.getElementById("fileInput").value = "";
    };
    div.appendChild(removeBtn);
    preview.appendChild(div);
}

async function sendMessage() {
    const input = document.getElementById("msgInput");
    const text = input.value.trim();
    const hasFile = !!pendingFile;
    const hasText = text.length > 0;
    if (!hasFile && !hasText) return;

    showTyping();

    addMessage("user", text, hasFile ? { filename: pendingFile.name } : null);

    if (hasFile) {
        const base64 = await fileToBase64(pendingFile);
        send({
            action: "send_file",
            filename: pendingFile.name,
            mimeType: pendingFile.type,
            data: base64.split(',')[1],
            text: text
        });
        if (pendingFile.tempUrl) URL.revokeObjectURL(pendingFile.tempUrl);
        document.getElementById("filePreview").innerHTML = "";
        pendingFile = null;
        document.getElementById("fileInput").value = "";
    } else {
        send({ action: "send_message", text: text });
    }

    input.value = "";
    input.style.height = 'auto';
    input.focus();
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

document.getElementById("sendBtn").onclick = e => { e.preventDefault(); sendMessage(); };
document.getElementById("msgInput").onkeydown = async e => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        await sendMessage();
    }
};

const textarea = document.getElementById('msgInput');
textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
});

const sidebar = document.getElementById("sidebar");
const openBtn = document.getElementById("openSidebarBtn");

openBtn.onclick = () => {
    sidebar.classList.toggle("closed");
};

document.getElementById("messages").addEventListener("click", () => {
    if (window.innerWidth <= 768 && !sidebar.classList.contains("closed")) {
        sidebar.classList.add("closed");
    }
});