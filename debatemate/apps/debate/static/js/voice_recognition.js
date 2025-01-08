// debatemate/apps/debate/static/js/voice_recognition.js
let mediaRecorder;
let isRecording = false;
let websocket = null;
const debateId = document.body.dataset.debateId;
let audioContext = null;
let streamSource = null;
let workletNode = null;
let voiceCallEnabled = false;

const workletCode = `
class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
    }

    process(inputs, outputs) {
        const input = inputs[0];
        if (input && input[0]) {
            const audioData = input[0];
            this.port.postMessage(audioData);
        }
        return true;
    }
}

registerProcessor('audio-processor', AudioProcessor);
`;

async function initAudioWorklet() {
    try {
        audioContext = new AudioContext({
            sampleRate: 16000
        });
        const blob = new Blob([workletCode], { type: 'application/javascript' });
        const url = URL.createObjectURL(blob);
        await audioContext.audioWorklet.addModule(url);
        URL.revokeObjectURL(url);
        return true;
    } catch (error) {
        console.error('AudioWorkletの初期化に失敗:', error);
        return false;
    }
}

function initializeWebSocket() {
    if (websocket !== null) {
        return websocket;
    }

    websocket = new WebSocket(`ws://localhost:8002/ws/debate/${debateId}/`);
    
    websocket.onopen = () => {
        console.log('WebSocket接続が確立されました');
    };

    websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };

    websocket.onclose = (event) => {
        console.log('WebSocket接続が切断されました', event.code, event.reason);
        websocket = null;
    };

    websocket.onerror = (error) => {
        console.error('WebSocketエラー:', error);
        websocket = null;
    };

    return websocket;
}

function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'partial':
        case 'final':
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.value = data.text;
            }
            break;
        case 'save':
            console.log('保存完了:', data.message);
            break;
        case 'error':
            console.error('音声認識エラー:', data.message);
            break;
    }
}

function updateRecordingState(recording) {
    isRecording = recording;
    const micButton = document.getElementById('micButton');
    
    // 通話中+録音と通常状態の2択
    if (isRecording && voiceCallEnabled) {
        micButton.textContent = '📞';  // 通話中+録音
    } else {
        micButton.textContent = '🎤';  // 通常状態
    }
    
    // ボタンのCSSクラス切り替え
    micButton.classList.toggle('recording', isRecording && voiceCallEnabled);
}

function processAudioData(audioData) {
    if (websocket && websocket.readyState === WebSocket.OPEN && isRecording) {
        websocket.send(audioData);
    }
}

async function setupAudioStream() {
    const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
            channelCount: 1,
            sampleRate: 16000,
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false  // より詳細な手動制御のため
        }
    });

    if (!audioContext) {
        const success = await initAudioWorklet();
        if (!success) {
            throw new Error('AudioWorkletの初期化に失敗しました');
        }
    }

    // より高いゲイン設定
    const gainNode = audioContext.createGain();
    gainNode.gain.value = 4.0;  // 音量を4倍に増幅

    // コンプレッサーノードを追加（さらなる音量調整）
    const compressor = audioContext.createDynamicsCompressor();
    compressor.threshold.setValueAtTime(-50, audioContext.currentTime);
    compressor.knee.setValueAtTime(40, audioContext.currentTime);
    compressor.ratio.setValueAtTime(12, audioContext.currentTime);
    compressor.attack.setValueAtTime(0, audioContext.currentTime);
    compressor.release.setValueAtTime(0.25, audioContext.currentTime);

    streamSource = audioContext.createMediaStreamSource(stream);
    workletNode = new AudioWorkletNode(audioContext, 'audio-processor');

    // 接続経路: ソース -> ゲイン -> コンプレッサー -> ワークレットノード -> 出力
    streamSource.connect(gainNode);
    gainNode.connect(compressor);
    compressor.connect(workletNode);
    workletNode.connect(audioContext.destination);

    workletNode.port.onmessage = (event) => {
        if (isRecording) {
            processAudioData(event.data);
        }
    };

    if (window.voiceCall) {
        window.voiceCall.setLocalStream(stream);
    }

    return {
        stream,
        stop: () => {
            if (gainNode) gainNode.disconnect();
            if (compressor) compressor.disconnect();
            if (workletNode) {
                workletNode.disconnect();
                workletNode = null;
            }
            if (streamSource) {
                streamSource.disconnect();
                streamSource = null;
            }
            if (audioContext) {
                audioContext.close();
                audioContext = null;
            }
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        }
    };
}
async function toggleRecording() {
    if (!isRecording) {
        try {
            if (!websocket || websocket.readyState !== WebSocket.OPEN) {
                websocket = initializeWebSocket();
                await new Promise((resolve, reject) => {
                    const timeout = setTimeout(() => reject(new Error('WebSocket接続がタイムアウトしました')), 5000);
                    websocket.onopen = () => {
                        clearTimeout(timeout);
                        resolve();
                    };
                });
            }

            if (!audioContext) {
                mediaRecorder = await setupAudioStream();
            }

            // 音声通話の開始
            if (window.voiceCall && !voiceCallEnabled) {
                voiceCallEnabled = true;
                await window.voiceCall.startCall();
            }

            updateRecordingState(true);

        } catch (err) {
            console.error('録音の開始に失敗しました:', err);
            alert('マイクへのアクセスに失敗しました。');
            updateRecordingState(false);
        }
    } else {
        try {
            updateRecordingState(false);
            
            if (mediaRecorder) {
                mediaRecorder.stop();
                mediaRecorder = null;
            }
            
            if (websocket && websocket.readyState === WebSocket.OPEN) {
                websocket.close(1000, "Recording stopped");
            }

            // 音声通話の停止
            if (window.voiceCall && voiceCallEnabled) {
                voiceCallEnabled = false;
                window.voiceCall.endCall();
            }
        } catch (err) {
            console.error('録音の停止に失敗しました:', err);
        }
    }
}

document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' && document.activeElement.tagName !== 'INPUT') {
        event.preventDefault();
        toggleRecording();
    }
});