# Website PCM Banjarsari (Django)

Tugas 1 — Pemrograman Web berbasis Framework (TIF1336): membangun dan men-deploy website untuk
**Pimpinan Cabang Muhammadiyah (PCM) Banjarsari, Kota Surakarta** dengan Django, Docker, dan PostgreSQL.

> Website ini dibuat untuk tugas kuliah dan **bukan website resmi** PCM Banjarsari.

## Kelompok

| Nama | NIM |
|------|-----|
| Daffa Raihan Harahap | L200240203 |
| Danar Tri Prayoga | L200240185 |
| Azwar Dipo Astuko | L200240173 |
| Kaukaban Syarqi Nur Budiono | L200240176 |
| Gibran Alghifari Maulana Masli | L200240172 |

**Nama kelompok:** PCM Banjarsari

## PCM yang dipilih

- **PCM Banjarsari**, Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah (PDM Kota Surakarta, PWM Jawa Tengah).
- Sekretariat: Jl. KH. Ahmad Dahlan No. 35, Keprabon, Surakarta, telp. 0271-667533 (kontak resmi sekretariat dari kop surat PCM).
- **Pengurus yang memberi izin:** Sumardi, Sekretaris PCM Banjarsari.

## Sumber data

| Data | Sumber | Tanggal diambil |
|------|--------|-----------------|
| Susunan pimpinan 2022–2027 | SK PCM Banjarsari No. 157/KEP/IV.0/D/2023 (21 Okt 2023) dan SK PDM Kota Surakarta No. 128/KEP/III.0/D/2023 | 16 Nov 2026 |
| Sejarah dan SK pendirian cabang | SK PWM Jawa Tengah No. K/79/1978 (24 Muharram 1398 H / 4 Jan 1978 M) | 16 Nov 2026 |
| Daftar ranting, SK pendirian ranting, jumlah anggota ber-NBM (513) | Laporan Musyawarah Cabang Muhammadiyah Banjarsari 2023, hlm. 9 (angka periode 2015–2022) | 16 Nov 2026 |
| Ketua ranting Keprabon, Timuran, Punggawan, Kestalan | SK PCM No. 168, 174, 171, 169/KEP/IV.0/D/2023 (25 Des 2023) | 16 Nov 2026 |
| Ketua ranting Ketelan dan Gilingan | SK PCM No. 018/KEP/IV.0/D/2026 (26 Jun 2026) dan No. 029/KEP/IV.0/D/2026 (9 Okt 2026) | 16 Nov 2026 |
| Ketua ranting Setabelan | **Belum tersedia** (SK belum diterima), ditulis "Belum tersedia" | - |
| Amal usaha (SMA Muhammadiyah 6, 9 masjid, Wisma Musolla Pemuda) | Laporan Musycab 2023 hlm. 12; berkas "amal usaha pcm banjarsari"; papan "Tanah Milik Muhammadiyah" di lokasi | 16 Nov 2026 |
| Berita dan agenda koordinasi 16 Okt 2026 | Poster dan contoh publikasi "PCM Banjarsari News" dari pengurus | 16 Nov 2026 |
| Agenda Pengajian Hari Bermuhammadiyah (25 Okt) dan Safari Dakwah (rencana Des–Jan, belum pasti) | Berkas "kegiatan mendatang pcm banjarsari" | 16 Nov 2026 |
| Kegiatan rutin (rapat pleno, pengajian HPT, dll.) | Berkas "kegiatan rutin pcm banjarsari" | 16 Nov 2026 |
| Visi dan misi | Berkas "visi misi muhammadiyah" | 16 Nov 2026 |
| Tagline "Memajukan Banjarsari, Mencerahkan Semesta." | Sampul/footer dokumen Musycab 2023 | 16 Nov 2026 |
| Tautan PDM, PWM, PP | muhammadiyahsolo.com (tercantum di kop PDM Kota Surakarta), pwmjateng.com, muhammadiyah.or.id | 16 Nov 2026 |

### Catatan data

- Tidak ada nomor HP pribadi, alamat rumah, NIK, atau NBM pengurus yang ditampilkan.
- Data yang tidak ada (email sekretariat, alamat dan telepon ranting, ketua PRM Setabelan, dokumen unduhan, serta sebagian foto pengurus yang belum tersedia) dikosongkan atau ditulis "Belum tersedia".
- Angka **513 anggota ber-KTAM** adalah data Musycab 2023 (periode 2015–2022). Perbarui lewat admin bila ada angka terbaru.
- Aset gambar awal (hero, sampul berita, foto pimpinan, dan gambar amal usaha) disimpan di `web/seed_assets/` dan otomatis dimuat ke `media/` saat menjalankan `uv run python manage.py seed_pcm`.

## Teknologi

Python 3.12+ (Docker memakai 3.14), Django 6.x, uv, template Django (server-side), CSS buatan sendiri,
SQLite (laptop) / PostgreSQL (produksi), WhiteNoise, Gunicorn, django-storages (S3-compatible) untuk media.

