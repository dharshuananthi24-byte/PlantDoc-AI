# ============================================================
# Dockerfile — PlantDoc AI
# ------------------------------------------------------------
# Same stack as before (Python + Flask + TensorFlow); this just
# packages it so the app runs identically on any machine/host.
# ============================================================

FROM python:3.11-slim

WORKDIR /app

# System deps needed by Pillow/TensorFlow at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/uploads logs

EXPOSE 5000

ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
