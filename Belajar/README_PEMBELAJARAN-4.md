# 📖 README PEMBELAJARAN - Sneat Django Admin Dashboard

## Selamat Datang! 👋

Dokumen ini adalah **panduan lengkap** untuk mempelajari proyek **Sneat Bootstrap HTML Django Admin Template Free v3.0.0**.

## 📚 Dokumen yang Tersedia

### 1. **PANDUAN_PEMBELAJARAN_SNEAT_DJANGO.md** ⭐ (WAJIB DIBACA)
   - **Panduan lengkap** dari awal hingga akhir
   - Konsep Django, Python, dan Sneat Dashboard
   - Penjelasan setiap file dan folder
   - Command-line tools Django
   - Tutorial membuat CRUD lengkap
   - **Mulai dari sini!**

### 2. **QUICK_REFERENCE.md** 🚀
   - Cheat sheet cepat untuk referensi sehari-hari
   - Command yang sering digunakan
   - Template tags Django
   - Bootstrap classes Sneat
   - Common patterns

### 3. **DIAGRAM_ARSITEKTUR.md** 📊
   - Diagram visual arsitektur Django MVT
   - Flow request-response
   - Struktur folder
   - Relasi database
   - Template inheritance

## 🎯 Cara Menggunakan Panduan Ini

### Untuk Pemula (Baru Belajar Django)
1. ✅ Baca **PANDUAN_PEMBELAJARAN_SNEAT_DJANGO.md** dari awal
2. ✅ Ikuti tutorial step-by-step di bagian 7
3. ✅ Praktikkan membuat CRUD sederhana
4. ✅ Gunakan **QUICK_REFERENCE.md** sebagai referensi cepat
5. ✅ Lihat **DIAGRAM_ARSITEKTUR.md** untuk memahami flow

### Untuk yang Sudah Familiar dengan Django
1. ✅ Baca bagian 6 di **PANDUAN_PEMBELAJARAN_SNEAT_DJANGO.md** (CRUD dengan Sneat)
2. ✅ Lihat contoh di `apps/kpi_management/`
3. ✅ Gunakan **QUICK_REFERENCE.md** untuk syntax
4. ✅ Referensi **DIAGRAM_ARSITEKTUR.md** untuk arsitektur

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### 2. Akses Aplikasi
- **Main Dashboard**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **KPI Management**: http://127.0.0.1:8000/kpi/

### 3. Login
- Gunakan superuser yang sudah dibuat
- Atau buat user baru melalui admin panel

## 📁 Struktur Proyek Penting

```
sneat-bootstrap-html-django-admin-template-free/
├── config/              → Konfigurasi utama
│   ├── settings.py      → Pengaturan aplikasi
│   └── urls.py          → URL routing utama
│
├── apps/                → Aplikasi Django
│   └── kpi_management/ → CRUD KPI Management (CONTOH LENGKAP)
│       ├── models.py    → Database structure
│       ├── views.py     → Business logic
│       ├── forms.py     → Form handling
│       ├── urls.py      → URL routing
│       └── templates/   → HTML templates
│
├── templates/           → Template global
│   └── layout/          → Base templates
│
└── src/assets/          → Frontend assets (CSS, JS, Images)
```

## 🎓 Topik Pembelajaran

### Level 1: Dasar-dasar
- ✅ Apa itu Django, Python, Sneat Dashboard
- ✅ Struktur folder dan file
- ✅ Model, View, Template (MVT)
- ✅ URL routing

### Level 2: CRUD Operations
- ✅ Membuat Model
- ✅ Membuat Form
- ✅ Membuat View (List, Create, Update, Delete)
- ✅ Membuat Template HTML
- ✅ Menggunakan komponen Sneat Bootstrap

### Level 3: Advanced
- ✅ Authentication & Authorization
- ✅ File upload (Media files)
- ✅ Pagination
- ✅ Search & Filter
- ✅ Custom queries
- ✅ Relationships (ForeignKey, ManyToMany)

## 📖 Contoh CRUD Lengkap

Proyek ini sudah memiliki contoh CRUD lengkap di:
- **`apps/kpi_management/`**

**Model yang tersedia:**
- Story (Story Management)
- DailyFeedReels (Feed/Reels Management)
- FYPPostValue (FYP Post Management)
- Campaign (Campaign Management)
- CollabBrand (Brand Collaboration)
- Profile (User Profile)
- Company (Company Management)
- SocialMediaAccount (Social Media Account)
- Report (Report Management)
- AuditLog (Activity Log)

