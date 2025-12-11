# 🚀 Panduan Deployment Django ke Render.com

Panduan lengkap untuk meng-deploy aplikasi Django IBGADGETSTORE ke Render.com.

## 📋 Daftar Isi

1. [Persiapan](#persiapan)
2. [Langkah-langkah Deployment](#langkah-langkah-deployment)
3. [Konfigurasi Database](#konfigurasi-database)
4. [Environment Variables](#environment-variables)
5. [Konfigurasi Static Files](#konfigurasi-static-files)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Persiapan

### 1. Pastikan Project Siap

Pastikan project Anda sudah memiliki:
- ✅ `requirements.txt` dengan semua dependencies
- ✅ `build.sh` untuk build script
- ✅ `manage.py` di root directory
- ✅ `config/wsgi.py` untuk WSGI application
- ✅ Static files configuration sudah benar

### 2. Push ke Git Repository

Pastikan project sudah di-push ke Git repository (GitHub, GitLab, atau Bitbucket):

```bash
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"
git remote add origin <URL_REPOSITORY_ANDA>
git push -u origin main
```

---

## 🚀 Langkah-langkah Deployment

### Langkah 1: Buat Akun Render.com

1. Kunjungi [https://render.com](https://render.com)
2. Daftar dengan GitHub/GitLab/Bitbucket account
3. Verifikasi email Anda

### Langkah 2: Buat PostgreSQL Database

1. Di dashboard Render, klik **"New +"** → **"PostgreSQL"**
2. Isi konfigurasi:
   - **Name**: `ibgadgetstore-db` (atau nama yang Anda inginkan)
   - **Database**: `ibgadgetstore`
   - **User**: `ibgadgetstore_user` (atau biarkan default)
   - **Region**: Pilih region terdekat (Singapore untuk Indonesia)
   - **PostgreSQL Version**: `16` (atau versi terbaru)
   - **Plan**: Pilih plan sesuai kebutuhan (Free tier tersedia untuk testing)
3. Klik **"Create Database"**
4. Tunggu hingga database selesai dibuat
5. **Catat informasi koneksi database** yang akan muncul:
   - Internal Database URL
   - External Database URL

### Langkah 3: Buat Web Service

1. Di dashboard Render, klik **"New +"** → **"Web Service"**
2. Pilih repository GitHub/GitLab/Bitbucket Anda
3. Isi konfigurasi:

#### Basic Settings:
- **Name**: `ibgadgetstore` (atau nama yang Anda inginkan)
- **Region**: Pilih region yang sama dengan database
- **Branch**: `main` (atau branch yang Anda gunakan)
- **Root Directory**: `sneat-bootstrap-html-django-admin-template-free` (sesuaikan dengan struktur folder Anda)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  chmod +x build.sh && ./build.sh
  ```
- **Start Command**: 
  ```bash
  gunicorn config.wsgi:application
  ```

#### Advanced Settings:

**Environment Variables** - Tambahkan variabel berikut:

```
SECRET_KEY=<generate-secret-key-di-bawah>
DEBUG=False
DJANGO_ENVIRONMENT=production
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
DATABASE_URL=<dari-postgresql-database-yang-dibuat>
```

**Generate SECRET_KEY**:
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Plan**: Pilih plan sesuai kebutuhan (Free tier tersedia untuk testing)

4. Klik **"Create Web Service"**

### Langkah 4: Link Database ke Web Service

1. Di halaman Web Service, klik tab **"Environment"**
2. Scroll ke bagian **"Add Environment Variable"**
3. Tambahkan:
   - **Key**: `DATABASE_URL`
   - **Value**: Copy dari PostgreSQL database yang dibuat (External Database URL)
4. Klik **"Save Changes"**

---

## 🗄️ Konfigurasi Database

### Migrasi Database

Setelah deployment pertama kali, database perlu di-migrate:

1. Di Render dashboard, buka Web Service Anda
2. Klik tab **"Shell"**
3. Jalankan command:
   ```bash
   python manage.py migrate
   ```
4. Buat superuser (opsional):
   ```bash
   python manage.py createsuperuser
   ```

### Backup Database (Opsional)

Untuk backup database di Render:
1. Buka PostgreSQL database di dashboard
2. Klik tab **"Connections"**
3. Gunakan External Database URL untuk backup menggunakan `pg_dump`

---

## 🔐 Environment Variables

Berikut adalah daftar lengkap Environment Variables yang perlu diset di Render:

### Required Variables:

| Variable | Value | Keterangan |
|----------|-------|------------|
| `SECRET_KEY` | `generated-secret-key` | Django secret key (generate dengan Python) |
| `DEBUG` | `False` | Set ke False untuk production |
| `DJANGO_ENVIRONMENT` | `production` | Environment identifier |
| `ALLOWED_HOSTS` | `your-app.onrender.com,localhost` | Domain yang diizinkan |
| `DATABASE_URL` | `postgresql://...` | URL dari PostgreSQL database |

### Optional Variables:

| Variable | Value | Keterangan |
|----------|-------|------------|
| `BASE_URL` | `https://your-app.onrender.com` | Base URL aplikasi |
| `TIME_ZONE` | `Asia/Jakarta` | Timezone (default: UTC) |

### Cara Set Environment Variables:

1. Buka Web Service di Render dashboard
2. Klik tab **"Environment"**
3. Scroll ke **"Environment Variables"**
4. Klik **"Add Environment Variable"**
5. Masukkan Key dan Value
6. Klik **"Save Changes"**

---

## 📁 Konfigurasi Static Files

Static files sudah dikonfigurasi dengan WhiteNoise untuk production.

### Build Script (`build.sh`)

Build script sudah termasuk:
- Install dependencies dari `requirements.txt`
- Collect static files dengan `collectstatic`
- Run database migrations

### Static Files Configuration

Di `config/settings.py` sudah dikonfigurasi:
- `STATIC_URL = "/static/"`
- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `STATICFILES_DIRS = [BASE_DIR / "src" / "assets"]`
- WhiteNoise middleware untuk serve static files

---

## 🔍 Troubleshooting

### Problem: Build Failed

**Solusi:**
1. Cek log build di Render dashboard
2. Pastikan `requirements.txt` lengkap
3. Pastikan `build.sh` executable (`chmod +x build.sh`)
4. Pastikan root directory benar

### Problem: Database Connection Error

**Solusi:**
1. Pastikan `DATABASE_URL` sudah diset di Environment Variables
2. Pastikan PostgreSQL database sudah dibuat dan running
3. Pastikan `psycopg2-binary` ada di `requirements.txt`
4. Cek Internal Database URL jika menggunakan di Render (lebih cepat)

### Problem: Static Files Tidak Muncul

**Solusi:**
1. Pastikan `collectstatic` berjalan di build script
2. Pastikan WhiteNoise middleware aktif di `settings.py`
3. Cek `STATIC_ROOT` dan `STATICFILES_DIRS` sudah benar
4. Pastikan `DEBUG=False` di production

### Problem: 500 Internal Server Error

**Solusi:**
1. Cek log aplikasi di Render dashboard
2. Pastikan `SECRET_KEY` sudah diset
3. Pastikan `ALLOWED_HOSTS` sudah benar
4. Pastikan database migrations sudah dijalankan
5. Cek apakah ada error di Django logs

### Problem: Media Files Tidak Tersimpan

**Catatan Penting:**
- Render.com **tidak menyimpan file upload secara permanen** di free tier
- File upload akan hilang saat redeploy
- **Solusi**: Gunakan cloud storage seperti:
  - AWS S3
  - Cloudinary
  - Google Cloud Storage
  - DigitalOcean Spaces

---

## 📝 Checklist Deployment

Sebelum deploy, pastikan:

- [ ] Project sudah di-push ke Git repository
- [ ] `requirements.txt` lengkap dan up-to-date
- [ ] `build.sh` sudah dibuat dan executable
- [ ] `SECRET_KEY` sudah di-generate
- [ ] PostgreSQL database sudah dibuat di Render
- [ ] Environment variables sudah diset dengan benar
- [ ] `ALLOWED_HOSTS` sudah diset dengan domain Render
- [ ] `DEBUG=False` untuk production
- [ ] Database migrations sudah dijalankan
- [ ] Superuser sudah dibuat (jika perlu)

---

## 🔄 Update Deployment

Setelah perubahan kode:

1. Commit dan push perubahan ke Git:
   ```bash
   git add .
   git commit -m "Update: description"
   git push
   ```

2. Render akan otomatis rebuild dan redeploy

3. Jika perlu run migrations:
   - Buka Shell di Render dashboard
   - Jalankan: `python manage.py migrate`

---

## 📞 Support

Jika mengalami masalah:

1. Cek log di Render dashboard (Web Service → Logs)
2. Cek Django logs di Shell:
   ```bash
   python manage.py check --deploy
   ```
3. Dokumentasi Render: [https://render.com/docs](https://render.com/docs)
4. Dokumentasi Django Deployment: [https://docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)

---

## 🎉 Selesai!

Setelah semua langkah di atas, aplikasi Django Anda akan berjalan di Render.com!

**URL aplikasi**: `https://your-app-name.onrender.com`

**Catatan**: 
- Free tier Render.com akan sleep setelah 15 menit tidak aktif
- Request pertama setelah sleep akan lebih lambat (cold start)
- Untuk production, pertimbangkan upgrade ke paid plan

---

**Selamat Deploy! 🚀**

