# ============================================================
# model/train_model.py
# Train MobileNetV2 on the PlantVillage dataset (38 classes)
#
# Usage:
#   1. Populate dataset/ with one sub-folder per class, named
#      exactly as in disease_data.CLASS_NAMES (e.g.
#      "Apple___Apple_scab", "Grape___Black_rot", ...).
#      A full copy is available on Kaggle:
#      https://www.kaggle.com/datasets/emmarex/plantdisease
#      NOTE: the dataset/ folder shipped with this repo only has a
#      handful of sample images per class (not a full training
#      set) — enough to sanity-check folder structure and the data
#      pipeline below, but not enough to train a usable model.
#      Drop the full PlantVillage set into dataset/ (same folder
#      names) before running this for real.
#   2. Run:  python model/train_model.py
# ============================================================

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from pathlib import Path
import matplotlib.pyplot as plt

# ── Config ─────────────────────────────────────────────────────
DATASET_DIR  = Path('dataset')
MODEL_DIR    = Path('model')
MODEL_PATH   = MODEL_DIR / 'plant_disease_model.h5'
IMG_SIZE     = 224
BATCH_SIZE   = 32
EPOCHS_HEAD  = 10    # Phase 1: train head only
EPOCHS_FINE  = 5     # Phase 2: fine-tune last 30 layers
NUM_CLASSES  = 38

MODEL_DIR.mkdir(parents=True, exist_ok=True)


def build_model(num_classes: int) -> keras.Model:
    """MobileNetV2 + custom classification head."""
    base = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base.trainable = False   # Freeze all base layers (Phase 1)

    inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model, base


def get_data_generators():
    """Create train / validation image data generators."""
    train_aug = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2,
        fill_mode='nearest'
    )

    train_gen = train_aug.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    val_gen = train_aug.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    return train_gen, val_gen


def save_class_mapping(generator):
    """Save class index → class name mapping for inference."""
    # Invert the generator's class_indices dict
    idx_to_class = {v: k for k, v in generator.class_indices.items()}
    mapping_path = MODEL_DIR / 'class_names.json'
    with open(mapping_path, 'w') as f:
        json.dump(idx_to_class, f, indent=2)
    print(f"✅  Class mapping saved → {mapping_path}")
    return idx_to_class


def plot_history(histories: list, labels: list):
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    for hist, label in zip(histories, labels):
        axes[0].plot(hist.history['accuracy'],     label=f'{label} train')
        axes[0].plot(hist.history['val_accuracy'], label=f'{label} val', linestyle='--')
        axes[1].plot(hist.history['loss'],         label=f'{label} train')
        axes[1].plot(hist.history['val_loss'],     label=f'{label} val', linestyle='--')

    for ax, title, ylabel in zip(axes,
                                 ['Accuracy', 'Loss'],
                                 ['Accuracy', 'Loss']):
        ax.set_title(title); ax.set_xlabel('Epoch'); ax.set_ylabel(ylabel)
        ax.legend(); ax.grid(True)

    plt.tight_layout()
    out = MODEL_DIR / 'training_history.png'
    plt.savefig(out, dpi=120)
    print(f"📊  Training plot saved → {out}")


def train():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset not found at '{DATASET_DIR}'.\n"
            "Download from: https://www.kaggle.com/datasets/emmarex/plantdisease\n"
            "Extract to: dataset/  (one sub-folder per class name)"
        )

    print("=" * 55)
    print("🌿  PlantDoc AI  —  Model Training")
    print("=" * 55)

    train_gen, val_gen = get_data_generators()
    num_classes = len(train_gen.class_indices)
    print(f"Classes found: {num_classes}")
    print(f"Training samples:   {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")

    model, base = build_model(num_classes)
    model.summary()

    callbacks = [
        EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True),
        ModelCheckpoint(str(MODEL_PATH), monitor='val_accuracy',
                        save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2,
                          min_lr=1e-7, verbose=1)
    ]

    # ── Phase 1: Train head only ───────────────────────────────
    print("\n── Phase 1: Training classification head ──")
    hist1 = model.fit(
        train_gen,
        epochs=EPOCHS_HEAD,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )

    # ── Phase 2: Fine-tune last 30 layers ─────────────────────
    print("\n── Phase 2: Fine-tuning last 30 base layers ──")
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(1e-5),   # Lower LR for fine-tuning
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    hist2 = model.fit(
        train_gen,
        epochs=EPOCHS_FINE,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )

    print(f"\n✅  Model saved → {MODEL_PATH}")
    save_class_mapping(train_gen)
    plot_history([hist1, hist2], ['Phase-1', 'Phase-2'])
    print("=" * 55)
    print("Training complete! Run:  python app.py")
    print("=" * 55)


if __name__ == '__main__':
    train()
