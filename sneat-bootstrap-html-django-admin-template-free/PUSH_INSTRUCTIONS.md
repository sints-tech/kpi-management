# 🚀 Instruksi Push ke GitHub

## Repository yang Benar
**URL Repository**: `https://github.com/sints-tech/kpi-management.git`

## Langkah-langkah di Git Bash:

### 1. Masuk ke directory project
```bash
cd /d/sneat-bootstrap-html-django-admin-template-free-v3.0.0/sneat-bootstrap-html-django-admin-template-free
```

### 2. Jalankan script push
```bash
bash push-to-github.sh
```

### ATAU Jalankan manual (jika script tidak berjalan):

```bash
# Update remote URL
git remote set-url origin https://github.com/sints-tech/kpi-management.git

# Verifikasi remote
git remote -v

# Cek status
git status

# Tambahkan file yang diubah
git add build.sh
git add requirements.txt
git add config/settings.py
git add web_project/views.py
git add gunicorn-cfg.py
git add RENDER_DEPLOYMENT.md

# Commit
git commit -m "Fix: Perbaikan deployment Render.com - Install Pillow secara eksplisit dan konfigurasi production"

# Push ke GitHub
git push origin main
```

## File yang akan di-push:
- ✅ `build.sh` - Install Pillow terlebih dahulu
- ✅ `requirements.txt` - Pillow==10.4.0
- ✅ `config/settings.py` - CSRF_TRUSTED_ORIGINS
- ✅ `web_project/views.py` - Handler 404/400/500
- ✅ `gunicorn-cfg.py` - Konfigurasi PORT
- ✅ `RENDER_DEPLOYMENT.md` - Dokumentasi

## Setelah Push:
Jika Render.com sudah dikonfigurasi dengan auto-deploy dari repository ini, deployment baru akan otomatis dimulai.


