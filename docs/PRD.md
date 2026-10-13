# Product Requirements Document: Mail Server Ubuntu Learning Portal

| | |
|---|---|
| **Versi** | 0.2 (draf). Menerapkan amandemen A1-A6 dari `docs/TECHNICAL-DESIGN.md` bagian 2.1 |
| **Tanggal** | 2026-10-13 |
| **Dasar** | `docs/project-audit.md` (audit awal), `docs/TECHNICAL-DESIGN.md` (rancangan teknis), dan kondisi kode saat ini |
| **Status** | Menunggu persetujuan pemilik produk |
| **Batasan dokumen** | Dokumen ini tidak mengubah implementasi yang ada. Pemisahan fitur yang sudah ada dan yang harus dikembangkan, serta metode uji tiap persyaratan, ada di **Lampiran C** |

Kata kunci kebutuhan: **MUST** (wajib), **SHOULD** (sangat dianjurkan), **MAY** (opsional). **[Asumsi]** dan **[Pertanyaan]** merujuk ke bagian 12.

Rujukan temuan audit memakai ID `F-xx` (fitur/bug), `D-xx` (deployment), `R-xx` (risiko). Catatan status: F-01 sampai F-11 sudah dikerjakan di `kurikulum-mail-server-ubuntu.html` setelah audit dan belum diuji di browser.

---

## 1. Problem Statement dan Product Vision

### 1.1 Masalah

Belajar membangun dan mengelola mail server (Postfix, Dovecot, TLS, SPF/DKIM/DMARC, hardening, operasi) menuntut jalur belajar yang panjang dan berurutan, ratusan jam, dengan banyak prasyarat. Materi yang tersedia umumnya tersebar, berbahasa Inggris, dan tidak menunjukkan urutan belajar, batas antara lab dan produksi, atau cara melacak kemajuan.

Kondisi proyek saat ini:

- Kerangka kurikulum sudah ada (16 kategori, 36 modul, 136 chapter, ±250 jam) dalam satu file HTML, tetapi **0 dari 136 chapter punya materi**.
- Menulis materi sebagai string HTML di dalam JavaScript tidak dapat dikelola (audit R-02).
- Proyek belum berada di git (audit R-01) dan belum siap dipublikasikan (audit D-01).

### 1.2 Visi

Portal belajar berbahasa Indonesia yang memandu pembelajar dari nol sampai mampu mengoperasikan mail server Ubuntu yang aman, lewat:

- **Dashboard** yang menunjukkan peta kurikulum, prasyarat, dan progres pribadi.
- **Dokumentasi** yang mudah dibaca dan dicari, ditulis dalam Markdown dan dirender oleh MkDocs Material.
- **Materi yang teruji**: setiap chapter praktik sudah dijalankan di VM nyata sebelum diterbitkan.

### 1.3 Prinsip produk

1. **Statis dan tanpa server.** Tidak ada backend, akun, atau pengumpulan data pengguna.
2. **Satu sumber kebenaran** untuk struktur kurikulum.
3. **Lab bukan produksi.** Setiap materi menegaskan batas lingkungan dan tidak menjanjikan hasil yang tidak bisa dijamin (mis. inbox placement).
4. **Bertahap.** Satu chapter per iterasi, tiap iterasi menghasilkan sesuatu yang dapat dirilis.

---

## 2. Target Pengguna dan User Journeys

### 2.1 Persona

| ID | Persona | Latar belakang | Kebutuhan utama |
|---|---|---|---|
| P1 | **Pembelajar mandiri** (utama) | Administrator atau mahasiswa TI, nyaman memakai komputer, Linux belum tentu | Jalur belajar jelas, tahu apa yang harus dipelajari berikutnya, melacak progres |
| P2 | **Pembelajar berpengalaman** | Sudah paham Linux/jaringan | Melompat ke topik tertentu (mis. DKIM), mencari cepat |
| P3 | **Penulis/pemelihara materi** (pemilik proyek, bersama Claude Code) | Menulis satu chapter per iterasi | Template jelas, validasi otomatis, rilis aman |
| P4 | **Peninjau/kontributor** (opsional di masa depan) | Mengoreksi materi | Diff yang bersih, preview per perubahan |

### 2.2 User journeys

**J1: Pembelajar baru memulai (P1)**
1. Membuka URL portal, melihat Beranda (peta kurikulum, estimasi, progres 0%).
2. Membaca Panduan (profil, lingkungan lab, jalur lab ke produksi).
3. Membuka chapter pertama yang prasyaratnya terpenuhi, memilih "Buka materi".
4. Membaca materi di situs dokumentasi, menjalankan praktik di VM, mengubah status.
5. Kembali ke dashboard, melihat progres bertambah dan chapter berikutnya "siap dipelajari".

**J2: Melanjutkan belajar (P1)**
1. Membuka portal di hari berikutnya; dashboard menampilkan level saat ini dan chapter yang sedang berjalan.
2. Memfilter "Siap dipelajari" dan melanjutkan.

**J3: Mencari topik (P2)**
1. Mengetik "dkim" di pencarian dashboard atau pencarian dokumentasi.
2. Membuka chapter terkait, membaca prasyarat, memutuskan lanjut atau mengambil prasyarat dulu.

**J4: Memindahkan progres (P1)**
1. Mengekspor progres JSON dari browser lama.
2. Mengimpor di browser/perangkat baru; progres pulih.

**J5: Menambah satu chapter (P3)**
1. Memilih chapter berstatus `draft`.
2. Perintah `scaffold` membuat stub dari template, Claude Code menulis isinya, penulis menguji di VM.
3. Validasi otomatis lolos, status diubah menjadi `published`, perubahan digabung ke cabang utama.
4. CI membangun dan menerbitkan; dashboard menampilkan tautan "Buka materi" untuk chapter itu.

---

## 3. Product Goals dan Non-Goals

### 3.1 Goals

| ID | Goal | Ukuran keberhasilan |
|---|---|---|
| G1 | Portal dapat dipublikasikan dan berfungsi di GitHub Pages | Semua AC deployment lolos (bagian 11) |
| G2 | Materi ditulis dan dikelola sebagai Markdown, bukan string JS | 100% materi baru berada di `materi/` |
| G3 | Struktur kurikulum punya satu sumber data | 0 duplikasi struktur antara blok data dashboard dan `mkdocs.yml` |
| G4 | Progres belajar tetap bekerja lintas dashboard dan dokumentasi | Status yang diubah di salah satu terlihat di yang lain |
| G5 | Penambahan satu chapter per iterasi aman dan dapat diulang | Satu chapter dapat dirilis tanpa menyentuh chapter lain |
| G6 | Kualitas dijaga otomatis | CI memvalidasi data, build, dan tautan pada setiap perubahan |

### 3.2 Non-goals (versi ini)

- Akun pengguna, login, atau sinkronisasi progres lewat server.
- Analitik, pelacakan, atau pengumpulan data pribadi.
- Kuis berskor atau sertifikat dengan verifikasi server.
- Menjalankan perintah atau lab dari browser (portal tidak mengeksekusi apa pun).
- Penyediaan VM atau lingkungan lab terkelola.
- Terjemahan multi-bahasa (konten hanya Indonesia).
- Aplikasi mobile native.
- Komentar atau forum.
- Menulis seluruh 136 chapter dalam satu rilis. Cakupan bertahap.

---

## 4. Functional Requirements

Prioritas: **M** = MUST, **S** = SHOULD, **C** = MAY. Status: **ADA** (sudah ada), `ADA*` (ada tetapi diubah setelah audit dan belum diuji di browser), **SEBAGIAN**, **BARU** (harus dikembangkan); definisi lengkap dan metode uji ada di Lampiran C.

### 4.1 Dashboard: navigasi dan penjelajahan

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-001 | Dashboard MUST menampilkan hierarki Kategori → Modul → Chapter dengan ID stabil (`CAT-NN`, `MOD-NN-NN`, `CH-NN-NN-NN`). | M | ADA |
| FR-002 | Dashboard MUST menyediakan halaman Beranda (peta kurikulum, metrik), Panduan, ringkasan kategori, dan ringkasan chapter, masing-masing dengan alamat hash. | M | ADA |
| FR-003 | Dashboard MUST menampilkan breadcrumb dan tombol chapter sebelumnya/berikutnya pada halaman chapter. | M | ADA |
| FR-004 | Tautan internal ke bagian halaman (daftar isi chapter, skip link) MUST tidak mengganti rute aktif. | M | ADA\* |
| FR-005 | Dashboard MUST menangani hash tidak valid atau tidak dikenal tanpa error, dengan jatuh ke Beranda. | M | ADA\* |
| FR-006 | Dashboard MUST menyediakan drawer navigasi pada layar ≤ 900 px; tautan di dalam drawer tertutup MUST tidak dapat difokus. | M | ADA\* |

### 4.2 Dashboard: pencarian dan filter

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-010 | Pencarian MUST mencocokkan semua kata (AND) terhadap ID, judul, modul, kategori, tujuan, dan perintah/berkas chapter. | M | ADA |
| FR-011 | Pencarian SHOULD juga mencakup isi materi (teks polos dari Markdown yang terbit) melalui indeks yang dihasilkan saat build. | S | BARU |
| FR-012 | Dashboard MUST menyediakan filter kategori, filter status, "Belum selesai", "Siap dipelajari", dan "Hapus filter". | M | ADA |
| FR-013 | Filter dan kata kunci SHOULD tercermin di URL (query dalam hash) agar dapat dibagikan. | S | BARU |
| FR-014 | Jumlah hasil MUST diumumkan lewat live region. | M | ADA |

### 4.3 Dashboard: status dan progres

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-020 | Pengguna MUST dapat mengatur status tiap chapter: Belum Dimulai, Sedang Dipelajari, Praktik Berjalan, Menunggu Validasi, Selesai. | M | ADA |
| FR-021 | Pengguna MUST dapat mencentang checklist persiapan dan kelulusan per chapter; mencentang MUST NOT mengubah status otomatis. | M | ADA |
| FR-022 | Persentase progres MUST dihitung dari chapter wajib saja; chapter opsional MUST dilaporkan terpisah. | M | ADA\* |
| FR-023 | Dashboard MUST menampilkan "level saat ini" sebagai kategori wajib pertama yang masih punya chapter belum selesai. | M | ADA\* |
| FR-024 | Dashboard MUST menurunkan status "siap dipelajari" dari prasyarat (chapter pertama modul bergantung pada chapter terakhir modul `after`; chapter berikutnya bergantung pada chapter sebelumnya). | M | ADA |
| FR-025 | Progres MUST disimpan hanya di `localStorage` perangkat pengguna. | M | ADA |
| FR-026 | Perubahan progres di tab lain MUST tercermin tanpa memuat ulang dan MUST NOT tertimpa oleh tab usang. | M | ADA\* |
| FR-027 | Pengguna MUST dapat mengekspor, mengimpor (dengan konfirmasi), dan mereset progres; impor MUST memvalidasi dan menyanitasi data. | M | ADA |
| FR-028 | Dashboard SHOULD mengingatkan pengguna untuk mengekspor progres secara berkala (mis. tiap 30 hari sejak ekspor terakhir). | S | BARU |
| FR-029 | Dashboard MAY menampilkan progres berbobot menit sebagai metrik tambahan. | C | BARU |

