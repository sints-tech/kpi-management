#!/bin/bash
# Script untuk push perubahan ke GitHub

echo "🔍 Mengecek remote repository..."
git remote -v

echo ""
echo "📝 Mengupdate remote URL ke repository yang benar..."
git remote set-url origin https://github.com/sints-tech/kpi-management.git

echo ""
echo "✅ Remote URL telah diupdate:"
git remote -v

echo ""
echo "📊 Mengecek status git..."
git status

echo ""
echo "📦 Menambahkan file yang telah diubah..."
git add build.sh
git add requirements.txt
git add config/settings.py
git add web_project/views.py
git add gunicorn-cfg.py
git add RENDER_DEPLOYMENT.md

echo ""
echo "📝 Menampilkan file yang akan di-commit..."
git status

echo ""
echo "💾 Melakukan commit..."
git commit -m "Fix: Perbaikan deployment Render.com - Install Pillow secara eksplisit dan konfigurasi production"

echo ""
echo "🚀 Push ke GitHub..."
git push origin main

echo ""
echo "✅ Selesai! Perubahan telah di-push ke GitHub."
echo "🔗 Repository: https://github.com/sints-tech/kpi-management.git"
