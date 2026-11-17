"""Mengisi database kosong dengan data riil PCM Banjarsari beserta aset gambar.

Aman dijalankan berulang kali: data dicocokkan lewat nama/judul lalu diperbarui, bukan digandakan.
Sumber setiap data dicatat di README.md (tabel "Sumber data").
Data yang tidak tersedia dikosongkan, tidak dikarang.
"""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from web.models import (
    Agenda,
    AmalUsaha,
    Berita,
    Pimpinan,
    Profil,
    Ranting,
    TautanTerkait,
)

WIB = ZoneInfo("Asia/Jakarta")
ASSET = Path(__file__).resolve().parents[2] / "seed_assets"


def waktu(tahun, bulan, hari, jam=0, menit=0):
    """Jam 00:00 berarti jam acara belum diketahui (tidak ditampilkan di website)."""
    return datetime(tahun, bulan, hari, jam, menit, tzinfo=WIB)


def pasang(obj, field, relatif):
    if not relatif:
        return
    path = ASSET / relatif
    if path.exists() and not field:
        field.save(path.name, ContentFile(path.read_bytes()), save=False)


PROFIL = {
    "nama": "Pimpinan Cabang Muhammadiyah Banjarsari",
    "nama_singkat": "PCM Banjarsari",
    "tagline": "Memajukan Banjarsari, Mencerahkan Semesta.",
    "tentang": (
        "PCM Banjarsari adalah pimpinan Persyarikatan Muhammadiyah di tingkat kecamatan, "
        "yaitu Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah. Saat ini PCM Banjarsari "
        "membawahi 7 ranting: Keprabon, Timuran, Punggawan, Ketelan, Setabelan, Kestalan, dan Gilingan.\n\n"
        "Periode Muktamar ke-48 (2022–2027) dipimpin oleh DR. Rusmanto, S.Pd.I., M.Pd.I. "
        "berdasarkan SK Pimpinan Daerah Muhammadiyah Kota Surakarta Nomor 128/KEP/III.0/D/2023.\n\n"
        "Kegiatan rutin: Kamis pertama rapat pleno cabang; Kamis kedua rapat pleno bersama majelis; "
        "Kamis ketiga pengajian pimpinan (kajian Himpunan Putusan Tarjih, dasar-dasar ibadah); "
        "Kamis keempat rapat cabang diperluas yang, bila diperlukan, melibatkan pimpinan ranting dan 'Aisyiyah. "
        "Selain itu diselenggarakan Pengajian Hari Bermuhammadiyah."
    ),
    "sejarah": (
        "PCM Banjarsari disahkan berdirinya oleh Pimpinan Muhammadiyah Wilayah Jawa Tengah melalui "
        "Surat Keputusan Nomor K/79/1978, ditetapkan di Semarang pada 24 Muharram 1398 H "
        "bertepatan dengan 4 Januari 1978 M. Dalam SK tersebut cakupan wilayah cabang meliputi 5 kelurahan.\n\n"
        "Menurut laporan Musyawarah Cabang 2023, pada saat didirikan PCM Banjarsari membawahi 5 ranting "
        "dan kini membawahi 7 ranting. SK pendirian ranting Kestalan, Timuran, Punggawan, dan Keprabon "
        "bertanggal 24 Muharram 1398 H / 4 Januari 1978 M, sedangkan ranting Gilingan 16 Shofar 1401 H / "
        "24 Desember 1980 M. Arsip SK pendirian ranting Ketelan dan Setabelan belum ditemukan di sekretariat cabang."
    ),
    "visi": "Terwujudnya masyarakat Islam yang sebenar-benarnya.",
    "misi": (
        "Menegakkan Tauhid yang murni berdasarkan Al-Quran dan As-Sunnah.\n"
        "Menyebarluaskan dan memajukan Ajaran Islam yang bersumber pada Al-Quran dan As-Sunnah "
        "yang shohihah/maqbulah.\n"
        "Mewujudkan Islam dalam kehidupan pribadi, keluarga dan masyarakat."
    ),
    "alamat_sekretariat": "Jl. KH. Ahmad Dahlan No. 35, Keprabon, Surakarta",
    "telepon": "0271-667533",
    "email": "",
    "jumlah_anggota_ktam": 513,
    "gambar_hero": "hero/IMG_4354.JPG",
}