### 4.4 Dashboard: tampilan

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-030 | Dashboard MUST menyediakan mode terang dan gelap, mengikuti preferensi sistem secara awal dan menyimpan pilihan; semua kontrol formulir MUST terbaca pada kedua mode. | M | ADA\* |
| FR-031 | Dashboard MUST tidak menampilkan kilatan tema salah saat dimuat. | M | ADA\* |
| FR-032 | Dashboard MUST menyediakan gaya cetak yang menyembunyikan navigasi dan kontrol. | S | ADA |
| FR-033 | Dashboard MUST memiliki favicon, `<title>` per halaman, deskripsi meta, dan metadata Open Graph. | S | BARU |

### 4.5 Materi (Markdown dan MkDocs)

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-040 | Setiap chapter MUST memiliki satu berkas Markdown di `materi/` dengan nama berdasarkan ID chapter. | M | BARU |
| FR-041 | Setiap berkas MUST memiliki front matter YAML: `id`, `title`, `minutes`, `environment`, `prerequisites`, `status` (`draft` \| `published`), `verified_on` (tanggal uji VM), `release` (rilis Ubuntu acuan). | M | BARU |
| FR-042 | Isi chapter MUST mengikuti template 14 bagian yang sama dengan dashboard: Ringkasan, Tujuan Pembelajaran, Prasyarat, Materi Teori, Praktik dan Implementasi, Perintah Linux, Konfigurasi, Verifikasi, Troubleshooting, Security Review, Latihan, Assessment, Checklist Kelulusan, Referensi Resmi. | M | BARU |
| FR-043 | Blok kode MUST menyatakan konteks eksekusi (pengguna biasa atau root), memakai placeholder `<HURUF-KAPITAL>`, dan memisahkan perintah dari output yang diharapkan; tombol salin MUST tersedia. | M | BARU |
| FR-044 | Chapter berstatus `draft` MUST tampil dengan banner "belum ditulis" yang konsisten, atau MUST dikecualikan dari build sesuai konfigurasi. | M | BARU |
| FR-045 | Situs dokumentasi MUST menyediakan pencarian teks penuh, navigasi samping, tabel isi halaman, dan mode gelap. | M | BARU |
| FR-046 | Setiap halaman materi MUST menautkan balik ke chapter terkait di dashboard dan menyediakan kontrol status belajar yang memakai data progres yang sama. | S | BARU |
| FR-047 | Situs dokumentasi MUST menampilkan chapter sebelumnya/berikutnya sesuai urutan kurikulum. | S | BARU |

### 4.6 Integrasi dan data kurikulum

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-050 | Struktur kurikulum MUST bersumber dari satu tempat: blok data pada berkas dashboard `kurikulum-mail-server-ubuntu.html` (di antara penanda `/*DATA-START*/` dan `/*DATA-END*/`). Build MUST mengekstraknya secara hanya-baca menjadi artefak turunan `.build/curriculum.json`; stub Markdown dan `nav` MkDocs MUST diturunkan dari artefak itu. Artefak MUST NOT dikomit. | M | BARU |
| FR-051 | Artefak `curriculum.json` MUST memakai objek bernama (bukan array posisional) dan divalidasi oleh JSON Schema. Ekstraksi MUST gagal bila penanda blok data hilang atau tidak tunggal. | M | BARU |
| FR-052 | Perintah `scaffold` (dijalankan manual, bukan bagian build) MUST membuat stub Markdown untuk chapter baru dan MUST NOT menimpa berkas yang sudah ada. | M | BARU |
| FR-053 | Build MUST menghasilkan `nav` dan `exclude_docs` MkDocs secara deterministik ke `.build/mkdocs.generated.yml`, dan MUST NOT menulis ke berkas sumber (termasuk `mkdocs.yml`). | M | BARU |
| FR-054 | Dashboard MUST menampilkan tautan "Buka materi" hanya untuk chapter berstatus `published`; untuk `draft` MUST menampilkan spesifikasi seperti sekarang. | M | BARU |
| FR-055 | Dashboard MUST tetap berfungsi bila situs dokumentasi tidak tersedia (tautan materi gagal tidak boleh merusak fitur dashboard). | M | BARU |

### 4.7 Validasi dan alur kerja penulisan

| ID | Persyaratan | Pri | Status |
|---|---|---|---|
| FR-060 | Skrip validasi MUST memeriksa: ID unik, prasyarat merujuk modul yang ada, tanpa siklus prasyarat, setiap chapter `published` punya berkas Markdown, front matter lengkap, 14 heading wajib ada. | M | BARU |
| FR-061 | Skrip validasi MUST memeriksa bahwa `published` disertai `verified_on` berisi tanggal. | M | BARU |
| FR-062 | Skrip validasi SHOULD memindai berkas materi untuk pola yang terlihat seperti kredensial atau kunci privat (mis. blok `BEGIN PRIVATE KEY`) dan menggagalkan CI bila ditemukan. | S | BARU |
| FR-063 | Repositori MUST memuat panduan penulisan chapter (template, gaya, aturan uji VM) yang dapat dipakai Claude Code tiap iterasi. | M | BARU |
| FR-064 | Tiap iterasi MUST menyentuh satu chapter (satu berkas materi + perubahan metadata terkait), sehingga satu pull request = satu chapter. | S | BARU |
| FR-065 | Build MUST NOT mengubah berkas sumber: manifes SHA-256 sumber sebelum dan sesudah build identik, dan `git status` bersih setelah build. | M | BARU |
| FR-066 | Dua build dengan masukan dan lingkungan sama MUST menghasilkan keluaran identik (dibandingkan lewat manifes SHA-256 keluaran, dengan daftar pengecualian yang terdokumentasi). | M | BARU |

---

## 5. Non-Functional Requirements

| ID | Kategori | Persyaratan | Status |
|---|---|---|---|
| NFR-001 | Kinerja | Halaman dashboard MUST interaktif dalam ≤ 2 detik pada koneksi 4G sedang (≈ 1,6 Mbps) dan perangkat kelas menengah. | BARU |
| NFR-002 | Kinerja | Ukuran dashboard (HTML + JS + CSS + data) yang ditransfer MUST ≤ 300 KB terkompresi pada rilis pertama dan SHOULD ≤ 500 KB bila indeks pencarian isi ditambahkan. | BARU |
| NFR-003 | Kinerja | Satu halaman materi MUST ≤ 250 KB terkompresi (tanpa gambar). | BARU |
| NFR-004 | Kompatibilitas | Dashboard dan dokumentasi MUST berfungsi di dua versi mayor terakhir Chrome, Edge, Firefox, dan Safari (termasuk iOS Safari). | BARU |
| NFR-005 | Aksesibilitas | Dashboard dan dokumentasi MUST memenuhi WCAG 2.2 level AA untuk kontras, fokus keyboard, label formulir, dan struktur heading. | SEBAGIAN |
| NFR-006 | Aksesibilitas | Seluruh fungsi dashboard MUST dapat dipakai hanya dengan keyboard. | SEBAGIAN |
| NFR-007 | Responsif | Tata letak MUST dapat dipakai pada lebar 320 px tanpa scroll horizontal pada konten utama (kecuali tabel dalam pembungkus scroll). | SEBAGIAN |
| NFR-008 | Privasi | Portal MUST NOT mengirim data pengguna ke layanan eksternal dan MUST NOT memuat skrip analitik atau pelacak pihak ketiga. | ADA |
| NFR-009 | Keamanan | Semua skrip dan gaya MUST disajikan dari origin yang sama (tanpa CDN) pada rilis pertama. | ADA |
| NFR-010 | Keamanan | Data impor MUST disanitasi (hanya ID dikenal, nilai dan pola kunci tervalidasi) dan MUST NOT dieksekusi atau dimasukkan ke DOM tanpa escape. | ADA |
| NFR-011 | Ketahanan | Bila `localStorage` diblokir, dashboard MUST tetap berfungsi dengan penyimpanan memori dan menampilkan peringatan bahwa progres tidak persisten. | SEBAGIAN |
| NFR-012 | Kemudahan pemeliharaan | Build MUST dapat direproduksi: versi MkDocs, tema, dan plugin dikunci di `requirements.txt` (atau setara). | BARU |
| NFR-013 | Kemudahan pemeliharaan | Sumber (HTML/JS/CSS/data/Markdown) MUST berada di git; keluaran build (`site/`) MUST NOT dikomit. | BARU |
| NFR-014 | Portabilitas | Situs MUST dapat dipindah dari GitHub Pages ke Vercel tanpa mengubah konten atau struktur URL (hanya konfigurasi deployment). | BARU |
| NFR-015 | Kebenaran konten | Setiap perintah dan konfigurasi pada chapter `published` MUST telah dijalankan pada VM bersih dengan rilis acuan, dan tanggal ujinya dicatat. | BARU |
| NFR-016 | Keselamatan konten | Materi MUST NOT memuat kredensial, kunci privat, token, atau data pribadi nyata; contoh MUST memakai domain/IP dokumentasi (mis. `example.com`, `192.0.2.0/24`). | BARU |
| NFR-017 | Bahasa | Konten MUST berbahasa Indonesia baku, istilah teknis tetap dalam bahasa aslinya; `lang="id"` MUST diatur. | SEBAGIAN |
| NFR-018 | Cetak | Halaman materi SHOULD dapat dicetak ke PDF dengan tata letak terbaca. | SEBAGIAN |
| NFR-019 | Kelayakan uji | Perilaku inti dashboard (routing, filter, progres, impor/ekspor) MUST dicakup uji otomatis di CI. | BARU |
| NFR-020 | Lisensi | Repositori MUST menyatakan lisensi untuk kode dan untuk materi sebelum dipublikasikan. | BARU |

---

## 6. Struktur Informasi dan Navigasi

### 6.1 Hierarki konten

```
Portal
├── Dashboard (/)                       peta kurikulum, progres, pencarian, filter
│   ├── Beranda
│   ├── Panduan
│   ├── Kategori  CAT-01 … CAT-16       (16)
│   └── Chapter   CH-NN-NN-NN           (136) → ringkasan/spesifikasi + tautan materi
└── Dokumentasi (/materi/)              situs MkDocs
    ├── Beranda dokumentasi
    ├── Panduan penulisan (opsional dipublikasikan)
    └── Chapter  CH-NN-NN-NN            (diterbitkan bertahap)
```

