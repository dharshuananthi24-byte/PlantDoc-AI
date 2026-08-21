// ============================================================
// main.js — Upload & Prediction Logic
// ============================================================

// ── DOM refs ─────────────────────────────────────────────────
const dropZone      = document.getElementById('dropZone');
const fileInput     = document.getElementById('fileInput');
const browseBtn     = document.getElementById('browseBtn');
const previewWrap   = document.getElementById('previewWrap');
const previewImg    = document.getElementById('previewImg');
const clearBtn      = document.getElementById('clearBtn');
const analyseBtn    = document.getElementById('analyseBtn');
const btnText       = document.getElementById('btnText');
const btnSpinner    = document.getElementById('btnSpinner');
const resultCard    = document.getElementById('resultCard');
const resultPlaceholder = document.getElementById('resultPlaceholder');

// Result elements
const resultIcon    = document.getElementById('resultIcon');
const resultDisease = document.getElementById('resultDisease');
const resultPlant   = document.getElementById('resultPlant');
const severityBadge = document.getElementById('severityBadge');
const confValue     = document.getElementById('confValue');
const confBar       = document.getElementById('confBar');
const resultDesc    = document.getElementById('resultDesc');
const top5List      = document.getElementById('top5List');
const tabContent    = document.getElementById('tabContent');

let selectedFile = null;
let currentData  = null;
let beepSound = null;

window.addEventListener('DOMContentLoaded', () => {
  beepSound = document.getElementById('beepSound');
});

function playBeep() {
  if (!beepSound) return;
  beepSound.currentTime = 0;
  beepSound.play();
}

// ── File selection ────────────────────────────────────────────
browseBtn.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

// Drag & drop
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
});

function setFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.style.display = 'block';
    dropZone.style.display    = 'none';
    analyseBtn.disabled       = false;
  };
  reader.readAsDataURL(file);
}

clearBtn.addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  previewWrap.style.display = 'none';
  dropZone.style.display    = 'block';
  analyseBtn.disabled       = true;
  resultCard.style.display  = 'none';
  resultPlaceholder.style.display = 'flex';
});

// ── Analyse ───────────────────────────────────────────────────
analyseBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

    //playBeep();

  // Loading state
  btnText.textContent  = 'Analysing…';
  btnSpinner.style.display = 'inline-block';
  analyseBtn.disabled  = true;

  try {
    const formData = new FormData();
    formData.append('image', selectedFile);

    const res  = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok || !data.success) {
      alert('Error: ' + (data.error || 'Prediction failed'));
      return;
    }
    renderResult(data);   playBeep();

  } catch (err) {
    alert('Network error: ' + err.message);
  } finally {
    btnText.textContent      = 'Analyse Leaf';
    btnSpinner.style.display = 'none';
    analyseBtn.disabled      = false;
  }
});

// ── Render result ─────────────────────────────────────────────
function renderResult(data) {
  currentData = data;
  const { prediction, disease } = data;

  resultIcon.textContent    = disease.icon    || '🍃';
  resultDisease.textContent = disease.name    || prediction.class_name;
  resultPlant.textContent   = disease.plant   || '';
  resultDesc.textContent    = disease.description || '';

  // Confidence
  const conf = prediction.confidence || 0;
  confValue.textContent     = conf.toFixed(1) + '%';
  confBar.style.width       = Math.min(conf, 100) + '%';

  // Severity badge
  const sev = (disease.severity || 'unknown').toLowerCase();
  severityBadge.textContent = disease.severity || 'Unknown';
  severityBadge.className   = 'severity-badge severity-' + sev;

  // Top 5
  top5List.innerHTML = '';
  (prediction.top5 || []).forEach((item, i) => {
    const li  = document.createElement('li');
    const pct = item.confidence.toFixed(1);
    li.innerHTML = `
      <div style="flex:1">
        <div style="display:flex;justify-content:space-between">
          <span>${formatClassName(item.class)}</span>
          <strong>${pct}%</strong>
        </div>
        <div class="top5-bar" style="width:${Math.min(item.confidence,100)}%"></div>
      </div>`;
    top5List.appendChild(li);
  });

  // Default tab: causes
  renderTab('causes');

  // Show result
  resultPlaceholder.style.display = 'none';
  resultCard.style.display        = 'block';
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ── Tabs ──────────────────────────────────────────────────────
document.getElementById('treatmentTabs').addEventListener('click', (e) => {
  if (e.target.classList.contains('tab')) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    e.target.classList.add('active');
    renderTab(e.target.dataset.tab);
  }
});

