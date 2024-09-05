# Gunakan Python image resmi versi 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file aplikasi ke container
COPY . .

# Expose port (opsional jika ada UI atau akses via HTTP, misalnya)
# EXPOSE 8080

# Jalankan bot menggunakan perintah ini
CMD ["python", "main.py"]
