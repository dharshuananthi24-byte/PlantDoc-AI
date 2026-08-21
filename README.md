# 🌿 PlantDoc AI — Plant Disease Detection

AI-powered plant disease diagnosis using MobileNetV2 + Google Gemini chatbot.  
Upload a leaf photo → get instant disease name, severity, and full treatment plan.

---

## 📁 Project Structure

```
plantdoc_ai/
│
├── app.py                        # Flask backend (main entry point)
├── disease_data.py               # Disease info for all 38 PlantVillage classes
├── requirements.txt              # Python dependencies
├── .env                          # API keys (never commit this)
├── .gitignore
│
├── model/
│   ├── __init__.py
│   ├── model_loader.py           # Model loading + prediction logic
│   ├── train_model.py            # Training script (run once)
│   └── plant_disease_model.h5   # ← Trained model goes here (generated)
│
├── static/
│   ├── css/style.css             # All styles
│   ├── js/
│   │   ├── main.js               # Upload + prediction UI logic
│   │   └── chatbot.js            # Floating chatbot widget
│   └── uploads/                  # Temp image storage (auto-created)
│
├── templates/
│   └── index.html                # Main UI
│
└── data/
    └── PlantVillage/             # Dataset goes here (download separately)
```

---

## ⚡ Quick Start

### 1. Create & activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> ⏱️ Takes 3–5 min (TensorFlow is ~500 MB)

### 3. Add your Gemini API key

Get a **free** key at → https://aistudio.google.com/app/apikey  
Open `.env` and replace the placeholder:

```env
GEMINI_API_KEY=AIzaSy...your_key_here
```

### 4. Train the model (or use a pre-trained one)

**Option A — Train from the PlantVillage dataset:**

```bash
# Download dataset from Kaggle:
# https://www.kaggle.com/datasets/emmarex/plantdisease
# Extract to:  data/PlantVillage/   (38 subdirectories)

python model/train_model.py
# Takes ~30–60 min with GPU, ~3–5 hrs on CPU
```

**Option B — Use a pre-trained model:**

Download a `plant_disease_model.h5` trained on PlantVillage (search Kaggle/HuggingFace)  
and place it at: `model/plant_disease_model.h5`

### 5. Run the app

```bash
python app.py
```

### 6. Open in browser

```
http://127.0.0.1:5000
```

---

## 🤖 Model Architecture

```
Input (224 × 224 × 3)
    ↓
MobileNetV2  (ImageNet pre-trained, frozen in Phase 1)
    ↓  GlobalAveragePooling2D
    ↓  BatchNormalization
    ↓  Dense(512, relu)  Dropout(0.5)
    ↓  Dense(256, relu)  Dropout(0.3)
    ↓
Output (38 classes, softmax)
```

**Two-phase training:**
- Phase 1 (10 epochs): base model frozen, train head only — lr = 1e-3
- Phase 2 (5 epochs): last 30 base layers unfrozen, fine-tune — lr = 1e-5
- Expected accuracy: **95–98%** on PlantVillage test set

---

## 🌱 Supported Plants & Diseases (38 Classes)

| Plant | Conditions |
|-------|-----------|
| 🍎 Apple | Scab, Black Rot, Cedar Rust, Healthy |
| 🫐 Blueberry | Healthy |
| 🍒 Cherry | Powdery Mildew, Healthy |
| 🌽 Corn | Gray Leaf Spot, Common Rust, N. Leaf Blight, Healthy |
| 🍇 Grape | Black Rot, Esca, Leaf Blight, Healthy |
| 🍊 Orange | Citrus Greening (HLB) |
| 🍑 Peach | Bacterial Spot, Healthy |
| 🫑 Pepper | Bacterial Spot, Healthy |
| 🥔 Potato | Early Blight, Late Blight, Healthy |
| 🫐 Raspberry | Healthy |
| 🌿 Soybean | Healthy |
| 🥒 Squash | Powdery Mildew |
| 🍓 Strawberry | Leaf Scorch, Healthy |
| 🍅 Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria, Spider Mites, Target Spot, TYLCV, Mosaic Virus, Healthy |

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: tensorflow` | `pip install tensorflow==2.15.0` |
| `FileNotFoundError: model not found` | Run `python model/train_model.py` or place `.h5` in `model/` |
| Chatbot says "check API key" | Set `GEMINI_API_KEY` in `.env` (must start with `AIzaSy...`) |
| Port 5000 in use | Change `port=5000` to `port=5001` in `app.py` |
| TensorFlow loads slowly | Normal — first load takes 10–30 s |

---

## 📦 Requirements

| Package | Version |
|---------|---------|
| flask | 3.0.0 |
| tensorflow | 2.15.0 |
| numpy | 1.26.3 |
| Pillow | 10.2.0 |
| google-generativeai | 0.4.0 |
| python-dotenv | 1.0.0 |
| Werkzeug | 3.0.1 |

---

*Built with Python, Flask, TensorFlow, and Google Gemini AI*

---

## 🚀 Professional Features (added)

These extend the original app without changing its UI, workflow, or model pipeline:

| Feature | What it does | File(s) |
|---|---|---|
| 🔐 Authentication | Session-based register/login/logout using the existing `users.db`, passwords hashed with Werkzeug | `database.py`, `app.py` |
| 🗂️ Prediction History | Every prediction is logged to SQLite and retrievable per user | `database.py` |
| 🚦 Rate Limiting | Custom sliding-window limiter protects `/predict` and `/chat` from abuse | `rate_limiter.py` |
| ⚡ Prediction Caching | SHA-256 image-hash cache skips redundant model inference | `prediction_cache.py` |
| ⚙️ Centralized Config | Environment-based `Development` / `Production` / `Testing` configs | `config.py` |
| 📝 Structured Logging | Rotating file logs at `logs/app.log`, alongside existing console logs | `app.py` |
| ✅ Automated Tests | 12 pytest tests covering routes, auth, and rate limiting | `tests/test_app.py` |
| 🐳 Containerization | `Dockerfile` + `docker-compose.yml` for one-command deployment | `Dockerfile`, `docker-compose.yml` |
| 🔁 CI Pipeline | GitHub Actions runs the test suite on every push | `.github/workflows/ci.yml` |
| 📖 API Docs | Full endpoint reference | `API_DOCS.md` |

### New API endpoints

```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
GET  /api/history          (login required)
GET  /api/stats
GET  /api/cache-stats
```

See [API_DOCS.md](API_DOCS.md) for full request/response examples.

### Run the tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Run with Docker

```bash
docker-compose up --build
```
