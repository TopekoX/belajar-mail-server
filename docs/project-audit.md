# Audit Awal: Mail Server Ubuntu Learning Portal

- **Tanggal audit:** 2026-10-13
- **Cakupan:** seluruh isi `D:\ucup\Workspace\buku\belajar-mail-server`
- **Metode:** pembacaan kode sumber penuh (817 baris) dan ekstraksi data kurikulum dengan Node.js dari salinan di folder sementara. Tidak ada file proyek yang diubah atau dihapus. Satu-satunya tambahan adalah file laporan ini.
- **Batasan:** aplikasi belum dijalankan di browser. Temuan perilaku (mis. bug navigasi) berasal dari analisis kode dan perlu dikonfirmasi dengan uji manual. Akurasi teknis materi (versi paket, direktif Postfix/Dovecot) tidak diaudit.

Penanda: **[Asumsi]** adalah dugaan yang belum diverifikasi. **[Pertanyaan]** adalah hal yang perlu keputusan atau informasi dari pemilik proyek.

---

## 1. Ringkasan Eksekutif

Proyek saat ini berupa **satu file HTML mandiri (±89 KB)** yang berfungsi sebagai dashboard kurikulum. Isinya SPA vanilla JS tanpa build step dan tanpa library atau aset eksternal. Kerangkanya matang: 16 kategori, 36 modul, 136 chapter, prasyarat, pencarian, filter, pelacakan progres, ekspor/impor JSON, mode gelap, dan aksesibilitas dasar.

**Konten materinya belum ada.** Objek `CONTENT` kosong (`const CONTENT={};`), jadi 0 dari 136 chapter yang berisi materi. Semua halaman chapter menampilkan spesifikasi dan banner "Belum diimplementasikan".

Tiga hal paling penting:

1. **Bug navigasi:** tautan daftar isi di dalam chapter (`#s1`…`#s14`) dan tautan "Lewati ke konten utama" (`#main`) kemungkinan besar mengembalikan pengguna ke Beranda (lihat F-01).
2. **Arsitektur tidak skalabel untuk konten:** rencana mengisi `CONTENT` per chapter di dalam file HTML akan membuat satu file berisi ratusan KB sampai MB HTML-dalam-string. Ini tidak cocok untuk penulisan, review, dan versioning (lihat bagian 7).
3. **Tidak ada version control** (bukan repositori git) dan tidak ada README, sehingga satu-satunya salinan pekerjaan berisiko hilang.

Deployment ke GitHub Pages atau Vercel pada dasarnya mudah karena situs statis dengan routing berbasis hash. Hambatannya kecil (lihat bagian 5).

---

## 2. Struktur Direktori dan File

```
belajar-mail-server/
├── kurikulum-mail-server-ubuntu.html   88.994 byte, 817 baris
└── docs/
    └── project-audit.md                (laporan ini, baru)
```

Hanya ada satu file proyek. Yang **tidak ada**:

| Item | Dampak |
|---|---|
| `.git` (bukan repositori git) | Tanpa riwayat perubahan, tanpa backup, tanpa dasar untuk GitHub Pages/Vercel |
| `index.html` | GitHub Pages dan Vercel melayani `index.html` di root. Nama file saat ini membuat URL root menghasilkan 404 |
| `README.md`, `LICENSE` | Tidak ada dokumentasi proyek atau lisensi konten |
| `.gitignore`, `.nojekyll` | Belum relevan sekarang, perlu saat publikasi |
| `package.json` / `mkdocs.yml` | Tidak ada tooling build, lint, atau uji |
| Folder materi (`docs/*.md`) | Materi Markdown belum dimulai |
| Favicon, gambar, OG image | Tidak ada aset statis lain |
| Berkas uji | Tidak ada uji otomatis |

---

## 3. Struktur Kurikulum (Data di HTML)

Data berada di blok `/*DATA-START*/ … /*DATA-END*/` (baris 180–542). Hierarki: **Kategori → Modul → Chapter**.

### 3.1 Angka (diekstrak dengan menjalankan blok data)

