# 🗄️ CARA MEMBUAT DATABASE POSTGRESQL DI RENDER.COM DAN MENDAPATKAN DATABASE_URL

Panduan lengkap langkah demi langkah untuk membuat database PostgreSQL di Render.com dan mendapatkan DATABASE_URL-nya.

---

## 📍 LANGKAH 1: BUAT POSTGRESQL DATABASE DI RENDER

### Step 1: Login ke Render.com

1. Buka browser, kunjungi: **https://render.com**
2. Login dengan akun GitHub/GitLab/Bitbucket Anda
3. Setelah login, Anda akan masuk ke **Dashboard**

---

### Step 2: Buat PostgreSQL Database Baru

1. Di dashboard Render, lihat bagian **"New +"** (tombol di pojok kanan atas)
2. Klik tombol **"New +"**
3. Menu dropdown akan muncul dengan beberapa pilihan:
   - Web Service
   - Background Worker
   - PostgreSQL
   - Redis
   - Static Site
   - dll

4. **KLIK** **"PostgreSQL"**

---

### Step 3: Isi Form Konfigurasi Database

Setelah klik PostgreSQL, form akan muncul. Isi dengan detail berikut:

#### **Name:**
```
ibgadgetstore-db
```
atau nama lain yang Anda inginkan (contoh: `myapp-db`, `django-db`)

**Catatan:** Nama ini hanya untuk identifikasi di dashboard Render, bisa diubah sesuai keinginan.

---

#### **Database:**
```
ibgadgetstore
```
atau nama lain (contoh: `myapp`, `djangodb`)

**Catatan:** Ini adalah nama database yang sebenarnya di PostgreSQL.

---

#### **User:**
```
ibgadgetstore_user
```
atau biarkan default (Render akan generate otomatis)

**Catatan:** Ini adalah username untuk koneksi database.

---

#### **Region:**
Pilih dari dropdown:
```
Singapore
```
atau region terdekat dengan Indonesia:
- **Singapore** (terdekat untuk Indonesia)
- **Oregon** (US West)
- **Frankfurt** (Europe)

**⚠️ PENTING:** Pilih region yang sama dengan Web Service Anda nanti!

---

#### **PostgreSQL Version:**
Pilih dari dropdown:
```
16
```
atau versi terbaru yang tersedia (biasanya 15 atau 16)

---

#### **Plan:**
Pilih:
```
Free
```
(untuk testing, bisa upgrade nanti ke Starter $7/bulan atau Professional $20/bulan)

**Catatan Free Plan:**
- ✅ Gratis
- ✅ 90 hari data retention
- ✅ Cocok untuk development/testing
- ❌ Akan dihapus jika tidak digunakan selama 90 hari

---

### Step 4: Create Database

1. Setelah semua field terisi, scroll ke bawah
2. Klik tombol **"Create Database"**
3. **TUNGGU** proses pembuatan database (sekitar 1-2 menit)
   - Status akan berubah: "Creating" → "Available"
   - Jangan tutup browser selama proses ini!

---

## 📍 LANGKAH 2: MENDAPATKAN DATABASE_URL

Setelah database selesai dibuat dan status menjadi **"Available"**:

### Step 1: Buka Halaman Database

1. Di dashboard Render, Anda akan melihat database baru muncul di list
2. **KLIK** database tersebut (nama yang Anda berikan, contoh: `ibgadgetstore-db`)

---

### Step 2: Cari Connection Info

Di halaman database, Anda akan melihat beberapa tab:
- Overview
- Connections
- Backups
- Settings
- dll

**KLIK** tab **"Connections"** atau cari bagian **"Connection Info"**

---

### Step 3: Copy Database URL

Di tab Connections, Anda akan melihat beberapa informasi:

#### **Internal Database URL** (untuk koneksi dari Web Service di Render)
```
postgresql://user:password@host:port/database
```

#### **External Database URL** (untuk koneksi dari luar Render)
```
postgresql://user:password@host:port/database
```

**⚠️ PENTING:** Gunakan **"External Database URL"** untuk Environment Variable!

---

### Step 4: Copy URL

1. Di bagian **"External Database URL"**, Anda akan melihat URL seperti ini:
   ```
   postgresql://ibgadgetstore_user:abc123xyz456@dpg-abcdefghijklmnop-a.singapore-postgres.render.com/ibgadgetstore_abcd
   ```

2. **KLIK** icon copy 📋 di sebelah URL (atau klik URL untuk select all, lalu Ctrl+C)

3. **PASTE** ke notepad untuk disimpan sementara

**Format DATABASE_URL biasanya seperti ini:**
```
postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE_NAME]
```

**Contoh lengkap:**
```
postgresql://ibgadgetstore_user:abc123xyz456def789@dpg-abcdefghijklmnop-a.singapore-postgres.render.com:5432/ibgadgetstore_abcd
```

---

## 📍 LANGKAH 3: GUNAKAN DATABASE_URL DI ENVIRONMENT VARIABLES

Setelah mendapatkan DATABASE_URL:

### Step 1: Buka Web Service

