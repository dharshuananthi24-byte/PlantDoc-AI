# ============================================================
# rate_limiter.py — Lightweight sliding-window rate limiter
# ------------------------------------------------------------
# No third-party dependency: pure stdlib (collections + threading).
# Good enough for a single-process fresher project and a strong
# talking point in interviews ("how would you scale this?" ->
# swap the in-memory store for Redis).
# ============================================================

import time
import threading
from collections import defaultdict, deque
from functools import wraps

from flask import request, jsonify

_lock = threading.Lock()
_hits = defaultdict(deque)  # key -> deque of request timestamps


def _client_key():
    # X-Forwarded-For support in case the app sits behind a proxy/load balancer
    forwarded = request.headers.get('X-Forwarded-For', '')
    return forwarded.split(',')[0].strip() if forwarded else request.remote_addr


def rate_limit(max_calls, window_seconds, key_prefix=''):
    """
    Decorator: allow at most `max_calls` requests per `window_seconds`
    per client IP, using a sliding time window.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            client = _client_key()
            key = f'{key_prefix}:{client}'
            now = time.time()

            with _lock:
                q = _hits[key]
                while q and now - q[0] > window_seconds:
                    q.popleft()

                if len(q) >= max_calls:
                    retry_after = max(0, window_seconds - (now - q[0]))
                    return jsonify({
                        'error': 'Rate limit exceeded. Please slow down.',
                        'retry_after_seconds': round(retry_after, 1)
                    }), 429

                q.append(now)

            return view_func(*args, **kwargs)
        return wrapped
    return decorator
