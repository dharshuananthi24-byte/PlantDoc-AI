# ============================================================
# tests/test_app.py — Unit & integration tests (pytest)
# ------------------------------------------------------------
# Uses Flask's built-in test client — no live server, no real
# TensorFlow model, and no real Gemini API key required, so
# these tests run anywhere (including CI).
#
# Run with:  pytest -v
# ============================================================

import io
import os
import sys
import importlib
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Use an isolated on-disk test DB so we never touch plantdoc_users.db
TEST_DB = str(Path(__file__).resolve().parent / 'test_plantdoc.db')


@pytest.fixture()
def client(monkeypatch, tmp_path):
    # Belt-and-suspenders isolation: run from a throwaway directory AND
    # point DATABASE_PATH at a throwaway file, so tests can never touch
    # the real plantdoc_users.db regardless of any config caching quirks.
    monkeypatch.chdir(tmp_path)
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_PATH'] = str(tmp_path / 'test.db')

    # Stub out the heavy ML model import so tests don't require
    # tensorflow / a trained .h5 file to be present.
    import types
    fake_model_pkg = types.ModuleType('model')
    fake_loader = types.ModuleType('model.model_loader')
    fake_loader.load_model = lambda: None
    fake_loader.predict = lambda image_bytes, class_names: {
        'class': class_names[0],
        'confidence': 91.2,
        'top5': [{'class': class_names[0], 'confidence': 91.2}]
    }
    fake_model_pkg.model_loader = fake_loader
    sys.modules['model'] = fake_model_pkg
    sys.modules['model.model_loader'] = fake_loader

    import app as flask_app_module
    importlib.reload(flask_app_module)

    flask_app_module.app.config['TESTING'] = True
    with flask_app_module.app.test_client() as c:
        yield c


# ── Health check ─────────────────────────────────────────────

def test_health_check(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'ok'
    assert 'database' in data


# ── /predict validation (existing behavior preserved) ───────

def test_predict_no_image_returns_400(client):
    resp = client.post('/predict', data={})
    assert resp.status_code == 400
    assert 'error' in resp.get_json()


def test_predict_invalid_extension_returns_400(client):
    data = {'image': (io.BytesIO(b'not a real image'), 'malware.exe')}
    resp = client.post('/predict', data=data, content_type='multipart/form-data')
    assert resp.status_code == 400


def test_predict_corrupted_image_returns_400(client):
    data = {'image': (io.BytesIO(b'not really a jpeg'), 'leaf.jpg')}
    resp = client.post('/predict', data=data, content_type='multipart/form-data')
    assert resp.status_code == 400


# ── /chat validation (existing behavior preserved) ───────────

def test_chat_missing_message_returns_400(client):
    resp = client.post('/chat', json={})
    assert resp.status_code == 400


def test_chat_fallback_reply(client):
    resp = client.post('/chat', json={'message': 'hello'})
    assert resp.status_code == 200
    assert resp.get_json()['success'] is True


# ── NEW: Authentication ───────────────────────────────────────

def test_register_and_login_flow(client):
    resp = client.post('/api/auth/register', json={
        'username': 'testfarmer',
        'email': 'farmer@example.com',
        'password': 'securepass123'
    })
    assert resp.status_code == 201
    assert resp.get_json()['success'] is True

    # Duplicate registration should be rejected
    dup = client.post('/api/auth/register', json={
        'username': 'testfarmer',
        'email': 'other@example.com',
        'password': 'securepass123'
    })
    assert dup.status_code == 409

    client.post('/api/auth/logout')

    login_resp = client.post('/api/auth/login', json={
        'username': 'testfarmer',
        'password': 'securepass123'
    })
    assert login_resp.status_code == 200
    assert login_resp.get_json()['user']['username'] == 'testfarmer'


def test_login_wrong_password_returns_401(client):
    client.post('/api/auth/register', json={
        'username': 'user2', 'email': 'u2@example.com', 'password': 'correctpass'
    })
    resp = client.post('/api/auth/login', json={'username': 'user2', 'password': 'wrongpass'})
    assert resp.status_code == 401


def test_history_requires_login(client):
    resp = client.get('/api/history')
    assert resp.status_code == 401


# ── NEW: Rate limiter ──────────────────────────────────────────

def test_rate_limiter_blocks_excess_chat_requests(client):
    responses = [client.post('/chat', json={'message': 'hi'}) for _ in range(25)]
    statuses = [r.status_code for r in responses]
    assert 429 in statuses, "Rate limiter should reject requests beyond the configured limit"


# ── NEW: Stats & cache endpoints ───────────────────────────────

def test_stats_endpoint(client):
    resp = client.get('/api/stats')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'total_users' in data
    assert 'total_predictions' in data


def test_cache_stats_endpoint(client):
    resp = client.get('/api/cache-stats')
    assert resp.status_code == 200
    assert 'hit_rate_percent' in resp.get_json()
