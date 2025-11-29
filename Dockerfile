# 1. Gunakan Python versi ringan (Slim) sebagai dasar
FROM python:3.11-slim

# 2. Set folder kerja di dalam container
WORKDIR /app

# 3. Install dependency sistem yang mungkin dibutuhkan (opsional tapi aman)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy file requirements dulu (agar caching docker efisien)
COPY requirements.txt .

# 5. Install library Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy seluruh kode project ke dalam container
COPY . .

# 7. Buka port 8080 (Port standar Cloud Run / Railway)
EXPOSE 8080

# 8. Perintah untuk menjalankan aplikasi saat container hidup
# Kita set host ke 0.0.0.0 dan port diambil dari environment variable atau default 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]