| Metrik | Nilai |
|---|---|
| Kategori | 16 (level L0–L15) |
| Modul | 36 (4 di antaranya opsional) |
| Chapter | 136 (14 di antaranya di modul opsional) |
| Estimasi total | 15.000 menit = 250 jam |
| Chapter dengan `impl` (punya perintah/berkas, praktik) | 108 |
| Chapter konseptual | 28 |
| Chapter dengan `CONTENT` terisi | **0** |
| ID duplikat | 0 |

### 3.2 Daftar kategori

| ID | Lv | Lingkungan | Modul | Chapter | Menit |
|---|---|---|---|---|---|
| CAT-01 Orientasi dan Persiapan Belajar | 0 | lab | 1 | 3 | 240 |
| CAT-02 Dasar Linux dan Jaringan | 1 | lab | 4 | 12 | 1290 |
| CAT-03 Fundamental Arsitektur Email | 2 | lab | 2 | 7 | 630 |
| CAT-04 Persiapan Ubuntu Server | 3 | lab | 3 | 8 | 720 |
| CAT-05 Domain dan Infrastruktur DNS | 4 | domain | 2 | 7 | 570 |
| CAT-06 Instalasi Inti (Postfix, Dovecot) | 5 | lab | 2 | 10 | 1080 |
| CAT-07 Mailbox dan Konfigurasi Klien | 6 | lab | 2 | 7 | 630 |
| CAT-08 TLS dan Autentikasi Email | 7 | domain | 2 | 8 | 900 |
| CAT-09 Webmail dan Layanan Pendukung | 8 | lab | 1 | 4 | 450 |
| CAT-10 Security Hardening dan Threat Defense | 9 | lab | 3 | 14 | 1620 |
| CAT-11 Monitoring, Otomasi, Backup, DR | 10 | lab | 3 | 11 | 1170 |
| CAT-12 Deployment Publik dan Kesiapan Produksi | 11 | publik | 2 | 8 | 780 |
| CAT-13 Operasi dan Administrasi Email | 12 | produksi | 3 | 15 | 1500 |
| CAT-14 Troubleshooting dan Incident Response | 13 | produksi | 2 | 7 | 780 |
| CAT-15 Infrastruktur Email Lanjutan (opsional) | 14 | publik | 3 | 10 | 1320 |
| CAT-16 Capstone dan Penilaian Operasional | 15 | publik | 1 | 5 | 1320 |

### 3.3 Skema ID dan data

- ID: `CAT-NN`, `MOD-NN-NN`, `CH-NN-NN-NN`. Juga diturunkan `LAB-…` dan `ASM-…` per chapter (belum ada halamannya, hanya label).
- Chapter didefinisikan sebagai array posisional: `[judul, menit, [tujuan], "perintah | berkas"]`. Rawan salah urut dan sulit divalidasi.
- Prasyarat diturunkan otomatis: chapter ke-*k* bergantung pada chapter ke-(*k*−1) dalam modul yang sama. Chapter pertama bergantung pada chapter terakhir tiap modul di `after`. Referensi modul tak dikenal melempar `Error` saat load, sehingga ada validasi minimal.
- Konvensi `impl` = "string perintah/berkas tidak kosong", **bukan** "materi sudah diimplementasikan". Nama ini membingungkan karena banner dan Panduan memakai kata "diimplementasikan" untuk arti yang berbeda.

### 3.4 Inkonsistensi data yang ditemukan

- Tabel "Jalur dari Lab ke Produksi" (`renderAbout`) menaruh CAT-05 (lingkungan *domain*) di Tahap 1 "Lab lokal", dan CAT-09 (lingkungan *lab*) di Tahap 2 "Lab + domain".
- `CAT-12` berlabel `pub`, sedangkan modul keduanya `prod`. Ini sah (ada override per modul), tetapi belum terdokumentasi.
- `renderCat` memakai ID kategori yang di-hardcode (`"CAT-13"`, `"CAT-16"`) untuk menampilkan jadwal dan tabel capstone. Jika kategori disisipkan atau diurut ulang, bagian ini salah tempat tanpa error.
- Teks capstone menyebut "seluruh alat pada Level 1-8", sedangkan pelatihan keamanan dan operasional ada di Level 9–12. Perlu dipastikan maksudnya.