# Susunan Pimpinan PCM Banjarsari periode 2022-2027 (SK PCM No. 157/KEP/IV.0/D/2023).
PIMPINAN = [
    ("DR. Rusmanto, S.Pd.I., M.Pd.I.", "Ketua", "pimpinan/IMG-20251003-WA0035.jpg"),
    ("H.M. Dedy Purnomo, S.S., S.H., M.H.", "Wakil Ketua 1", "pimpinan/1691497765_9ea87bbb-3765-4dcb-afda-f977e0s3e1201.jpg"),
    ("Sumardi", "Sekretaris", ""),
    ("H. Wiwit Hidayat, S.E.", "Wakil Sekretaris", ""),
    ("H. Farid Tribune Unique, S.E.", "Bendahara", ""),
    ("Fatchul Hadi, S.H.", "Wakil Bendahara", ""),
    ("Drs. HM. Joko Riyanto, S.H., M.M., M.H.", "Anggota", ""),
    ("Drs. H. Sukendar, M.Pd.", "Anggota", ""),
    ("Drs. H. Mahmud Hasni", "Anggota", ""),
    ("H.M. Rochmadin Mansyur, S.E.", "Anggota", ""),
    ("Andy Ratmanto, S.H.", "Anggota", ""),
    ("Drs. Sinwan Fajar Nahari", "Anggota", ""),
]

# Ketua ranting dari SK penetapan struktur masing-masing PRM. Setabelan: SK belum diterima.
RANTING = [
    ("PRM Gilingan", "Drs. H. Sinwan Fajar Nahari", "Jl. S. Parman No. 229, Cinderejo Kidul RT 02 RW 09, Gilingan, Banjarsari", "0878 3533 5489"),
    ("PRM Keprabon", "H.M. Rochmadin Mansyur, S.E.", "Jl. KH. Ahmad Dahlan No. 35, Keprabon", "0813 2905 7993"),
    ("PRM Kestalan", "H. Heru Purwoko, S.E.", "Masjid Mukmin Kandangdoro, Jl. Mayang No. 14, Kestalan", "0812 2611 340"),
    ("PRM Ketelan", "Drs. H. Sukendar, M.Pd.", "Gedung Wisma Musolla Pemuda, Jl. Jageran No. 10, Ketelan, Banjarsari", "0821 3642 3266"),
    ("PRM Punggawan", "Joko Jaelani, S.Pd.", "Masjid Ar Ridho Bromantakan, Punggawan, Banjarsari", "0896 7228 0921"),
    ("PRM Setabelan", "H. Trijoko Suryanto, S.E.", "Masjid As Sirodj, Jl. Pringgading I, Pringgading (Ps. Legi), Setabelan", "0813 3364 1371"),
    ("PRM Timuran", "Drs. H. Mahmud Hasni", "Masjid Mukmin Priyobadan, Timuran, Banjarsari", "0819 1873 9163"),
]

