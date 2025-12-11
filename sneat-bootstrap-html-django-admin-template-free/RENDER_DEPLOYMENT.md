# 📋 Panduan Deployment ke Render.com

Dokumentasi ini menjelaskan cara melakukan deployment aplikasi Django ini ke Render.com.

## 🔧 Konfigurasi yang Diperlukan

### 1. Environment Variables di Render.com

Di dashboard Render.com, tambahkan environment variables berikut:

```
DEBUG=False
SECRET_KEY=<your-secret-key-here>
ALLOWED_HOSTS=kpi-management-creative.onrender.com
CSRF_TRUSTED_ORIGINS=https://kpi-management-creative.onrender.com
DJANGO_ENVIRONMENT=production
BASE_URL=https://kpi-management-creative.onrender.com
```

**Cara mendapatkan SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Build Command

Di Render.com dashboard, set **Build Command**:
```bash
bash build.sh
```

Atau manual:
```bash
python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear
```

### 3. Start Command

Di Render.com dashboard, set **Start Command**:
```bash
gunicorn config.wsgi:application --config gunicorn-cfg.py
```

### 4. Root Directory (jika perlu)

Jika project berada di subfolder, set **Root Directory**:
```
sneat-bootstrap-html-django-admin-template-free
```

## 📁 File yang Telah Dikonfigurasi

### ✅ `build.sh`
Script untuk build process yang menjalankan:
- Database migrations
- Collect static files

### ✅ `gunicorn-cfg.py`
Konfigurasi Gunicorn yang sudah mendukung:
- PORT environment variable dari Render.com
- Konfigurasi untuk production

### ✅ `config/settings.py`
Sudah dikonfigurasi dengan:
- ALLOWED_HOSTS untuk domain Render.com
- WhiteNoise untuk static files
- Environment variables support

### ✅ `requirements.txt`
Dependencies yang diperlukan sudah terdaftar.

## 🚀 Langkah Deployment

1. **Push code ke repository Git** (GitHub, GitLab, Bitbucket)

2. **Buat Web Service baru di Render.com:**
   - Pilih "New" → "Web Service"
   - Connect repository Anda
   - Isi konfigurasi:
     - **Build Command**: `bash build.sh`
     - **Start Command**: `gunicorn config.wsgi:application --config gunicorn-cfg.py`
     - **Environment**: Python 3
     - **Root Directory**: `sneat-bootstrap-html-django-admin-template-free` (jika perlu)

3. **Tambahkan Environment Variables** (lihat bagian 1)

4. **Deploy!**

## 🔍 Troubleshooting

### Error 404
- Pastikan `ALLOWED_HOSTS` sudah diisi dengan domain Render.com
- Pastikan build command berhasil menjalankan `collectstatic`
- Pastikan database sudah di-migrate

### Static Files Tidak Muncul
- Pastikan WhiteNoise sudah terinstall (`pip install whitenoise`)
- Pastikan `collectstatic` berjalan di build command
- Check logs di Render.com untuk error messages

### Database Errors
- Pastikan SQLite database file ada (untuk SQLite) atau konfigurasi database sudah benar
- Pastikan migrations sudah dijalankan

### Pillow Installation Error
Jika mendapatkan error "Cannot use ImageField because Pillow is not installed":
- Build script sudah diperbaiki untuk memastikan Pillow terinstall
- Pastikan `requirements.txt` ada dan berisi `Pillow==10.4.0`
- Build script akan verify instalasi Pillow sebelum menjalankan migrations
- Jika masih error, cek logs di Render.com untuk detail error instalasi

### Gunicorn Timeout
- Gunicorn config sudah di-set timeout=120 detik
- Jika masih timeout, bisa increase di `gunicorn-cfg.py`

## 📝 Catatan Penting

- Untuk production, pastikan `DEBUG=False`
- Secret key harus unik dan rahasia
- ALLOWED_HOSTS harus sesuai dengan domain Render.com
- Static files akan di-serve oleh WhiteNoise middleware
- Database SQLite akan di-reset setiap deploy (kecuali menggunakan persistent disk)

## 🔐 Keamanan

1. Jangan commit `.env` file ke Git
2. Gunakan environment variables di Render.com untuk sensitive data
3. Pastikan `DEBUG=False` di production
4. Gunakan secret key yang kuat

