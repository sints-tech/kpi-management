# 📝 CARA MENGISI ENVIRONMENT VARIABLES DI RENDER.COM

Panduan lengkap langkah demi langkah untuk mengisi environment variables di Render.com.

---

## 🎯 METODE 1: TAMBAH SATU PER SATU (RECOMMENDED)

### Langkah 1: Buka Halaman Web Service

1. Login ke [render.com](https://render.com)
2. Di dashboard, klik **Web Service** yang sudah Anda buat
3. Klik tab **"Environment"** (di bagian atas, sebelah "Logs", "Metrics", dll)

### Langkah 2: Tambah Environment Variables

Untuk setiap variabel berikut, ikuti langkah ini:

1. Scroll ke bawah, cari bagian **"Environment Variables"**
2. Klik tombol **"+ Tambahkan Variabel Lingkungan"** atau **"+ Add Environment Variable"**
3. Form akan muncul dengan 2 field:
   - **Key** (di kiri)
   - **Value** (di kanan)
4. Isi Key dan Value sesuai tabel di bawah
5. Klik **"Add"** atau **"Save"**
6. Ulangi untuk variabel berikutnya

---

## 📋 DAFTAR ENVIRONMENT VARIABLES YANG HARUS DITAMBAHKAN

### 1. SECRET_KEY (WAJIB)

**Key:**
```
SECRET_KEY
```

**Value:**
Generate dulu dengan command ini di terminal komputer Anda:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy hasilnya dan paste sebagai Value.

**Contoh Value:**
```
abc123xyz456def789ghi012jkl345mno678pqr901stu234vwx567yz890ABC123XYZ456
```

---

### 2. DEBUG (WAJIB)

**Key:**
```
DEBUG
```

**Value:**
```
False
```

**⚠️ PENTING:** Harus `False` (huruf F besar) untuk production!

---

### 3. DJANGO_ENVIRONMENT (WAJIB)

**Key:**
```
DJANGO_ENVIRONMENT
```

**Value:**
```
production
```

---

### 4. ALLOWED_HOSTS (WAJIB)

**Key:**
```
ALLOWED_HOSTS
```

**Value:**
Ganti `your-app-name` dengan nama aplikasi Anda di Render!

```
your-app-name.onrender.com,localhost,127.0.0.1
```

**Contoh jika nama aplikasi Anda "ibgadgetstore":**
```
ibgadgetstore.onrender.com,localhost,127.0.0.1
```

**Cara cek nama aplikasi:**
- Di halaman Web Service, lihat bagian "URL" atau "Domain"
- Contoh: `https://ibgadgetstore.onrender.com`
- Maka nama aplikasinya adalah: `ibgadgetstore`

---

### 5. DATABASE_URL (WAJIB)

**Key:**
```
DATABASE_URL
```

**Value:**
Copy dari PostgreSQL database yang sudah Anda buat di Render.

**Cara mendapatkan DATABASE_URL:**
1. Di dashboard Render, klik **PostgreSQL database** yang sudah dibuat
2. Di halaman database, cari bagian **"Connections"** atau **"Connection Info"**
3. Copy **"External Database URL"**
   - Formatnya seperti: `postgresql://user:password@host:port/database`
4. Paste sebagai Value

**Contoh Value:**
```
postgresql://ibgadgetstore_user:abc123xyz@dpg-xxxxx-a.singapore-postgres.render.com/ibgadgetstore
```

---

### 6. BASE_URL (OPSIONAL)

**Key:**
```
BASE_URL
```

**Value:**
Ganti dengan URL aplikasi Anda di Render.

```
https://your-app-name.onrender.com
```

**Contoh:**
```
https://ibgadgetstore.onrender.com
```

---

### 7. TIME_ZONE (OPSIONAL)

**Key:**
```
TIME_ZONE
```

**Value:**
```
Asia/Jakarta
```

---

## 🚀 METODE 2: TAMBAH DARI FILE .ENV (LEBIH CEPAT)

Jika Anda ingin menambahkan semua variabel sekaligus:

### Langkah 1: Siapkan File .env

1. Buka file `render.env.template` yang sudah saya buat
2. Copy semua isinya
3. Buka Notepad atau text editor
4. Paste isi file tersebut
5. **ISI** nilai-nilai yang masih `GANTI_DENGAN_...`:

   **Yang harus diganti:**
   - `SECRET_KEY` → Generate dengan command Python
   - `your-app-name` → Ganti dengan nama aplikasi Anda
   - `DATABASE_URL` → Copy dari PostgreSQL database

**Contoh hasil akhir:**
```
SECRET_KEY=abc123xyz456def789ghi012jkl345mno678pqr901stu234vwx567yz890ABC123XYZ456
DEBUG=False
DJANGO_ENVIRONMENT=production
ALLOWED_HOSTS=ibgadgetstore.onrender.com,localhost,127.0.0.1
DATABASE_URL=postgresql://ibgadgetstore_user:abc123xyz@dpg-xxxxx-a.singapore-postgres.render.com/ibgadgetstore
BASE_URL=https://ibgadgetstore.onrender.com
TIME_ZONE=Asia/Jakarta
```

### Langkah 2: Paste ke Render.com

1. Di halaman Web Service → tab **"Environment"**
2. Scroll ke bagian **"Environment Variables"**
3. Klik tombol **"+ Tambahkan dari .env"** atau **"+ Add from .env"**
4. Modal dialog akan muncul
5. **PASTE** semua isi file .env yang sudah Anda siapkan ke text area
6. Klik **"Tambahkan variabel"** atau **"Add variables"**
7. Semua variabel akan langsung ditambahkan sekaligus!

---

## ✅ VERIFIKASI ENVIRONMENT VARIABLES

Setelah menambahkan semua variabel, pastikan:

1. Di tab **"Environment"**, scroll ke bagian **"Environment Variables"**
2. Anda harus melihat semua variabel berikut:
   - ✅ SECRET_KEY
   - ✅ DEBUG
   - ✅ DJANGO_ENVIRONMENT
   - ✅ ALLOWED_HOSTS
   - ✅ DATABASE_URL
   - (Opsional) BASE_URL
   - (Opsional) TIME_ZONE

3. **JANGAN** ada variabel yang Value-nya masih kosong atau masih `GANTI_DENGAN_...`

---

## 🔍 CARA CEK NILAI VARIABLES

Untuk melihat nilai variabel yang sudah diset:

1. Di tab **"Environment"**
2. Scroll ke **"Environment Variables"**
3. Anda akan melihat list semua variabel dengan:
   - **Key** di kolom kiri
   - **Value** di kolom kanan (nilai akan disembunyikan untuk security)

**Untuk melihat nilai:**
- Klik icon mata 👁️ di sebelah Value (jika tersedia)
- Atau klik variabel untuk edit dan lihat nilainya

---

## ✏️ CARA EDIT VARIABLE

Jika ada variabel yang salah:

1. Di tab **"Environment"** → **"Environment Variables"**
2. Cari variabel yang ingin diubah
3. Klik variabel tersebut atau klik icon edit ✏️
4. Ubah Value-nya
5. Klik **"Save"** atau **"Update"**

---

## 🗑️ CARA HAPUS VARIABLE

Jika ada variabel yang tidak diperlukan:

1. Di tab **"Environment"** → **"Environment Variables"**
2. Cari variabel yang ingin dihapus
3. Klik icon trash 🗑️ atau icon X
4. Konfirmasi penghapusan

---

## ⚠️ PENTING!

1. **JANGAN** commit file `.env` ke Git repository (sudah ada di .gitignore)
2. **JANGAN** share SECRET_KEY atau DATABASE_URL ke publik
3. Setelah menambah/edit variabel, aplikasi akan **otomatis restart**
4. Pastikan semua variabel sudah benar sebelum deploy

---

## 🎯 CONTOH LENGKAP

Berikut contoh lengkap environment variables yang sudah diisi dengan benar:

```
SECRET_KEY=django-insecure-abc123xyz456def789ghi012jkl345mno678pqr901stu234vwx567yz890ABC123XYZ456DEF789
DEBUG=False
DJANGO_ENVIRONMENT=production
ALLOWED_HOSTS=ibgadgetstore.onrender.com,localhost,127.0.0.1
DATABASE_URL=postgresql://ibgadgetstore_user:abc123xyz456@dpg-abcdefghijklmnop-a.singapore-postgres.render.com/ibgadgetstore_abcd
BASE_URL=https://ibgadgetstore.onrender.com
TIME_ZONE=Asia/Jakarta
```

---

## 🆘 TROUBLESHOOTING

### Problem: Variabel tidak tersimpan

**Solusi:**
- Pastikan tidak ada spasi sebelum/sesudah `=` (tanda sama dengan)
- Pastikan Key tidak ada spasi
- Pastikan Value tidak kosong

### Problem: Aplikasi error setelah set variabel

**Solusi:**
- Cek log di tab **"Logs"**
- Pastikan SECRET_KEY sudah benar (panjang minimal 50 karakter)
- Pastikan DATABASE_URL format benar (harus dimulai dengan `postgresql://`)
- Pastikan ALLOWED_HOSTS sudah termasuk domain Render

### Problem: Tidak bisa edit variabel

**Solusi:**
- Pastikan Anda login sebagai owner repository
- Coba refresh halaman
- Coba logout dan login lagi

---

## ✅ CHECKLIST

Sebelum lanjut deploy, pastikan:

- [ ] SECRET_KEY sudah di-generate dan diisi
- [ ] DEBUG sudah diset ke `False`
- [ ] DJANGO_ENVIRONMENT sudah diset ke `production`
- [ ] ALLOWED_HOSTS sudah termasuk domain Render Anda
- [ ] DATABASE_URL sudah di-copy dari PostgreSQL database
- [ ] Semua variabel sudah tersimpan (lihat di list Environment Variables)
- [ ] Tidak ada variabel yang Value-nya kosong

---

**Setelah semua environment variables sudah diisi, aplikasi siap untuk di-deploy! 🚀**

