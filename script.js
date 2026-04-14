// AI Voice Function using Browser Speech API
function speak(text) {
    // Check if browser is already speaking to avoid overlap
    if (window.speechSynthesis.speaking) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9; // Mild professional speed
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
}

let lastVoiceTime = 0;

// Main function to fetch data from Flask Backend
async function updateDashboard() {
    try {
        const response = await fetch('/get_data');
        const data = await response.json();

        // Update UI Elements
        const emotionEl = document.getElementById('emotion');
        const bpmEl = document.getElementById('bpm');
        const attentionEl = document.getElementById('attention');

        if (data.status === "Face Detected") {
            emotionEl.innerText = data.emotion;
            bpmEl.innerText = data.bpm + " ❤️";
            attentionEl.innerText = data.attention;
            
            // Highlight Attention if not 100%
            attentionEl.style.color = (data.attention === "100%") ? "#27ae60" : "#e67e22";
        } else {
            emotionEl.innerText = "Searching...";
            bpmEl.innerText = "--";
            attentionEl.innerText = "MISSING";
            attentionEl.style.color = "#e74c3c";
        }

        // AI Voice Logic
        let currentTime = Date.now();
        if (data.attention === "MISSING" || data.attention === "LEFT" || data.attention === "RIGHT") {
            // Speak only once every 7 seconds to not be annoying
            if (currentTime - lastVoiceTime > 7000) {
                speak("Attention miss, please see camera");
                lastVoiceTime = currentTime;
            }
        }

    } catch (error) {
        console.error("Data fetch error:", error);
    }
}

// Update every 1 second
setInterval(updateDashboard, 1000);