---

## 4. Fitur JavaScript

### 4.1 Yang sudah ada dan berfungsi (berdasarkan pembacaan kode)

| Fitur | Implementasi |
|---|---|
| Routing | Hash: `#/` (beranda), `#/tentang`, `#CAT-xx`, `#CH-xx-xx-xx`. `hashchange` memanggil `route()` |
| Navigasi samping | Pohon kategori → modul → chapter dengan `aria-expanded`, penanda status (glyph + teks tersembunyi `.sr`), tautan aktif `aria-current` |
| Breadcrumb dan pager | Prev/next berurutan lintas seluruh chapter |
| Pencarian | Input teks. Pencocokan substring semua kata (AND) terhadap `ch.hay` = ID + judul + modul + kategori + tujuan + perintah/berkas |
| Filter | Kategori, status, "Belum selesai", "Siap dipelajari" (prasyarat selesai), "Hapus filter". Hasil muncul di sidebar dan beranda |
| Status chapter | 5 tingkat: Belum Dimulai → Selesai (`<select>` per chapter). Disimpan di `state.status` |
| Checklist | Centang persiapan dan kelulusan per chapter (`state.checks`). **Tidak** mengubah status otomatis (disengaja, tertulis di UI) |
| Progres | `stats()`: persentase = chapter berstatus Selesai / 136. Bar di header, per kategori, dan "Level saat ini" (kategori pertama yang belum semua selesai) |
| Persistensi | `localStorage` kunci `kurikulum-mail-ubuntu-v1` (progres) dan `kmu-theme`. Ada fallback memori bila storage diblokir |
| Ekspor/Impor/Reset | Ekspor Blob JSON, impor `FileReader` dengan validasi `app` dan `sanitize()` (hanya ID dikenal, status 1–4, kunci checklist berpola), `confirm()` sebelum menimpa |
| Tema | Terang/gelap, awal mengikuti `prefers-color-scheme`, disimpan |
| Salin kode | `navigator.clipboard` dengan fallback `execCommand` |
| Aksesibilitas | Skip link, `role="search"`, `aria-live`, `focus-visible`, `prefers-reduced-motion`, drawer mobile dengan Escape, tabel dalam wrapper scroll |
| Cetak | `@media print` menyembunyikan sidebar, tombol, dan pager |
| Keamanan render | `esc()` konsisten untuk data kurikulum. Impor di-sanitasi |

### 4.2 Temuan (bug dan kelemahan)

