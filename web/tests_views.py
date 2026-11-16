from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Berita, Profil


class AksesibilitasHalamanTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nama="PCM Uji", nama_singkat="PCM Uji")

    def test_skip_link_dan_target_konten(self):
        respons = self.client.get(reverse("web:beranda"))
        self.assertContains(respons, 'href="#konten"')
        self.assertContains(respons, 'id="konten"')

    def test_menu_aktif_memakai_aria_current(self):
        respons = self.client.get(reverse("web:profil"))
        self.assertContains(respons, 'aria-current="page"')

    def test_tabel_ranting_punya_caption_aksesibel(self):
        respons = self.client.get(reverse("web:ranting"))
        self.assertContains(respons, "Daftar pimpinan ranting PCM Banjarsari")


class PaginasiPencarianTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profil.objects.create(nama="PCM Uji", nama_singkat="PCM Uji")
        sekarang = timezone.now()
        for i in range(7):
            Berita.objects.create(
                judul=f"Pengajian Ahad {i}",
                ringkasan="Ringkasan pengajian",
                isi="Isi pengajian",
                status=Berita.Status.TERBIT,
                tanggal_terbit=sekarang - timedelta(days=i),
            )
        Berita.objects.create(
            judul="Rapat Pleno",
            ringkasan="Ringkasan rapat",
            isi="Isi rapat",
            status=Berita.Status.TERBIT,
            tanggal_terbit=sekarang,
        )

    def test_paginasi_membawa_kata_kunci(self):
        respons = self.client.get(reverse("web:berita_daftar"), {"q": "pengajian"})
        self.assertEqual(len(respons.context["halaman"]), 6)
        self.assertContains(respons, "q=pengajian")
        self.assertContains(respons, "page=2")
        self.assertNotContains(respons, "Rapat Pleno")

    def test_halaman_kedua_pencarian(self):
        respons = self.client.get(
            reverse("web:berita_daftar"), {"q": "pengajian", "page": 2}
        )
        self.assertEqual(len(respons.context["halaman"]), 1)
