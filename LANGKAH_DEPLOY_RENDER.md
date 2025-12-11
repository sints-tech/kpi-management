# 🚀 LANGKAH-LANGKAH DEPLOY KE RENDER.COM - STEP BY STEP

Panduan detail langkah demi langkah untuk deploy aplikasi Django IBGADGETSTORE ke Render.com.

---

## 📝 BAGIAN 1: PERSIAPAN DI KOMPUTER ANDA

### Langkah 1.1: Generate SECRET_KEY

Buka terminal/PowerShell di folder project Anda, lalu jalankan:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Contoh output:**
```
abc123xyz456def789ghi012jkl345mno678pqr901stu234vwx567yz890ABC123XYZ456
```

**⚠️ PENTING:** Copy hasil SECRET_KEY ini dan simpan di notepad, Anda akan membutuhkannya nanti!

---

### Langkah 1.2: Pastikan Project Sudah di Git

Buka terminal di folder project, jalankan:

```bash
# Cek apakah sudah ada git repository
git status
```

**Jika belum ada git:**
```bash
git init
git add .
git commit -m "Ready for Render deployment"
```

**Jika sudah ada git, pastikan sudah di-push:**
```bash
git add .
git commit -m "Update: Ready for Render"
git push
```

---

### Langkah 1.3: Catat Informasi Project

Catat informasi berikut:
- **Nama repository GitHub/GitLab/Bitbucket:** _________________
- **URL repository:** https://github.com/username/repo-name
- **Branch yang digunakan:** biasanya `main` atau `master`
- **SECRET_KEY yang sudah di-generate:** _________________

---

## 🌐 BAGIAN 2: SETUP DI RENDER.COM

### Langkah 2.1: Buat Akun Render.com

1. Buka browser, kunjungi: **https://render.com**
2. Klik tombol **"Get Started for Free"** atau **"Sign Up"**
3. Pilih **"Sign up with GitHub"** (atau GitLab/Bitbucket)
4. Authorize Render untuk mengakses repository Anda
5. Verifikasi email jika diminta

---

### Langkah 2.2: Buat PostgreSQL Database

1. Setelah login, di dashboard Render, klik tombol **"New +"** (di pojok kanan atas)
2. Pilih **"PostgreSQL"**

3. Isi form yang muncul:

   **Name:**
   ```
   ibgadgetstore-db
   ```
   (atau nama lain yang Anda inginkan)

   **Database:**
   ```
   ibgadgetstore
   ```
   (atau nama lain)

   **User:**
   ```
   ibgadgetstore_user
   ```
   (biarkan default atau ubah sesuai keinginan)

   **Region:**
   ```
   Singapore
   ```
   (pilih yang terdekat dengan Indonesia)

   **PostgreSQL Version:**
   ```
   16
   ```
   (atau versi terbaru yang tersedia)

   **Plan:**
   ```
   Free
   ```
   (untuk testing, bisa upgrade nanti)

4. Scroll ke bawah, klik tombol **"Create Database"**

5. **TUNGGU** hingga database selesai dibuat (sekitar 1-2 menit)
   - Status akan berubah dari "Creating" menjadi "Available"

6. Setelah selesai, klik database yang baru dibuat

7. Di halaman database, cari bagian **"Connections"** atau **"Connection Info"**

8. **COPY** **"External Database URL"** yang terlihat seperti ini:
   ```
   postgresql://user:password@host:port/database
   ```

   **⚠️ PENTING:** Simpan URL ini di notepad, Anda akan membutuhkannya!

---

### Langkah 2.3: Buat Web Service

1. Kembali ke dashboard Render (klik logo Render di kiri atas)

2. Klik tombol **"New +"** lagi

3. Pilih **"Web Service"**

4. Render akan meminta koneksi ke repository:
   - Jika belum connect, klik **"Connect account"** atau **"Configure account"**
   - Pilih GitHub/GitLab/Bitbucket
   - Authorize jika diminta

5. Setelah repository muncul, **PILIH repository Anda**

6. Klik **"Connect"** atau **"Continue"**

---

### Langkah 2.4: Konfigurasi Web Service

Setelah repository terhubung, Anda akan melihat form konfigurasi. Isi dengan detail berikut:

#### **Basic Settings:**