function renderTab(tabName) {
  if (!currentData) return;
  const d = currentData.disease;
  let items = [];

  if (tabName === 'causes')     items = d.causes             || [];
  if (tabName === 'organic')    items = d.organic_treatment  || [];
  if (tabName === 'chemical')   items = d.chemical_treatment || [];
  if (tabName === 'prevention') items = d.prevention         || [];

  if (!items.length) {
    tabContent.innerHTML = '<p style="color:var(--text-light);font-size:.88rem;padding:8px 0">No information available.</p>';
    return;
  }

  tabContent.innerHTML = `<ul>${items.map(i => `<li>${i}</li>`).join('')}</ul>`;
}

// ── Disease grid ──────────────────────────────────────────────
function buildDiseaseGrid() {
  const plants = {};
  // Group by plant prefix (e.g. "Tomato" from "Tomato___Late_blight")
  CLASS_NAMES.forEach(cls => {
    const parts = cls.split('___');
    const plant = parts[0].replace(/_/g, ' ').replace(/,/g, '');
    const cond  = parts[1] ? parts[1].replace(/_/g, ' ') : 'Unknown';
    if (!plants[plant]) plants[plant] = [];
    plants[plant].push(cond);
  });

  const grid = document.getElementById('plantGrid');
  if (!grid) return;

  Object.entries(plants).forEach(([plant, conditions]) => {
    const card = document.createElement('div');
    card.className = 'plant-card';
    card.innerHTML = `
      <h3>${getPlantEmoji(plant)} ${plant}</h3>
      <ul>
        ${conditions.map(c => `<li class="${c.toLowerCase() === 'healthy' ? 'healthy' : ''}">${c}</li>`).join('')}
      </ul>`;
    grid.appendChild(card);
  });
}

function formatClassName(cls) {
  return cls.replace(/___/g, ' — ').replace(/_/g, ' ');
}

function getPlantEmoji(plant) {
  const map = {
    'Apple': '🍎', 'Blueberry': '🫐', 'Cherry': '🍒',
    'Corn': '🌽', 'Grape': '🍇', 'Orange': '🍊',
    'Peach': '🍑', 'Pepper bell': '🫑', 'Potato': '🥔',
    'Raspberry': '🍓', 'Soybean': '🌿', 'Squash': '🥒',
    'Strawberry': '🍓', 'Tomato': '🍅'
  };
  for (const [key, emoji] of Object.entries(map)) {
    if (plant.toLowerCase().startsWith(key.toLowerCase())) return emoji;
  }
  return '🌱';
}

// CLASS_NAMES injected from server — fallback list for grid
const CLASS_NAMES = [
  'Apple___Apple_scab','Apple___Black_rot','Apple___Cedar_apple_rust','Apple___healthy',
  'Blueberry___healthy','Cherry_(including_sour)___Powdery_mildew','Cherry_(including_sour)___healthy',
  'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot','Corn_(maize)___Common_rust_',
  'Corn_(maize)___Northern_Leaf_Blight','Corn_(maize)___healthy',
  'Grape___Black_rot','Grape___Esca_(Black_Measles)','Grape___Leaf_blight_(Isariopsis_Leaf_Spot)','Grape___healthy',
  'Orange___Haunglongbing_(Citrus_greening)','Peach___Bacterial_spot','Peach___healthy',
  'Pepper,_bell___Bacterial_spot','Pepper,_bell___healthy',
  'Potato___Early_blight','Potato___Late_blight','Potato___healthy',
  'Raspberry___healthy','Soybean___healthy','Squash___Powdery_mildew',
  'Strawberry___Leaf_scorch','Strawberry___healthy',
  'Tomato___Bacterial_spot','Tomato___Early_blight','Tomato___Late_blight',
  'Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot',
  'Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot',
  'Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato___healthy'
];

// Build grid on load
buildDiseaseGrid();