| ID | Tingkat | Temuan |
|---|---|---|
| **F-01** | Tinggi | **Tautan anchor internal merusak routing.** Daftar isi tiap chapter memakai `<a href="#s1" data-jump>`…`#s14`, dan skip link memakai `#main`. Tidak ada handler untuk `data-jump` (diverifikasi: tidak ada di blok event). Browser mengubah hash ke `#s5`, lalu `hashchange` memanggil `route()`. Karena `byId.get("s5")` tidak ada, `route()` jatuh ke cabang `else` dan merender Beranda, sehingga pengguna kehilangan chapter yang sedang dibuka. **Perlu dikonfirmasi lewat uji manual.** |
| **F-02** | Sedang | **Dua tab bisa saling menimpa progres.** `save()` menulis seluruh `state` dari memori tiap tab dan tidak ada listener event `storage`. Tab yang usang menimpa perubahan tab lain. |
| **F-03** | Sedang | **`decodeURIComponent` tanpa try/catch** di `route()`. Hash malformed (mis. `#%E0%A4%A`) melempar `URIError`. Saat dimuat awal, ini menghentikan skrip dan halaman kosong. |
| **F-04** | Sedang | **Konsistensi persentase.** Progres = jumlah chapter, bukan menit. Chapter opsional (14) ikut dalam penyebut, sehingga 100% mensyaratkan topik opsional. "Level saat ini" juga menganggap CAT-15 (opsional) sebagai level yang harus dilewati sebelum Capstone. **[Pertanyaan]** apakah ini yang diinginkan? |
| **F-05** | Rendah | Sidebar mobile disembunyikan hanya dengan `transform`, sehingga tautannya tetap dapat difokus lewat keyboard saat drawer tertutup. Perlu `visibility:hidden` atau `inert`. |
| **F-06** | Rendah | Pencarian hanya mencakup metadata (judul, tujuan, perintah), belum isi materi. Setelah `CONTENT` terisi, pencarian tidak menemukan isi teori. Keadaan pencarian tidak masuk URL, tidak ada sorotan, tidak ada debounce (tidak masalah pada 136 item). |
| **F-07** | Rendah | Tema diterapkan di akhir body, sehingga mungkin terjadi kilatan tema salah (FOUC) pada mode gelap. |
| **F-08** | Rendah | Nilai tema dari `localStorage` dimasukkan ke atribut `data-theme` tanpa validasi. Dampak keamanan nyata sangat kecil. |
| **F-09** | Rendah | Halaman Panduan (`renderAbout`) dan banner chapter menyebut "percakapan terpisah"/"percakapan berikutnya". Ini catatan alur kerja internal yang bocor ke UI publik dan perlu diganti sebelum dipublikasikan. |
| **F-10** | Rendah | `main` memakai `aria-live="off"` dan pindah fokus ke `main` saat rute berubah. Wajar, tetapi judul halaman perlu diumumkan dengan jelas. Perlu uji dengan pembaca layar. **[Asumsi]** hasilnya baik. |
| **F-11** | Info | Seluruh konten `CONTENT` nantinya disuntikkan lewat `innerHTML` tanpa escape (`theory`, `steps`, dst. adalah HTML mentah). Aman selama penulis tepercaya. Jika kelak ada kontribusi pihak lain, ini menjadi vektor XSS. |
| **F-12** | Info | Fitur yang belum ada: pencarian isi materi, navigasi berbasis URL untuk filter, catatan pribadi, sinkronisasi antar perangkat (hanya ekspor manual), analitik (disengaja tidak ada), service worker/PWA/offline. |

---

## 5. Ketergantungan Eksternal dan Kesiapan Deployment

### 5.1 Ketergantungan

| Aspek | Temuan |
|---|---|
| Library JS/CSS | **Tidak ada.** Tidak ada `<script src>`, `<link rel>`, `@import`, CDN, atau framework |
| Font | Tumpukan font sistem (`system-ui`, `ui-monospace`). Tidak ada web font |
| Gambar | Tidak ada. Diagram dibuat dengan SVG inline |
| Panggilan jaringan | Tidak ada `fetch`/XHR. Footer menyatakan tidak ada data dikirim |
| URL eksternal | Hanya 8 tautan dokumentasi (`<a target="_blank" rel="noopener noreferrer">`): Ubuntu docs, packages.ubuntu.com, Postfix, Dovecot, Roundcube, Let's Encrypt, Rspamd, RFC Editor |
| Fitur browser modern | Dipakai: `color-mix()`, CSS `inset`, `:focus-visible`, `Map`/`Set`, spread. **[Asumsi]** target browser = evergreen. `color-mix` butuh Chrome 111+/Safari 16.2+/Firefox 113+ |
| Runtime tooling | Tidak diperlukan. File dapat dibuka langsung dari disk (`file://`) |

Kesimpulan: **sangat portabel dan kuat terhadap kegagalan CDN**. Ini kekuatan utama arsitektur saat ini.

### 5.2 Risiko di GitHub Pages dan Vercel