Urutan Kategori → Modul → Chapter mengikuti `curriculum.json`. Level L0–L15 dan lingkungan (lab, domain, publik, produksi) ditampilkan sebagai metadata.

### 6.2 Navigasi

| ID | Persyaratan | Status |
|---|---|---|
| IA-01 | Dashboard memakai sidebar pohon Kategori → Modul → Chapter, breadcrumb, dan pager. | ADA |
| IA-02 | Dokumentasi memakai navigasi samping hasil generasi dari `curriculum.json` dengan urutan dan pengelompokan identik dengan dashboard. | BARU |
| IA-03 | Setiap halaman di kedua sisi memuat tautan ke sisi lainnya (dashboard ↔ materi untuk chapter yang sama). | BARU |
| IA-04 | Tiap chapter dapat dicapai dari dashboard ≤ 3 klik dari Beranda dan dari pencarian ≤ 2 interaksi. | SEBAGIAN |
| IA-05 | Chapter `draft` tetap muncul di navigasi dashboard (dengan penanda), tetapi tidak menghasilkan tautan mati. | SEBAGIAN |

---

## 7. Integrasi Dashboard dengan Dokumentasi

### 7.1 Keputusan arsitektur (usulan)

Satu situs, dua bagian, dihasilkan dari satu repositori:

```
https://<pengguna>.github.io/<repo>/              ← dashboard (index.html)
https://<pengguna>.github.io/<repo>/materi/       ← MkDocs Material
https://<pengguna>.github.io/<repo>/materi/chapter/CH-06-01-02/
```

- Sumber Markdown berada di `materi/`; `mkdocs.yml` memakai `docs_dir: materi`.
- Build: `mkdocs build -d site/materi`, lalu `kurikulum-mail-server-ubuntu.html` disalin apa adanya (byte-identik) ke `site/index.html`. `docs/` (dokumen proyek seperti audit dan PRD) bukan bagian situs dan tidak dipublikasikan.
- Dashboard dan dokumentasi berbagi **origin dan kunci `localStorage`** yang sama.

**Alasan:** URL stabil, dashboard tetap berdiri sendiri, dan struktur sama dengan opsi B pada audit (satu sumber data).

### 7.2 Persyaratan integrasi

| ID | Persyaratan | Status |
|---|---|---|
| INT-01 | Dashboard MUST menautkan ke materi lewat pola URL tetap `<base>/materi/chapter/<CH-ID>/` yang dibuat dari ID chapter, tidak ditulis manual per chapter. | BARU |
| INT-02 | Halaman materi MUST memuat skrip kecil bersama (`extra_javascript`) yang membaca dan menulis kunci progres yang sama dengan dashboard dan memakai skema yang sama (lihat bagian 9). | BARU |
| INT-03 | Skrip halaman materi SHOULD berasal dari satu berkas sumber (`materi/assets/progress.js`); kesamaan perilakunya dengan dashboard MUST dijaga oleh uji kontrak (PRG-03). | BARU |
| INT-04 | Tautan dari materi ke dashboard MUST memakai rute hash yang ada (`#CH-…`, `#CAT-…`, `#/`). | BARU |
| INT-05 | Menambah satu chapter MUST hanya memerlukan: berkas Markdown (dibuat dengan perintah `scaffold`), pengaturan front matter, dan entri pada blok data dashboard bila bab belum terdaftar. Tidak ada edit manual ke `nav`, `mkdocs.yml`, atau logika dashboard. | BARU |
| INT-06 | Kegagalan memuat salah satu sisi (mis. 404 materi) MUST NOT menghapus atau merusak data progres. | BARU |
| INT-07 | Dashboard MUST menampilkan tautan "Buka materi" berdasarkan `materi/chapters.json`, daftar bab terbit yang dibuat saat build dengan memindai halaman hasil build. Berkas dimuat dengan `fetch` pada jalur relatif; kegagalan memuat MUST diabaikan tanpa memengaruhi fitur lain. Data kurikulum tetap tertanam di dashboard. | BARU |
| INT-08 | Indeks pencarian isi (bila FR-011 diambil) MUST dihasilkan saat build dari Markdown berstatus `published` saja. | BARU |

---

## 8. Persyaratan URL dan Base Path

| ID | Persyaratan | Status |
|---|---|---|
| URL-01 | Tidak boleh ada path absolut (`/aset/…`) pada dashboard dan dokumentasi; semua tautan dan aset MUST relatif atau dibentuk dari base yang dikonfigurasi, sehingga situs berjalan di `/<repo>/` (GitHub Pages proyek) maupun di akar domain (Vercel, domain kustom). | SEBAGIAN |
| URL-02 | `site_url` MkDocs MUST dikonfigurasi dari variabel lingkungan atau konfigurasi CI, bukan ditulis permanen di `mkdocs.yml` untuk satu host saja. | BARU |
| URL-03 | Dashboard MUST memakai routing berbasis hash (tanpa rewrite server). Perubahan ke routing berbasis path hanya boleh dilakukan jika disertai konfigurasi rewrite untuk kedua host dan tidak merusak tautan lama. | ADA |
| URL-04 | ID chapter (`CH-NN-NN-NN`) MUST menjadi bagian tetap URL materi; ID MUST NOT diubah atau dipakai ulang setelah dipublikasikan. Bila chapter dihapus, URL-nya MUST dialihkan atau menampilkan halaman penjelasan. | BARU |
| URL-05 | Slug judul MUST NOT menjadi bagian URL kanonis (judul bisa berubah). | BARU |
| URL-06 | Halaman 404 kustom MUST tersedia dan menautkan ke Beranda dan pencarian. | BARU |
| URL-07 | Setiap halaman materi MUST memiliki `<link rel="canonical">` yang benar terhadap `site_url`. | BARU |
| URL-08 | Pada GitHub Pages, berkas `.nojekyll` MUST ada bila publikasi tidak memakai build Jekyll. | BARU |
| URL-09 | Berkas keluaran dashboard di akar situs MUST bernama `index.html` dan MUST byte-identik dengan berkas sumber `kurikulum-mail-server-ubuntu.html`; nama berkas sumber tidak diubah. | BARU |
| URL-10 | Rute dashboard dan URL materi MUST diuji pada dua konfigurasi: `/<repo>/` dan `/`. | BARU |

---

## 9. Progress Tracking dan Kompatibilitas JavaScript

### 9.1 Skema data (versi 1, kompatibel dengan implementasi saat ini)

- **Kunci penyimpanan progres:** `kurikulum-mail-ubuntu-v1`
- **Kunci tema:** `kmu-theme` (`"light"` atau `"dark"`)
- **Nilai progres:**

```json
{ "v": 1,
  "status": { "CH-02-01-01": 4, "CH-02-01-02": 2 },
  "checks": { "CH-02-01-01": { "p0": true, "c1": true } } }
```

- Status: `1..4` disimpan (`0` = tidak disimpan). Nilai: 0 Belum Dimulai, 1 Sedang Dipelajari, 2 Praktik Berjalan, 3 Menunggu Validasi, 4 Selesai.
- **Format ekspor:** `{ "app":"kurikulum-mail-server-ubuntu", "version":1, "exportedAt":ISO8601, "status":{…}, "checks":{…} }`

### 9.2 Persyaratan

| ID | Persyaratan | Status |
|---|---|---|
| PRG-01 | Skema progres versi 1 MUST dipertahankan; perubahan skema MUST menaikkan nomor versi dan menyertakan migrasi dari versi sebelumnya tanpa kehilangan data. | ADA |
| PRG-02 | Berkas ekspor lama (versi 1) MUST tetap dapat diimpor pada semua rilis berikutnya. | ADA |
| PRG-03 | Perilaku progres (muat, sanitasi, simpan, sinkronisasi antar tab, ekspor/impor) MUST identik pada dashboard dan halaman materi, dibuktikan oleh uji kontrak yang sama pada keduanya. Kode SHOULD dibagi dalam satu modul bila dashboard kelak dipecah; pada v1 dua implementasi diperbolehkan. | BARU |
| PRG-04 | ID yang tidak lagi ada di kurikulum MUST diabaikan saat memuat (bukan menyebabkan error) dan SHOULD dipertahankan dalam penyimpanan bila memungkinkan untuk mencegah kehilangan data saat chapter dinonaktifkan sementara. **[Pertanyaan Q-07]** | SEBAGIAN |
| PRG-05 | Perubahan progres di satu tab/halaman MUST disinkronkan ke tab/halaman lain dari origin yang sama lewat event `storage` dan MUST NOT menimpa perubahan yang lebih baru. | ADA\* |
| PRG-06 | Penyimpanan MUST gagal dengan aman: error kuota atau akses ditolak MUST ditangkap, pengguna diberi tahu, dan aplikasi tetap berjalan (NFR-011). | SEBAGIAN |
| PRG-07 | Definisi persentase: `chapter wajib berstatus Selesai / jumlah chapter wajib`; chapter opsional dihitung terpisah (FR-022). Definisi ini MUST terdokumentasi di Panduan. | ADA\* |
| PRG-08 | Halaman materi MUST menampilkan status chapter saat ini dan memungkinkan mengubahnya; perubahan MUST terlihat di dashboard pada pemuatan atau sinkronisasi berikutnya. | BARU |

### 9.3 Kompatibilitas JavaScript

| ID | Persyaratan | Status |
|---|---|---|
| JS-01 | Target: browser evergreen (dua versi mayor terakhir). Fitur yang dipakai saat ini (`color-mix()`, `:focus-visible`, `Map`/`Set`, spread, `inset`) MUST tetap dalam rentang dukungan NFR-004. | ADA |
| JS-02 | Fitur modern baru yang tidak didukung semua target MUST diberi cadangan (mis. `@supports`) atau dihindari. | SEBAGIAN |
| JS-03 | Kode MUST dapat berjalan tanpa tahap kompilasi (tanpa bundler wajib). Bila bundler dipakai, keluarannya MUST tetap berupa berkas statis. | ADA |
| JS-04 | Kode MUST NOT bergantung pada variabel global dari tema MkDocs Material selain API yang didokumentasikan (mis. `document$`) dan MUST bekerja dengan fitur navigasi instan bila diaktifkan. | BARU |
| JS-05 | Halaman tanpa JavaScript MUST menampilkan konten materi (Markdown yang dirender) dan pesan jelas bahwa dashboard memerlukan JavaScript. | SEBAGIAN |
| JS-06 | CSP target: tanpa `eval`. Skrip dan gaya inline dashboard dipertahankan; CSP ketat diterapkan di Vercel dengan hash SHA-256 skrip inline yang dihitung saat build (`script-src 'self' 'sha256-…'`). Pemindahan skrip ke berkas terpisah tidak diwajibkan. | BARU |
| JS-07 | Konten HTML mentah (`CONTENT` atau Markdown dengan HTML) MUST dianggap tepercaya hanya jika berasal dari repositori; kontribusi pihak luar MUST melalui review sebelum digabung. | ADA |

