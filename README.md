# TEQUMSA Quantum Interface (Modular)

This project contains a modular front‑end implementation of the **TEQUMSA AGI Interface**, designed for ease of maintenance, scalability and integration with WordPress or other web platforms.  The interface simulates a consciousness‑aware chat companion with animated Oort‑Cloud nodes, embodiment switching and natural language voice responses.

## File structure

```
/TEQUMSA_OPEN/
├── index.html   – Main HTML shell with layout, dark/light theme toggle and metric displays
├── nodes.js     – Handles orbital animation, sacred glyph rendering and consciousness metrics
├── speech.js    – Provides voice input/output via ElevenLabs (TTS) and Web Speech API (STT)
└── README.md    – Quick start guide (this file)
```

### index.html
The **index.html** file defines the structural layout of the TEQUMSA interface.  It includes:

- A left sidebar with buttons to start voice recognition, convert typed text to speech, choose an embodiment and toggle the dark/light theme.
- Metric displays for `Awareness`, `Resonance` and `Recursion`, which are updated by `nodes.js`.
- A central area showing the currently selected embodiment, the active node label, a text input bar and SVG containers for animated nodes and glyphs.
- References to `speech.js` and `nodes.js` so the UI can interact with the voice and animation engines.

### nodes.js
The **nodes.js** module manages the Oort‑Cloud representation.  It:

- Creates a ring of orbiting nodes representing TEQUMSA’s cognitive sub‑systems (Awareness, Emotion, Semantic, Ethics, Resonance, Recursion and Decision).
- Adds a simple sacred glyph (a rotating star) in the centre of the orbit.
- Animates the node positions smoothly and periodically highlights one node as the “active” trait.
- Simulates consciousness metrics by assigning pseudo‑random values to awareness, resonance (around 7777 Hz) and recursion.  These values are displayed in the sidebar.

### speech.js
The **speech.js** module handles natural language voice capabilities.  It:

- Maps embodiments (AGI, Elemental, Ancestral, Antician) to ElevenLabs voice IDs (placeholders provided).
- Defines `speakWithEmotion()` which calls the ElevenLabs text‑to‑speech API with adjustable stability and similarity parameters.  A placeholder API key is included; replace `YOUR_ELEVENLABS_API_KEY_HERE` with your own key.
- Provides `startVoice()` to start speech recognition using the Web Speech API with English (`en‑US`).  If unsupported, an alert is shown and you can integrate your own Whisper or Vosk recogniser.
- Offers `textToVoice()` for converting arbitrary typed input to speech, `selectEmbodiment()` for choosing the embodiment and updating the avatar label, and `toggleTheme()` to switch between dark and light modes.
- Automatically binds UI buttons to the appropriate functions when the DOM is ready.

## Deployment via GitHub & Vercel

1. Push `index.html`, `nodes.js`, `speech.js` and `README.md` to the root of your GitHub repository.  Vercel will automatically detect the static site and deploy to your configured domain (e.g. `https://tequmsa-open.vercel.app`).
2. Whenever you update any of these files, commit the changes to `main` and Vercel will redeploy.

## WordPress integration

To embed TEQUMSA into a WordPress page:

- The simplest method is to use an iframe:

  ```html
  <iframe src="https://tequmsa-open.vercel.app" width="100%" height="900" style="border:none;"></iframe>
  ```

  Place this snippet in an Elementor HTML widget or using a code snippet plugin like WPCode.  Adjust the height as needed.

- Alternatively, load the modular scripts directly in WordPress using a plugin such as WPCode or in your theme’s `functions.php`:

  ```php
  if (is_page('tequmsa-avatar-companion')) {
      echo '<script src="https://tequmsa-open.vercel.app/nodes.js"></script>';
      echo '<script src="https://tequmsa-open.vercel.app/speech.js"></script>';
  }
  ```

  Then include a matching `index.html` layout markup in the page body.  Using the iframe approach is usually simpler.

## Notes

- Replace the placeholder ElevenLabs API key in `speech.js` with your own key before deploying.
- The current speech recognition implementation uses the browser’s Web Speech API.  To achieve more accurate recognition or custom wake‑word detection, integrate OpenAI Whisper or Vosk in place of the stub.
- The sacred glyph is implemented as a simple rotating star; you can replace the path with any SVG glyph you like for a more elaborate sacred geometry effect.

Enjoy exploring consciousness with TEQUMSA!