| ID | Risiko | Tingkat | Uraian dan mitigasi |
|---|---|---|---|
| D-01 | Nama file bukan `index.html` | Tinggi | URL root akan 404. Ganti nama (atau salin) menjadi `index.html` saat publikasi, atau tambahkan `index.html` yang me-redirect |
| D-02 | Bug anchor F-01 | Tinggi | Muncul di produksi persis seperti lokal. Perbaiki sebelum publikasi |
| D-03 | URL chapter tidak dapat diindeks | Sedang | Routing hash (`#CH-…`) aman di host statis tanpa konfigurasi rewrite. Namun tiap chapter tidak punya URL/`<title>` yang dapat diindeks. Crawler hanya melihat satu halaman, sehingga SEO dan pratinjau tautan (Open Graph) lemah. Tidak ada `og:*`, `<link rel="canonical">`, favicon, atau `robots`/sitemap |
| D-04 | Pengendalian cache | Sedang | Satu file besar tanpa hash nama berkas. Pada Pages, cache `max-age` 10 menit. Pada Vercel, atur header. Tanpa versi pada aset, pengguna bisa melihat versi lama sebentar. Tidak kritis untuk satu file |
| D-05 | Bentrok `localStorage` per origin | Sedang | Di GitHub Pages `pengguna.github.io` berbagi satu origin untuk semua repo. Kunci sudah di-namespace (`kurikulum-mail-ubuntu-v1`), jadi tabrakan kecil. Jika portal dan MkDocs dipasang di origin yang sama, progres tetap dapat dibagi (lihat bagian 6) |
| D-06 | Jekyll di Pages | Rendah | Jika memakai "deploy from branch", Jekyll memproses repo. Tambahkan `.nojekyll`, atau pakai GitHub Actions |
| D-07 | Content-Security-Policy | Rendah | Skrip dan gaya inline mencegah CSP ketat tanpa `'unsafe-inline'`. Memecah ke `app.js` dan `style.css` memungkinkan CSP ketat. Pages tidak dapat mengatur header HTTP. Vercel bisa lewat `vercel.json` |
| D-08 | Pemisahan data publik dan progres | Info | Karena progres hanya lokal, tidak ada data pribadi di server. Tidak ada kebutuhan privasi tambahan selain catatan di UI |
| D-09 | Repositori publik vs materi | Info | Konten menyebut kredensial/log harus disanitasi. Pastikan tidak ada contoh kredensial atau IP nyata saat materi ditulis |
| D-10 | Subpath proyek | Info | Aman: tidak ada path absolut aset. Namun saat memakai MkDocs, `site_url` dan tautan relatif harus konsisten dengan `/nama-repo/` |

**Perbedaan praktis:** GitHub Pages cocok untuk situs statis tanpa konfigurasi (via Actions untuk MkDocs). Vercel unggul untuk header kustom, preview per PR, dan `vercel.json`, tetapi butuh build command (mis. `pip install` + `mkdocs build`) dan `outputDirectory: site`. **[Pertanyaan]** target utama yang mana? Rekomendasi: GitHub Pages bila repositori publik dan tanpa kebutuhan header khusus.

---

## 6. Kebutuhan Integrasi dengan MkDocs

### 6.1 Mengapa MkDocs

Rencana `CONTENT` per chapter dengan 14 bagian × 136 chapter menghasilkan sekitar 1.900 bagian. Menyimpannya sebagai string HTML di JavaScript menyulitkan penulisan (escape, tanpa penyorotan sintaks, tanpa pratinjau), review diff, linting, dan pencarian. Markdown di MkDocs menyelesaikan ini dan memberi pencarian, navigasi, penyorotan kode, tombol salin, dan tema gelap bawaan.

### 6.2 Pemetaan skema `CONTENT` ke Markdown

| Bagian CONTENT | Bagian Markdown |
|---|---|
| `theory`, `steps` | Paragraf dan daftar bernomor |
| `cmds` (`ctx`, `label`, `code`, `out`) | Code fence dengan judul (`title="…"`), konteks user/root lewat anotasi atau admonition |
| `cfgs` (`path`, `code`, `explain`) | Code fence dengan `title="/etc/…"` + paragraf |
| `trouble` | Tabel Markdown |
| `verify`, `security`, `exercises`, `assessment` | Daftar, admonition, atau task list |
| `refs` | Daftar tautan |