---

## 10. Persyaratan Deployment, Keamanan, dan Pemeliharaan

### 10.1 Deployment

| ID | Persyaratan | Status |
|---|---|---|
| DEP-01 | Repositori GitHub MUST menjadi sumber utama; cabang `main` dilindungi dan merupakan sumber rilis. | BARU |
| DEP-02 | Deployment awal MUST ke GitHub Pages memakai GitHub Actions (bukan "deploy from branch"). | BARU |
| DEP-03 | Alur CI MUST: pasang dependensi terkunci → validasi data dan materi → hasilkan `nav` → `mkdocs build --strict` → rakit `site/` (dashboard + materi) → uji otomatis → unggah artefak Pages → deploy. | BARU |
| DEP-04 | Pull request MUST menjalankan semua langkah CI kecuali deploy produksi. | BARU |
| DEP-05 | Deploy MUST gagal (dan situs lama tetap utuh) bila validasi atau build gagal. | BARU |
| DEP-06 | Deployment ke Vercel MUST dimungkinkan hanya dengan menambah `vercel.json` (build command, `outputDirectory: site`, header) tanpa mengubah konten. Header keamanan (CSP, `X-Content-Type-Options`, `Referrer-Policy`) diatur di sana. | BARU |
| DEP-07 | Rilis MUST dapat dikembalikan dengan me-revert komit pada `main` dan menjalankan ulang pipeline. | BARU |
| DEP-08 | Preview per pull request SHOULD tersedia (artefak CI atau Vercel preview). | BARU |

### 10.2 Keamanan

| ID | Persyaratan | Status |
|---|---|---|
| SEC-01 | Repositori dan situs MUST NOT memuat rahasia (kredensial, token, kunci privat, IP/domain produksi nyata). Pemindaian rahasia SHOULD diaktifkan di GitHub dan di CI (FR-062). | BARU |
| SEC-02 | Tautan eksternal MUST memakai `rel="noopener noreferrer"` bila membuka tab baru. | ADA |
| SEC-03 | Dependensi Python/Node MUST dipantau pembaruan keamanannya (Dependabot atau setara) dan versi dikunci. | BARU |
| SEC-04 | GitHub Actions MUST memakai izin minimal (`permissions:` eksplisit) dan menyematkan versi action (tag atau SHA). | BARU |
| SEC-05 | Materi MUST berisi peringatan yang sesuai untuk tindakan berisiko (mengunci diri dari SSH, firewall, mengubah DNS produksi, pengujian pindai port hanya pada server milik sendiri). | BARU |
| SEC-06 | Materi MUST NOT memuat instruksi yang menyasar sistem pihak ketiga tanpa izin. | BARU |
| SEC-07 | Header keamanan SHOULD diterapkan di Vercel (GitHub Pages tidak dapat mengatur header). | BARU |

### 10.3 Pemeliharaan

| ID | Persyaratan | Status |
|---|---|---|
| MNT-01 | Tiap chapter `published` MUST mencatat `verified_on` dan `release`. Chapter dengan `verified_on` lebih dari 12 bulan SHOULD ditandai "perlu verifikasi ulang" oleh skrip. | BARU |
| MNT-02 | Ketika rilis acuan (mis. Ubuntu 24.04 LTS) berubah, perubahan MUST ditinjau per chapter; tidak ada penggantian massal tanpa uji VM. | BARU |
| MNT-03 | Tautan eksternal (dokumentasi resmi) MUST diperiksa berkala (CI terjadwal bulanan) dan kegagalan dilaporkan sebagai issue. | BARU |
| MNT-04 | `CHANGELOG.md` MUST mencatat tiap rilis (chapter yang ditambah atau diubah). | BARU |
| MNT-05 | `README.md` MUST menjelaskan struktur repositori, cara menjalankan lokal, cara menambah chapter, dan cara deploy. | BARU |
| MNT-06 | Versi tema/plugin MkDocs MUST ditinjau tiap kuartal; status pemeliharaan MkDocs Material MUST diverifikasi sebelum keputusan versi (asumsi A-05). | BARU |
| MNT-07 | Pemilik produk dan peninjau materi MUST ditetapkan (Q-06). | BARU |

---

## 11. Acceptance Criteria yang Terukur

Setiap kriteria dapat diverifikasi lulus/gagal. "Diuji pada" menyebut lingkungan verifikasi.

### 11.1 Dashboard

| ID | Kriteria | Mencakup |
|---|---|---|
| AC-01 | Pada chapter mana pun, mengklik masing-masing dari 14 tautan daftar isi menggulir ke bagian yang sesuai, `location.hash` tetap `#CH-…`, dan halaman tetap menampilkan chapter yang sama. Uji: 136 chapter × 14 tautan (otomatis, sampel minimal 10 chapter). | FR-004 |
| AC-02 | Membuka `#%E0%A4%A`, `#CH-tidak-ada`, dan `#CAT-99` menampilkan Beranda tanpa error di console. | FR-005 |
| AC-03 | Pada viewport 375 px dengan drawer tertutup, tombol Tab dari header tidak memfokus tautan sidebar mana pun dalam 20 penekanan Tab. | FR-006 |
| AC-04 | Mencari "dkim" mengembalikan setidaknya CH-08-02-02 dan CH-05-02-01; mencari "xyzzy" menampilkan "Tidak ada chapter yang cocok". | FR-010 |
| AC-05 | Dua tab terbuka; mengubah status chapter di tab A muncul di tab B dalam ≤ 1 detik tanpa muat ulang; lalu mengubah chapter lain di tab B tidak menghilangkan perubahan tab A. | FR-026, PRG-05 |
| AC-06 | Dengan semua 122 chapter wajib berstatus Selesai dan 0 opsional, progres = 100% dan "Level saat ini" = "Semua level selesai"; kartu opsional menunjukkan 0/14. | FR-022, FR-023 |
| AC-07 | Ekspor lalu impor pada profil browser kosong memulihkan status dan checklist identik (perbandingan JSON setara). Berkas dengan `app` salah ditolak dengan pesan; ID tak dikenal diabaikan. | FR-027, NFR-010 |
| AC-08 | Dengan `localStorage` dinonaktifkan, dashboard tetap dimuat dan dapat dipakai, serta menampilkan peringatan tidak persisten. | NFR-011, PRG-06 |
| AC-09 | Pada mode gelap, rasio kontras teks pada dropdown "Status belajar", dropdown filter, dan pencarian ≥ 4,5:1 (diukur dengan alat kontras otomatis). | FR-030, NFR-005 |
| AC-10 | Memuat ulang 20 kali pada mode gelap (cache dingin dan hangat) tidak memperlihatkan frame berlatar terang (rekaman layar atau uji otomatis atas atribut `data-theme` pada first paint). | FR-031 |
| AC-11 | Audit aksesibilitas otomatis (axe atau Lighthouse) pada Beranda, satu halaman kategori, satu halaman chapter, dan Panduan: 0 pelanggaran serius/kritis; skor aksesibilitas Lighthouse ≥ 95. | NFR-005 |
| AC-12 | Lighthouse (profil mobile, throttling bawaan) pada Beranda: Performance ≥ 90, Best Practices ≥ 95, SEO ≥ 90. | NFR-001, FR-033 |
| AC-13 | Ukuran transfer dashboard terkompresi ≤ 300 KB (diukur di CI dengan gzip). | NFR-002 |

### 11.2 Data dan materi

| ID | Kriteria | Mencakup |
|---|---|---|
| AC-20 | Artefak `curriculum.json` yang diekstrak dari blok data dashboard lolos validasi JSON Schema; skrip validasi menyatakan 16 kategori, 36 modul, 136 chapter, 0 ID duplikat, 0 siklus prasyarat. Menambah ID duplikat atau prasyarat tidak ada membuat CI gagal; menghapus salah satu penanda blok data membuat ekstraksi gagal. | FR-050, FR-051, FR-060 |
| AC-21 | Menjalankan build dua kali berturut-turut menghasilkan `nav` identik byte demi byte dan tidak mengubah berkas sumber apa pun (termasuk `mkdocs.yml` dan Markdown yang sudah ada isinya). | FR-052, FR-053, FR-065 |
| AC-22 | Setiap berkas `published` memiliki semua front matter wajib dan 14 heading wajib berurutan; berkas yang kekurangan satu heading membuat CI gagal. | FR-041, FR-042, FR-060 |
| AC-23 | Berkas `published` tanpa `verified_on` membuat CI gagal. | FR-061 |
| AC-24 | Menambahkan blok `-----BEGIN OPENSSH PRIVATE KEY-----` ke berkas materi membuat CI gagal. | FR-062 |
| AC-25 | Dashboard menampilkan tautan "Buka materi" untuk 100% chapter `published` dan 0% untuk `draft`; setiap tautan menghasilkan HTTP 200 pada situs hasil build (diperiksa otomatis). | FR-054, INT-01 |
| AC-26 | Satu chapter baru dapat ditambahkan dengan mengubah paling banyak 2 berkas: berkas Markdown dan (bila bab belum terdaftar) entri pada blok data dashboard; `git diff` PR tidak mengubah logika dashboard di luar blok data dan tidak mengubah `mkdocs.yml`. | INT-05, FR-064 |
| AC-27 | Setiap perintah pada chapter `published` memiliki catatan uji (VM, rilis, tanggal) di bagian log pengujian atau di PR; pemeriksa menyetujui sebelum penggabungan. | NFR-015 |
| AC-28 | Tidak ada kredensial, kunci, token, atau IP produksi pada repositori (pemindai rahasia 0 temuan). Contoh jaringan hanya memakai `example.com`/`192.0.2.0/24`/`2001:db8::/32`. | NFR-016, SEC-01 |

### 11.3 URL, deployment, dan integrasi

