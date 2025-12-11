# 🔧 Fix Push ke GitHub - Error 403 Permission Denied

## ❌ Masalah yang Terjadi:
1. **Error 403**: `Permission to sints-tech/kpi-management.git denied to ibgadgetstore`
   - Akun GitHub "ibgadgetstore" tidak punya akses ke repository "sints-tech/kpi-management"

2. **File tidak ter-commit**: "nothing added to commit"
   - Mungkin file sudah di-commit sebelumnya atau tidak ada perubahan

## ✅ Solusi:

### **Langkah 1: Diagnosa Masalah**
Jalankan script diagnosis:
```bash
bash fix-push-github.sh
```

### **Langkah 2: Pilih Salah Satu Metode Authentication**

#### **Opsi A: Menggunakan Personal Access Token (PAT)** ⭐ Recommended

1. **Buat Personal Access Token:**
   - Buka: https://github.com/settings/tokens
   - Klik "Generate new token (classic)"
   - Beri nama token (misalnya: "kpi-management-push")
   - Centang permission: **`repo`** (full control of private repositories)
   - Klik "Generate token"
   - **COPY TOKEN** (hanya muncul sekali!)

2. **Push menggunakan token:**
   ```bash
   # Ganti <YOUR_TOKEN> dengan token yang sudah dibuat
   git push https://<YOUR_TOKEN>@github.com/sints-tech/kpi-management.git main
   ```

   Atau set remote dengan token:
   ```bash
   git remote set-url origin https://<YOUR_TOKEN>@github.com/sints-tech/kpi-management.git
   git push origin main
   ```

#### **Opsi B: Menggunakan SSH** (Jika sudah setup SSH key)

```bash
# Ubah remote ke SSH
git remote set-url origin git@github.com:sints-tech/kpi-management.git

# Push
git push origin main
```

#### **Opsi C: Login dengan Akun yang Benar**

Pastikan menggunakan akun GitHub "sints-tech":
```bash
# Cek credential yang tersimpan
git config --global user.name
git config --global user.email

# Update jika perlu
git config --global user.name "sints-tech"
git config --global user.email "email@sints-tech.com"

# Clear cached credentials
git credential-cache exit
# atau di Windows:
git credential-manager-core erase https://github.com

# Push lagi (akan diminta login)
git push origin main
```

### **Langkah 3: Pastikan File Sudah Di-commit**

Jika file belum di-commit, jalankan:
```bash
# Cek perubahan
git status

# Tambahkan file yang diubah
git add build.sh requirements.txt config/settings.py web_project/views.py gunicorn-cfg.py RENDER_DEPLOYMENT.md

# Commit
git commit -m "Fix: Perbaikan deployment Render.com - Install Pillow secara eksplisit"

# Push
git push origin main
```

## 🎯 Cara Paling Mudah (Recommended):

1. Buat Personal Access Token di GitHub
2. Gunakan perintah ini (ganti TOKEN dengan token Anda):
   ```bash
   git remote set-url origin https://TOKEN@github.com/sints-tech/kpi-management.git
   git push origin main
   ```

## ⚠️ Catatan Penting:

- **JANGAN** commit token ke repository (simpan di local saja)
- Token hanya muncul sekali saat dibuat, jadi pastikan sudah dicopy
- Jika menggunakan token di command line, jangan share ke orang lain

## ✅ Setelah Push Berhasil:

Jika Render.com sudah dikonfigurasi dengan auto-deploy dari repository ini, deployment akan otomatis dimulai.


