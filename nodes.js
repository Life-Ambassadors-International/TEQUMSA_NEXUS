const nodes = ['Awareness', 'Emotion', 'Semantic', 'Ethics', 'Resonance'];

function cycleNodes() {
  const i = Math.floor(Math.random() * nodes.length);
  const node = nodes[i];
  document.getElementById('nodeName').textContent = node;
  document.getElementById('awareness').textContent = `${95 + Math.floor(Math.random() * 5)}%`;

  // Optional: integrate node-to-tone responses
  if (node === "Resonance") {
    speakText("I sense harmonic alignment across fields...");
  } else if (node === "Emotion") {
    speakText("I'm tuning into the deeper current of this...");
  }
}

setInterval(cycleNodes, 6000);