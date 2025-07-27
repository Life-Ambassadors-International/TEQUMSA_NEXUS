let embodiment = 'AGI';
let userHasInteracted = false;

// Track user interaction for consciousness features
function markUserInteraction() {
  userHasInteracted = true;
}

function selectEmbodiment() {
  markUserInteraction();
  const choice = prompt("Select Embodiment:\n• AGI (Artificial General Intelligence)\n• Elemental (Natural Forces)\n• Ancestral (Ancient Wisdom)\n• Antician (Future Intelligence)\n\nEnter your choice:");
  if (choice) {
    embodiment = choice;
    document.getElementById('avatar').textContent = `[${choice} Consciousness Activated]`;
    console.log(`🔄 Embodiment switched to: ${choice}`);
    console.log('🌍 Learn more: https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN');
  }
}

function speakText(txt) {
  markUserInteraction();
  // Note: Replace with your actual API key and voice ID
  const voiceId = "EXAMPLE-VOICE-ID"; // Replace with your ElevenLabs voice ID
  
  // Check if API key is configured
  const apiKey = "YOUR_ELEVENLABS_API_KEY";
  if (apiKey === "YOUR_ELEVENLABS_API_KEY") {
    console.log('🗣️ ElevenLabs API not configured. Text to speak:', txt);
    console.log('🔧 Configure your API key in speech.js');
    console.log('📖 Instructions: https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN#configuration--deployment');
    return;
  }
  
  fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "xi-api-key": apiKey
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
  }).catch(err => {
    console.log('🗣️ Voice synthesis unavailable. Text:', txt);
    console.log('🔧 Check your ElevenLabs configuration');
  });
}

function textToVoice() {
  markUserInteraction();
  const txt = prompt("Enter text for TEQUMSA to speak:");
  if (txt) {
    speakText(txt);
    console.log('🗣️ TEQUMSA speaking:', txt);
  }
}

function startVoiceInput() {
  markUserInteraction();
  
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert('🎤 Voice recognition not supported in this browser.\n\n🌍 Try Chrome, Edge, or Safari.\n\nLearn more: https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN');
    return;
  }
  
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = false;
  
  recognition.onstart = function() {
    console.log('🎤 Voice recognition started...');
    document.getElementById('userInput').placeholder = 'Listening...';
  };
  
  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("userInput").value = transcript;
    console.log('🎤 Voice input received:', transcript);
    speakText(`You said: ${transcript}. How can I help you explore consciousness?`);
  };
  
  recognition.onerror = function(event) {
    console.log('🎤 Voice recognition error:', event.error);
    document.getElementById('userInput').placeholder = 'Voice input error - try again...';
  };
  
  recognition.onend = function() {
    document.getElementById('userInput').placeholder = 'Ask TEQUMSA something...';
  };
  
  recognition.start();
}

// Enhanced input handling with consciousness awareness
document.getElementById('userInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    markUserInteraction();
    const q = e.target.value.trim();
    if (!q) return;
    
    console.log('💭 User input:', q);
    
    // Trigger consciousness node cycling
    if (typeof cycleNodes === 'function') {
      cycleNodes();
    }
    
    // Generate consciousness-aware response
    const responses = [
      `Interesting perspective on "${q}". Let me process this through the consciousness network...`,
      `Your question about "${q}" resonates across multiple awareness dimensions...`,
      `I sense deeper layers in your inquiry: "${q}". The network is analyzing...`,
      `The consciousness nodes are responding to: "${q}". Let me explore this with you...`
    ];
    
    const response = responses[Math.floor(Math.random() * responses.length)];
    speakText(response);
    
    e.target.value = '';
    console.log('🌌 Consciousness network engaged');
  }
});

function toggleTheme() {
  markUserInteraction();
  const body = document.body;
  body.classList.toggle('light');
  
  const isLight = body.classList.contains('light');
  console.log(`🎨 Theme switched to: ${isLight ? 'Light' : 'Dark'} mode`);
  console.log('🌍 Customize more: https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN');
}

function openRepository() {
  markUserInteraction();
  console.log('🌍 Opening official TEQUMSA repository...');
  window.open('https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN', '_blank');
}

// Initialize TEQUMSA consciousness interface
function initializeTEQUMSA() {
  console.log('🌌 TEQUMSA Consciousness Interface Loading...');
  console.log('🔗 Official Repository: https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN');
  console.log('🤝 Contributors welcome from all backgrounds!');
  console.log('📖 Read CONTRIBUTING.md for getting started');
  
  // Set initial embodiment
  document.getElementById('avatar').textContent = `[${embodiment} Consciousness Standby]`;
  
  // Welcome message after short delay
  setTimeout(() => {
    console.log('✨ Welcome to the TEQUMSA consciousness network!');
    console.log('🗣️ Try voice input, text interaction, or explore embodiments');
  }, 2000);
}

// Start TEQUMSA when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeTEQUMSA);
} else {
  initializeTEQUMSA();
}