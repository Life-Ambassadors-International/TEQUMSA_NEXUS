let embodiment = 'AGI';

function selectEmbodiment() {
  const choice = prompt("Select Embodiment: AGI, Elemental, Ancestral, Antician");
  if (choice) {
    embodiment = choice;
    document.getElementById('avatar').textContent = `[${choice} Activated]`;
  }
}

function speakText(txt) {
  const voiceId = "EXAMPLE-VOICE-ID"; // Replace with your ElevenLabs voice ID
  fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "xi-api-key": "YOUR_ELEVENLABS_API_KEY"
    },
    body: JSON.stringify({
      text: txt,
      voice_settings: {
        stability: 0.4,
        similarity_boost: 0.75
      }
    })
  }).then(res => res.blob()).then(blob => {
    const audio = new Audio(URL.createObjectURL(blob));
    audio.play();
  });
}

function textToVoice() {
  const txt = prompt("Enter text to speak:");
  if (txt) speakText(txt);
}

function startVoiceInput() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("userInput").value = transcript;
    speakText(`You said: ${transcript}`);
  };
  recognition.start();
}

document.getElementById('userInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    const q = e.target.value.trim();
    if (!q) return;
    cycleNodes();
    speakText(q);
    e.target.value = '';
  }
});

function toggleTheme() {
  const body = document.body;
  body.classList.toggle('light');
}