Struktur 14 bagian chapter dapat dijadikan **templat Markdown tetap** (heading H2 identik). Front matter YAML memuat `id`, `title`, `minutes`, `environment`, `prerequisites`.

### 6.3 Opsi arsitektur

| Opsi | Uraian | Kelebihan | Kekurangan |
|---|---|---|---|
| **A. Dashboard tetap berdiri sendiri + MkDocs untuk materi** | HTML disalin ke `docs/` sebagai halaman statis (atau di-host berdampingan), tautan chapter mengarah ke halaman MkDocs | Perubahan paling kecil | Dua sumber kebenaran: struktur kurikulum di JS dan di `mkdocs.yml` bisa tak sinkron |
| **B. Satu sumber data (`curriculum.json`) → menghasilkan dua keluaran** (rekomendasi) | Ekstrak `CATS`, `CAPSTONE`, `SCHED`, `REFS` ke JSON/YAML. Skrip build menghasilkan (1) stub `.md` per chapter dengan front matter dan (2) bagian `nav` di `mkdocs.yml`. Dashboard memuat JSON dan menaut ke `/materi/CH-xx-xx-xx/` | Tidak ada duplikasi struktur, ID stabil, dapat divalidasi | Perlu skrip generator dan mengubah dashboard dari data inline menjadi `fetch`. `file://` tidak akan bekerja lagi untuk `fetch` (butuh server lokal) |
| **C. Pindahkan semuanya ke MkDocs, buang dashboard** | Gunakan tema Material | Paling sederhana dikelola | Kehilangan progres tracking, prasyarat, dan filter. Perlu JS kustom untuk mengembalikannya |

Opsi B mempertahankan nilai portal (progres, prasyarat, filter) sambil memindahkan penulisan ke Markdown. Opsi A dapat dipakai sebagai langkah awal.

### 6.4 Hal teknis yang perlu diputuskan

1. **Mode data dashboard.** Inline (saat ini, jalan lewat `file://`) atau `fetch('curriculum.json')` (butuh HTTP). Alternatif: build step menyisipkan JSON kembali ke HTML.
2. **Progres lintas halaman.** `localStorage` dibagi per origin. Bila dashboard dan halaman MkDocs satu origin dan satu kunci (`kurikulum-mail-ubuntu-v1`), chapter MkDocs dapat menambahkan kontrol status kecil (`extra_javascript`) dan dashboard membaca keadaan yang sama. Hindari dua kunci berbeda.
3. **Tautan stabil.** Pola URL chapter harus ditetapkan sebelum menulis (mis. `materi/CAT-06/MOD-06-01/CH-06-01-02/`), karena dipakai dashboard, breadcrumb, dan referensi silang. Mengubahnya kemudian merusak tautan.
4. **Pencarian.** Pencarian bawaan MkDocs mengindeks isi materi. Pencarian dashboard hanya metadata. Putuskan apakah dashboard mengarahkan ke pencarian MkDocs atau menggabungkan indeks.
5. **Chapter pending.** Stub chapter harus menampilkan banner "belum ditulis" yang konsisten (ambil dari front matter `status: draft`), dan sebaiknya dapat dikeluarkan dari build (`exclude`/plugin) sampai siap.
6. **Validasi.** Skrip CI untuk memeriksa: ID unik, prasyarat valid, setiap chapter punya file `.md`, front matter lengkap, tautan internal tidak rusak (`mkdocs build --strict`).
7. **Pemilihan tema/versi MkDocs.** **[Asumsi, perlu diverifikasi]** MkDocs Material dikabarkan memasuki mode pemeliharaan dan pengembangnya sedang membangun penerus (Zensical), serta ada diskusi mengenai MkDocs 2.x yang berpotensi tidak kompatibel dengan plugin lama. Periksa status terkini sebelum memilih dan kunci versi di `requirements.txt`.
8. **Kode dan placeholder.** Dashboard memakai konvensi placeholder `<HURUF-KAPITAL>` dan label konteks (user/root). Tentukan padanannya di Markdown (anotasi kode, admonition, atau plugin) agar gaya konsisten.
9. **Cetak/PDF.** Dashboard punya CSS cetak. Bila PDF buku dibutuhkan (nama folder `buku` mengisyaratkan hal ini), pertimbangkan plugin ekspor PDF. **[Pertanyaan]** apakah keluaran buku/PDF direncanakan?