**Name:**
```
ibgadgetstore
```
(atau nama lain yang Anda inginkan)

**Region:**
```
Singapore
```
(pilih yang sama dengan database)

**Branch:**
```
main
```
(atau `master` jika branch Anda bernama master)

**Root Directory:**
```
sneat-bootstrap-html-django-admin-template-free
```
**⚠️ PENTING:** Sesuaikan dengan nama folder project Anda di repository!

**Runtime:**
```
Python 3
```
(pilih dari dropdown)

**Build Command:**
```bash
chmod +x build.sh && ./build.sh
```
(copy paste persis seperti ini)

**Start Command:**
```bash
gunicorn config.wsgi:application
```
(copy paste persis seperti ini)

**Instance Type:**
```
Free
```
(untuk testing, bisa upgrade nanti)

---

#### **Environment Variables:**

Scroll ke bawah, cari bagian **"Environment Variables"** atau klik tab **"Environment"**

Klik **"Add Environment Variable"** untuk setiap variabel berikut:

**1. SECRET_KEY**
- **Key:** `SECRET_KEY`
- **Value:** (paste SECRET_KEY yang sudah Anda generate di Langkah 1.1)
- Klik **"Add"**

**2. DEBUG**
- **Key:** `DEBUG`
- **Value:** `False`
- Klik **"Add"**

**3. DJANGO_ENVIRONMENT**
- **Key:** `DJANGO_ENVIRONMENT`
- **Value:** `production`
- Klik **"Add"**

**4. ALLOWED_HOSTS**
- **Key:** `ALLOWED_HOSTS`
- **Value:** `ibgadgetstore.onrender.com,localhost,127.0.0.1`
  (ganti `ibgadgetstore` dengan nama yang Anda pilih di Name)
- Klik **"Add"**

**5. DATABASE_URL**
- **Key:** `DATABASE_URL`
- **Value:** (paste External Database URL yang Anda copy di Langkah 2.2)
- Klik **"Add"**

---

### Langkah 2.5: Deploy!

1. Setelah semua konfigurasi selesai, scroll ke bawah

2. Klik tombol **"Create Web Service"**

3. **TUNGGU** proses build dan deploy (bisa memakan waktu 5-15 menit)
   - Anda bisa melihat progress di halaman yang muncul
   - Status akan berubah: "Building" → "Deploying" → "Live"

4. **JANGAN TUTUP** browser selama proses ini!

---

## 🗄️ BAGIAN 3: SETUP DATABASE

### Langkah 3.1: Jalankan Migrations

Setelah deployment selesai dan status menjadi **"Live"**:

1. Di halaman Web Service, cari tab **"Shell"** atau **"Console"**
   (biasanya di bagian atas, sebelah "Logs", "Metrics", dll)

2. Klik tab **"Shell"**

3. Terminal akan muncul di bawah

4. Ketik command berikut (copy paste):
   ```bash
   python manage.py migrate
   ```

5. Tekan **Enter**

6. Tunggu hingga migrations selesai
   - Anda akan melihat output seperti: "Applying migrations... OK"

---

### Langkah 3.2: Buat Superuser (Opsional)

Jika Anda ingin bisa login ke admin panel:

1. Di Shell yang sama, ketik:
   ```bash
   python manage.py createsuperuser
   ```

2. Tekan **Enter**

3. Ikuti prompt:
   - **Username:** (ketik username, tekan Enter)
   - **Email:** (ketik email, tekan Enter, bisa dikosongkan)
   - **Password:** (ketik password, tekan Enter)
   - **Password (again):** (ketik password lagi, tekan Enter)

4. Setelah selesai, Anda akan melihat: "Superuser created successfully"

---

## ✅ BAGIAN 4: VERIFIKASI

### Langkah 4.1: Cek Aplikasi

1. Di halaman Web Service, cari bagian **"URL"** atau **"Domain"**
   - Biasanya terlihat seperti: `https://ibgadgetstore.onrender.com`

2. **COPY** URL tersebut

3. Buka tab baru di browser, paste URL tersebut

4. Aplikasi Anda seharusnya sudah muncul!

---

### Langkah 4.2: Test Login

1. Buka URL aplikasi + `/auth/login/`
   Contoh: `https://ibgadgetstore.onrender.com/auth/login/`

2. Login dengan superuser yang sudah Anda buat

