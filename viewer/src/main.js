import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import './style.css';

const canvas = document.querySelector('#scene');
const viewport = document.querySelector('#viewport');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1923);
scene.fog = new THREE.Fog(0x0d1923, 18, 65);
const camera = new THREE.PerspectiveCamera(72, 1, 0.05, 500);
camera.position.set(0, 1.65, 5);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
scene.add(new THREE.HemisphereLight(0xd9efff, 0x34404a, 2.0));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(5, 10, 7); scene.add(key);
const grid = new THREE.GridHelper(30, 30, 0x355366, 0x203746); grid.position.y = 0; scene.add(grid);
const controls = new PointerLockControls(camera, renderer.domElement);
const loader = new GLTFLoader();
let currentModel = null;
const keys = new Set();
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
const clock = new THREE.Clock();
const status = document.querySelector('#modelStatus');
const enterButton = document.querySelector('#enterButton');
const emptyState = document.querySelector('#emptyState');

function resize(){const w=viewport.clientWidth,h=viewport.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);}
new ResizeObserver(resize).observe(viewport); resize();

function showModel(gltf, name, format){
  if(currentModel) scene.remove(currentModel);
  currentModel = gltf.scene;
  currentModel.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(currentModel);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  currentModel.position.sub(center);
  // Place the model's lowest point on the viewer's ground plane.
  currentModel.position.y += size.y/2;
  scene.add(currentModel);
  const maxDim = Math.max(size.x,size.y,size.z,1);
  camera.position.set(0, Math.max(1.55, size.y*0.12), Math.max(2.5, maxDim*0.8));
  camera.lookAt(0, Math.min(size.y*0.45, 2), 0);
  document.querySelector('#modelName').textContent = name;
  document.querySelector('#modelFormat').textContent = format;
  let objects=0, triangles=0;
  currentModel.traverse(o=>{if(o.isMesh){objects++;const g=o.geometry;triangles+=g.index?g.index.count/3:(g.attributes.position?.count||0)/3;}});
  document.querySelector('#objectCount').textContent = objects.toLocaleString();
  document.querySelector('#triangleCount').textContent = Math.round(triangles).toLocaleString();
  status.textContent = `Loaded: ${name}`;
  enterButton.disabled = false;
  emptyState.classList.add('hidden');
  document.querySelector('.crosshair').style.opacity='1';
}


async function loadFile(file) {
  if (!file) return;

  const ext = file.name.split('.').pop().toLowerCase();

  if (ext !== 'glb') {
    alert('Please select a .glb file.');
    return;
  }

  status.textContent = 'Loading model...';

  const url = URL.createObjectURL(file);

  loader.load(
    url,
    (gltf) => {
      try {
        showModel(gltf, file.name, 'GLB');
        console.log('GLB loaded successfully:', file.name);
      } catch (error) {
        console.error('Model display error:', error);
        status.textContent = 'Model display failed';
        alert('The model loaded, but could not be displayed. Check Console.');
      } finally {
        URL.revokeObjectURL(url);
      }
    },
    (progress) => {
      if (progress.total > 0) {
        const percent = Math.round(
          (progress.loaded / progress.total) * 100
        );
        status.textContent = `Loading model... ${percent}%`;
      }
    },
    (error) => {
      console.error('GLB loading error:', error);
      status.textContent = 'Model failed to load';
      URL.revokeObjectURL(url);
      alert('GLB loading failed. Open F12 > Console for details.');
    }
  );
}

for(const input of [document.querySelector('#modelInput'),document.querySelector('#emptyInput')]) input.addEventListener('change',e=>loadFile(e.target.files[0]));
enterButton.addEventListener('click',()=>controls.lock());
renderer.domElement.addEventListener('click',()=>{if(currentModel&&!controls.isLocked)controls.lock();});
document.querySelector('#resetButton').addEventListener('click',()=>{if(!currentModel)return;camera.position.set(0,1.65,5);camera.lookAt(0,1.4,0);});
controls.addEventListener('lock',()=>{status.textContent='Walkthrough active';});
controls.addEventListener('unlock',()=>{status.textContent=currentModel?'Model loaded · click to resume':'No model loaded';});
window.addEventListener('keydown',e=>keys.add(e.code));
window.addEventListener('keyup',e=>keys.delete(e.code));
function animate(){requestAnimationFrame(animate);const delta=Math.min(clock.getDelta(),0.05);if(controls.isLocked){direction.set(Number(keys.has('KeyD'))-Number(keys.has('KeyA')),0,Number(keys.has('KeyS'))-Number(keys.has('KeyW'))).normalize();const speed=3.0;controls.moveRight(direction.x*speed*delta);controls.moveForward(direction.z*speed*delta);camera.position.y = 1.65;}renderer.render(scene,camera);}
animate();
