#!/bin/bash
# Script untuk push perubahan ke GitHub

echo "🚀 Memulai proses push ke GitHub..."

# Masuk ke subdirectory project
cd sneat-bootstrap-html-django-admin-template-free

# Cek apakah kita sudah di directory yang benar
if [ ! -f "build.sh" ]; then
    echo "❌ Error: build.sh tidak ditemukan. Pastikan Anda berada di directory yang benar."
    exit 1
fi

echo "✅ Directory benar, file build.sh ditemukan"

# Cek remote repository
echo "📡 Mengecek remote repository..."
git remote -v

# Cek status git
echo "📋 Status perubahan:"
git status

# Add file yang sudah diubah
echo "➕ Menambahkan file yang diubah..."
git add build.sh
git add requirements.txt
git add config/settings.py
git add web_project/views.py
git add gunicorn-cfg.py
git add RENDER_DEPLOYMENT.md

# Tampilkan file yang akan di-commit
echo "📝 File yang akan di-commit:"
git status --short

# Commit perubahan
echo "💾 Melakukan commit..."
git commit -m "Fix: Perbaikan deployment Render.com - Install Pillow secara eksplisit dan konfigurasi production

- Install Pillow terlebih dahulu sebelum dependencies lain di build.sh
- Tambah CSRF_TRUSTED_ORIGINS untuk Render.com di settings.py
- Perbaiki handler 404/400/500 di web_project/views.py
- Update gunicorn-cfg.py untuk menggunakan PORT dari Render.com
- Tambah dokumentasi RENDER_DEPLOYMENT.md"

# Push ke GitHub
echo "⬆️  Push ke GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Berhasil push ke GitHub!"
    echo "🔄 Render.com akan otomatis trigger deployment jika auto-deploy sudah dikonfigurasi"
else
    echo "❌ Gagal push ke GitHub. Periksa remote repository dan koneksi."
    echo "💡 Jika remote belum dikonfigurasi, gunakan:"
    echo "   git remote add origin <URL_REPOSITORY_GITHUB>"
    exit 1
fi