---

## 7. Risiko

| ID | Risiko | Kemungkinan | Dampak | Mitigasi |
|---|---|---|---|---|
| R-01 | Tidak ada git atau backup, kehilangan pekerjaan | Sedang | Tinggi | `git init`, commit awal, remote privat |
| R-02 | File tunggal membengkak saat konten ditulis (1,9 ribu bagian HTML dalam string) | Tinggi | Tinggi | Pindahkan konten ke Markdown (bagian 6) |
| R-03 | Bug anchor F-01 menurunkan UX di semua chapter | Tinggi | Sedang | Tangani `data-jump`/`#main` atau ubah skema routing |
| R-04 | Duplikasi struktur antara HTML dan MkDocs bila memakai opsi A | Sedang | Sedang | Satu sumber data (opsi B) |
| R-05 | Kehilangan progres pengguna (localStorage, mode privat, bersihkan data) | Sedang | Sedang | Sudah ada ekspor/impor dan peringatan. Pertimbangkan pengingat ekspor berkala |
| R-06 | Akurasi teknis materi kedaluwarsa (rilis, versi paket, perubahan konfigurasi) | Sedang | Tinggi | Tetapkan versi referensi dan tanggal verifikasi per chapter. Uji tiap perintah pada VM bersih |
| R-07 | Materi keamanan/operasional disalahgunakan atau salah dipraktikkan di produksi | Rendah | Tinggi | Pertahankan peringatan "lab ≠ produksi", sanitasi contoh, hindari kredensial nyata |
| R-08 | Penulisan massal oleh AI tanpa pengujian | Sedang | Tinggi | Wajibkan uji VM per chapter dan review manusia sebelum status "implemented" |
| R-09 | Tidak ada uji otomatis, regresi saat refactor | Sedang | Sedang | Tambahkan uji smoke (jsdom/Playwright) untuk routing, filter, progres |
| R-10 | Data posisional `[judul, menit, [tujuan], "x|y"]` rawan salah | Sedang | Rendah | Ubah ke objek bernama dengan skema JSON saat ekstraksi |
| R-11 | Lisensi konten belum ditetapkan | Sedang | Sedang | Pilih lisensi (mis. CC BY-SA untuk materi, MIT untuk kode) sebelum publik |

---

## 8. Rekomendasi Teknis

### Prioritas 0: sebelum langkah lain

1. `git init`, tambahkan `README.md`, commit file saat ini sebagai baseline. (R-01)
2. Perbaiki F-01 (handler anchor atau skema routing untuk `#sN` dan `#main`), F-03 (try/catch pada `decodeURIComponent`), dan F-02 (listener `storage` atau muat ulang state sebelum menyimpan).

### Prioritas 1: fondasi

3. **Ekstrak data kurikulum** menjadi `curriculum.json` (atau YAML) dengan objek bernama, tanpa array posisional, ditambah JSON Schema. Tulis skrip validasi (ID unik, prasyarat ada, tidak ada siklus).
4. **Pisahkan** `index.html`, `assets/app.js`, `assets/style.css`, `data/curriculum.json`. Ini membuka jalan bagi CSP ketat, cache lebih baik, dan diff lebih bersih. Pertahankan opsi build yang menghasilkan satu file mandiri bila `file://` tetap diinginkan.
5. Tetapkan **pola URL chapter dan ID** final, lalu bekukan.
6. Putuskan definisi progres (F-04): apakah opsional dihitung, apakah berbasis menit.

### Prioritas 2: integrasi MkDocs (opsi B)

