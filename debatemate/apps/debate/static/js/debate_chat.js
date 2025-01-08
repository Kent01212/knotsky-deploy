// debate_chat.js
document.addEventListener("DOMContentLoaded", () => {
    // データ属性の取得と検証
    const debateId = document.body.dataset.debateId;
    const currentUser = document.body.dataset.currentUser;

    if (!currentUser) {
        console.error("Error: Username is not set");
        return;
    }

    // DOM要素
    const messageForm = document.getElementById("messageForm");
    const messageInput = document.getElementById("messageInput");
    const chatMessages = document.getElementById("chat-messages");

    // HTMLエスケープ用の関数
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // メッセージ表示用の関数
    function appendMessage(data) {
        console.log("Appending message:", data);
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${data.username === currentUser ? 'message-own' : ''}`;
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-author">${escapeHtml(data.username)}</span>
                <span class="message-time">${data.timestamp}</span>
            </div>
            <div class="message-content">${escapeHtml(data.message)}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // WebSocket接続用の関数
    function createWebSocket() {
        const wsUrl = `ws://localhost:8001/ws/debate/${debateId}/`;
        const ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            console.log("WebSocket connection established");
            messageForm.classList.add('connected');
            messageForm.classList.remove('error');
        };
        
        ws.onmessage = (event) => {
            console.log("Raw message received:", event.data);
            try {
                const data = JSON.parse(event.data);
                console.log("Parsed message:", data);
                appendMessage(data);
            } catch (e) {
                console.error("Error processing message:", e);
            }
        };
        
        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            messageForm.classList.add('error');
        };
        
        ws.onclose = (event) => {
            console.log("WebSocket closed:", event);
            messageForm.classList.remove('connected');
            
            setTimeout(() => {
                console.log("Attempting to reconnect...");
                chatSocket = createWebSocket();
            }, 3000);
        };
        
        return ws;
    }
    
    // サーバーへのメッセージ送信
    async function sendMessage(messageData) {
        try {
            if (chatSocket.readyState === WebSocket.OPEN) {
                chatSocket.send(JSON.stringify(messageData));
                // 自分のメッセージも表示
                appendMessage(messageData);
            } else {
                console.error("WebSocket is not open");
                messageForm.classList.add('error');
            }
        } catch (e) {
            console.error("Error sending message:", e);
            messageForm.classList.add('error');
        }
    }
    
    // WebSocket接続の開始
    let chatSocket = createWebSocket();
    
    // フォーム送信のハンドリング
    messageForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;
        
        const messageData = {
            username: currentUser,
            message: message,
            timestamp: new Date().toLocaleString()
        };
        
        await sendMessage(messageData);
        messageInput.value = "";
    });

    // ページ離脱時の処理
    window.addEventListener('beforeunload', () => {
        if (chatSocket) {
            chatSocket.close();
        }
    });
});