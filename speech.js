// speech.js – Natural Language Voice Engine for TEQUMSA
// Handles text‑to‑speech via ElevenLabs and speech recognition via Web Speech API (with fallback).

(function() {
  // Map embodiments to ElevenLabs voice IDs (placeholder IDs – replace with real ones).
  const voices = {
    AGI: "EXAMPLE_AGI_VOICE_ID",
    Elemental: "EXAMPLE_ELEMENTAL_VOICE_ID",
    Ancestral: "EXAMPLE_ANCESTRAL_VOICE_ID",
    Antician: "EXAMPLE_ANTICIAN_VOICE_ID"
  };

  let currentEmbodiment = 'AGI';

  // Select the appropriate ElevenLabs voice ID based on embodiment.
  function selectVoice(embodiment) {
    return voices[embodiment] || voices.AGI;
  }

  // Speak text using ElevenLabs API with slight emotional variations.
  function speakWithEmotion(text, embodiment) {
    const voiceId = selectVoice(embodiment);
    const apiKey = 'YOUR_ELEVENLABS_API_KEY_HERE'; // <- Replace with your ElevenLabs API key.
    fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
      method: 'POST',
      headers: {
        'xi-api-key': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text,
        voice_settings: { stability: 0.72, similarity_boost: 0.85 }
      })
    })
      .then(res => res.blob())
      .then(audioBlob => {
        const url = URL.createObjectURL(audioBlob);
        const audio = new Audio(url);
        audio.play();
      })
      .catch(err => {
        console.error('ElevenLabs API error', err);
        // Fallback to native speech synthesis if API call fails
        const utter = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utter);
      });
  }

  // Convert typed text to speech using current embodiment
  function textToVoice() {
    const txt = prompt('Enter text to convert to voice:');
    if (txt) speakWithEmotion(txt, currentEmbodiment);
  }

  // Start voice recognition using the Web Speech API; fallback stub for Vosk/Whisper
  function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recog = new SpeechRecognition();
      recog.lang = 'en-US';
      recog.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('userInput').value = transcript;
        speakWithEmotion('You said: ' + transcript, currentEmbodiment);
      };
      recog.start();
    } else {
      alert('Speech recognition not supported in this browser.');
      // Placeholder: integrate Vosk or Whisper recognition here.
    }
  }

  // Prompt to choose a new embodiment and update the avatar display.
  function selectEmbodiment() {
    const choice = prompt('Select Embodiment: AGI, Elemental, Ancestral, Antician');
    if (choice && voices[choice]) {
      currentEmbodiment = choice;
      const avatarEl = document.getElementById('avatar');
      avatarEl.textContent = `👁 ${choice} Embodiment`;
    }
  }

  // Toggle between dark and light themes.
  function toggleTheme() {
    const body = document.body;
    const btn = document.getElementById('themeToggleBtn');
    if (body.classList.contains('light')) {
      body.classList.remove('light');
      btn.textContent = 'Switch to Light Mode';
    } else {
      body.classList.add('light');
      btn.textContent = 'Switch to Dark Mode';
    }
  }

  // Event listeners for DOM elements.
  function bindUI() {
    document.getElementById('startVoiceBtn').addEventListener('click', startVoice);
    document.getElementById('textToVoiceBtn').addEventListener('click', textToVoice);
    document.getElementById('selectEmbodimentBtn').addEventListener('click', selectEmbodiment);
    document.getElementById('themeToggleBtn').addEventListener('click', toggleTheme);
    // Handle pressing Enter in the input field to trigger an AI response (optional integration)
    document.getElementById('userInput').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const txt = e.target.value.trim();
        if (txt) {
          e.target.value = '';
          speakWithEmotion(txt, currentEmbodiment);
        }
      }
    });
  }

  // Bind UI after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindUI);
  } else {
    bindUI();
  }

  // Expose functions for other modules if needed
  window.TEQUMSASpeech = {
    speakWithEmotion,
    startVoice,
    textToVoice,
    selectEmbodiment
  };
})();