1. Kembali ke dashboard Render (klik logo Render di kiri atas)
2. Klik **Web Service** yang sudah Anda buat
   - Jika belum buat Web Service, buat dulu (lihat panduan deployment)

### Step 2: Tambahkan Environment Variable

1. Di halaman Web Service, klik tab **"Environment"**
2. Scroll ke bagian **"Environment Variables"**
3. Klik **"+ Tambahkan Variabel Lingkungan"** atau **"+ Add Environment Variable"**
4. Isi form:
   - **Key:** `DATABASE_URL`
   - **Value:** (paste DATABASE_URL yang sudah di-copy)
5. Klik **"Add"** atau **"Save"**

---

## 🔍 CARA ALTERNATIF: MENDAPATKAN DATABASE_URL DARI OVERVIEW

Jika tidak menemukan tab Connections:

1. Di halaman database, cari bagian **"Connection Info"** atau **"Database URL"**
2. Biasanya ada di bagian **Overview** atau **Info**
3. Cari teks yang dimulai dengan `postgresql://`
4. Copy URL tersebut

---

## 📋 INFORMASI DATABASE YANG PERLU ANDA CATAT

Setelah membuat database, catat informasi berikut:

- **Database Name:** `ibgadgetstore` (atau nama yang Anda pilih)
- **Database User:** `ibgadgetstore_user` (atau yang di-generate Render)
- **Database Host:** `dpg-xxxxx-a.singapore-postgres.render.com` (dari URL)
- **Database Port:** `5432` (default PostgreSQL)
- **Database URL:** `postgresql://user:password@host:port/database` (lengkap)

**⚠️ PENTING:** Simpan informasi ini dengan aman, terutama password!

---

## ✅ VERIFIKASI DATABASE_URL

Setelah menambahkan DATABASE_URL ke Environment Variables:

1. Di tab **"Environment"** → **"Environment Variables"**
2. Cari variabel `DATABASE_URL`
3. Klik variabel tersebut untuk melihat nilainya
4. Pastikan URL dimulai dengan `postgresql://`
5. Pastikan URL lengkap (tidak ada bagian yang terpotong)

---

## 🆘 TROUBLESHOOTING

### Problem: Tidak menemukan tab Connections

**Solusi:**
- Cek di tab **"Overview"** atau **"Info"**
- Scroll ke bawah, cari bagian **"Connection Info"**
- Atau cari teks **"External Database URL"**

### Problem: Database URL tidak muncul

**Solusi:**
- Pastikan database status sudah **"Available"** (bukan "Creating")
- Refresh halaman (F5)
- Tunggu beberapa detik, database URL mungkin perlu waktu untuk generate

### Problem: Tidak bisa copy URL

**Solusi:**
- Klik URL untuk select all, lalu Ctrl+C (Windows) atau Cmd+C (Mac)
- Atau klik icon copy jika tersedia
- Atau manual copy dengan select text

### Problem: Database URL tidak valid

**Solusi:**
- Pastikan URL dimulai dengan `postgresql://`
- Pastikan tidak ada spasi di awal/akhir URL
- Pastikan semua bagian URL lengkap (user, password, host, port, database)

---

## 📝 CONTOH LENGKAP DATABASE_URL

Berikut contoh lengkap DATABASE_URL yang benar:

```
postgresql://ibgadgetstore_user:abc123xyz456def789ghi012@dpg-abcdefghijklmnop-a.singapore-postgres.render.com:5432/ibgadgetstore_abcd
```

**Struktur:**
- `postgresql://` → Protocol
- `ibgadgetstore_user` → Username
- `:` → Separator
- `abc123xyz456def789ghi012` → Password
- `@` → Separator
- `dpg-abcdefghijklmnop-a.singapore-postgres.render.com` → Host
- `:5432` → Port (default PostgreSQL)
- `/ibgadgetstore_abcd` → Database name

---

## 🎯 CHECKLIST

Sebelum lanjut, pastikan:

- [ ] Sudah login ke Render.com
- [ ] Sudah klik "New +" → "PostgreSQL"
- [ ] Sudah isi form konfigurasi database
- [ ] Sudah klik "Create Database"
- [ ] Database status sudah "Available"
- [ ] Sudah buka halaman database
- [ ] Sudah klik tab "Connections" atau cari "Connection Info"
- [ ] Sudah copy "External Database URL"
- [ ] Sudah paste DATABASE_URL ke Environment Variables di Web Service
- [ ] DATABASE_URL sudah tersimpan dengan benar

---

## 🚀 LANGKAH SELANJUTNYA

Setelah mendapatkan DATABASE_URL dan menambahkannya ke Environment Variables:

1. ✅ Pastikan semua Environment Variables sudah lengkap
2. ✅ Pastikan Web Service sudah dibuat
3. ✅ Tunggu build dan deploy selesai
4. ✅ Jalankan migrations di Shell: `python manage.py migrate`
5. ✅ Buat superuser (opsional): `python manage.py createsuperuser`
6. ✅ Test aplikasi di browser

---

**Setelah database dibuat dan DATABASE_URL sudah di-set, aplikasi siap untuk di-deploy! 🚀**

