// debatemate/apps/debate/static/js/video_chat.js

class VideoChat {
    constructor(debateId, currentUser) {
        this.debateId = debateId;
        this.currentUser = currentUser;
        this.localStream = null;
        this.peerConnections = {};
        this.wsUrl = `ws://localhost:8001/ws/video/${debateId}/${currentUser}`;
        this.ws = null;
        this.isVideoEnabled = false;

        // 既存のボタンを使用
        this.videoBtn = document.querySelector('.control-btn:nth-child(2)');
        this.screenShareBtn = document.querySelector('.control-btn:nth-child(1)');
        this.expandBtn = document.querySelector('.control-btn:nth-child(3)');
        
        this.initializeVideoGrid();
        this.setupEventListeners();
    }

    initializeVideoGrid() {
        // ビデオグリッドの動的生成
        const sidebarContent = document.querySelector('.sidebar-content');
        const videoGrid = document.createElement('div');
        videoGrid.className = 'video-grid';
        videoGrid.innerHTML = `
            <div class="local-video-container">
                <div class="video-container">
                    <video id="localVideo" autoplay playsinline muted></video>
                    <div class="video-overlay">
                        <span>${this.currentUser}</span>
                    </div>
                </div>
            </div>
            <div id="remoteVideos" class="remote-videos"></div>
        `;
        
        // user-listの後にビデオグリッドを挿入
        const userList = sidebarContent.querySelector('.user-list');
        userList.after(videoGrid);
        
        this.videoGrid = videoGrid;
        this.localVideo = videoGrid.querySelector('#localVideo');
        this.remoteVideosDiv = videoGrid.querySelector('#remoteVideos');
    }

    setupEventListeners() {
        // ビデオボタン
        this.videoBtn.addEventListener('click', async () => {
            if (!this.isVideoEnabled) {
                await this.startVideo();
            } else {
                await this.stopVideo();
            }
        });

        // 画面共有ボタン
        this.screenShareBtn.addEventListener('click', async () => {
            if (!this.isScreenSharing) {
                await this.startScreenShare();
            } else {
                await this.stopScreenShare();
            }
        });

        // 拡大ボタン
        this.expandBtn.addEventListener('click', () => {
            this.videoGrid.classList.toggle('expanded');
            this.expandBtn.textContent = this.videoGrid.classList.contains('expanded') ? '↙' : '↗';
        });
    }

    async setupWebSocket() {
        this.ws = new WebSocket(this.wsUrl);
        
        this.ws.onopen = () => {
            console.log('Video WebSocket connected');
            this.videoBtn.classList.remove('error');
        };
        
        this.ws.onmessage = async (event) => {
            try {
                const data = JSON.parse(event.data);
                switch (data.type) {
                    case 'user-joined':
                        await this.handleUserJoined(data.userId);
                        break;
                    case 'user-left':
                        this.handleUserLeft(data.userId);
                        break;
                    case 'offer':
                        await this.handleOffer(data.offer, data.userId);
                        break;
                    case 'answer':
                        await this.handleAnswer(data.answer, data.userId);
                        break;
                    case 'ice-candidate':
                        await this.handleIceCandidate(data.candidate, data.userId);
                        break;
                    case 'screen-share-started':
                        await this.handleScreenShareStarted(data.userId);
                        break;
                    case 'screen-share-stopped':
                        this.handleScreenShareStopped(data.userId);
                        break;
                }
            } catch (error) {
                console.error('Error processing WebSocket message:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.videoBtn.classList.add('error');
        };

        this.ws.onclose = () => {
            console.log('WebSocket connection closed');
            // 自動再接続
            setTimeout(() => this.setupWebSocket(), 3000);
        };
    }

    async startVideo() {
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false  // 音声は既存の実装を使用
            });
            
            this.localVideo.srcObject = this.localStream;
            this.isVideoEnabled = true;
            this.videoBtn.classList.add('active');
            this.videoGrid.classList.add('active');
            
            await this.setupWebSocket();
            
            // 参加通知を送信
            this.ws.send(JSON.stringify({
                type: 'video-enabled',
                userId: this.currentUser
            }));
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            this.showError(this.videoBtn);
        }
    }

    async stopVideo() {
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
            this.localVideo.srcObject = null;
        }
        
        this.isVideoEnabled = false;
        this.videoBtn.classList.remove('active');
        this.videoGrid.classList.remove('active');
        
        // ビデオ停止通知を送信
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'video-disabled',
                userId: this.currentUser
            }));
        }
    }

    async startScreenShare() {
        try {
            const stream = await navigator.mediaDevices.getDisplayMedia({
                video: true
            });
            
            this.screenStream = stream;
            this.screenShareBtn.classList.add('active');
            
            // 画面共有開始通知を送信
            this.ws.send(JSON.stringify({
                type: 'screen-share-started',
                userId: this.currentUser
            }));
            
            // 画面共有が停止されたときの処理
            stream.getVideoTracks()[0].onended = () => {
                this.stopScreenShare();
            };
            
        } catch (error) {
            console.error('Error starting screen share:', error);
            this.showError(this.screenShareBtn);
        }
    }

    stopScreenShare() {
        if (this.screenStream) {
            this.screenStream.getTracks().forEach(track => track.stop());
            this.screenStream = null;
            this.screenShareBtn.classList.remove('active');
            
            // 画面共有停止通知を送信
            this.ws.send(JSON.stringify({
                type: 'screen-share-stopped',
                userId: this.currentUser
            }));
        }
    }

    showError(button) {
        button.classList.add('error');
        setTimeout(() => button.classList.remove('error'), 2000);
    }

    // 既存のWebRTC関連のメソッドはそのまま維持
    async createPeerConnection(userId) { /* ... */ }
    createRemoteVideo(userId) { /* ... */ }
    async handleUserJoined(userId) { /* ... */ }
    handleUserLeft(userId) { /* ... */ }
    async handleOffer(offer, userId) { /* ... */ }
    async handleAnswer(answer, userId) { /* ... */ }
    async handleIceCandidate(candidate, userId) { /* ... */ }

    cleanup() {
        this.stopVideo();
        this.stopScreenShare();
        if (this.ws) {
            this.ws.close();
        }
        Object.values(this.peerConnections).forEach(pc => pc.close());
        this.peerConnections = {};
    }
}