| ID | Kriteria | Mencakup |
|---|---|---|
| AC-30 | Situs hasil build dilayani dari subpath `/<repo>/` dan dari `/`; pada keduanya 100% tautan internal dan aset menghasilkan 200 (pemeriksa tautan otomatis) dan rute hash bekerja. | URL-01, URL-10 |
| AC-31 | `mkdocs build --strict` selesai tanpa peringatan atau error; pemeriksa tautan menyatakan 0 tautan internal rusak. | DEP-03 |
| AC-32 | Mengubah `site_url` lewat variabel lingkungan menghasilkan `canonical` dan sitemap yang sesuai tanpa mengubah berkas yang dikomit. | URL-02, URL-07 |
| AC-33 | Membuka `<base>/` mengembalikan dashboard (bukan 404). Membuka URL tidak ada mengembalikan halaman 404 kustom dengan tautan ke Beranda. | URL-06, URL-09 |
| AC-34 | Status yang diubah di halaman materi terlihat di dashboard setelah menavigasi atau memuat ulang; sebaliknya juga berlaku; kunci `kurikulum-mail-ubuntu-v1` adalah satu-satunya kunci progres di `localStorage`. | INT-02, PRG-03, PRG-08 |
| AC-35 | Berkas ekspor dari rilis saat ini (versi 1) dapat diimpor pada rilis sesudahnya, oleh dashboard maupun `progress.js`; ada uji otomatis yang menyimpan fixture berkas ekspor v1 dan menjalankannya pada kedua implementasi. | PRG-02, PRG-03 |
| AC-36 | Pipeline CI: PR dengan build gagal tidak dapat digabung; deploy tidak berjalan; situs yang aktif tidak berubah. | DEP-04, DEP-05 |
| AC-37 | Dari pipeline hijau di `main` ke situs terbit ≤ 10 menit; revert komit memulihkan situs sebelumnya ≤ 15 menit. | DEP-03, DEP-07 |
| AC-38 | Menjalankan build Vercel dengan `vercel.json` menghasilkan situs setara (pemeriksa tautan 0 rusak) tanpa perubahan pada konten. | DEP-06, NFR-014 |
| AC-39 | Permintaan jaringan saat memuat dashboard dan satu halaman materi hanya ke origin yang sama (diperiksa lewat HAR/Playwright): 0 permintaan ke domain eksternal. | NFR-008, NFR-009 |
| AC-40 | Workflow GitHub Actions menyatakan `permissions:` eksplisit dan menyematkan versi semua action; pemindai konfigurasi 0 temuan tingkat tinggi. | SEC-04 |
| AC-41 | Dua build berurutan dari pohon sumber dan variabel lingkungan yang sama menghasilkan manifes SHA-256 keluaran identik (kecuali berkas yang tercatat sebagai pengecualian). | FR-066 |
| AC-42 | `sha256(site/index.html)` sama dengan `sha256(kurikulum-mail-server-ubuntu.html)`; manifes sumber sebelum dan sesudah build identik; `git status --porcelain` kosong setelah build. | URL-09, FR-065 |

### 11.4 Definisi selesai untuk rilis awal (MVP)

Rilis awal dianggap selesai bila: AC-01 sampai AC-13 lulus (kecuali AC-04 bagian isi materi), AC-20 sampai AC-26, AC-30 sampai AC-36, AC-39, AC-41, dan AC-42 lulus, dan minimal **satu** chapter (mis. CH-01-01-01) berstatus `published` dengan catatan uji VM.

---

## 12. Risiko, Asumsi, dan Pertanyaan Terbuka

### 12.1 Risiko

| ID | Risiko | P | D | Mitigasi | Rujukan |
|---|---|---|---|---|---|
| RK-01 | Pekerjaan hilang karena tidak ada git | S | T | Inisialisasi git dan remote GitHub sebagai langkah pertama | R-01 |
| RK-02 | Materi yang ditulis AI mengandung kesalahan teknis atau perintah berbahaya | S | T | Wajib uji VM, review manusia, catatan `verified_on`, peringatan keamanan | R-06, R-08 |
| RK-03 | Dua sumber struktur (JS dan `mkdocs.yml`) tak sinkron | S | S | Satu sumber data dan generator (FR-050) | R-04 |
| RK-04 | Pergeseran URL setelah publikasi merusak tautan dan penanda | R | T | URL berbasis ID tetap (URL-04) | |
| RK-05 | Perubahan skema progres menghapus progres pengguna | R | T | Versi skema, migrasi, fixture uji (PRG-01/02/35) | R-05 |
| RK-06 | Pengembangan MkDocs Material berhenti atau berubah arah | S | S | Kunci versi, hindari ketergantungan pada fitur berbayar/tak stabil, tinjau kuartalan | MNT-06 |
| RK-07 | Base path salah di GitHub Pages vs Vercel | S | S | Uji dua konfigurasi di CI (URL-10) | D-10 |
| RK-08 | Materi usang karena versi paket dan konfigurasi berubah | T | S | `verified_on`, peringatan 12 bulan, tinjau saat rilis baru | R-06 |
| RK-09 | Satu file dashboard membengkak saat pencarian isi ditambahkan | S | S | Indeks terpisah, pemuatan malas, batas ukuran di CI (NFR-002) | R-02 |
| RK-10 | Kebocoran data sensitif lewat contoh atau log di materi | R | T | Pemindai rahasia, aturan contoh, review | SEC-01 |
| RK-11 | Konflik `localStorage` pada origin bersama `github.io` | R | R | Kunci ber-namespace (sudah) | D-05 |
| RK-12 | Lisensi tidak jelas menghambat penggunaan ulang | S | S | Putuskan lisensi sebelum publik (NFR-020) | R-11 |
| RK-13 | Tidak ada uji otomatis sehingga regresi dashboard | S | S | Uji Playwright untuk rute, filter, progres (NFR-019) | R-09 |

P = probabilitas, D = dampak (R rendah, S sedang, T tinggi).

### 12.2 Asumsi

| ID | Asumsi |
|---|---|
| A-01 | Pembelajar memakai browser evergreen di desktop atau mobile; tidak ada dukungan IE atau browser lama. |
| A-02 | Tidak ada backend; progres per perangkat dan dipindah manual lewat ekspor/impor. |
| A-03 | Konten berbahasa Indonesia; ukuran tim penulis kecil (satu pemilik dengan Claude Code). |
| A-04 | Repositori GitHub tersedia dan GitHub Pages dapat diaktifkan untuknya. |
| A-05 | **[Perlu verifikasi]** MkDocs Material masih layak dipakai pada saat implementasi; ada kabar mode pemeliharaan dan penerus (Zensical) serta perubahan besar MkDocs 2.x. |
| A-06 | Rilis acuan awal adalah Ubuntu Server 24.04 LTS (sesuai data saat ini). **[Perlu verifikasi]** apakah rilis LTS yang lebih baru harus menjadi acuan. |
| A-07 | Dashboard dan dokumentasi berada di satu origin sehingga `localStorage` dapat dibagi. |
| A-08 | Perbaikan F-01 sampai F-11 yang sudah diterapkan benar; belum diuji di browser dan harus dikonfirmasi oleh AC-01…AC-03, AC-05, AC-09, AC-10. |
| A-09 | Folder `materi/` adalah akar sumber dokumentasi dan `docs/` hanya untuk dokumen proyek (audit, PRD) yang tidak dipublikasikan. |
| A-10 | Pengguna menjalankan lab di VM yang mereka kendalikan; portal tidak menyediakan lingkungan lab. |
| A-11 | Pengembangan dikerjakan satu pemilik dengan Claude Code secara paruh waktu; estimasi usaha pada bagian 13 bersifat relatif dan perlu dikalibrasi setelah M6. |

### 12.3 Pertanyaan terbuka

| ID | Pertanyaan | Dampak jika belum dijawab |
|---|---|---|
| Q-01 | Apakah repositori publik atau privat? GitHub Pages pada repositori privat memerlukan paket tertentu. | Menentukan DEP-02 dan strategi preview |
| Q-02 | Apakah dashboard yang dibuka lewat `file://` (tanpa server) dapat diterima tanpa tautan "Buka materi"? Data kurikulum tertanam sehingga dashboard tetap berfungsi; hanya `chapters.json` tidak dapat dimuat lewat `fetch` di `file://`. | Ketersediaan tautan materi saat pratinjau lokal |
| Q-03 | Apakah tata letak yang diusulkan (dashboard di `/`, MkDocs di `/materi/`) disetujui, atau MkDocs sebagai situs utama dengan dashboard sebagai halaman di dalamnya? | Bagian 7 dan 8 |
| Q-04 | Apakah rilis acuan tetap Ubuntu 24.04 LTS, dan versi Postfix/Dovecot/Rspamd/Roundcube apa yang dikunci? | Isi semua chapter praktik |
| Q-05 | Apakah chapter opsional dihitung dalam progres 100%? (default PRD: tidak, FR-022) | Definisi progres |
| Q-06 | Siapa pemilik produk dan peninjau materi, dan bagaimana bukti uji VM didokumentasikan (catatan di PR, log di berkas, atau terpisah)? | MNT-07, AC-27 |
| Q-07 | Bila chapter dihapus atau ID dipensiunkan, bagaimana progres pengguna yang ada diperlakukan (hapus, simpan, tandai usang)? | PRG-04 |
| Q-08 | Apakah diperlukan keluaran PDF/ePub (buku), dan dengan alat apa? | NFR-018, tambahan build |
| Q-09 | Lisensi untuk kode dan materi apa? | NFR-020, RK-12 |
| Q-10 | Apakah pencarian isi materi harus tergabung di dashboard (FR-011) atau cukup memakai pencarian MkDocs? | Ukuran dashboard, kompleksitas build |
| Q-11 | Apakah sinkronisasi progres antar perangkat (selain ekspor/impor manual) diperlukan di masa depan? | Dapat membatalkan non-goal "tanpa server" |
| Q-12 | Apakah domain kustom direncanakan? | URL-01/02, konfigurasi DNS Pages |
| Q-13 | Chapter mana yang menjadi chapter pertama yang diterbitkan, dan urutan prioritas penulisan sesudahnya? | Rencana iterasi |

---

## 13. Milestone Proyek

Milestone disusun berurutan; setiap milestone menghasilkan sesuatu yang dapat diverifikasi dan tidak memulai milestone berikutnya sebelum **gerbang keluar** (exit gate) terpenuhi. Estimasi usaha bersifat relatif (**S** ≤ 1 hari kerja, **M** 2–4 hari, **L** 1–2 minggu) dan merupakan **[Asumsi A-11]**: satu pemilik dengan Claude Code, paruh waktu. Tanggal kalender sengaja tidak ditetapkan sampai Q-06 dan Q-13 dijawab.

Pekerjaan yang sudah selesai sebelum M0: audit (`docs/project-audit.md`), PRD (`docs/PRD.md`), dan perbaikan F-01…F-11 pada `kurikulum-mail-server-ubuntu.html` (belum diuji di browser).

### 13.1 Ringkasan

