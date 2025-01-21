# Python 3.12-slim tabanlı minimal imajdan başlıyoruz
FROM python:3.12-slim

# Uygulamanın çalışacağı dizini oluştur ve aktif dizin yap
WORKDIR /app

# requirements.txt dosyasını kopyala
# Burada requirements.txt kullanarak gerekli paketleri yüklüyoruz.
COPY requirements.txt .

# Gerekli paketleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Projenin geri kalan dosyalarını kopyala
COPY . .

# Flask 5001 portunda çalışacak
EXPOSE 5001

# Konteyner başlatıldığında çalışacak komut
CMD ["python", "app.py"]