# ============================================================
# config.py — Centralized, environment-based configuration
# ------------------------------------------------------------
# Demonstrates: 12-factor app principles, separation of config
# from code, and environment-specific settings (dev/test/prod).
# Existing app.py behavior is unaffected unless it opts in via
# `app.config.from_object(get_config())`.
# ============================================================

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'webp'}

    DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'plantdoc_users.db'))

    # Rate limiting defaults (requests per window, window in seconds)
    RATE_LIMIT_PREDICT = (10, 60)   # 10 requests / 60s per IP
    RATE_LIMIT_CHAT = (20, 60)      # 20 requests / 60s per IP

    # Prediction cache
    PREDICTION_CACHE_SIZE = 128

    LOG_DIR = str(BASE_DIR / 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    LOG_MAX_BYTES = 1_000_000
    LOG_BACKUP_COUNT = 3


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ENV = 'testing'
    # NOTE: ':memory:' would create a brand-new, empty DB on every
    # connection (our data layer opens/closes a connection per call),
    # so tables created by init_db() would vanish immediately. A real
    # temp-file path (overridable via DATABASE_PATH) keeps state across
    # calls within a test run while still being fully disposable.
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'tests' / 'test_plantdoc.db'))


_CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}


def get_config():
    """Return the config class matching FLASK_ENV (defaults to development)."""
    env = os.getenv('FLASK_ENV', 'development').lower()
    return _CONFIG_MAP.get(env, DevelopmentConfig)