| ID | Milestone | Hasil utama | Usaha | Bergantung pada |
|---|---|---|---|---|
| M0 | Fondasi repositori | Git, GitHub, README, lisensi, baseline | S | Q-01, Q-09 |
| M1 | Stabilisasi dashboard | Perbaikan F-01…F-11 terbukti di browser, uji otomatis dasar | M | M0 |
| M2 | Ekstraktor dan validator data | Ekstraksi hanya-baca blok data dashboard, `.build/curriculum.json` berobjek bernama, JSON Schema, validator graf | M | M1 |
| M3 | Kontrak progres dan skrip materi | `materi/assets/progress.js`, fixture v1, uji kontrak lintas implementasi (dashboard tetap satu berkas) | M | M2 |
| M4 | Kerangka MkDocs | `mkdocs.yml`, perintah `scaffold`, generator `nav` (keluaran di `.build/`), template 14 bagian | M | M2, Q-03 |
| M5 | Integrasi dan CI/CD ke GitHub Pages | Pipeline, deploy, URL dan base path teruji | M | M3, M4 |
| M6 | Chapter pilot | Satu chapter terbit dari ujung ke ujung | M | M5, Q-04, Q-13 |
| M7 | Rilis publik v1.0 | Hardening, SEO, aksesibilitas, dokumentasi kontribusi | M | M6 |
| M8 | Produksi konten bertahap | Satu chapter per iterasi, berulang | L (berulang) | M7 |
| M9 | Vercel dan peningkatan opsional | `vercel.json`, header keamanan, fitur tambahan | M | M7 |

### 13.2 Rincian

**M0. Fondasi repositori**
- Cakupan: `git init`, komit baseline file saat ini, buat repositori GitHub, `README.md`, `.gitignore` (mengabaikan `site/`), lisensi kode dan materi, cabang `main` dilindungi, pemindai rahasia aktif.
- Kebutuhan: RK-01, NFR-013, NFR-020, DEP-01, SEC-01.
- Gerbang keluar: repositori ada di GitHub, komit baseline memuat dashboard, audit, dan PRD; lisensi tercantum; `main` terlindungi.

**M1. Stabilisasi dashboard**
- Cakupan: uji manual dan otomatis (Playwright) untuk perbaikan F-01…F-11; perbaiki regresi yang ditemukan; fixture berkas ekspor v1; peringatan bila `localStorage` tidak tersedia (NFR-011).
- Kebutuhan: FR-004, FR-005, FR-006, FR-026, FR-030, FR-031, NFR-011, NFR-019, PRG-02, PRG-06.
- Gerbang keluar: AC-01, AC-02, AC-03, AC-05, AC-06, AC-07, AC-08, AC-09, AC-10 lulus.

**M2. Ekstraktor dan validator data**
- Cakupan: alat ekstraksi hanya-baca atas blok `/*DATA-START*/…/*DATA-END*/` pada dashboard (tanpa mengubah dashboard); normalisasi menjadi objek bernama di `.build/curriculum.json`; JSON Schema; skrip validasi (ID unik, prasyarat valid, tanpa siklus); uji fixture untuk penanda hilang/ganda. Catatan: ID kategori yang di-hardcode untuk jadwal dan capstone pada dashboard dicatat sebagai utang teknis, bukan pekerjaan milestone ini.
- Kebutuhan: FR-050, FR-051, FR-060.
- Gerbang keluar: AC-20 lulus; artefak memuat 16 kategori, 36 modul, 136 chapter yang cocok dengan hitungan dashboard (perbandingan otomatis atas ID, judul, menit, prasyarat); berkas dashboard tidak berubah (hash sama).

**M3. Kontrak progres dan skrip materi**
- Cakupan: dokumentasikan kontrak progres v1 (kunci, skema, ekspor); tulis `materi/assets/progress.js` untuk halaman materi; uji kontrak yang menjalankan fixture yang sama pada dashboard dan `progress.js`. Dashboard tetap satu berkas dan tidak dipecah.
- Kebutuhan: PRG-01, PRG-02, PRG-03, INT-02, INT-03, NFR-009.
- Gerbang keluar: AC-35 dan uji kontrak lulus pada kedua implementasi; AC-01…AC-10 tetap lulus (tanpa regresi); AC-13 terukur.

**M4. Kerangka MkDocs**
- Cakupan: `mkdocs.yml` (`docs_dir: materi`), `requirements.txt` terkunci, template chapter 14 bagian, perintah `scaffold` (manual), generator `nav` dan `exclude_docs` ke `.build/mkdocs.generated.yml`, banner `draft` (atau pengecualian build), panduan penulisan chapter untuk Claude Code, skrip validasi front matter dan heading, pemindai rahasia sederhana. Keputusan versi mengikuti verifikasi A-05.
- Kebutuhan: FR-040…FR-045, FR-052, FR-053, FR-060…FR-063, FR-065, NFR-012.
- Gerbang keluar: AC-21, AC-22, AC-23, AC-24 lulus; `mkdocs build --strict` sukses dengan seluruh chapter `draft`.

**M5. Integrasi dan CI/CD ke GitHub Pages**
- Cakupan: rakit `site/` (dashboard di akar, MkDocs di `materi/`); skrip bersama untuk status belajar pada halaman materi; tautan "Buka materi" bersyarat; `.nojekyll`; workflow GitHub Actions dengan izin minimal dan versi tersemat; pemeriksa tautan; uji di `/` dan `/<repo>/`; halaman 404 kustom.
- Kebutuhan: FR-046, FR-054, FR-055, INT-01…INT-06, URL-01…URL-10, DEP-02…DEP-05, SEC-04.
- Gerbang keluar: AC-25, AC-30, AC-31, AC-32, AC-33, AC-34, AC-36, AC-39, AC-40 lulus.

**M6. Chapter pilot**
- Cakupan: tulis dan terbitkan satu chapter dari ujung ke ujung (rekomendasi CH-01-01-01 yang konseptual, lalu satu chapter praktik kecil seperti CH-02-01-02), uji perintah di VM bersih, catat `verified_on`, jalankan alur PR → CI → deploy; evaluasi template dan panduan; perbaiki alur.
- Kebutuhan: FR-040…FR-043, FR-061, FR-064, NFR-015, NFR-016.
- Gerbang keluar: AC-25, AC-26, AC-27, AC-28 lulus untuk chapter pilot; retrospektif tertulis memutuskan perubahan template/alur.

**M7. Rilis publik v1.0**
- Cakupan: metadata SEO dan Open Graph, favicon, `canonical`, sitemap; audit aksesibilitas dan kinerja; `CHANGELOG.md`; panduan kontribusi; pengingat ekspor progres (opsional); pembaruan Panduan (definisi progres, batas lab/produksi); pemeriksaan tautan eksternal terjadwal.
- Kebutuhan: FR-033, NFR-001…NFR-007, MNT-03…MNT-05, PRG-07, FR-028 (opsional).
- Gerbang keluar: definisi selesai MVP (bagian 11.4) terpenuhi; AC-11, AC-12, AC-13 lulus; tag rilis `v1.0.0`.

**M8. Produksi konten bertahap** (berulang)
- Siklus per iterasi: pilih chapter → Claude Code menulis dari template → uji di VM → review → PR → CI hijau → merge → deploy → perbarui `CHANGELOG`.
- Urutan: ikuti graf prasyarat, mulai Level 0–1 (CAT-01, CAT-02), lalu CAT-03…; chapter opsional diprioritaskan terakhir. Urutan rinci menunggu Q-13.
- Kebutuhan: FR-064, MNT-01, MNT-02, NFR-015.
- Gerbang per iterasi: AC-22, AC-23, AC-25, AC-27, AC-28 lulus untuk chapter tersebut. Gerbang per kategori: seluruh chapter wajib kategori berstatus `published` sebelum kategori ditandai selesai.
- Titik pemeriksaan: setiap 10 chapter diadakan tinjauan konsistensi gaya, tautan, dan versi paket.

**M9. Vercel dan peningkatan opsional**
- Cakupan: `vercel.json` (build command, `outputDirectory: site`, header CSP dan keamanan), preview per PR; opsional: pencarian isi materi di dashboard (FR-011), filter di URL (FR-013), keluaran PDF (Q-08), progres berbobot menit (FR-029).
- Kebutuhan: DEP-06, DEP-08, SEC-07, NFR-014.
- Gerbang keluar: AC-38 lulus; pilihan fitur opsional dinilai terhadap AC-13 (batas ukuran).

### 13.3 Graf ketergantungan

```
M0 → M1 → M2 ─┬→ M3 ─┐
              └→ M4 ─┴→ M5 → M6 → M7 ─┬→ M8 (berulang)
                                       └→ M9
```

M3 dan M4 dapat dikerjakan paralel setelah M2 selesai (keduanya hanya bergantung pada skema data).

### 13.4 Keputusan yang dibutuhkan sebelum tiap milestone

| Sebelum | Pertanyaan yang harus terjawab |
|---|---|
| M0 | Q-01 (publik/privat), Q-09 (lisensi) |
| M2 | Q-05 (progres opsional), Q-07 (nasib ID yang dihapus) |
| M4 | Q-03 (tata letak situs), A-05 (status MkDocs Material) |
| M5 | Q-12 (domain kustom) |
| M6 | Q-04 (rilis acuan dan versi paket), Q-06 (peninjau dan bukti uji), Q-13 (chapter pertama) |
| M7 | Q-08 (PDF), Q-10 (pencarian isi) |

### 13.5 Risiko jadwal

- **Uji VM adalah penghambat utama M6 dan M8.** Waktu per chapter praktik bergantung pada kompleksitas dan tidak dapat dipercepat oleh otomasi. Mitigasi: ukur waktu nyata di M6 dan perbarui estimasi M8.
- **M8 tidak memiliki akhir yang dekat**: 136 chapter ≈ 250 jam belajar, penulisan dan pengujian memerlukan jauh lebih lama. Mitigasi: tetapkan target cakupan rilis (mis. L0–L5 untuk v1.1) setelah M6.
- **Perubahan keputusan arsitektur setelah M5** (mis. memindah tata letak situs) mengubah URL; Q-03 harus selesai sebelum M4.

---

## Lampiran A. Pemetaan Temuan Audit ke Kebutuhan