AMAL_USAHA = [
    {
        "nama": "SMA Muhammadiyah 6 Surakarta",
        "bidang": AmalUsaha.Bidang.PENDIDIKAN,
        "alamat": "Jl. Banyuanyar, Banyuanyar, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57137",
        "deskripsi": "Sekolah menengah atas amal usaha Muhammadiyah di wilayah Banjarsari.",
        "gambar": "amal-usaha/unnamed.jpg",
    },
    {
        "nama": "Wisma Musolla Pemuda",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Jageran No. 10, Ketelan, Banjarsari, Surakarta",
        "deskripsi": (
            "Gedung wakaf di Jageran, Ketelan. Papan di lokasi menyebutnya tanah milik Muhammadiyah "
            "Kota Surakarta (nomor HMW 1, luas 214 m²)."
        ),
        "gambar": "amal-usaha/unnamed.webp",
    },
    {
        "nama": "Masjid Muhammadiyah Balai",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Teuku Umar, Keprabon, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57131",
        "deskripsi": (
            "Masjid Muhammadiyah Balai beralamat di Jl. Teuku Umar, Keprabon, Kecamatan Banjarsari, "
            "Kota Surakarta, Jawa Tengah 57131. Masjid ini berada di lingkungan Persyarikatan Muhammadiyah "
            "dan menjadi pusat ibadah serta kegiatan dakwah jamaah di sekitarnya."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_194249.png",
    },
    {
        "nama": "Masjid Sontohartanan",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. K.H Ahmad Dahlan No.25, Keprabon, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57131",
        "deskripsi": (
            "Masjid Sontohartanan beralamat di Jl. K.H. Ahmad Dahlan No. 25, Keprabon, Kecamatan Banjarsari, "
            "Kota Surakarta, Jawa Tengah 57131. Masjid ini memiliki nilai sejarah yang penting bagi persyarikatan, "
            "karena menjadi tempat lahirnya Muhammadiyah dan 'Aisyiyah di Kota Surakarta. Kini masjid tersebut "
            "dikenang sebagai monumen perjalanan dakwah Muhammadiyah dan 'Aisyiyah di Kota Surakarta."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_195037.png",
    },
    {
        "nama": "Masjid Nur Rohim Keprabon",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Saparua 3, Keprabon, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57131",
        "deskripsi": (
            "Masjid Nur Rohim berlokasi di Jl. Saparua 3, Keprabon, Kecamatan Banjarsari, "
            "Kota Surakarta, Jawa Tengah 57131. Masjid ini melayani kebutuhan ibadah dan kegiatan "
            "keagamaan jamaah di lingkungan Keprabon."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_195704.png",
    },
    {
        "nama": "Masjid As Siraaj",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Pringgading II, RT.01/RW.IX, Setabelan, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57139",
        "deskripsi": (
            "Masjid As Siraaj berlokasi di Jl. Pringgading II, RT 01/RW IX, Kelurahan Setabelan, "
            "Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah 57139. Masjid ini melayani kebutuhan ibadah "
            "dan kegiatan keagamaan jamaah di lingkungan Setabelan."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_200243.png",
    },
    {
        "nama": "Masjid Al-Mubarokah",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Sambeng, Mangkubumen, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57139",
        "deskripsi": (
            "Masjid Al-Mubarokah berlokasi di Jl. Sambeng, Kelurahan Mangkubumen, Kecamatan Banjarsari, "
            "Kota Surakarta, Jawa Tengah 57139. Masjid ini melayani kebutuhan ibadah dan kegiatan "
            "keagamaan jamaah di lingkungan Mangkubumen."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_200623.png",
    },
    {
        "nama": "Masjid Al Falah Solo",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Manunggal No.RT.01/14, Banjarsari, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57136",
        "deskripsi": (
            "Masjid Al Falah berlokasi di Jl. Manunggal, RT 01/RW 14, Kelurahan Banjarsari, "
            "Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah 57136. Masjid ini melayani kebutuhan ibadah "
            "dan kegiatan keagamaan jamaah di lingkungan sekitarnya."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_201100.png",
    },
    {
        "nama": "Masjid As Salaam",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Rejosari, Gilingan, Banjarsari, Surakarta City, Central Java 57134",
        "deskripsi": (
            "Masjid As Salaam berlokasi di Jl. Rejosari, Kelurahan Gilingan, Kecamatan Banjarsari, "
            "Kota Surakarta, Jawa Tengah 57134. Masjid ini melayani kebutuhan ibadah dan kegiatan "
            "keagamaan jamaah di lingkungan Gilingan."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_201446.png",
    },
    {
        "nama": "Masjid Mukmin",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Mayang, Kestalan, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57139",
        "deskripsi": (
            "Masjid Mukmin berlokasi di Jl. Mayang, Kelurahan Kestalan, Kecamatan Banjarsari, "
            "Kota Surakarta, Jawa Tengah 57139. Masjid ini melayani kebutuhan ibadah dan kegiatan "
            "keagamaan jamaah di lingkungan Kestalan."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_202048.png",
    },
    {
        "nama": "Masjid H. Munawarhadi RS PKU Muhammadiyah Surakarta",
        "bidang": AmalUsaha.Bidang.SOSIAL,
        "alamat": "Jl. Ronggowarsito No.130, Timuran, Kec. Banjarsari, Kota Surakarta, Jawa Tengah 57131",
        "deskripsi": (
            "Masjid H. Munawarhadi berada di lingkungan RS PKU Muhammadiyah Surakarta, Jl. Ronggowarsito No. 130, "
            "Kelurahan Timuran, Kecamatan Banjarsari, Kota Surakarta, Jawa Tengah 57131. Masjid ini melayani "
            "kebutuhan ibadah pasien, keluarga pasien, tenaga kesehatan, dan masyarakat sekitar rumah sakit."
        ),
        "gambar": "amal-usaha/Screenshot_2026-11-16_202454.png",
    },
]

BERITA = [
    {
        "judul": "Perkuat Sinergi, PCM, PCA, dan PCPM Banjarsari Gelar Koordinasi",
        "ringkasan": (
            "PCM, PCA, dan PCPM Banjarsari berkoordinasi di SMP Muhammadiyah 1 Simpon Surakarta "
            "membahas Pengajian Hari Bermuhammadiyah dan Pengukuhan Pengurus Masjid Al Falah Gilingan."
        ),
        "isi": (
            "Alhamdulillah, PCM, PCA, dan PCPM Banjarsari melaksanakan koordinasi pada Jumat, 16 Oktober 2026, "
            "bertempat di SMP Muhammadiyah 1 Simpon Surakarta.\n\n"
            "Pertemuan ini membahas persiapan Pengajian Hari Bermuhammadiyah dan Pengukuhan Pengurus "
            "Masjid Al Falah Gilingan.\n\n"
            "Melalui koordinasi ini, pimpinan menyatukan langkah dan menguatkan kebersamaan agar kegiatan dapat "
            "terlaksana dengan baik serta membawa manfaat bagi jamaah dan masyarakat.\n\n"
            "Semoga Allah Swt. memudahkan setiap ikhtiar dan menjadikan pengabdian ini sebagai amal jariyah. Aamiin.\n\n"
            "Bersama Menguatkan Persyarikatan, Menebar Dakwah yang Mencerahkan."
        ),
        "tanggal": waktu(2026, 10, 16, 12, 0),
        "gambar_sampul": "berita/IMG_4354.JPG",
    },
]

AGENDA = [
    {
        "nama": "Koordinasi PCM, PCA, dan PCPM Banjarsari",
        "waktu_mulai": waktu(2026, 10, 16),
        "keterangan_waktu": "",
        "tempat": "SMP Muhammadiyah 1 Simpon Surakarta",
        "keterangan": "Membahas Pengajian Hari Bermuhammadiyah dan Pengukuhan Pengurus Masjid Al Falah Gilingan.",
    },
    {
        "nama": "Pengajian Hari Bermuhammadiyah",
        "waktu_mulai": waktu(2026, 10, 25),
        "keterangan_waktu": "",
        "tempat": "Masjid Al Falah Gilingan",
        "keterangan": "Pengajian bermuhammadiyah bersama jamaah dan warga persyarikatan.",
    },
    {
        "nama": "Safari Dakwah",
        "waktu_mulai": waktu(2026, 12, 1),
        "keterangan_waktu": "Rencana Desember 2026 – Januari 2027 (jadwal belum pasti)",
        "tempat": "Masjid di 5 ranting",
        "keterangan": "Waktu pelaksanaan dan daftar ranting belum ditentukan.",
    },
]

TAUTAN = [
    ("PDM Kota Surakarta", "https://muhammadiyahsolo.com"),
    ("PWM Jawa Tengah", "https://pwmjateng.com"),
    ("PP Muhammadiyah", "https://muhammadiyah.or.id"),
]


class Command(BaseCommand):
    help = "Mengisi database dengan data riil PCM Banjarsari beserta gambar (aman dijalankan berulang)."

    @transaction.atomic
    def handle(self, *args, **options):
        profil = Profil.objects.first() or Profil()
        for kolom, nilai in PROFIL.items():
            if kolom != "gambar_hero":
                setattr(profil, kolom, nilai)
        pasang(profil, profil.gambar_hero, PROFIL.get("gambar_hero", ""))
        profil.save()

        for urutan, (nama, jabatan, foto) in enumerate(PIMPINAN, start=1):
            obj, _ = Pimpinan.objects.update_or_create(
                nama=nama,
                defaults={"jabatan": jabatan, "periode": "2022–2027", "urutan": urutan},
            )
            if foto:
                pasang(obj, obj.foto, foto)
                obj.save(update_fields=["foto"])
                
        for nama, ketua, alamat, telepon in RANTING:
            Ranting.objects.update_or_create(
                nama=nama,
                defaults={
                    "ketua": ketua,
                    "alamat": alamat,
                    "telepon": telepon,
                },
            )

        # Hapus data agregat lama jika ada agar diganti 11 data riil individual
        AmalUsaha.objects.filter(nama="Masjid Milik Muhammadiyah (9 masjid)").delete()

        for data in AMAL_USAHA:
            obj, _ = AmalUsaha.objects.update_or_create(
                nama=data["nama"],
                defaults={k: data[k] for k in ("bidang", "alamat", "deskripsi")},
            )
            if data.get("gambar"):
                pasang(obj, obj.gambar, data["gambar"])
                obj.save(update_fields=["gambar"])

        for data in BERITA:
            obj, _ = Berita.objects.update_or_create(
                judul=data["judul"],
                defaults={
                    "ringkasan": data["ringkasan"],
                    "isi": data["isi"],
                    "tanggal_terbit": data["tanggal"],
                    "status": Berita.Status.TERBIT,
                },
            )
            if data.get("gambar_sampul"):
                pasang(obj, obj.gambar_sampul, data["gambar_sampul"])
                obj.save(update_fields=["gambar_sampul"])

        for data in AGENDA:
            Agenda.objects.update_or_create(
                nama=data["nama"],
                defaults={k: data[k] for k in ("waktu_mulai", "keterangan_waktu", "tempat", "keterangan")},
            )

        for urutan, (nama, url) in enumerate(TAUTAN, start=1):
            TautanTerkait.objects.update_or_create(nama=nama, defaults={"url": url, "urutan": urutan})

        self.stdout.write(self.style.SUCCESS("Data PCM Banjarsari beserta aset gambar berhasil dimuat."))
