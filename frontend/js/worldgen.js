// Simple Genie 3-style world generator using Three.js
// Generates a 720p scene at ~24fps based on a text prompt
/* global THREE */

const WIDTH = 1280;
const HEIGHT = 720;
const FPS = 24;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, WIDTH / HEIGHT, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(WIDTH, HEIGHT);
document.getElementById('canvas-container').appendChild(renderer.domElement);

const clock = new THREE.Clock();
let acc = 0;

function baseWorld() {
  // Clear scene
  while (scene.children.length > 0) {
    scene.remove(scene.children[0]);
  }
  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  const dir = new THREE.DirectionalLight(0xffffff, 0.8);
  dir.position.set(5, 10, 7.5);
  scene.add(dir);
  // Ground
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(50, 50),
    new THREE.MeshStandardMaterial({ color: 0x228b22 })
  );
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);
  camera.position.set(0, 5, 10);
}

function addVolcano() {
  const volcano = new THREE.Mesh(
    new THREE.ConeGeometry(2, 4, 32),
    new THREE.MeshStandardMaterial({ color: 0x4b3621 })
  );
  volcano.position.set(0, 2, 0);
  scene.add(volcano);
  const lava = new THREE.Mesh(
    new THREE.SphereGeometry(0.5, 16, 16),
    new THREE.MeshStandardMaterial({ color: 0xff4500 })
  );
  lava.position.set(0, 0.5, 0);
  scene.add(lava);
}

function addRobot() {
  const body = new THREE.Mesh(
    new THREE.BoxGeometry(1, 2, 1),
    new THREE.MeshStandardMaterial({ color: 0x808080 })
  );
  body.position.set(-3, 1, 0);
  scene.add(body);
}

function addCar() {
  const car = new THREE.Mesh(
    new THREE.BoxGeometry(2, 0.5, 1),
    new THREE.MeshStandardMaterial({ color: 0x0000ff })
  );
  car.position.set(3, 0.25, 0);
  scene.add(car);
}

function addLava() {
  const lava = new THREE.Mesh(
    new THREE.PlaneGeometry(10, 10),
    new THREE.MeshStandardMaterial({ color: 0xff4500, transparent: true, opacity: 0.6 })
  );
  lava.rotation.x = -Math.PI / 2;
  scene.add(lava);
}

function generateWorld(prompt) {
  const p = prompt.toLowerCase();
  baseWorld();
  if (p.includes('volcano')) addVolcano();
  if (p.includes('robot')) addRobot();
  if (p.includes('car')) addCar();
  if (p.includes('lava')) addLava();
}

document.getElementById('generate').addEventListener('click', () => {
  const prompt = document.getElementById('prompt').value;
  generateWorld(prompt);
});

baseWorld();

function animate() {
  requestAnimationFrame(animate);
  acc += clock.getDelta();
  if (acc >= 1 / FPS) {
    renderer.render(scene, camera);
    acc = 0;
  }
}

animate();