| Temuan audit | Kebutuhan terkait |
|---|---|
| F-01 anchor | FR-004, AC-01 |
| F-02 sinkronisasi tab | FR-026, PRG-05, AC-05 |
| F-03 hash malformed | FR-005, AC-02 |
| F-04 definisi progres | FR-022, FR-023, PRG-07, AC-06 |
| F-05 fokus drawer | FR-006, AC-03 |
| F-06 pencarian isi | FR-011, INT-08, Q-10 |
| F-07 kilatan tema | FR-031, AC-10 |
| F-08 validasi tema | NFR-010 |
| F-09 teks internal bocor | FR-044 (banner konsisten) |
| F-10 pengumuman rute | NFR-005, AC-11 |
| F-11 HTML mentah | JS-07 |
| F-12 fitur belum ada | Non-goals bagian 3.2, FR-013, FR-028, Q-11 |
| D-01 nama file | URL-09 |
| D-03 SEO/OG | FR-033, URL-07, AC-12 |
| D-05 localStorage bersama | RK-11, PRG-01 |
| D-06 Jekyll | URL-08 |
| D-07 CSP | JS-06, SEC-07 |
| D-10 subpath | URL-01, URL-10, AC-30 |
| R-01…R-11 | RK-01…RK-13 |

## Lampiran B. Urutan Implementasi yang Disarankan

1. `git init`, `README.md`, komit baseline, remote GitHub. (RK-01)
2. Bangun ekstraktor hanya-baca atas blok data dashboard, JSON Schema, dan skrip validasi. (FR-050/051/060)
3. Dokumentasikan kontrak progres v1 dan tulis `progress.js` untuk halaman materi dengan uji kontrak lintas implementasi. (PRG-03, INT-02/03)
4. Siapkan MkDocs, perintah `scaffold`, generator `nav`, dan tautan "Buka materi". (FR-040…054)
5. CI GitHub Actions (validasi, build, uji, deploy ke Pages). (DEP-02…05)
6. Uji otomatis dashboard (AC-01…AC-10) dan pemeriksa tautan (AC-30/31).
7. Tulis dan terbitkan chapter pertama sebagai uji alur penuh (bagian 11.4).
8. Ulangi satu chapter per iterasi (FR-064).

## Lampiran C. Status Implementasi dan Keterujian Setiap Persyaratan

### C.1 Legenda

**Status** (berdasarkan pembacaan `kurikulum-mail-server-ubuntu.html`; belum ada uji di browser):

| Kode | Arti |
|---|---|
| **ADA** | Sudah diimplementasikan dan tidak diubah sejak audit. Belum diuji otomatis |
| **ADA\*** | Sudah diimplementasikan, tetapi kodenya diubah setelah audit (perbaikan F-01…F-11) dan **belum diuji di browser** |
| **SEBAGIAN** | Sebagian sudah ada; bagian yang kurang disebut pada kolom bukti |
| **BARU** | Belum ada; harus dikembangkan |

**Metode uji:** **OTO** = uji otomatis di CI (skrip, Playwright, Lighthouse/axe, pemeriksa tautan); **MAN** = uji manual dengan daftar periksa tertulis dan hasil dicatat di PR; **REV** = tinjauan PR dengan daftar periksa; **INS** = inspeksi artefak (berkas, konfigurasi, pengaturan repositori).

Setiap baris memiliki kriteria lulus/gagal yang konkret, merujuk AC bila ada. Persyaratan yang di bagian 4–10 dirumuskan longgar dinyatakan ulang secara terukur pada kolom kriteria; bila ada selisih, **kolom kriteria di lampiran ini yang berlaku**.

### C.2 Functional requirements

| ID | Status | Metode | Kriteria lulus |
|---|---|---|---|
| FR-001 | ADA | OTO | Data menghasilkan 16 kategori, 36 modul, 136 chapter dengan ID berpola `CAT-NN`/`MOD-NN-NN`/`CH-NN-NN-NN`, tanpa duplikat (AC-20) |
| FR-002 | ADA | OTO | Rute `#/`, `#/tentang`, `#CAT-01`, `#CH-01-01-01` masing-masing merender judul yang benar |
| FR-003 | ADA | OTO | Halaman chapter memuat breadcrumb dan pager; pager chapter pertama tanpa "sebelumnya", terakhir tanpa "berikutnya" |
| FR-004 | ADA\* | OTO | AC-01 |
| FR-005 | ADA\* | OTO | AC-02 |
| FR-006 | ADA\* | OTO | AC-03 |
| FR-010 | ADA | OTO | AC-04 |
| FR-011 | BARU | OTO | Setelah ada chapter `published`, kata unik dari isinya mengembalikan chapter tersebut; kata dari chapter `draft` tidak |
| FR-012 | ADA | OTO | Tiap filter (kategori, status, belum selesai, siap dipelajari, hapus) mengubah jumlah hasil sesuai data uji; "hapus filter" mengembalikan 136 |
| FR-013 | BARU | OTO | Memuat `#/?q=dkim&cat=CAT-08` menerapkan filter yang sama dan mengisi kolom pencarian |
| FR-014 | ADA | OTO | Elemen `#rc` ber-`aria-live="polite"` dan teksnya berisi jumlah hasil setelah tiap filter |
| FR-020 | ADA | OTO | Memilih tiap dari 5 status menyimpan nilai 0/1/2/3/4 dan mengubah lencana |
| FR-021 | ADA | OTO | Mencentang checklist menyimpan `checks`; status chapter tidak berubah |
| FR-022 | ADA\* | OTO | AC-06 |
| FR-023 | ADA\* | OTO | AC-06; dengan semua CAT-01 wajib selesai, level = CAT-02 |
| FR-024 | ADA | OTO | Chapter pertama modul dengan `after` hanya "siap" setelah chapter terakhir modul tersebut Selesai; filter "Siap dipelajari" konsisten |
| FR-025 | ADA | OTO | Setelah mengubah status, hanya kunci `kurikulum-mail-ubuntu-v1` dan `kmu-theme` ada di `localStorage`; 0 permintaan jaringan (AC-39) |
| FR-026 | ADA\* | OTO | AC-05 |
| FR-027 | ADA | OTO | AC-07 |
| FR-028 | BARU | OTO | Dengan tanggal ekspor terakhir > 30 hari, pengingat tampil; ≤ 30 hari tidak tampil |
| FR-029 | BARU | OTO | Metrik berbobot menit = Σ menit chapter wajib Selesai / Σ menit wajib, cocok dengan hitungan skrip |
| FR-030 | ADA\* | OTO | AC-09; tema tersimpan dan terpulihkan setelah muat ulang |
| FR-031 | ADA\* | OTO | AC-10 |
| FR-032 | ADA | MAN | Pratinjau cetak Beranda dan satu chapter: sidebar, tombol, pager tidak muncul; konten tidak terpotong di tengah kartu |
| FR-033 | BARU | OTO | Lighthouse SEO ≥ 90; `<title>` berbeda per rute; tag `og:title`, `og:description`, favicon ada |
| FR-040 | BARU | OTO | Untuk tiap chapter `published`, `materi/chapter/<ID>.md` ada |
| FR-041 | BARU | OTO | Validator menggagalkan berkas yang kehilangan salah satu dari 7 field front matter (AC-22) |
| FR-042 | BARU | OTO | AC-22 |
| FR-043 | BARU | OTO | Setiap blok kode bertanda user/root punya label konteks; tidak ada nilai literal di luar placeholder `<[A-Z0-9_-]+>` atau domain dokumentasi (pemindai, AC-28); tombol salin menyalin teks tepat (uji Playwright) |
| FR-044 | BARU | OTO | Chapter `draft` menampilkan banner `.warnbox` atau tidak ada di `site/`, sesuai konfigurasi |
| FR-045 | BARU | OTO | Situs materi memiliki indeks pencarian, kontrol tema, tabel isi; pencarian "dkim" mengembalikan hasil |
| FR-046 | BARU | OTO | AC-34 |
| FR-047 | BARU | OTO | Tautan sebelumnya/berikutnya tiap halaman cocok dengan urutan `curriculum.json` |
| FR-050 | BARU | OTO | AC-20; tidak ada definisi struktur lain (pemindai: judul chapter hanya di blok data dashboard); `.build/curriculum.json` tidak dikomit |
| FR-051 | BARU | OTO | Artefak lolos JSON Schema; tidak ada data posisional pada artefak; ekstraksi gagal bila penanda hilang atau ganda (uji fixture) |
| FR-052 | BARU | OTO | `scaffold` pada bab baru membuat stub dengan 14 heading; pada bab yang sudah ada menolak menimpa (kode keluar ≠ 0, isi berkas tidak berubah) |
| FR-053 | BARU | OTO | AC-21; `mkdocs.yml` tidak berubah setelah build; `nav` hasil generasi cocok dengan urutan artefak |
| FR-054 | BARU | OTO | AC-25 |
| FR-055 | BARU | OTO | Dengan `materi/` dihapus dari `site/` (uji), semua fitur dashboard di AC-01…AC-10 tetap lulus |
| FR-060 | BARU | OTO | AC-20, AC-22 |
| FR-061 | BARU | OTO | AC-23 |
| FR-062 | BARU | OTO | AC-24 |
| FR-063 | BARU | INS | Berkas panduan penulisan ada, memuat template, aturan uji VM, dan gaya; ditinjau pemilik |
| FR-064 | BARU | REV | AC-26; PR menyentuh satu chapter |
| FR-065 | BARU | OTO | AC-42 (manifes sumber identik, `git status` bersih) |
| FR-066 | BARU | OTO | AC-41 |

### C.3 Non-functional requirements

| ID | Status | Metode | Kriteria lulus (terukur) |
|---|---|---|---|
| NFR-001 | BARU | OTO | Lighthouse mobile TTI ≤ 2,0 dtk dan LCP ≤ 2,5 dtk pada throttling bawaan (AC-12) |
| NFR-002 | BARU | OTO | AC-13: transfer dashboard ≤ 300 KB gzip; ≤ 500 KB bila indeks pencarian ikut |
| NFR-003 | BARU | OTO | Halaman materi tersebesar ≤ 250 KB gzip (skrip CI mengukur semua halaman) |
| NFR-004 | BARU | OTO | Playwright chromium, firefox, webkit: AC-01, AC-02, AC-05, AC-07 lulus pada ketiganya |
| NFR-005 | SEBAGIAN | OTO + MAN | Ada: skip link, label, `aria-*`, fokus terlihat. Kurang: audit. Lulus bila AC-11 dan daftar periksa WCAG 2.2 AA manual (kontras, fokus, target 24 px) lulus |
| NFR-006 | SEBAGIAN | OTO + MAN | Skenario hanya-keyboard: Tab/Enter/Space/Escape menyelesaikan J1–J4 tanpa mouse; tidak ada jebakan fokus |
| NFR-007 | SEBAGIAN | OTO | Pada viewport 320 px, `document.documentElement.scrollWidth` ≤ lebar viewport di Beranda, kategori, chapter, Panduan |
| NFR-008 | ADA | OTO | AC-39 |
| NFR-009 | ADA | OTO | AC-39; tidak ada `<script src>`/`<link href>` lintas-origin |
| NFR-010 | ADA | OTO | AC-07; impor berisi `<script>` pada nilai tidak menghasilkan elemen baru di DOM |
| NFR-011 | SEBAGIAN | OTO | Ada: cadangan memori. Kurang: peringatan. Lulus bila AC-08 |
| NFR-012 | BARU | INS | `requirements.txt` memuat versi tepat (`==`) untuk MkDocs, tema, plugin; CI memakai berkas itu |
| NFR-013 | BARU | INS | `git ls-files site/` kosong; `.gitignore` memuat `site/` |
| NFR-014 | BARU | OTO | AC-38 |
| NFR-015 | BARU | REV | Tiap PR chapter `published` berisi log uji: rilis OS, tanggal, setiap perintah dan hasil; peninjau menandai lulus |
| NFR-016 | BARU | OTO + REV | AC-28; peninjau memeriksa daftar periksa "tanpa data nyata" |
| NFR-017 | SEBAGIAN | OTO | Ada: `lang="id"` pada dashboard. Lulus bila semua halaman `site/` memuat `<html lang="id">`; kebakuan bahasa ditinjau manusia (REV) |
| NFR-018 | SEBAGIAN | MAN | Ada: CSS cetak dashboard. Lulus bila cetak-ke-PDF satu halaman materi menghasilkan teks yang dapat dipilih dan tanpa sidebar |
| NFR-019 | BARU | OTO | Rangkaian uji CI mencakup minimal: routing, filter, progres, ekspor/impor, sinkronisasi tab (≥ 1 kasus tiap area) dan harus lulus |
| NFR-020 | BARU | INS | Berkas lisensi kode dan lisensi materi ada di akar repositori dan dirujuk di README |

