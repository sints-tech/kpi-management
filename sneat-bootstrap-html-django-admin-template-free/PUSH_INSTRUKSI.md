# 🚀 Instruksi Push ke GitHub

## Masalah yang Terjadi:
Error: `Repository not found` - Repository belum dibuat di GitHub atau URL salah.

## Solusi:

### Opsi 1: Buat Repository Baru di GitHub (Disarankan)

1. **Buka GitHub dan login**: https://github.com/sints-tech
2. **Klik "New" untuk membuat repository baru**
3. **Isi detail repository:**
   - Repository name: `sneat-bootstrap-html-django-admin-template-free-v3.0.0`
   - Description: (opsional)
   - Visibility: Public atau Private (sesuai kebutuhan)
   - **JANGAN** centang "Initialize with README"
   - **JANGAN** centang "Add .gitignore"
   - **JANGAN** centang "Choose a license"
4. **Klik "Create repository"**

### Opsi 2: Update Remote URL (Jika Repository Sudah Ada dengan Nama Berbeda)

```bash
# Di Git Bash, jalankan:
cd sneat-bootstrap-html-django-admin-template-free

# Cek remote saat ini
git remote -v

# Update remote URL jika perlu
git remote set-url origin https://github.com/sints-tech/NAMA_REPOSITORY_YANG_BENAR.git
```

### Opsi 3: Gunakan Script Push

Setelah repository dibuat di GitHub, jalankan script:

```bash
cd sneat-bootstrap-html-django-admin-template-free
bash push-to-github.sh
```

### Opsi 4: Push Manual

```bash
cd sneat-bootstrap-html-django-admin-template-free

# 1. Add files
git add build.sh requirements.txt config/settings.py web_project/views.py gunicorn-cfg.py RENDER_DEPLOYMENT.md

# 2. Commit
git commit -m "Fix: Perbaikan deployment Render.com - Install Pillow secara eksplisit dan konfigurasi production"

# 3. Push (setelah repository dibuat di GitHub)
git push -u origin main
```

## Catatan Penting:

- **Jika repository baru dibuat**, gunakan `git push -u origin main` untuk pertama kali
- **Jika menggunakan branch master**, ganti `main` dengan `master`
- **Jika memerlukan authentication**, GitHub sekarang menggunakan Personal Access Token, bukan password

## Setup Personal Access Token (jika diperlukan):

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Berikan permission: `repo`
4. Copy token
5. Saat push, gunakan token sebagai password (username tetap username GitHub)

## Setelah Push Berhasil:

1. Render.com akan otomatis detect perubahan jika auto-deploy sudah dikonfigurasi
2. Atau manual trigger deployment di dashboard Render.com
3. Build akan menggunakan `build.sh` yang baru dengan instalasi Pillow

