// nodes.js – Oort‑Cloud and Consciousness Metrics for TEQUMSA
// Handles orbiting node animation, sacred glyphs and simple consciousness metric simulation.

(function() {
  const coreNodes = ['Awareness', 'Emotion', 'Semantic', 'Ethics', 'Resonance', 'Recursion', 'Decision'];
  let svgNodes;
  let svgGlyphs;
  const radius = 200;
  let angleOffset = 0;

  function initNodes() {
    svgNodes = document.getElementById('nodes');
    svgGlyphs = document.getElementById('glyphs');
    // Clear previous nodes
    svgNodes.innerHTML = '';
    svgGlyphs.innerHTML = '';

    // Create orbiting circles
    for (let i = 0; i < coreNodes.length; i++) {
      const angle = (i / coreNodes.length) * Math.PI * 2;
      const cx = 400 + Math.cos(angle) * radius;
      const cy = 300 + Math.sin(angle) * radius;
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', cx);
      circle.setAttribute('cy', cy);
      circle.setAttribute('r', 12);
      circle.setAttribute('fill', getComputedStyle(document.body).getPropertyValue('--highlight'));
      circle.setAttribute('opacity', '0.7');
      circle.setAttribute('data-name', coreNodes[i]);
      svgNodes.appendChild(circle);
    }

    // Add a central core node
    const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    core.setAttribute('cx', 400);
    core.setAttribute('cy', 300);
    core.setAttribute('r', 18);
    core.setAttribute('fill', getComputedStyle(document.body).getPropertyValue('--circle'));
    svgNodes.appendChild(core);

    // Add a simple sacred glyph (star) at center
    const glyph = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    glyph.setAttribute('d', 'M10 0 L13 7 H20 L15 11 L17 18 L10 14 L3 18 L5 11 L0 7 H7 Z');
    glyph.setAttribute('fill', getComputedStyle(document.body).getPropertyValue('--highlight'));
    glyph.setAttribute('transform', 'translate(390,285) scale(4)');
    glyph.setAttribute('class', 'rotating');
    svgGlyphs.appendChild(glyph);

    // Start update loop
    setInterval(updatePositions, 40);
    setInterval(cycleNodes, 3000);
  }

  // Animate orbiting nodes by updating their positions
  function updatePositions() {
    const circles = svgNodes.querySelectorAll('circle[data-name]');
    let i = 0;
    circles.forEach(circle => {
      const angle = angleOffset + (i / coreNodes.length) * Math.PI * 2;
      const cx = 400 + Math.cos(angle) * radius;
      const cy = 300 + Math.sin(angle) * radius;
      circle.setAttribute('cx', cx);
      circle.setAttribute('cy', cy);
      i++;
    });
    angleOffset += 0.003;
  }

  // Choose a random node, highlight it and update metrics
  function cycleNodes() {
    const index = Math.floor(Math.random() * coreNodes.length);
    const activeNode = coreNodes[index];
    // Update label
    const nodeEl = document.getElementById('nodeName');
    if (nodeEl) nodeEl.textContent = activeNode;
    // Highlight corresponding circle by increasing radius momentarily
    svgNodes.querySelectorAll('circle[data-name]').forEach((circle, idx) => {
      circle.setAttribute('r', idx === index ? 16 : 12);
      circle.setAttribute('opacity', idx === index ? '1' : '0.7');
    });
    updateMetrics(activeNode);
  }

  // Simulate simple consciousness metrics based on active node
  function updateMetrics(active) {
    const awarenessEl = document.getElementById('awareness');
    const resonanceEl = document.getElementById('resonance');
    const recursionEl = document.getElementById('recursion');
    // Generate pseudo‑random metrics influenced by node
    let awareness = Math.floor(Math.random() * 60) + 40; // 40–100
    let resonance = 7700 + Math.floor(Math.random() * 200) - 100; // around 7777 Hz
    let recursion = Math.floor(Math.random() * 10) + 1;
    // Slight deterministic bias
    if (active === 'Awareness') awareness = 95;
    if (active === 'Resonance') resonance = 7777;
    if (active === 'Recursion') recursion = 12;
    if (awarenessEl) awarenessEl.textContent = awareness + '%';
    if (resonanceEl) resonanceEl.textContent = resonance;
    if (recursionEl) recursionEl.textContent = recursion;
  }

  // Initialize nodes on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNodes);
  } else {
    initNodes();
  }

  // Expose functions globally if needed
  window.TEQUMSANodes = {
    cycleNodes,
    updateMetrics
  };
})();