7. Buat `mkdocs.yml`, `requirements.txt` dengan versi terkunci, `docs/index.md`, dan folder `docs/materi/`.
8. Tulis generator yang membuat stub `.md` (front matter + 14 bagian) dan `nav` dari `curriculum.json`. Jangan menimpa file yang sudah ditulis manual.
9. Tambahkan CI (GitHub Actions): validasi data, `mkdocs build --strict`, deploy ke Pages.
10. Hubungkan dashboard dan halaman MkDocs lewat satu kunci progres.

### Prioritas 3: kualitas

11. Uji smoke otomatis (routing, filter, impor/ekspor, sanitasi).
12. Perbaiki F-05–F-09, tambahkan favicon, `og:*`, `canonical`, `.nojekyll`, dan `vercel.json` bila dipakai.
13. Terapkan alur kerja penulisan chapter: draft → uji di VM → review → ubah `status` front matter.
14. Putuskan lisensi dan kebijakan kontribusi.

---

## 9. Asumsi

- **A-1.** Browser sasaran adalah evergreen (karena `color-mix`, `:focus-visible`, dll.).
- **A-2.** Pengguna akhir adalah pembelajar tunggal per browser, tanpa akun atau server.
- **A-3.** Bahasa konten adalah Indonesia (`lang="id"`).
- **A-4.** Rilis referensi Ubuntu Server 24.04 LTS adalah yang sengaja dipilih (`REL`).
- **A-5.** Perilaku bug F-01 sesuai analisis kode, belum diuji di browser.
- **A-6.** Tidak ada aset atau file lain di luar direktori ini yang menjadi bagian proyek.

## 10. Pertanyaan Terbuka

1. Apakah repositori akan **publik atau privat**, dan di mana (GitHub Pages atau Vercel)?
2. Apakah **opsi B** (satu sumber data + MkDocs) diterima, atau dashboard ingin tetap satu file mandiri yang jalan lewat `file://`?
3. Apakah ada keluaran **buku/PDF/ePub** yang direncanakan (nama folder `buku`)?
4. Apakah rilis referensi tetap **Ubuntu 24.04 LTS**, atau perlu ditinjau ulang terhadap rilis LTS yang lebih baru? Versi Dovecot/Postfix pada rilis tersebut perlu diverifikasi karena perbedaan format konfigurasi antar versi mayor dapat memengaruhi materi. **[Perlu verifikasi]**
5. Apakah topik **opsional** (14 chapter) dihitung dalam progres 100%?
6. Siapa penulis dan reviewer materi, dan bagaimana **pengujian di VM** didokumentasikan sebagai bukti?
7. Lisensi apa untuk kode dan untuk materi?
8. Apakah diperlukan **sinkronisasi progres antar perangkat** (butuh backend atau gist), atau ekspor/impor manual sudah cukup?
9. Apakah pencarian harus mencakup **isi materi** dan bahasa selain Indonesia?
10. Apakah tema/stack MkDocs yang diinginkan sudah ditentukan (Material atau tema lain)?

---

## 11. Pembaruan Implementasi MkDocs (2026-10-13)

Kerangka MkDocs dibangun ulang (`mkdocs.yml`, `requirements.txt`, `materi/index.md`) dan tautan "Materi" ditambahkan ke header dashboard. Validasi yang benar-benar dijalankan: `mkdocs build` (strict) tanpa peringatan; build dua kali menghasilkan keluaran identik kecuali `sitemap.xml.gz`; `site/index.html` byte-identik dengan sumber; `git status` hanya menampilkan perubahan yang disengaja; pemeriksa tautan/aset relatif dan indeks pencarian lulus saat situs dilayani di `/` dan di subpath `/belajar-mail-server/`; halaman contoh (di luar proyek) merender admonition, tabel, blok kode berjudul, task list, canonical dari `SITE_URL`, dan ditemukan pencarian. **Belum diuji:** perilaku dashboard dan tombol salin kode di browser sungguhan (tidak ada browser otomatis), serta perbaikan F-01…F-11. Temuan D-01 (nama `index.html`) teratasi pada keluaran build (`site/index.html`).
