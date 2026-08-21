# ============================================================
# prediction_cache.py — Image-hash based LRU prediction cache
# ------------------------------------------------------------
# Avoids re-running the (relatively expensive) TensorFlow forward
# pass when the exact same image is uploaded again. Keyed on a
# SHA-256 hash of the raw image bytes rather than filename, so it
# is correct even if two different filenames contain identical
# image data.
#
# Demonstrates: hashing, caching strategy (LRU via OrderedDict),
# time/space tradeoffs — a common fresher-interview topic.
# ============================================================

import hashlib
from collections import OrderedDict
from threading import Lock

_lock = Lock()


class PredictionCache:
    def __init__(self, max_size=128):
        self.max_size = max_size
        self._store = OrderedDict()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def hash_bytes(image_bytes):
        return hashlib.sha256(image_bytes).hexdigest()

    def get(self, image_bytes):
        key = self.hash_bytes(image_bytes)
        with _lock:
            if key in self._store:
                self._store.move_to_end(key)
                self.hits += 1
                return self._store[key]
            self.misses += 1
            return None

    def set(self, image_bytes, result):
        key = self.hash_bytes(image_bytes)
        with _lock:
            self._store[key] = result
            self._store.move_to_end(key)
            if len(self._store) > self.max_size:
                self._store.popitem(last=False)

    def stats(self):
        total = self.hits + self.misses
        hit_rate = round(self.hits / total * 100, 1) if total else 0.0
        return {
            'size': len(self._store),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate_percent': hit_rate
        }


# Module-level singleton used by app.py
prediction_cache = PredictionCache(max_size=128)