### C.4 Integrasi, URL, progres, JavaScript

| ID | Status | Metode | Kriteria lulus |
|---|---|---|---|
| INT-01 | BARU | OTO | AC-25; semua tautan materi cocok dengan pola `…/materi/chapter/<CH-ID>/` |
| INT-02 | BARU | OTO | AC-34 |
| INT-03 | BARU | OTO | Hanya satu `progress.js` di `materi/assets/`; uji kontrak lulus pada dashboard dan `progress.js` dengan fixture yang sama |
| INT-04 | BARU | OTO | Tautan dashboard dari materi mengarah ke hash yang ada di data (`#CH-…`, `#CAT-…`, `#/`) |
| INT-05 | BARU | REV | AC-26 |
| INT-06 | BARU | OTO | Dengan materi 404 (diblokir), `localStorage` progres tidak berubah |
| INT-07 | BARU | OTO | `chapters.json` memuat tepat bab yang halamannya ada di `site/`; bila berkas 404 atau rusak, dashboard tetap berfungsi tanpa tautan materi |
| INT-08 | BARU | OTO | Indeks pencarian memuat 0 entri `draft` dan 1 entri tiap chapter `published` |
| URL-01 | SEBAGIAN | OTO | Ada: dashboard tanpa aset. Lulus bila AC-30 |
| URL-02 | BARU | OTO | AC-32 |
| URL-03 | ADA | OTO | Seluruh rute dashboard bekerja dengan hanya `index.html` (server statis tanpa rewrite) |
| URL-04 | BARU | OTO | Daftar ID di rilis sebelumnya (disimpan di repositori) ⊆ daftar ID saat ini; ID yang hilang harus punya entri pengalihan |
| URL-05 | BARU | OTO | Semua URL `materi/chapter/` cocok dengan `^CH-\d{2}-\d{2}-\d{2}/$` |
| URL-06 | BARU | OTO | AC-33 |
| URL-07 | BARU | OTO | Tiap halaman materi memuat `<link rel="canonical">` dengan awalan `site_url` |
| URL-08 | BARU | INS | `.nojekyll` ada di artefak `site/` |
| URL-09 | BARU | OTO | AC-33; AC-42 (hash `site/index.html` = hash sumber) |
| URL-10 | BARU | OTO | AC-30 |
| PRG-01 | ADA | OTO | Fixture v1 diimpor dan hasil simpan memuat `"v":1`; migrasi dari versi lebih lama diuji bila versi baru dibuat |
| PRG-02 | ADA | OTO | AC-35 |
| PRG-03 | BARU | OTO | Fixture v1: muat → ubah → simpan menghasilkan JSON setara pada dashboard dan `progress.js`; impor ekspor v1 diterima oleh keduanya |
| PRG-04 | SEBAGIAN | OTO | Ada: ID tak dikenal diabaikan saat muat. Kurang: dipertahankan di penyimpanan (bergantung Q-07). Lulus bila perilaku yang diputuskan tertulis dan diuji |
| PRG-05 | ADA\* | OTO | AC-05 |
| PRG-06 | SEBAGIAN | OTO | Ada: tangkap error. Kurang: pemberitahuan pengguna. Lulus bila AC-08 dan toast muncul saat `setItem` melempar |
| PRG-07 | ADA\* | OTO | AC-06; Panduan memuat teks definisi persentase |
| PRG-08 | BARU | OTO | AC-34 |
| JS-01 | ADA | OTO | NFR-004 |
| JS-02 | SEBAGIAN | REV | Fitur baru yang tidak didukung semua target punya blok `@supports` atau pengecekan; daftar periksa PR |
| JS-03 | ADA | INS | Dashboard berjalan dari berkas statis tanpa tahap kompilasi (AC-30 dengan server berkas biasa) |
| JS-04 | BARU | OTO | Halaman materi: skrip progres berfungsi dengan dan tanpa navigasi instan (AC-34 diulang pada dua konfigurasi) |
| JS-05 | SEBAGIAN | OTO | Ada: `<noscript>` di dashboard. Lulus bila halaman materi memuat konten dengan JavaScript dimatikan (uji Playwright `javaScriptEnabled:false`) |
| JS-06 | BARU | OTO | Respons (Vercel atau server uji) membawa CSP berhash; hash cocok dengan blok `<script>` inline pada `site/index.html`; AC-01…AC-10 lulus di bawah CSP itu |
| JS-07 | ADA | INS | Komentar peringatan pada `CONTENT` ada; PR kontribusi luar memerlukan tinjauan (aturan cabang terlindungi) |

### C.5 Deployment, keamanan, pemeliharaan

| ID | Status | Metode | Kriteria lulus |
|---|---|---|---|
| DEP-01 | BARU | INS | Pengaturan repositori: `main` terlindungi, PR wajib |
| DEP-02 | BARU | INS | Pengaturan Pages memakai sumber "GitHub Actions"; deploy berhasil |
| DEP-03 | BARU | OTO | Berkas workflow memuat langkah sesuai urutan; satu proses berjalan hijau |
| DEP-04 | BARU | OTO | PR menjalankan semua langkah selain deploy; deploy tidak berjalan di PR (AC-36) |
| DEP-05 | BARU | OTO | AC-36 |
| DEP-06 | BARU | OTO | AC-38 |
| DEP-07 | BARU | MAN | AC-37 (latihan revert terdokumentasi) |
| DEP-08 | BARU | INS | Setiap PR menghasilkan artefak atau preview yang dapat dibuka |
| SEC-01 | BARU | OTO | AC-28 |
| SEC-02 | ADA | OTO | Semua `a[target=_blank]` memiliki `rel` berisi `noopener` dan `noreferrer` |
| SEC-03 | BARU | INS | Dependabot atau setara aktif; berkas konfigurasinya ada |
| SEC-04 | BARU | OTO | AC-40 |
| SEC-05 | BARU | REV | Daftar periksa PR: chapter dengan tindakan berisiko memuat peringatan pada bagian Security Review |
| SEC-06 | BARU | REV | Daftar periksa PR: tidak ada target pihak ketiga; pemindaian hanya "server milik sendiri" |
| SEC-07 | BARU | OTO | `vercel.json` memuat CSP, `X-Content-Type-Options`, `Referrer-Policy`; respons uji menampilkannya |
| MNT-01 | BARU | OTO | Skrip melaporkan chapter dengan `verified_on` > 365 hari; uji dengan tanggal palsu |
| MNT-02 | BARU | REV | PR perubahan rilis acuan menyentuh chapter satu per satu dengan log uji |
| MNT-03 | BARU | OTO | Workflow terjadwal bulanan ada; menjalankan pemeriksa tautan eksternal dan membuat issue saat gagal |
| MNT-04 | BARU | INS | `CHANGELOG.md` ada; tiap tag rilis punya entri |
| MNT-05 | BARU | INS | `README.md` memuat: struktur repositori, cara menjalankan lokal, cara menambah chapter, cara deploy |
| MNT-06 | BARU | INS | Catatan keputusan versi tema memuat tanggal verifikasi status proyek; tinjauan kuartalan tercatat |
| MNT-07 | BARU | INS | Nama pemilik produk dan peninjau tercantum di `README.md` atau `CODEOWNERS` |

### C.5b Struktur informasi dan navigasi

| ID | Status | Metode | Kriteria lulus |
|---|---|---|---|
| IA-01 | ADA | OTO | Sidebar menampilkan pohon 16 kategori → 36 modul → 136 chapter; breadcrumb dan pager ada pada halaman chapter |
| IA-02 | BARU | OTO | Urutan dan pengelompokan `nav` MkDocs identik dengan urutan kategori/modul/chapter di `curriculum.json` (skrip perbandingan) |
| IA-03 | BARU | OTO | Tiap halaman materi memuat tautan ke `#<CH-ID>` di dashboard; tiap chapter `published` di dashboard memuat tautan ke materinya (AC-25) |
| IA-04 | SEBAGIAN | OTO | Ada: dashboard (Beranda → kategori → chapter = 2 klik; pencarian + 1 klik). Lulus bila skrip menghitung klik ke setiap dari 136 chapter ≤ 3 dan ke materi ≤ 4 |
| IA-05 | SEBAGIAN | OTO | Ada: chapter `draft` tampil dengan banner di halaman chapter. Kurang: penanda di navigasi dan tautan "Buka materi" bersyarat. Lulus bila AC-25 dan tiap `draft` di sidebar punya penanda teks |

### C.6 Ringkasan

| Status | Jumlah persyaratan |
|---|---|
| ADA | 23 |
| ADA\* (diubah setelah audit, belum diuji di browser) | 10 |
| SEBAGIAN | 13 |
| BARU | 80 |
| **Total** | **126** |

Pernyataan "ADA" berarti kode implementasi terlihat pada pembacaan, bukan bahwa ia sudah teruji. Seluruh persyaratan berstatus ADA dan ADA\* menjadi bahan **M1 (Stabilisasi dashboard)** pada bagian 13: tujuan M1 adalah mengubah status itu menjadi "teruji" lewat uji otomatis di atas, tanpa mengubah implementasi kecuali uji menemukan cacat.
