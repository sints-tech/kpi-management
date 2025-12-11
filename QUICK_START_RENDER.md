# ⚡ Quick Start - Deploy ke Render.com

Panduan cepat untuk deploy aplikasi Django ke Render.com dalam 5 langkah.

## 🎯 Langkah Cepat

### 1. Push ke GitHub
```bash
git init
git add .
git commit -m "Ready for Render"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

### 2. Buat PostgreSQL Database di Render
- Login ke [render.com](https://render.com)
- Klik **"New +"** → **"PostgreSQL"**
- Pilih **Free** plan
- Klik **"Create Database"**
- **Copy External Database URL**

### 3. Buat Web Service
- Klik **"New +"** → **"Web Service"**
- Pilih repository GitHub Anda
- Isi konfigurasi:

**Build Command:**
```bash
chmod +x build.sh && ./build.sh
```

**Start Command:**
```bash
gunicorn config.wsgi:application
```

**Root Directory:**
```
sneat-bootstrap-html-django-admin-template-free
```

### 4. Set Environment Variables

Di tab **Environment**, tambahkan:

```
SECRET_KEY=<generate-dengan-python>
DEBUG=False
DJANGO_ENVIRONMENT=production
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<dari-postgresql-database>
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Deploy!

- Klik **"Create Web Service"**
- Tunggu build selesai (5-10 menit)
- Setelah selesai, buka Shell dan jalankan:
  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  ```

## ✅ Selesai!

Aplikasi Anda akan tersedia di: `https://your-app-name.onrender.com`

---

**Catatan Penting:**
- Free tier akan sleep setelah 15 menit tidak aktif
- Request pertama setelah sleep akan lambat (cold start)
- File upload tidak tersimpan permanen di free tier (gunakan cloud storage)

**Untuk detail lengkap, lihat:** `RENDER_DEPLOYMENT_GUIDE.md`