**Pelajari struktur CRUD ini sebagai referensi!**

## 🔧 Command Penting

```bash
# Development
python manage.py runserver          # Jalankan server
python manage.py shell              # Django shell

# Database
python manage.py makemigrations     # Buat migration
python manage.py migrate            # Terapkan migration
python manage.py showmigrations     # Lihat status migration

# User Management
python manage.py createsuperuser    # Buat admin user

# Static Files
python manage.py collectstatic      # Kumpulkan static files
```

## 🎨 Komponen Sneat yang Tersedia

- **Cards**: Card components untuk konten
- **Tables**: Table dengan styling Sneat
- **Forms**: Form components dengan Bootstrap 5
- **Buttons**: Button variants (primary, secondary, success, danger, warning)
- **Alerts**: Alert messages
- **Modals**: Modal dialogs
- **Charts**: Chart components (ApexCharts)
- **Icons**: Iconify icons

## 📝 Tips Belajar

1. **Praktik Langsung**: Jangan hanya membaca, praktikkan!
2. **Baca Kode**: Pelajari kode di `apps/kpi_management/` sebagai contoh
3. **Experiment**: Coba ubah kode dan lihat hasilnya
4. **Debug**: Gunakan `print()` atau Django shell untuk debug
5. **Documentation**: Baca dokumentasi Django resmi

## 🐛 Troubleshooting

### Error: "No module named 'apps'"
**Solusi**: Pastikan struktur folder benar dan `INSTALLED_APPS` sudah terdaftar di `settings.py`

### Error: "TemplateDoesNotExist"
**Solusi**: Pastikan template ada di folder `templates/` dan `TEMPLATES['DIRS']` setting benar

### Error: "CSRF verification failed"
**Solusi**: Tambahkan `{% csrf_token %}` di dalam tag `<form>`

### Error: "FieldError: Cannot resolve keyword"
**Solusi**: Pastikan field ada di model dan jalankan `makemigrations` & `migrate`

## 📚 Sumber Belajar Tambahan

### Dokumentasi Resmi
- **Django**: https://docs.djangoproject.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **Sneat Docs**: https://demos.themeselection.com/sneat-bootstrap-html-admin-template/documentation/

### Video Tutorial
- Django for Beginners (YouTube)
- Django Tutorial (Django Official Channel)

### Buku
- "Django for Beginners" by William S. Vincent
- "Two Scoops of Django" by Daniel & Audrey Feldroy

## 🎯 Checklist Pembelajaran

### Week 1: Dasar-dasar
- [ ] Memahami konsep Django MVT
- [ ] Memahami struktur folder proyek
- [ ] Bisa menjalankan server development
- [ ] Bisa membuat superuser dan login

### Week 2: CRUD Basics
- [ ] Membuat Model sederhana
- [ ] Membuat Form
- [ ] Membuat View (List, Create, Update, Delete)
- [ ] Membuat Template HTML
- [ ] Bisa membuat CRUD lengkap

### Week 3: Advanced Features
- [ ] Menggunakan komponen Sneat Bootstrap
- [ ] Implementasi search & filter
- [ ] File upload (Media files)
- [ ] Pagination
- [ ] Authentication & Authorization

### Week 4: Project Building
- [ ] Membuat aplikasi baru
- [ ] Membuat CRUD dengan relasi
- [ ] Customisasi template Sneat
- [ ] Deploy aplikasi

## 💡 Next Steps

Setelah memahami dasar-dasar:

1. **Eksplorasi Kode**: Pelajari lebih dalam kode di `apps/kpi_management/`
2. **Buat Aplikasi Baru**: Coba buat aplikasi CRUD baru sendiri
3. **Customisasi**: Ubah tampilan menggunakan komponen Sneat
4. **Deploy**: Pelajari cara deploy Django ke production

## 🤝 Kontribusi

Jika menemukan kesalahan atau ingin menambahkan konten:
1. Buat issue di repository
2. Atau submit pull request

## 📞 Support

Untuk pertanyaan atau bantuan:
- Baca dokumentasi di folder ini
- Cek dokumentasi Django resmi
- Cek dokumentasi Sneat

---

## 🎉 Selamat Belajar!

Ingat: **Praktik adalah kunci!** Jangan hanya membaca, praktikkan langsung.

**Happy Coding! 🚀**

