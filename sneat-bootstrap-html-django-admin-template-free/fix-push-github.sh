#!/bin/bash
# Script untuk fix dan push ke GitHub

echo "🔍 Diagnosis Masalah GitHub Push..."
echo ""

# 1. Cek apakah file sudah di-commit
echo "📊 1. Mengecek status git dan commit terakhir..."
git status
echo ""
git log --oneline -5
echo ""

# 2. Cek apakah ada perubahan yang belum di-commit
echo "📋 2. Mengecek perubahan yang belum di-track..."
git diff --name-only
git diff --cached --name-only
echo ""

# 3. Cek apakah file build.sh ada dan sudah di-track
echo "🔍 3. Mengecek apakah file penting sudah ada di git..."
git ls-files | grep -E "(build.sh|requirements.txt|config/settings.py|web_project/views.py|gunicorn-cfg.py)"
echo ""

# 4. Cek remote
echo "🌐 4. Mengecek remote repository..."
git remote -v
echo ""

# 5. Cek apakah file sudah ada perubahan
echo "📝 5. Mengecek perbedaan dengan commit terakhir..."
git diff HEAD -- build.sh requirements.txt config/settings.py web_project/views.py gunicorn-cfg.py 2>/dev/null | head -20
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "📌 SOLUSI MASALAH AUTHENTICATION GITHUB:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Error 403 berarti akun 'ibgadgetstore' tidak punya akses."
echo ""
echo "PILIHAN SOLUSI:"
echo ""
echo "1️⃣ Gunakan Personal Access Token (PAT):"
echo "   - Buka: https://github.com/settings/tokens"
echo "   - Buat token baru dengan permission 'repo'"
echo "   - Gunakan token saat push:"
echo "     git push https://<TOKEN>@github.com/sints-tech/kpi-management.git main"
echo ""
echo "2️⃣ Atau gunakan SSH (jika sudah setup):"
echo "   git remote set-url origin git@github.com:sints-tech/kpi-management.git"
echo "   git push origin main"
echo ""
echo "3️⃣ Atau pastikan akun 'sints-tech' yang digunakan untuk push"
echo ""
echo "═══════════════════════════════════════════════════════════"


