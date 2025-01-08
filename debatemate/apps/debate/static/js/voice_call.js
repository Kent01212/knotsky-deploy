// debatemate/apps/debate/static/js/voice_call.js
class VoiceCall {
    constructor() {
        this.debateId = document.body.dataset.debateId;
        this.userName = document.body.dataset.currentUser;
        this.peerConnections = new Map();
        this.localStream = null;
        this.websocket = null;
        this.isActive = false;
        this.isMuted = false;

        this.soundButton = document.getElementById('soundBtn');
        this.soundButton.addEventListener('click', () => this.toggleAudio());
    }

    async init() {
        try {
            this.websocket = new WebSocket(
                 `ws://localhost:8003/ws/debate/${this.debateId}?user=${encodeURIComponent(this.userName)}`
            );

            this.websocket.onmessage = (event) => this.handleSignalingMessage(JSON.parse(event.data));
            this.websocket.onclose = () => this.handleWebSocketClose();

            // 初期のマイクアクセス設定
            if (!this.localStream) {
                this.localStream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: false
                });
            }

            this.localStream.getAudioTracks()[0].enabled = !this.isMuted;

        } catch (error) {
            console.error('音声通話の初期化エラー:', error);
            throw error;
        }
    }

    async handleSignalingMessage(message) {
        try {
            switch (message.type) {
                case 'user_join':
                    await this.createPeerConnection(message.user);
                    break;
                case 'user_leave':
                    this.removePeerConnection(message.user);
                    break;
                case 'offer':
                    await this.handleOffer(message);
                    break;
                case 'answer':
                    await this.handleAnswer(message);
                    break;
                case 'ice_candidate':
                    await this.handleIceCandidate(message);
                    break;
            }
        } catch (error) {
            console.error('シグナリングメッセージ処理エラー:', error);
        }
    }

    async createPeerConnection(userId) {
        const peerConnection = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        });

        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                this.websocket.send(JSON.stringify({
                    type: 'ice_candidate',
                    candidate: event.candidate,
                    targetUser: userId
                }));
            }
        };

        peerConnection.ontrack = (event) => {
            const audioElement = new Audio();
            audioElement.srcObject = event.streams[0];
            audioElement.play();
        };

        if (this.localStream) {
            this.localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, this.localStream);
            });
        }

        this.peerConnections.set(userId, peerConnection);
        return peerConnection;
    }

    removePeerConnection(userId) {
        const peerConnection = this.peerConnections.get(userId);
        if (peerConnection) {
            peerConnection.close();
            this.peerConnections.delete(userId);
        }
    }

    async handleOffer(message) {
        const peerConnection = await this.createPeerConnection(message.sender);
        await peerConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
        
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);

        this.websocket.send(JSON.stringify({
            type: 'answer',
            answer: answer,
            targetUser: message.sender
        }));
    }

    async handleAnswer(message) {
        const peerConnection = this.peerConnections.get(message.sender);
        if (peerConnection) {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
        }
    }

    async handleIceCandidate(message) {
        const peerConnection = this.peerConnections.get(message.sender);
        if (peerConnection) {
            await peerConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
        }
    }

    toggleAudio() {
        this.isMuted = !this.isMuted;
        if (this.localStream) {
            this.localStream.getAudioTracks()[0].enabled = !this.isMuted;
            this.soundButton.textContent = this.isMuted ? '🔇' : '🔊';
        }
    }

    handleWebSocketClose() {
        setTimeout(() => this.init(), 3000);
    }

    async startCall() {
        if (this.isActive) return;
        
        try {
            this.isActive = true;
            if (!this.localStream) {
                await this.init();
            }
        } catch (error) {
            console.error('音声通話の開始に失敗:', error);
            this.isActive = false;
            throw error;
        }
    }

    endCall() {
        this.isActive = false;
        if (this.websocket) {
            this.websocket.close();
        }
        this.peerConnections.forEach(pc => pc.close());
        this.peerConnections.clear();
    }

    setLocalStream(stream) {
        this.localStream = stream;
        if (this.isActive) {
            this.peerConnections.forEach(pc => {
                stream.getTracks().forEach(track => {
                    pc.addTrack(track, stream);
                });
            });
        }
    }

    isCallActive() {
        return this.isActive;
    }
}

window.voiceCall = new VoiceCall();
document.addEventListener('DOMContentLoaded', () => {
    window.voiceCall.init();
});