## Menjalankan di laptop (uv)

```bash
uv sync
cp .env.example .env          # lalu isi; di laptop cukup DEBUG=True
uv run python manage.py migrate
uv run python manage.py seed_pcm
uv run python manage.py createsuperuser
uv run python manage.py runserver
# buka http://127.0.0.1:8000  dan  http://127.0.0.1:8000/admin/
```

Test: `uv run python manage.py test`

**Logo (wajib):** unduh [Muhammadiyah.svg](https://commons.wikimedia.org/wiki/File:Muhammadiyah.svg) dari Wikimedia Commons
**tanpa diubah**, simpan sebagai `static/img/logo-muhammadiyah.svg`, lalu commit. Atribusi CC BY-SA 4.0 sudah ada di footer.

## Menjalankan dengan Docker

```bash
docker compose up --build
# buka http://localhost:8000
docker compose exec web uv run python manage.py seed_pcm
docker compose exec web uv run python manage.py createsuperuser
```

- Database PostgreSQL 17 berjalan di service `db` (volume `postgres_data`, `healthcheck` `pg_isready`).
  Port database tidak dibuka ke host, sehingga tidak ada password yang disimpan di repo.
- `web` menunggu `db` sehat, menjalankan `migrate`, lalu Gunicorn. `SECRET_KEY` dibuat acak jika tidak ada di `.env`.
- Gambar unggahan disimpan di volume `media_data`, sehingga tetap ada setelah `docker compose down` lalu `up`.
- `docker compose down -v` **menghapus volume** (database dan gambar) sehingga semuanya kembali kosong. Gunakan hanya untuk mengulang dari awal.

## Deployment

- **Platform:** Vercel — gratis tanpa kartu kredit, serverless function dengan global CDN untuk file statis, auto-deploy dari GitHub
- **Database:** Neon (PostgreSQL serverless gratis) — direct connection untuk migrasi dari laptop, connection pooler untuk produksi
- **Object storage media:** Supabase Storage (via S3-compatible API) — gratis 1 GB, mudah diintegrasikan dengan django-storages
- **URL produksi:** https://pcm-banjarsari.vercel.app/

Langkah ringkas: atur environment variable di dashboard platform, jalankan
`DATABASE_URL=<url produksi> uv run python manage.py migrate` lalu `... seed_pcm` dari laptop, dan buat superuser.
Jika memakai pooler mode transaction (Supabase port 6543 atau Neon "-pooler"), set `DB_TRANSACTION_POOLER=True`.
Untuk migrasi di Neon, pakai koneksi *direct*.

## Environment variable

Lihat [`.env.example`](.env.example): `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`,
`DB_TRANSACTION_POOLER`, dan `AWS_*` untuk object storage.

## Struktur singkat

```
config/        settings, urls, wsgi
web/           models (+custom QuerySet), views, forms, admin, context processor, tests
web/seed_assets/  aset gambar awal untuk perintah seed_pcm
web/management/commands/seed_pcm.py   data riil PCM beserta gambar
templates/     base.html, 404.html, web/*.html (+ _kartu_berita, _item_agenda)
static/css/    site.css
```

## Kontribusi anggota

| Anggota | Dikerjakan |
|---------|------------|
| Danar Tri Prayoga | Inisialisasi proyek (struktur Django, Docker, CI, settings) |
| Daffa Raihan Harahap | fitur/model-admin — model & admin Django (A1/A3) |
| Azwar Dipo Astuko | fitur/seed-data-aset — seed_pcm data riil beserta gambar |
| Gibran Alghifari Maulana Masli | fitur/config-docker-ci — S3-compatible storage & entrypoint migrate |
| Kaukaban Syarqi Nur Budiono | fitur/deploy-vercel — deployment ke Vercel + Neon + Supabase Storage |

## Akun admin demo

Dikirim terpisah ke dosen, tidak di-commit.

## Lisensi dan atribusi

- **Logo Muhammadiyah:** K. H. Siradj Dahlan, vektor oleh Hibensis, via Wikimedia Commons, lisensi CC BY-SA 4.0.
- **Kredit foto & dokumentasi:**
  - Foto kegiatan koordinasi & hero (`IMG_4354.JPG`): Dokumentasi PCM Banjarsari (atas izin Sumardi, Sekretaris PCM Banjarsari).
  - Foto pimpinan (`IMG-20251003-WA0035.jpg`, `1691497765_9ea87bbb-3765-4dcb-afda-f977e0s3e1201.jpg`): Arsip publikasi & dokumentasi pengurus PCM Banjarsari.
  - Gambar lokasi amal usaha (`unnamed.jpg`, `unnamed.webp`, `Screenshot_*.png`): Dokumentasi lokasi & Google Maps/Street View untuk keperluan pemetaan amal usaha PCM Banjarsari.
