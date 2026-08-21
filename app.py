# ============================================================
# app.py  —  PlantDoc AI  |  Main Flask Backend
# Run:  python app.py
# ============================================================

import os
import sys
import logging
from io import BytesIO
from pathlib import Path

from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# ── Load .env ─────────────────────────────────────────────────
load_dotenv()

# ── Local imports ──────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from disease_data import DISEASE_DATA, CLASS_NAMES, get_disease_info
from model.model_loader import load_model, predict

# ── New professional-feature modules (additive only) ────────────
from config import get_config
import database as db
from rate_limiter import rate_limit
from prediction_cache import prediction_cache

# ── Flask setup ────────────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16 MB
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load centralized, environment-based config (adds SECRET_KEY, rate-limit
# defaults, DB path, etc. on top of the two keys already set above).
app.config.from_object(get_config())
app.secret_key = app.config['SECRET_KEY']

# ── Database (users + prediction history) ───────────────────────
db.DEFAULT_DB_PATH = app.config['DATABASE_PATH']
db.init_db(app.config['DATABASE_PATH'])

# ── Logging ────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(levelname)s:  %(message)s')
logger = logging.getLogger(__name__)

# Rotating file handler — adds persistent, size-capped log files under
# logs/app.log without changing the existing console logging behavior.
os.makedirs(app.config['LOG_DIR'], exist_ok=True)
_file_handler = RotatingFileHandler(
    app.config['LOG_FILE'],
    maxBytes=app.config['LOG_MAX_BYTES'],
    backupCount=app.config['LOG_BACKUP_COUNT']
)
_file_handler.setLevel(logging.INFO)
_file_handler.setFormatter(logging.Formatter('%(asctime)s  %(levelname)s:  %(message)s'))
logging.getLogger().addHandler(_file_handler)

# ── Allowed extensions ──────────────────────────────────────────
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ── Gemini setup ────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
gemini_model = None

def init_gemini():
    global gemini_model
    if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini API ready")
        except Exception as e:
            logger.warning(f"⚠️  Gemini init failed: {e}")
    else:
        logger.warning("⚠️  No Gemini API key — chatbot uses fallback responses")

init_gemini()

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# ── Prediction ─────────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
@rate_limit(*app.config.get('RATE_LIMIT_PREDICT', (10, 60)), key_prefix='predict')
def predict_disease():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    try:
        image_bytes = file.read()

        # Validate image
        try:
            img = Image.open(BytesIO(image_bytes))
            img.verify()
        except Exception:
            return jsonify({'error': 'Invalid or corrupted image file'}), 400

        logger.info(f"Predicting: {file.filename}")

        # Check the image-hash cache first to avoid redundant inference
        # on a previously-seen image (see prediction_cache.py).
        cached = prediction_cache.get(image_bytes)
        if cached is not None:
            result = cached
            logger.info("Cache hit — skipped model inference")
        else:
            result = predict(image_bytes, CLASS_NAMES)
            prediction_cache.set(image_bytes, result)

        disease_info = get_disease_info(result['class'])

        # Persist to prediction history (tied to the logged-in user if any;
        # anonymous predictions are logged with user_id=None).
        try:
            db.log_prediction(
                filename=secure_filename(file.filename),
                predicted_class=result['class'],
                disease_name=disease_info.get('name'),
                confidence=result['confidence'],
                user_id=session.get('user_id')
            )
        except Exception as log_err:
            logger.warning(f"Could not save prediction history: {log_err}")

        response = {
            'success': True,
            'prediction': {
                'class_name': result['class'],
                'confidence': result['confidence'],
                'top5': result['top5']
            },
            'disease': {
                'name':               disease_info['name'],
                'plant':              disease_info['plant'],
                'description':        disease_info['description'],
                'causes':             disease_info['causes'],
                'severity':           disease_info['severity'],
                'icon':               disease_info['icon'],
                'organic_treatment':  disease_info['organic_treatment'],
                'chemical_treatment': disease_info['chemical_treatment'],
                'prevention':         disease_info['prevention']
            }
        }
        logger.info(f"Result: {disease_info['name']}  ({result['confidence']:.1f}%)")
        return jsonify(response), 200

    except ValueError as e:
        logger.error(f"Preprocessing error: {e}")
        return jsonify({'error': str(e)}), 422
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        return jsonify({'error': 'Prediction failed. Please try again.'}), 500


# ── Chatbot ────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are PlantDoc AI, an expert plant pathologist and agricultural advisor.
Help farmers and gardeners with:
- Plant disease identification and diagnosis
- Treatment recommendations (organic and chemical)
- Prevention strategies
- General plant care and health tips

Guidelines:
- Keep responses concise (3-5 sentences max) and practical
- Suggest consulting a local agricultural extension if unsure
- Mention both organic and chemical options when recommending treatments
- If asked about non-plant topics, politely redirect to plant health
- Use simple language — farmers may not have scientific backgrounds
- Use bullet points for lists of treatments or prevention tips"""

@app.route('/chat', methods=['POST'])
@rate_limit(*app.config.get('RATE_LIMIT_CHAT', (20, 60)), key_prefix='chat')
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message  = data.get('message', '').strip()
    chat_history  = data.get('history', [])

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    try:
        if gemini_model:
            conversation = SYSTEM_PROMPT + "\n\n"
            for msg in chat_history[-8:]:
                role = "User" if msg.get('role') == 'user' else "PlantDoc AI"
                conversation += f"{role}: {msg.get('content', '')}\n"
            conversation += f"User: {user_message}\nPlantDoc AI:"

            response = gemini_model.generate_content(
                conversation,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=300,
                    temperature=0.7,
                )
            )
            reply = response.text.strip()
        else:
            reply = get_fallback_response(user_message)

        return jsonify({'reply': reply, 'success': True})

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        return jsonify({
            'reply': "I'm having trouble connecting right now. Please check your Gemini API key in the .env file.",
            'success': False
        })


def get_fallback_response(message):
    msg = message.lower()
    if any(w in msg for w in ['hello', 'hi', 'hey']):
        return "Hello! 🌿 I'm PlantDoc AI. Upload a leaf image to diagnose a disease, or ask me any plant health question!"
    elif any(w in msg for w in ['tomato', 'blight']):
        return "🍅 For tomato blight: apply copper-based fungicide immediately, remove infected leaves, and water only at the base. Use mancozeb + cymoxanil for severe cases."
    elif any(w in msg for w in ['neem', 'organic', 'natural']):
        return "🌿 Neem oil is excellent! Mix 2 tbsp neem oil + 1 tsp dish soap per gallon of water. Spray every 7–14 days, covering leaf undersides. Apply in the morning or evening."
    elif any(w in msg for w in ['yellow', 'yellowing']):
        return "💛 Yellow leaves may indicate: nitrogen deficiency, overwatering, fungal disease, or viral infection. Upload a photo for accurate diagnosis!"
    elif any(w in msg for w in ['prevent', 'prevention']):
        return "🛡️ Key prevention: rotate crops, use resistant varieties, water at the base, space plants for airflow, remove infected material immediately, and sanitize tools."
    else:
        return "🌱 For accurate diagnosis, upload a clear photo of the affected leaf. I can also answer questions about specific diseases, treatments, or plant care tips!"


# ============================================================
# NEW: Authentication API (session-based, uses existing users.db)
# ============================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''

    if not username or not email or not password:
        return jsonify({'error': 'username, email and password are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if db.get_user_by_username(username):
        return jsonify({'error': 'Username already taken'}), 409
    if db.get_user_by_email(email):
        return jsonify({'error': 'Email already registered'}), 409

    try:
        user_id = db.create_user(username, email, password)
        session['user_id'] = user_id
        session['username'] = username
        logger.info(f"New user registered: {username}")
        return jsonify({'success': True, 'user': {'id': user_id, 'username': username, 'email': email}}), 201
    except Exception as e:
        logger.error(f"Registration error: {e}", exc_info=True)
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    user = db.verify_user(username, password)
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    session['user_id'] = user['id']
    session['username'] = user['username']
    logger.info(f"User logged in: {username}")
    return jsonify({'success': True, 'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}})


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


@app.route('/api/auth/me')
def me():
    if 'user_id' not in session:
        return jsonify({'authenticated': False}), 200
    return jsonify({'authenticated': True, 'user_id': session['user_id'], 'username': session.get('username')})


# ============================================================
# NEW: Prediction history & analytics API
# ============================================================

@app.route('/api/history')
def history():
    if 'user_id' not in session:
        return jsonify({'error': 'Login required to view history'}), 401
    limit = request.args.get('limit', default=50, type=int)
    records = db.get_history(session['user_id'], limit=limit)
    return jsonify({'success': True, 'count': len(records), 'history': records})


@app.route('/api/stats')
def stats():
    """Aggregate app-wide stats — total users, predictions, top diseases."""
    return jsonify({'success': True, **db.get_stats()})


@app.route('/api/cache-stats')
def cache_stats():
    """Prediction cache hit/miss metrics — useful to demo the caching feature."""
    return jsonify({'success': True, **prediction_cache.stats()})


# ── Health check ───────────────────────────────────────────────
@app.route('/health')
def health():
    db_ok = True
    try:
        db.get_stats()
    except Exception:
        db_ok = False
    return jsonify({
        'status': 'ok',
        'gemini': gemini_model is not None,
        'database': db_ok
    })


# ── Error handlers ─────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    logger.info("=" * 55)
    logger.info("🌿  PlantDoc AI  —  Starting up...")
    logger.info("=" * 55)
    logger.info("Loading ML model (may take 30–60 seconds)...")
    try:
        load_model()
        logger.info("✅  ML model loaded successfully!")
    except Exception as e:
        logger.error(f"❌  Model loading failed: {e}")
        logger.info("App will still run — predictions unavailable until model is ready.")
    logger.info("=" * 55)
    logger.info("🚀  Running at:  http://127.0.0.1:5000")
    logger.info("    Press Ctrl+C to stop")
    logger.info("=" * 55)

    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
