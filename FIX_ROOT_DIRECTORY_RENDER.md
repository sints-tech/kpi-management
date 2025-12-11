# 🔧 PERBAIKAN: Root Directory di Render.com

Error yang Anda alami:
```
Service Root Directory "/opt/render/project/src/sneat-bootstrap-html-django-admin-template-free" is missing.
cd: /opt/render/project/src/sneat-bootstrap-html-django-admin-template-free: No such file or directory
```

**Masalah:** Root Directory yang di-set di Render tidak sesuai dengan struktur repository Anda.

---

## 🔍 CARA MENENTUKAN ROOT DIRECTORY YANG BENAR

### Opsi 1: Jika Repository Root Langsung Berisi manage.py

Jika struktur repository Anda seperti ini:
```
your-repo/
  ├── manage.py          ← ada di sini
  ├── config/
  ├── apps/
  ├── build.sh
  └── requirements.txt
```

**Root Directory di Render:** **KOSONG** (biarkan kosong, tidak perlu diisi)

---

### Opsi 2: Jika Repository Root Berisi Folder Project

Jika struktur repository Anda seperti ini:
```
your-repo/
  └── sneat-bootstrap-html-django-admin-template-free/
      ├── manage.py          ← ada di sini
      ├── config/
      ├── apps/
      ├── build.sh
      └── requirements.txt
```

**Root Directory di Render:** `sneat-bootstrap-html-django-admin-template-free`

---

## 🛠️ CARA MEMPERBAIKI DI RENDER.COM

### Langkah 1: Tentukan Struktur Repository Anda

1. Buka repository GitHub/GitLab/Bitbucket Anda
2. Cek apakah `manage.py` ada di:
   - **Root repository** (langsung terlihat setelah buka repo)
   - **Atau di dalam folder** (misalnya di folder `sneat-bootstrap-html-django-admin-template-free/`)

---

### Langkah 2: Update Root Directory di Render

1. Buka **Web Service** di Render dashboard
2. Klik tab **"Settings"**
3. Scroll ke bagian **"Build & Deploy"**
4. Cari field **"Root Directory"**

5. **Pilih salah satu:**

   **Jika manage.py ada di root repository:**
   - **Kosongkan** field Root Directory (hapus semua isinya)
   - Atau isi dengan: `.` (titik saja)
   - Atau biarkan **kosong**

   **Jika manage.py ada di folder `sneat-bootstrap-html-django-admin-template-free/`:**
   - Isi dengan: `sneat-bootstrap-html-django-admin-template-free`
   - **TANPA** slash di depan atau belakang
   - **TANPA** spasi

6. Klik **"Save Changes"** di bagian bawah halaman

---

### Langkah 3: Redeploy

1. Setelah save, klik tab **"Manual Deploy"**
2. Klik **"Deploy latest commit"**
3. Tunggu build selesai

---

## ✅ VERIFIKASI

Setelah redeploy, cek log build:

1. Buka tab **"Logs"**
2. Scroll ke bagian build (awal log)
3. Pastikan **TIDAK ADA** error tentang root directory
4. Pastikan Anda melihat:
   ```
   📦 Installing Python dependencies...
   📁 Creating staticfiles directory...
   📁 Collecting static files...
   ```

---

## 🆘 JIKA MASIH ERROR

### Cek 1: Pastikan Root Directory Benar

Buka repository di GitHub, cek struktur:
- Jika `manage.py` langsung terlihat → Root Directory = **KOSONG**
- Jika `manage.py` di dalam folder → Root Directory = **nama folder tersebut**

### Cek 2: Format Root Directory

- ✅ Benar: `sneat-bootstrap-html-django-admin-template-free`
- ❌ Salah: `/sneat-bootstrap-html-django-admin-template-free` (ada slash di depan)
- ❌ Salah: `sneat-bootstrap-html-django-admin-template-free/` (ada slash di belakang)
- ❌ Salah: `sneat-bootstrap-html-django-admin-template-free ` (ada spasi)

### Cek 3: Reload Halaman

Setelah save, refresh halaman (F5) untuk memastikan perubahan tersimpan.

---

## 📋 CHECKLIST

Sebelum redeploy, pastikan:

- [ ] Sudah cek struktur repository di GitHub
- [ ] Sudah tentukan apakah manage.py di root atau di subfolder
- [ ] Sudah update Root Directory di Render sesuai struktur
- [ ] Root Directory tidak ada slash di depan/belakang
- [ ] Root Directory tidak ada spasi
- [ ] Sudah klik "Save Changes"
- [ ] Sudah klik "Manual Deploy" → "Deploy latest commit"

---

## 🎯 SOLUSI CEPAT

**Paling sering masalahnya:**

1. **Buka Web Service → Settings**
2. **Hapus isi Root Directory** (biarkan kosong)
3. **Save Changes**
4. **Manual Deploy**

Jika masih error, baru isi dengan nama folder project Anda.

---

**Setelah perbaikan ini, build seharusnya berjalan dengan baik! 🚀**

