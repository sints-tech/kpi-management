# 🎯 CARA MENGISI ENVIRONMENT VARIABLES DI RENDER.COM - LANGKAH DEMI LANGKAH

Panduan super detail dengan screenshot untuk mengisi environment variables di Render.com.

---

## 📍 LOKASI: Di Mana Mengisi Environment Variables?

1. Login ke [render.com](https://render.com)
2. Klik **Web Service** yang sudah Anda buat (nama aplikasi Anda)
3. Klik tab **"Environment"** (di bagian atas, sebelah "Logs", "Metrics", "Settings")
4. Scroll ke bawah, cari bagian **"Environment Variables"**

---

## 🚀 CARA 1: TAMBAH SATU PER SATU (MUDAH UNTUK PEMULA)

### Step-by-Step:

#### 1. Klik Tombol Tambah Variabel

Di bagian **"Environment Variables"**, klik tombol:
```
+ Tambahkan Variabel Lingkungan
```
atau
```
+ Add Environment Variable
```

#### 2. Form Akan Muncul

Anda akan melihat 2 field:
- **Key** (di kiri) - Nama variabel
- **Value** (di kanan) - Nilai variabel

#### 3. Isi Variabel Berikut Satu Per Satu:

---

### ✅ VARIABEL 1: SECRET_KEY

**Key:**
```
SECRET_KEY
```

**Value:**
Saya sudah generate untuk Anda, gunakan ini:
```
ZCGObm1yxilkE5IyR7bzXp4la9LbseVup9EnHnQkU9szuDUdZ1f0xYzfgmFWyUlEvdo
```

**Cara:**
1. Di field **Key**, ketik: `SECRET_KEY`
2. Di field **Value**, paste: `ZCGObm1yxilkE5IyR7bzXp4la9LbseVup9EnHnQkU9szuDUdZ1f0xYzfgmFWyUlEvdo`
3. Klik **"Add"** atau **"Save"**

---

### ✅ VARIABEL 2: DEBUG

**Key:**
```
DEBUG
```

**Value:**
```
False
```

**Cara:**
1. Klik **"+ Tambahkan Variabel Lingkungan"** lagi
2. Key: `DEBUG`
3. Value: `False` (huruf F besar, sisanya kecil)
4. Klik **"Add"**

---

### ✅ VARIABEL 3: DJANGO_ENVIRONMENT

**Key:**
```
DJANGO_ENVIRONMENT
```

**Value:**
```
production
```

**Cara:**
1. Klik **"+ Tambahkan Variabel Lingkungan"** lagi
2. Key: `DJANGO_ENVIRONMENT`
3. Value: `production`
4. Klik **"Add"**

---

### ✅ VARIABEL 4: ALLOWED_HOSTS

**Key:**
```
ALLOWED_HOSTS
```

**Value:**
**⚠️ PENTING:** Ganti `your-app-name` dengan nama aplikasi Anda di Render!

Format:
```
your-app-name.onrender.com,localhost,127.0.0.1
```

**Cara cek nama aplikasi:**
- Di halaman Web Service, lihat bagian **"URL"** atau **"Domain"**
- Contoh URL: `https://ibgadgetstore.onrender.com`
- Maka nama aplikasinya: `ibgadgetstore`

**Contoh jika nama aplikasi Anda "ibgadgetstore":**
```
ibgadgetstore.onrender.com,localhost,127.0.0.1
```

**Cara:**
1. Klik **"+ Tambahkan Variabel Lingkungan"** lagi
2. Key: `ALLOWED_HOSTS`
3. Value: `ibgadgetstore.onrender.com,localhost,127.0.0.1` (ganti dengan nama Anda)
4. Klik **"Add"**

---

### ✅ VARIABEL 5: DATABASE_URL (PENTING!)

**Key:**
```
DATABASE_URL
```

**Value:**
Copy dari PostgreSQL database yang sudah Anda buat.

**Cara mendapatkan DATABASE_URL:**

1. **Buka tab baru** di browser (biarkan tab Web Service terbuka)
2. Di dashboard Render, klik **PostgreSQL database** yang sudah dibuat
   - Biasanya namanya seperti: `ibgadgetstore-db`
3. Di halaman database, scroll ke bagian **"Connections"** atau **"Connection Info"**
4. Cari **"External Database URL"**
   - Formatnya: `postgresql://user:password@host:port/database`
5. **COPY** seluruh URL tersebut
6. Kembali ke tab Web Service → tab **"Environment"**
7. Klik **"+ Tambahkan Variabel Lingkungan"**
8. Key: `DATABASE_URL`
9. Value: **PASTE** URL yang sudah di-copy
10. Klik **"Add"**

**Contoh DATABASE_URL:**
```
postgresql://ibgadgetstore_user:abc123xyz@dpg-abcdefghijklmnop-a.singapore-postgres.render.com/ibgadgetstore_abcd
```

---

### ✅ VARIABEL 6: BASE_URL (OPSIONAL)

**Key:**
```
BASE_URL
```

**Value:**
Ganti dengan URL aplikasi Anda.

Format:
```
https://your-app-name.onrender.com
```

**Contoh:**
```
https://ibgadgetstore.onrender.com
```

**Cara:**
1. Klik **"+ Tambahkan Variabel Lingkungan"** lagi
2. Key: `BASE_URL`
3. Value: `https://ibgadgetstore.onrender.com` (ganti dengan URL Anda)
4. Klik **"Add"**

---

### ✅ VARIABEL 7: TIME_ZONE (OPSIONAL)

**Key:**
```
TIME_ZONE
```

**Value:**
```
Asia/Jakarta
```

**Cara:**
1. Klik **"+ Tambahkan Variabel Lingkungan"** lagi
2. Key: `TIME_ZONE`
3. Value: `Asia/Jakarta`
4. Klik **"Add"**

---

## 🚀 CARA 2: TAMBAH DARI FILE .ENV (LEBIH CEPAT)

Jika Anda ingin menambahkan semua sekaligus:

### Langkah 1: Siapkan File .env

1. Buka file `RENDER_ENV_VARIABLES.txt` yang sudah saya buat
2. Copy semua isinya
3. Buka Notepad
4. Paste isi file tersebut
5. **EDIT** bagian yang masih perlu diganti:

   **Yang HARUS diganti:**
   - `your-app-name` → Ganti dengan nama aplikasi Anda (2 tempat)
   - `GANTI_DENGAN_DATABASE_URL_DARI_POSTGRESQL` → Copy dari PostgreSQL database

**Contoh hasil akhir setelah di-edit:**
```
SECRET_KEY=ZCGObm1yxilkE5IyR7bzXp4la9LbseVup9EnHnQkU9szuDUdZ1f0xYzfgmFWyUlEvdo
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
   - Tombol ini biasanya ada di dekat tombol "+ Tambahkan Variabel Lingkungan"
4. Modal dialog akan muncul dengan text area besar
5. **PASTE** semua isi file .env yang sudah Anda edit ke text area tersebut
6. Klik tombol **"Tambahkan variabel"** atau **"Add variables"** (di bawah text area)
7. Semua variabel akan langsung ditambahkan sekaligus!

**Format yang benar di text area:**
```
KEY1=VALUE1
KEY2=VALUE2
KEY3=VALUE3
```

**JANGAN** pakai spasi sebelum/sesudah tanda `=`

---

## ✅ VERIFIKASI SETELAH MENGISI

Setelah menambahkan semua variabel:

1. Di tab **"Environment"** → scroll ke **"Environment Variables"**
2. Anda harus melihat list seperti ini:

```
✅ SECRET_KEY                    (nilai tersembunyi)
✅ DEBUG                         False
✅ DJANGO_ENVIRONMENT            production
✅ ALLOWED_HOSTS                 ibgadgetstore.onrender.com,localhost,127.0.0.1
✅ DATABASE_URL                  (nilai tersembunyi)
✅ BASE_URL                      https://ibgadgetstore.onrender.com
✅ TIME_ZONE                     Asia/Jakarta
```

3. Pastikan **SEMUA** variabel sudah ada
4. Pastikan tidak ada yang Value-nya kosong

---

## 🔍 CARA CEK NILAI VARIABLE

Untuk melihat nilai variabel yang sudah diset:

1. Di list Environment Variables, klik variabel yang ingin dilihat
2. Atau klik icon edit ✏️ di sebelah variabel
3. Nilai akan muncul di form edit

**Catatan:** 
- Nilai SECRET_KEY dan DATABASE_URL biasanya disembunyikan untuk security
- Klik icon mata 👁️ untuk melihat (jika tersedia)

---

## ✏️ CARA EDIT VARIABLE

Jika ada variabel yang salah:

1. Di list Environment Variables, klik variabel yang ingin diubah
2. Atau klik icon edit ✏️
3. Form edit akan muncul
4. Ubah Value-nya
5. Klik **"Save"** atau **"Update"**

---

## 🗑️ CARA HAPUS VARIABLE

Jika ada variabel yang tidak diperlukan:

1. Di list Environment Variables, klik icon trash 🗑️ di sebelah variabel
2. Atau klik variabel → klik icon delete
3. Konfirmasi penghapusan

---

## ⚠️ PENTING!

1. **Setelah menambah/edit variabel, aplikasi akan otomatis restart**
   - Tunggu beberapa detik hingga restart selesai
   - Status akan berubah dari "Updating" menjadi "Live"

2. **JANGAN** share SECRET_KEY atau DATABASE_URL ke publik

3. **Pastikan** semua variabel sudah benar sebelum deploy

4. **Format yang benar:**
   - ✅ `KEY=VALUE` (benar)
   - ❌ `KEY = VALUE` (salah, ada spasi)
   - ❌ `KEY=VALUE ` (salah, ada spasi di akhir)

---

## 🎯 CONTOH LENGKAP YANG SIAP PAKAI

Berikut contoh lengkap yang bisa langsung di-copy paste ke Render.com:

**GANTI bagian yang masih perlu diganti:**
- `ibgadgetstore` → Ganti dengan nama aplikasi Anda (2 tempat)
- `postgresql://...` → Ganti dengan DATABASE_URL dari PostgreSQL

```
SECRET_KEY=ZCGObm1yxilkE5IyR7bzXp4la9LbseVup9EnHnQkU9szuDUdZ1f0xYzfgmFWyUlEvdo
DEBUG=False
DJANGO_ENVIRONMENT=production
ALLOWED_HOSTS=ibgadgetstore.onrender.com,localhost,127.0.0.1
DATABASE_URL=postgresql://ibgadgetstore_user:password@dpg-xxxxx-a.singapore-postgres.render.com/ibgadgetstore
BASE_URL=https://ibgadgetstore.onrender.com
TIME_ZONE=Asia/Jakarta
```

---

## ✅ CHECKLIST FINAL

Sebelum lanjut, pastikan:

- [ ] Sudah buka tab **"Environment"** di Web Service
- [ ] Sudah klik **"+ Tambahkan Variabel Lingkungan"** atau **"+ Tambahkan dari .env"**
- [ ] SECRET_KEY sudah diisi (gunakan yang sudah saya generate)
- [ ] DEBUG sudah diset ke `False`
- [ ] DJANGO_ENVIRONMENT sudah diset ke `production`
- [ ] ALLOWED_HOSTS sudah termasuk domain Render Anda
- [ ] DATABASE_URL sudah di-copy dari PostgreSQL database
- [ ] Semua variabel sudah tersimpan (lihat di list)
- [ ] Tidak ada variabel yang Value-nya kosong

---

## 🆘 TROUBLESHOOTING

### Problem: Tombol "+ Tambahkan Variabel Lingkungan" tidak muncul

**Solusi:**
- Pastikan Anda sudah klik tab **"Environment"**
- Pastikan Anda login sebagai owner repository
- Refresh halaman (F5)

### Problem: Variabel tidak tersimpan

**Solusi:**
- Pastikan tidak ada spasi sebelum/sesudah tanda `=`
- Pastikan Key tidak kosong
- Pastikan Value tidak kosong
- Coba tambah satu per satu dulu

### Problem: Format .env tidak diterima

**Solusi:**
- Pastikan format: `KEY=VALUE` (satu variabel per baris)
- Jangan ada spasi sebelum/sesudah `=`
- Jangan ada karakter khusus yang tidak perlu

---

**Setelah semua environment variables sudah diisi, aplikasi siap untuk di-deploy! 🚀**

**Langkah selanjutnya:** Kembali ke tab **"Logs"** untuk melihat proses build dan deploy.

