# 📝 Instruksi Commit & Push ke GitHub

File sudah diupdate, sekarang perlu commit dan push ke GitHub secara manual.

## Langkah-langkah:

### 1. Buka Terminal/Git Bash
Pastikan Anda berada di root directory project:
```bash
cd D:\sneat-bootstrap-html-django-admin-template-free-v3.0.0
```

### 2. Masuk ke subdirectory project
```bash
cd sneat-bootstrap-html-django-admin-template-free
```

### 3. Cek status perubahan
```bash
git status
```

### 4. Tambahkan file yang diubah
```bash
git add build.sh
git add requirements.txt
git add config/settings.py
git add web_project/views.py
git add gunicorn-cfg.py
git add RENDER_DEPLOYMENT.md
```

Atau tambahkan semua perubahan:
```bash
git add .
```

### 5. Commit perubahan
```bash
git commit -m "Fix: Perbaikan deployment Render.com - Install Pillow secara eksplisit dan konfigurasi production"
```

### 6. Push ke GitHub
```bash
git push origin main
```

Atau jika branch Anda berbeda (misalnya master):
```bash
git push origin master
```

## File yang telah diubah:
- ✅ `build.sh` - Install Pillow secara eksplisit sebelum dependencies lain
- ✅ `requirements.txt` - Memastikan Pillow==10.4.0 ada
- ✅ `config/settings.py` - CSRF_TRUSTED_ORIGINS untuk Render.com
- ✅ `web_project/views.py` - Perbaikan handler 404/400/500
- ✅ `gunicorn-cfg.py` - Konfigurasi PORT dari Render.com
- ✅ `RENDER_DEPLOYMENT.md` - Dokumentasi deployment

## Catatan:
Setelah push ke GitHub, Render.com akan otomatis trigger deployment baru jika sudah dikonfigurasi dengan auto-deploy.

