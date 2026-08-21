# PlantDoc AI — API Documentation

Base URL (local): `http://127.0.0.1:5000`

All responses are JSON unless noted. Endpoints marked 🔒 require an active
session (login first via `/api/auth/login`).

---

## Core (existing)

### `GET /`
Renders the main UI (`templates/index.html`).

### `POST /predict`
Diagnose a plant disease from an uploaded leaf image.

- **Form-data**: `image` (file — jpg/jpeg/png/bmp/webp, max 16 MB)
- **Rate limit**: 10 requests / 60s per IP
- **200 response**
```json
{
  "success": true,
  "prediction": { "class_name": "Tomato___Late_blight", "confidence": 96.4, "top5": [...] },
  "disease": { "name": "Tomato Late Blight", "plant": "Tomato", "severity": "High", "...": "..." }
}
```
- **Errors**: `400` (missing/invalid file), `422` (preprocessing failure), `500` (server error)

### `POST /chat`
Chat with the Gemini-powered (or fallback) plant-health assistant.

- **JSON body**: `{ "message": "how do I treat tomato blight?", "history": [...] }`
- **Rate limit**: 20 requests / 60s per IP
- **200 response**: `{ "reply": "...", "success": true }`

### `GET /health`
Liveness/readiness probe.
```json
{ "status": "ok", "gemini": true, "database": true }
```

---

## Authentication (new)

### `POST /api/auth/register`
```json
// request
{ "username": "farmer1", "email": "farmer1@example.com", "password": "min6chars" }
// 201 response
{ "success": true, "user": { "id": 1, "username": "farmer1", "email": "farmer1@example.com" } }
```
`400` missing fields / weak password · `409` username or email already taken

### `POST /api/auth/login`
```json
{ "username": "farmer1", "password": "min6chars" }
```
`200` on success (sets session cookie) · `401` invalid credentials

### `POST /api/auth/logout`
Clears the session. `200 { "success": true }`

### `GET /api/auth/me`
Returns current session identity: `{ "authenticated": true, "user_id": 1, "username": "farmer1" }`

---

## Prediction History & Analytics (new)

### `GET /api/history` 🔒
Query params: `limit` (default 50)
```json
{ "success": true, "count": 3, "history": [ { "id": 5, "filename": "leaf.jpg", "predicted_class": "...", "disease_name": "...", "confidence": 91.2, "created_at": "2026-08-01T10:00:00+00:00" } ] }
```

### `GET /api/stats`
App-wide analytics (public).
```json
{ "success": true, "total_users": 12, "total_predictions": 340, "top_diseases": [ { "disease_name": "Tomato Late Blight", "count": 58 } ] }
```

### `GET /api/cache-stats`
Prediction cache performance metrics.
```json
{ "success": true, "size": 42, "max_size": 128, "hits": 17, "misses": 55, "hit_rate_percent": 23.6 }
```

---

## Rate Limiting

Implemented as a custom sliding-window limiter (see `rate_limiter.py`) — no external service required.
Exceeding a limit returns:
```json
// 429
{ "error": "Rate limit exceeded. Please slow down.", "retry_after_seconds": 12.4 }
```

## Error Format
All error responses follow `{ "error": "<message>" }` with an appropriate HTTP status code
(400 validation, 401 unauthorized, 409 conflict, 422 unprocessable, 429 rate-limited, 500 server error).
