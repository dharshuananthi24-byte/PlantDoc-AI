# ============================================================
# model/model_loader.py
# Handles loading the trained .h5 model and running predictions
# ============================================================

import os
import logging
import numpy as np
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────
MODEL_PATH  = os.path.join(os.path.dirname(__file__), 'plant_disease_model.h5')
IMG_SIZE    = 224          # MobileNetV2 input size
_model      = None         # Cached model (loaded once at startup)


def load_model():
    """
    Load the trained Keras model from disk.
    Call this once at app startup.
    """
    global _model

    if _model is not None:
        return _model                  # Already loaded

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'.\n"
            "Please train the model first:\n"
            "  python model/train_model.py\n"
            "Or place a pre-trained plant_disease_model.h5 in the model/ folder."
        )

    # Import TensorFlow only when needed (keeps startup fast if model missing)
    import keras
    logger.info(f"Loading model from: {MODEL_PATH}")
    _model = keras.models.load_model(MODEL_PATH, compile=False)
    logger.info("Model loaded ✅")
    return _model


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Convert raw image bytes → (1, 224, 224, 3) float32 tensor
    ready for MobileNetV2 inference.
    """
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)

    # MobileNetV2 preprocessing: scale to [-1, 1]
    arr = (arr / 127.5) - 1.0
    return np.expand_dims(arr, axis=0)   # shape: (1, 224, 224, 3)


def predict(image_bytes: bytes, class_names: list) -> dict:
    """
    Run inference on image_bytes.

    Returns:
        {
          'class':      str,   # top-1 class name
          'confidence': float, # top-1 confidence in %
          'top5': [           # list of top-5 predictions
              {'class': str, 'confidence': float}, ...
          ]
        }
    """
    global _model

    if _model is None:
        load_model()

    tensor = preprocess_image(image_bytes)
    probs  = _model.predict(tensor, verbose=0)[0]   # shape: (num_classes,)

    # Top-5 indices sorted by confidence (descending)
    top5_indices = np.argsort(probs)[::-1][:5]

    top5 = [
        {
            'class':      class_names[i],
            'confidence': round(float(probs[i]) * 100, 2)
        }
        for i in top5_indices
    ]

    return {
        'class':      top5[0]['class'],
        'confidence': top5[0]['confidence'],
        'top5':       top5
    }