3. Jika berhasil login, berarti deployment berhasil! 🎉

---

## 🔧 BAGIAN 5: TROUBLESHOOTING

### Problem: Build Failed

**Gejala:** Status stuck di "Build failed" atau "Build error"

**Solusi:**
1. Klik tab **"Logs"** di Web Service
2. Scroll ke bawah, cari error message
3. Cek apakah ada error seperti:
   - "build.sh: Permission denied" → Pastikan build command benar
   - "Module not found" → Pastikan requirements.txt lengkap
   - "Directory not found" → Cek Root Directory sudah benar

**Fix umum:**
- Pastikan `build.sh` ada di repository
- Pastikan Root Directory sesuai dengan struktur folder
- Pastikan semua dependencies ada di `requirements.txt`

---

### Problem: Database Connection Error

**Gejala:** Error "could not connect to server" atau "database does not exist"

**Solusi:**
1. Buka tab **"Environment"** di Web Service
2. Cek apakah `DATABASE_URL` sudah ada dan benar
3. Pastikan URL dimulai dengan `postgresql://`
4. Jika salah, edit dan paste ulang External Database URL dari PostgreSQL

---

### Problem: Static Files Tidak Muncul

**Gejala:** CSS/JS tidak muncul, halaman terlihat rusak

**Solusi:**
1. Buka tab **"Logs"**
2. Cek apakah ada error "collectstatic"
3. Pastikan di build script ada: `python manage.py collectstatic --noinput`
4. Redeploy dengan klik **"Manual Deploy"** → **"Deploy latest commit"**

---

### Problem: 500 Internal Server Error

**Gejala:** Halaman muncul tapi error 500

**Solusi:**
1. Buka tab **"Logs"**
2. Scroll ke bawah, cari error message Django
3. Cek apakah:
   - `SECRET_KEY` sudah diset → Pastikan sudah ada di Environment Variables
   - `ALLOWED_HOSTS` sudah benar → Pastikan domain Render sudah ditambahkan
   - Database migrations sudah dijalankan → Jalankan `python manage.py migrate` di Shell

---

## 📋 CHECKLIST FINAL

Sebelum menutup, pastikan:

- [ ] PostgreSQL database sudah dibuat dan status "Available"
- [ ] Web Service sudah dibuat dan status "Live"
- [ ] Semua Environment Variables sudah diset:
  - [ ] SECRET_KEY
  - [ ] DEBUG=False
  - [ ] DJANGO_ENVIRONMENT=production
  - [ ] ALLOWED_HOSTS (dengan domain Render)
  - [ ] DATABASE_URL (dari PostgreSQL)
- [ ] Migrations sudah dijalankan (`python manage.py migrate`)
- [ ] Superuser sudah dibuat (jika perlu)
- [ ] Aplikasi bisa diakses di browser
- [ ] Login berfungsi

---

## 🎉 SELESAI!

Jika semua checklist sudah ✅, berarti aplikasi Anda sudah berhasil di-deploy!

**URL aplikasi:** `https://your-app-name.onrender.com`

---

## 📝 CATATAN PENTING

1. **Free Tier Limitations:**
   - Aplikasi akan "sleep" setelah 15 menit tidak aktif
   - Request pertama setelah sleep akan lambat (cold start ~30 detik)
   - Untuk production, pertimbangkan upgrade ke paid plan ($7/bulan)

2. **File Upload:**
   - File yang di-upload tidak tersimpan permanen di free tier
   - File akan hilang saat redeploy
   - Untuk production, gunakan cloud storage (AWS S3, Cloudinary, dll)

3. **Update Aplikasi:**
   - Setiap kali push ke Git, Render akan otomatis rebuild
   - Atau klik "Manual Deploy" → "Deploy latest commit"

4. **Backup Database:**
   - Database di Render bisa di-backup
   - Buka PostgreSQL → tab "Backups" → "Create Backup"

---

## 🆘 BUTUH BANTUAN?

Jika masih ada masalah:

1. **Cek Logs:** Tab "Logs" di Web Service
2. **Cek Shell:** Tab "Shell" untuk run command manual
3. **Dokumentasi Render:** https://render.com/docs
4. **Dokumentasi Django:** https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Selamat! Aplikasi Anda sudah online di Render.com! 🚀**

