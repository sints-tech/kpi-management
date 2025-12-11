# 🔧 CARA MEMPERBAIKI ERROR 404 DI RENDER.COM

Berdasarkan log yang Anda berikan, ada beberapa masalah yang perlu diperbaiki.

---

## 🔍 ANALISIS MASALAH

Dari log yang Anda berikan, saya melihat:

1. ✅ Aplikasi sudah running dengan baik (gunicorn listening di port 10000)
2. ⚠️ **Warning:** `No directory at: /opt/render/project/src/staticfiles/`
3. ✅ Request ke "/" mengembalikan 200 (berhasil)
4. ❌ Tapi Anda melihat 404 di browser

**Masalah utama:**
- Static files tidak ter-collect dengan benar
- Root directory mungkin salah di konfigurasi Render

---

## 🛠️ SOLUSI: PERBAIKI BUILD SCRIPT

Saya sudah memperbaiki `build.sh` untuk membuat directory staticfiles terlebih dahulu.

### File yang sudah diperbaiki:
- ✅ `build.sh` - Sudah ditambahkan `mkdir -p staticfiles` dan `--clear` flag

---

## 📋 LANGKAH PERBAIKAN DI RENDER.COM

### Langkah 1: Pastikan Root Directory Benar

1. Buka Web Service di Render dashboard
2. Klik tab **"Settings"**
3. Scroll ke bagian **"Build & Deploy"**
4. Cek **"Root Directory"**:
   - Harus: `sneat-bootstrap-html-django-admin-template-free`
   - Jika kosong atau salah, ubah menjadi: `sneat-bootstrap-html-django-admin-template-free`

### Langkah 2: Update Build Script

1. Pastikan file `build.sh` sudah di-push ke Git dengan perubahan terbaru:
   ```bash
   git add build.sh
   git commit -m "Fix: Add staticfiles directory creation"
   git push
   ```

2. Atau jika belum, Render akan otomatis menggunakan versi terbaru setelah push

### Langkah 3: Manual Deploy

1. Di Web Service → tab **"Manual Deploy"**
2. Klik **"Deploy latest commit"**
3. Tunggu build selesai

---

## 🔍 CEK LOG BUILD

Setelah redeploy, cek log build untuk memastikan:

1. Buka tab **"Logs"** di Web Service
2. Scroll ke bagian build (awal log)
3. Pastikan Anda melihat:
   ```
   📁 Creating staticfiles directory...
   📁 Collecting static files...
   ```
4. Pastikan tidak ada error tentang staticfiles

---

## 🆘 JIKA MASIH 404 SETELAH PERBAIKAN

### Cek 1: Root Directory

Pastikan Root Directory di Render sudah benar:
- Buka Web Service → Settings → Root Directory
- Harus: `sneat-bootstrap-html-django-admin-template-free`
- Jika kosong, isi dengan: `sneat-bootstrap-html-django-admin-template-free`

### Cek 2: Environment Variables

Pastikan Environment Variables sudah lengkap:
- Buka Web Service → Environment
- Pastikan ada:
  - ✅ SECRET_KEY
  - ✅ DEBUG=False
  - ✅ DJANGO_ENVIRONMENT=production
  - ✅ ALLOWED_HOSTS (dengan domain Render Anda)
  - ✅ DATABASE_URL

### Cek 3: Database Migrations

Pastikan migrations sudah dijalankan:
1. Buka tab **"Shell"** di Web Service
2. Jalankan:
   ```bash
   python manage.py migrate
   ```
3. Tunggu hingga selesai

### Cek 4: Cek URL Routing

Coba akses URL berikut di browser:
- `https://kpi-management-creative.onrender.com/` (root)
- `https://kpi-management-creative.onrender.com/auth/login/` (login)
- `https://kpi-management-creative.onrender.com/kpi/stories/` (stories)

Jika salah satu berhasil, berarti routing sudah benar.

---

## 🔧 PERBAIKAN TAMBAHAN: Update Build Script

Saya sudah memperbaiki `build.sh` dengan:
1. Membuat directory staticfiles jika belum ada
2. Menambahkan flag `--clear` untuk clear staticfiles lama
3. Memastikan collectstatic berjalan dengan benar

**File yang sudah diperbaiki:**
- ✅ `build.sh` - Sudah ditambahkan `mkdir -p staticfiles`

---

## 📝 CHECKLIST PERBAIKAN

Sebelum redeploy, pastikan:

- [ ] Root Directory di Render sudah benar: `sneat-bootstrap-html-django-admin-template-free`
- [ ] File `build.sh` sudah di-push ke Git dengan perubahan terbaru
- [ ] Semua Environment Variables sudah lengkap
- [ ] Database migrations sudah dijalankan
- [ ] Build script sudah executable (`chmod +x build.sh`)

---

## 🚀 LANGKAH REDEPLOY

1. **Push perubahan ke Git:**
   ```bash
   git add build.sh
   git commit -m "Fix: Add staticfiles directory creation in build script"
   git push
   ```

2. **Atau Manual Deploy di Render:**
   - Buka Web Service → tab "Manual Deploy"
   - Klik "Deploy latest commit"

3. **Tunggu build selesai** (5-10 menit)

4. **Cek log** untuk memastikan tidak ada error

5. **Test aplikasi** di browser

---

## 🎯 JIKA MASIH ERROR

Jika masih error setelah semua perbaikan:

1. **Cek Logs** di Render dashboard untuk error message lengkap
2. **Cek Shell** untuk run command manual:
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
3. **Cek Environment Variables** sudah benar semua
4. **Cek Root Directory** sudah benar

---

**Setelah perbaikan ini, aplikasi seharusnya sudah berjalan dengan baik! 🚀**

