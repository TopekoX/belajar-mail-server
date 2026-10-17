# Technical Design Document: Mail Server Ubuntu Learning Portal

| | |
|---|---|
| **Versi** | 0.1 (draf, belum ada implementasi) |
| **Tanggal** | 2026-10-13 |
| **Dasar** | `docs/PRD.md` (PRD v0.2) dan `docs/project-audit.md` |
| **Status** | Menunggu persetujuan sebelum implementasi |
| **Aturan dokumen** | Tidak ada kode, konfigurasi, atau berkas build yang dibuat berdasarkan dokumen ini sebelum dokumen disetujui dan keselarasannya dengan PRD terkonfirmasi (bagian 2) |

Kata kunci **MUST/SHOULD/MAY** dipakai seperti di PRD. Rujukan memakai ID PRD (`FR-`, `NFR-`, `INT-`, `URL-`, `PRG-`, `JS-`, `DEP-`, `SEC-`, `MNT-`, `AC-`, `Q-`, `A-`). Hal yang belum terverifikasi ditandai **[Verifikasi T-nn]** dan menjadi tugas spike di bagian 14.

---

## 1. Tujuan dan Batasan Desain

### 1.1 Tujuan

Merancang cara menerbitkan **satu website statis** yang berisi:

- **Dashboard** kurikulum di `/index.html`, bersumber dari `kurikulum-mail-server-ubuntu.html`.
- **Dokumentasi materi** di `/materi/`, bersumber dari Markdown di `materi/` dan dirender oleh MkDocs.

### 1.2 Batasan wajib (dari pemilik produk)

| ID | Batasan |
|---|---|
| C-01 | `kurikulum-mail-server-ubuntu.html` tetap menjadi sumber dashboard utama. |
| C-02 | Dashboard diterbitkan sebagai `/index.html`. |
| C-03 | Sumber materi tetap Markdown di `materi/`. |
| C-04 | MkDocs membangun dokumentasi ke `site/materi/`. |
| C-05 | Dashboard dan dokumentasi dipublikasikan sebagai satu website. |
| C-06 | Deployment awal: GitHub Pages. |
| C-07 | Arsitektur harus dapat diadaptasi ke Vercel. |
| C-08 | Tautan bab mengacu pada ID bab dan hanya ke URL yang benar-benar tersedia. |
| C-09 | **Build tidak boleh mengubah berkas sumber.** |
| C-10 | Hasil build dapat dibuat ulang secara konsisten (deterministik). |

### 1.3 Di luar cakupan dokumen ini

Isi materi per chapter, desain visual dashboard, dan keputusan produk yang masih terbuka di PRD bagian 12.3 (dirujuk di bagian 14).

---

## 2. Keselarasan dengan PRD

Rancangan ini memenuhi PRD pada hampir semua persyaratan. Enam persyaratan PRD diamandemen karena batasan C-01, C-09, dan C-10 menutup jalur yang diasumsikan PRD v0.1. **Amandemen A1-A6 sudah diterapkan ke PRD v0.2** (2026-10-13); tabel berikut mencatat alasannya.

### 2.1 Amandemen PRD (diterapkan pada PRD v0.2)

| ID | PRD v0.1 | Konflik | Rancangan di dokumen ini | Amandemen yang diterapkan |
|---|---|---|---|---|
| A1 | FR-050, FR-051, INT-05, M2: `data/curriculum.json` adalah satu-satunya sumber; dashboard diturunkan darinya | C-01: sumber dashboard tetap berkas HTML yang saat ini memuat datanya sendiri (blok `/*DATA-START*/…/*DATA-END*/`) | **Blok data di HTML tetap menjadi sumber tunggal.** Build mengekstraknya (hanya baca) menjadi `.build/curriculum.json` berobjek bernama, divalidasi JSON Schema. Berkas itu artefak turunan, bukan sumber | Ubah FR-050 menjadi "satu sumber = blok data pada berkas dashboard; artefak `curriculum.json` diturunkan saat build". FR-051 berlaku untuk artefak |
| A2 | M3, PRG-03, INT-03: kode progres di satu modul bersama; HTML dipecah menjadi `index.html`, JS, CSS | C-01 dan keharusan menyalin HTML apa adanya (bagian 8.2 langkah 8) | Dashboard tetap satu berkas. Halaman materi memakai `materi/assets/progress.js` dengan **kontrak yang sama**; kesamaan perilaku dijaga uji kontrak (bagian 11.4), bukan berbagi kode | Turunkan PRG-03/INT-03 dari MUST menjadi SHOULD; tambah persyaratan uji kontrak; ubah M3 menjadi "kontrak progres dan skrip materi" |
| A3 | INT-07: dashboard memuat data kurikulum lewat `fetch` dengan cadangan tertanam | Dashboard sudah memuat data tertanam; `fetch` data tidak diperlukan | Data tetap tertanam. Yang di-`fetch` hanya `materi/chapters.json` (daftar bab terbit, bagian 6.3), opsional dan gagal-aman | Ganti INT-07 dengan persyaratan `chapters.json`; Q-02 (`file://`) tidak lagi memengaruhi pemuatan data |
| A4 | FR-052/FR-053: generator membuat stub dan memperbarui `nav` di `mkdocs.yml` | C-09: build tidak boleh menulis ke sumber | Stub dibuat oleh perintah terpisah `scaffold` yang dijalankan manual dan tidak bagian dari build. `nav` dihasilkan ke `.build/mkdocs.generated.yml`, bukan ke `mkdocs.yml` | Pisahkan FR-052 (perintah scaffold) dari FR-053 (nav saat build, keluaran di luar sumber) |
| A5 | URL-09: nama berkas masuk dashboard di akar situs `index.html` | Tidak ada konflik. Hanya klarifikasi | Berkas sumber tetap bernama `kurikulum-mail-server-ubuntu.html`; **keluaran** `site/index.html` adalah salinan byte-identik | Klarifikasi redaksi URL-09 |
| A6 | JS-06: skrip inline hanya jika tidak ada alternatif; dapat dipindah ke berkas terpisah | C-01/A2: dashboard tetap berskrip dan bergaya inline | CSP ketat diterapkan dengan **hash** skrip inline yang dihitung saat build (bagian 10.3), bukan memindahkan skrip | Ubah JS-06 agar mengizinkan CSP berbasis hash |

### 2.2 Persyaratan PRD yang dipenuhi tanpa perubahan

| Kelompok | Bagian TDD |
|---|---|
| Tata letak situs, URL materi, base path (PRD 7.1, URL-01…URL-10) | 5, 6, 7 |
| Alur CI/CD dan deployment (DEP-01…DEP-08) | 8, 9 |
| Build dapat direproduksi, versi dikunci (NFR-012, NFR-013) | 4.4, 8.3 |
| Kompatibilitas progres v1 (PRG-01, PRG-02, AC-35) | 11 |
| Validasi data dan materi (FR-060…FR-062, AC-20…AC-24) | 4.3, 12 |
| Keamanan (SEC-01…SEC-07) | 10 |
| Pemeliharaan dan pemulihan (MNT-01…MNT-07, DEP-05, DEP-07) | 13 |

### 2.3 Perubahan pada sumber dashboard (bukan oleh build)

Beberapa persyaratan PRD memerlukan penyuntingan `kurikulum-mail-server-ubuntu.html` oleh pengembang pada fase implementasi. Itu perubahan kode biasa yang melalui PR; **build tidak pernah menyentuh berkas itu** (C-09).

| Persyaratan | Perubahan pada dashboard |
|---|---|
| FR-054, FR-055 | Muat `materi/chapters.json`; tampilkan tautan "Buka materi" hanya untuk bab di dalamnya; kegagalan memuat diabaikan |
| FR-033 | Tambah favicon (tautan relatif), metadata Open Graph |
| NFR-011/PRG-06 | Peringatan bila `localStorage` tidak dapat ditulis |
| FR-011 (opsional, Q-10) | Tidak diperlukan pada v1.0 |

Semua perubahan harus mempertahankan penanda `/*DATA-START*/` dan `/*DATA-END*/` serta rute hash yang ada (kontrak, bagian 6.5).

---

## 3. Gambaran Arsitektur

```
 SUMBER (hanya dibaca oleh build)                     BUILD (tools/build.mjs)                       KELUARAN (site/)
┌───────────────────────────────────┐    ┌────────────────────────────────────────────┐   ┌─────────────────────────────┐
│ kurikulum-mail-server-ubuntu.html │──▶ │ 1 ekstrak + validasi data                  │   │ index.html   (salinan byte- │
│   (dashboard + blok data)         │    │   → .build/curriculum.json                 │   │               identik)      │
│ materi/**/*.md  (+ assets/)       │──▶ │ 2 validasi front matter + heading          │   │ .nojekyll  404.html         │
│ mkdocs.yml                        │──▶ │ 3 hasilkan .build/mkdocs.generated.yml     │   │ favicon …   (dari public/)  │
│ public/  (404, favicon …)         │──▶ │ 4 mkdocs build --strict  ─────────────────▶│──▶│ materi/  (hasil MkDocs)     │
│ tools/  tests/  .github/          │    │ 5 hasilkan materi/chapters.json (dari      │   │   chapter/CH-…/index.html   │
└───────────────────────────────────┘    │   berkas hasil build, bukan dari sumber)   │   │   chapters.json             │
                                         │ 6 rakit + verifikasi (hash, tautan, sumber)│   └─────────────────────────────┘
                                         └────────────────────────────────────────────┘
                                            artefak antara ditulis hanya ke .build/ dan site/
```

Prinsip:

1. **Satu arah:** sumber → build → keluaran. Build menulis hanya ke `.build/` dan `site/` (keduanya diabaikan git).
2. **Keluaran dapat diperiksa terhadap sumber:** `site/index.html` harus byte-identik dengan sumber (diuji).
3. **Tautan hanya ke yang ada:** daftar bab terbit dibuat dari berkas hasil build (bagian 6.3).
4. **Satu variabel konfigurasi host:** `SITE_URL` menentukan base path dan `site_url` MkDocs.

---

## 4. Struktur Folder, Konfigurasi, dan Alat

### 4.1 Struktur folder

```
belajar-mail-server/
├── kurikulum-mail-server-ubuntu.html     SUMBER dashboard (tidak diubah build)
├── materi/                               SUMBER dokumentasi (docs_dir MkDocs)
│   ├── index.md                          beranda dokumentasi
│   ├── chapter/
│   │   └── CH-NN-NN-NN.md                satu berkas per bab (nama = ID bab)
│   └── assets/
│       ├── progress.js                   skrip status belajar untuk halaman materi
│       └── extra.css
├── public/                               berkas yang disalin apa adanya ke akar site/
│   ├── favicon.svg
│   └── 404.template.html                 satu-satunya templat; diisi {{BASE}} saat build
├── tools/                                alat build (Node.js, ESM)
│   ├── build.mjs                         orkestrator
│   ├── scaffold.mjs                      perintah manual pembuat stub (BUKAN bagian build)
│   ├── lib/                              extract-curriculum, validate, nav, chapters-index, assemble, hashes, check-links
│   └── schema/                           curriculum.schema.json, frontmatter.schema.json
├── tests/
│   ├── unit/   integration/   e2e/   fixtures/
├── docs/                                 dokumen proyek (PRD, TDD, audit); TIDAK dipublikasikan
├── .github/workflows/                    ci.yml, deploy.yml, links.yml
├── mkdocs.yml                            konfigurasi dasar MkDocs (sumber, tidak diubah build)
├── requirements.txt                      dependensi Python berkunci hash
├── package.json, package-lock.json       dependensi Node berkunci
├── .nvmrc, .python-version               versi runtime
├── .gitattributes                        `* text=auto eol=lf`
├── .gitignore                            site/  .build/  node_modules/
└── vercel.json                           ditambahkan pada milestone Vercel (bagian 9)

--- dihasilkan, tidak dikomit ---
├── .build/                               curriculum.json, mkdocs.generated.yml, manifest.json, log, cadangan site/
└── site/                                 keluaran akhir
    ├── index.html  .nojekyll  404.html  favicon.svg
    └── materi/                           keluaran MkDocs + chapters.json
```

Catatan:

- `docs/` bukan `docs_dir` MkDocs. `docs_dir` adalah `materi/` (A-09 PRD).
- `.gitattributes` memastikan akhir baris LF di semua sistem. Tanpa itu, pengembang Windows dapat memicu perbedaan hash antara salinan lokal dan CI (build di Linux), sehingga uji byte-identik (bagian 12.2) gagal secara palsu.

### 4.2 Alat dan alasan

| Komponen | Pilihan | Alasan |
|---|---|---|
| Orkestrasi build | Node.js (ESM), tanpa bundler | Dashboard perlu diekstrak dengan JavaScript; uji e2e (Playwright) juga Node. Satu bahasa untuk semua alat selain MkDocs |
| Generator dokumentasi | MkDocs + tema Material (nama tema final menunggu **A-05 PRD**) | Ditetapkan PRD |
| Parsing front matter | paket `yaml` | Kecil, mengurai YAML standar |
| Validasi skema | `ajv` | JSON Schema sesuai FR-051 |
| Uji e2e | Playwright (chromium, firefox, webkit) | NFR-004, AC-01…AC-10 |
| Uji aksesibilitas/kinerja | axe, Lighthouse CI | AC-11, AC-12 |
| Server uji | server statis kecil di `tools/` yang dapat dipasang pada awalan path | Menguji `/` dan `/<repo>/` (URL-10) |

Dependensi dijaga minimal; tiap penambahan melalui PR dan lockfile (SEC-03).

### 4.3 Ekstraksi data dari dashboard (hanya baca)

Dashboard menyimpan data kurikulum dalam blok JavaScript yang dibatasi penanda. `extract-curriculum.mjs`:

1. Membaca berkas HTML sebagai teks (tanpa menulis).
2. Mengambil teks di antara `/*DATA-START*/` dan `/*DATA-END*/`; gagal jika salah satu penanda hilang atau muncul lebih dari sekali.
3. Mengevaluasi blok itu di **sandbox `node:vm`** (konteks kosong, tanpa `require`, tanpa jaringan, `timeout`), dengan membaca `CAT`, `MODS`, `CHS`, `CATS`, `CAPSTONE`, `SCHED`, `REFS`, `CONTENT`.
4. Menormalkan array posisional chapter menjadi **objek bernama** (R-10 audit) dan menulis `.build/curriculum.json` dengan kunci terurut.
5. Memvalidasi terhadap `curriculum.schema.json` dan aturan graf: ID unik, prasyarat merujuk modul yang ada, tidak ada siklus (AC-20).

Bentuk keluaran (ringkas):

```json
{
  "schema": 1,
  "release": "Ubuntu Server 24.04 LTS (Noble Numbat)",
  "categories": [{ "id": "CAT-01", "level": 0, "name": "...", "environment": "lab", "optional": false,
    "modules": [{ "id": "MOD-01-01", "title": "...", "after": [], "optional": false,
      "chapters": [{ "id": "CH-01-01-01", "title": "...", "minutes": 60,
                     "objectives": ["..."], "commands": "", "files": "", "prerequisites": [] }] }] }]
}
```

**Risiko dan mitigasi.** Mengevaluasi JavaScript dari repositori sendiri berisiko jika PR berbahaya masuk. Mitigasi: sandbox tanpa kemampuan I/O, tinjauan PR atas perubahan blok data, dan `ajv` pada keluaran. Alternatif tanpa eksekusi dibahas di bagian 4.5.

### 4.4 Konfigurasi

**`mkdocs.yml`** (sumber, dibaca; nilai bergaris bawah **[Verifikasi T-01]**):

```yaml
site_name: Kurikulum Mail Server Ubuntu: Materi
site_url: !ENV [MATERI_SITE_URL, null]      # null bila tidak diatur (lokal); CI/host mengisinya
docs_dir: materi
site_dir: site/materi                        # C-04
use_directory_urls: true                     # chapter/CH-…/ (INT-01, URL-04)
strict: true
theme:
  name: material                             # menunggu A-05
  language: id
  features: [navigation.sections, navigation.footer, search.suggest, content.code.copy]
  # navigation.instant sengaja tidak diaktifkan pada v1 (bagian 11.5)
extra_javascript: [assets/progress.js]
extra_css: [assets/extra.css]
plugins: [search]
validation:
  nav: { omitted_files: info }
  links: { not_found: warn, absolute_links: warn, unrecognized_links: warn }   # strict: peringatan = galat
markdown_extensions: [admonition, attr_list, pymdownx.highlight, pymdownx.superfences, tables, toc]
```

`nav` dan `exclude_docs` **tidak** ditulis di berkas ini. Keduanya dihasilkan (bagian 4.4.1).

#### 4.4.1 Konfigurasi hasil generasi

`.build/mkdocs.generated.yml`:

```yaml
INHERIT: ../mkdocs.yml
docs_dir: ../materi
site_dir: ../site/materi
nav:
  - Beranda: index.md
  - "L0 · Orientasi dan Persiapan Belajar":
      - "Orientasi Kurikulum":
          - "CH-01-01-01 · Peta Belajar dan Profil Pembelajar": chapter/CH-01-01-01.md
exclude_docs: |
  chapter/CH-01-01-02.md       # bab berstatus draft
```

Aturan generator:

- Hanya bab `status: published` masuk `nav`; kategori/modul tanpa bab terbit dihilangkan.
- Bab `draft` masuk `exclude_docs` (FR-044: tidak muncul di situs; dashboard menampilkan spesifikasinya).
- Urutan dan pengelompokan mengikuti urutan di `curriculum.json` (IA-02).
- Judul `nav` = `ID · judul` dari `curriculum.json`, bukan dari Markdown, agar urutan dan nama konsisten dengan dashboard.
- Keluaran deterministik: tanpa tanda waktu, kunci dan daftar terurut.

#### 4.4.2 Variabel lingkungan

| Variabel | Fungsi | Asal |
|---|---|---|
| `SITE_URL` | URL kanonis seluruh situs, mis. `https://pengguna.github.io/repo/`. Dinormalisasi agar diakhiri `/` | CI (`actions/configure-pages`), Vercel (bagian 9), atau kosong untuk lokal |
| `MATERI_SITE_URL` | Diturunkan oleh `build.mjs`: `SITE_URL` + `materi/`. Dibaca `mkdocs.yml` | `build.mjs` |
| `SITE_BASE` | Diturunkan: path dari `SITE_URL` (`/repo/` atau `/`) | `build.mjs` |
| `TZ=UTC`, `LC_ALL=C.UTF-8`, `PYTHONHASHSEED=0` | Menetapkan lingkungan deterministik | `build.mjs` |

### 4.5 Alternatif ekstraksi data

| Opsi | Cara | Kelebihan | Kekurangan |
|---|---|---|---|
| **E1. Evaluasi blok data di `node:vm` (dipilih)** | Jalankan blok `DATA-START…DATA-END` di sandbox | Akurat: memakai logika penurunan yang sama dengan dashboard (ID, prasyarat); tanpa dependensi parser | Mengeksekusi kode repositori (dimitigasi sandbox dan tinjauan PR) |
| E2. Parser JavaScript (mis. `acorn`) + evaluator literal | Urai AST, evaluasi hanya literal `CATS`, `CAPSTONE`, `SCHED`, `REFS` | Tanpa eksekusi kode | Logika penurunan ID/prasyarat harus ditulis ulang → dua implementasi bisa menyimpang; tambah dependensi |
| E3. Pindahkan data ke `curriculum.json` (rancangan awal PRD) | JSON menjadi sumber; HTML memuatnya | Format netral, mudah divalidasi | Mengubah sumber dashboard secara struktural; bertentangan dengan arah C-01 untuk v1; menunda hasil |

**Keputusan: E1.** Alasan: memenuhi C-01 dan C-09 dengan perubahan nol pada dashboard, dan paling kecil risiko ketidakselarasan data. E3 tetap jalur evolusi bila kelak data dipisahkan (tidak menutup pintu: skema artefak sama).

---

## 5. Alternatif Arsitektur Perakitan Situs

| Opsi | Uraian | Kelebihan | Kekurangan |
|---|---|---|---|
| **P1. Dua keluaran dirakit oleh skrip (dipilih)** | MkDocs menulis ke `site/materi/`; skrip menyalin dashboard ke `site/index.html` dan berkas publik | Memenuhi C-02 dan C-04 persis; dashboard byte-identik; MkDocs terisolasi pada subpath; mudah dipindah ke Vercel | Perlu skrip perakit (kecil) |
| P2. Dashboard sebagai berkas statis di dalam `docs_dir` MkDocs | Taruh HTML di `materi/` | Satu perintah build | Dashboard berada di `/materi/…`, melanggar C-02; MkDocs mengelola berkas non-Markdown tanpa jaminan nama/jalur akar |
| P3. MkDocs membangun seluruh situs dari satu `docs_dir` berisi dashboard dan materi | Dashboard di akar `docs_dir`, materi di subfolder | Satu build | MkDocs menulis ke `site/` secara keseluruhan, bukan `site/materi/` (C-04); tema memengaruhi struktur akar; sulit menjaga `index.html` byte-identik |
| P4. Dua situs terpisah (dua deploy) | Dashboard dan materi pada URL berbeda | Sederhana per bagian | Melanggar C-05; progres lintas-origin tidak bisa dibagi (G4 PRD) |

**Keputusan: P1.** Alasan: hanya P1 memenuhi C-02, C-04, dan C-05 sekaligus sambil menjaga dashboard sebagai salinan byte-identik (verifiable) dan tidak bergantung pada perilaku internal MkDocs untuk berkas akar.

### 5.1 Alternatif pembuatan `nav`

| Opsi | Kelebihan | Kekurangan |
|---|---|---|
| N1. Tulis `nav` manual di `mkdocs.yml` | Paling sederhana | Dua sumber kebenaran (R-04 audit) |
| N2. Plugin berbasis struktur direktori (`awesome-pages`, `literate-nav`) | Tanpa skrip | Struktur direktori datar per ID; kategori/modul tidak tercermin di path; tambah dependensi plugin |
| **N3. Konfigurasi hasil generasi di `.build/` dengan `INHERIT` (dipilih)** | Nav dari data; tidak mengubah `mkdocs.yml` (C-09); deterministik | Bergantung pada perilaku `INHERIT` dan resolusi path **[Verifikasi T-01]** |
| N4. Generator menulis `nav` ke `mkdocs.yml` | Konfigurasi tunggal | Build mengubah sumber (C-09) |

**Keputusan: N3.**

---

## 6. Pemetaan URL

### 6.1 Peta URL situs

Misalkan `BASE` = `/` (domain akar) atau `/<repo>/` (GitHub Pages proyek). Semua jalur relatif terhadap `BASE`.

| Sumber / keluaran | URL | Catatan |
|---|---|---|
| `kurikulum-mail-server-ubuntu.html` → `site/index.html` | `BASE` dan `BASE index.html` | Dashboard; rute di hash |
| Beranda dashboard | `BASE#/` | |
| Panduan dashboard | `BASE#/tentang` | |
| Kategori | `BASE#CAT-NN` | |
| Bab (spesifikasi di dashboard) | `BASE#CH-NN-NN-NN` | Selalu ada untuk 136 bab |
| `materi/index.md` | `BASE materi/` | Beranda dokumentasi |
| `materi/chapter/CH-NN-NN-NN.md` | `BASE materi/chapter/CH-NN-NN-NN/` | Hanya bab `published`; `use_directory_urls: true` |
| Daftar bab terbit | `BASE materi/chapters.json` | Dibuat saat build (6.3) |
| Pencarian MkDocs | `BASE materi/search/search_index.json` | Dari MkDocs |
| `public/404.template.html` | `BASE 404.html` | Hanya dipakai GitHub Pages di akar situs |
| `.nojekyll` | `BASE .nojekyll` | URL-08 |

### 6.2 Aturan pemetaan ID ke URL

| Invarian | Aturan | Diuji oleh |
|---|---|---|
| I-1 | Nama berkas materi = ID bab = `id` di front matter (`CH-NN-NN-NN`) | validator front matter |
| I-2 | URL bab = `materi/chapter/<ID>/` dan tidak memuat slug judul (URL-05) | uji pola `^CH-\d{2}-\d{2}-\d{2}/$` |
| I-3 | ID di front matter ada di `curriculum.json` | validator |
| I-4 | ID yang pernah terbit tidak dihapus/dipakai ulang (URL-04) | uji terhadap `tools/published-ids.json` yang dikomit |
| I-5 | Dashboard hanya menaut ke bab yang tercantum di `chapters.json` | e2e + uji tautan |
| I-6 | Setiap entri `chapters.json` memiliki berkas hasil build di `site/materi/chapter/<ID>/index.html` | langkah 5 build + uji tautan |
| I-7 | Setiap bab `published` di sumber muncul di `chapters.json` | uji integrasi |

`tools/published-ids.json` (dikomit; diperbarui oleh PR, bukan oleh build) mencatat ID yang pernah terbit; bab dihapus harus diberi pengalihan atau halaman penjelasan (URL-04).

### 6.3 `materi/chapters.json`: sumber tunggal tautan bab

Dibuat pada langkah 5 build **dengan memindai berkas hasil build**, bukan dari sumber, sehingga hanya memuat bab yang URL-nya benar-benar tersedia (C-08):

```json
{
  "schema": 1,
  "chapters": {
    "CH-01-01-01": { "path": "chapter/CH-01-01-01/", "title": "Peta Belajar dan Profil Pembelajar" }
  }
}
```

- Ekstensi implementasi saat ini (skema tetap 1, aditif): kunci `levels` memetakan `CAT-NN` ke `{path: "level/L<n>/", title}` untuk halaman ringkasan level (`materi/level/L<n>.md`). Dashboard memakainya untuk tombol "Buka materi level" pada tampilan kategori.
- `path` relatif terhadap `BASE materi/`. Tidak ada URL absolut, sehingga sama di semua host.
- Kunci terurut; tanpa tanda waktu atau hash komit (deterministik).
- Jika `materi/chapters.json` tidak dapat dimuat, dashboard tidak menampilkan tautan materi dan seluruh fitur lain berjalan (FR-055).

### 6.4 Tautan antarhalaman

| Dari | Ke | Mekanisme |
|---|---|---|
| Dashboard | Materi bab | `new URL("materi/" + path, document.baseURI)` dari `chapters.json` |
| Materi bab | Dashboard bab | `progress.js` membentuk tautan dari `location`: tiga tingkat ke atas dari `…/materi/chapter/<ID>/`, lalu `#<ID>` (kedalaman tetap karena I-2) |
| Materi bab | Bab lain | Tautan Markdown relatif ke berkas (`CH-NN-NN-NN.md`), diperiksa `mkdocs --strict`; dilarang tautan absolut atau tulisan URL manual (INT-01) |
| Materi | Dashboard umum | `../../../` (+ hash) lewat `progress.js`; halaman 404 memakai `{{BASE}}` |

### 6.5 Kontrak dashboard yang tidak boleh berubah tanpa memperbarui build

| Kontrak | Dipakai oleh |
|---|---|
| Penanda `/*DATA-START*/` dan `/*DATA-END*/` tepat satu pasang | ekstraktor |
| Nama simpanan: `CATS`, `CAPSTONE`, `SCHED`, `REFS`, `CAT`, `MODS`, `CHS`, `CONTENT` | ekstraktor |
| Rute hash `#/`, `#/tentang`, `#CAT-NN`, `#CH-NN-NN-NN` | tautan materi → dashboard; uji e2e |
| Kunci `localStorage` `kurikulum-mail-ubuntu-v1`, `kmu-theme`, skema v1 | `progress.js`; uji kontrak |
| Tidak ada URL absolut ke aset | uji URL-01 |

Perubahan kontrak ini memerlukan pembaruan alat/uji pada PR yang sama; uji yang gagal menjadi pengaman.

---

## 7. Strategi Base Path

### 7.1 Prinsip

1. **Semua jalur relatif.** Dashboard tidak memuat aset eksternal. Satu-satunya `fetch` memakai jalur relatif `materi/chapters.json` (URL-01).
2. **Nilai absolut hanya untuk hal yang memang wajib absolut:** `canonical`, sitemap, dan Open Graph, semuanya dari `SITE_URL`.
3. **Satu variabel (`SITE_URL`) menentukan semuanya**; nilainya tidak ditulis ke berkas yang dikomit (URL-02).

### 7.2 Perlakuan per komponen

| Komponen | Strategi |
|---|---|
| Dashboard | Rute hash tidak bergantung path. `fetch("materi/chapters.json")` relatif ke dokumen. Aman di `/` dan `/repo/` |
| MkDocs | Tautan dan aset relatif secara bawaan. `site_url` hanya untuk `canonical` dan `sitemap.xml` |
| `progress.js` | Menghitung tautan balik dari kedalaman tetap `location` (6.4) |
| `404.html` | Satu-satunya berkas yang disajikan pada path sembarang, jadi jalur relatif tidak aman. Dirender dari templat dengan `{{BASE}}` dari `SITE_BASE` |
| `.nojekyll` | Berkas kosong di akar `site/` |
| Pratinjau lokal | `SITE_URL` kosong → `BASE` = `/`; server uji juga dapat memasang situs pada awalan `/repo/` |

### 7.3 Turunan `SITE_BASE`

`SITE_BASE` = bagian path dari `SITE_URL` dengan `/` di awal dan akhir. Contoh: `https://x.github.io/repo/` → `/repo/`; `https://belajar.contoh/` → `/`; kosong → `/`.

### 7.4 Pengujian dua konfigurasi (URL-10, AC-30)

Build dijalankan sekali menghasilkan `site/`, lalu pemeriksa tautan dan e2e dijalankan terhadap dua pemasangan: `http://localhost:PORT/` dan `http://localhost:PORT/repo/`. Karena semua tautan relatif, keluaran identik pada keduanya; hanya `canonical`/`404` yang bergantung `SITE_URL`, sehingga CI juga membangun varian kedua dengan `SITE_URL` berbeda untuk memeriksa kedua nilai tersebut (AC-32).

---

## 8. Alur Build

### 8.1 Perintah

| Perintah | Fungsi | Menulis ke sumber? |
|---|---|---|
| `node tools/build.mjs` | Build penuh (langkah 8.2) | **Tidak** (hanya `.build/`, `site/`) |
| `node tools/build.mjs --check` | Validasi tanpa membangun situs (langkah 1–3) | Tidak |
| `node tools/scaffold.mjs CH-NN-NN-NN` | Membuat stub Markdown dari templat 14 bagian bila belum ada | **Ya**, manual dan disengaja (A4) |
| `node tools/verify.mjs` | Verifikasi pasca-build (langkah 8.2 #9–11) | Tidak |

`scaffold` sengaja bukan bagian `build` agar C-09 tidak pernah dilanggar oleh proses otomatis. Ia menolak menimpa berkas yang ada.

### 8.2 Langkah

| # | Langkah | Masukan | Keluaran | Gagal bila |
|---|---|---|---|---|
| 0 | Persiapan | versi Node/Python, variabel lingkungan | lingkungan deterministik | versi tidak sesuai `.nvmrc`/`.python-version` |
| 1 | Cuplikan sumber | pohon sumber | `.build/source-manifest.json` (SHA-256 semua berkas sumber) | — |
| 2 | Ekstrak + validasi data | HTML dashboard | `.build/curriculum.json` | penanda hilang, skema tak valid, ID ganda, prasyarat rusak (AC-20) |
| 3 | Validasi materi | `materi/**/*.md` | daftar bab dan status | front matter tidak lengkap, `id` ≠ nama berkas, 14 heading tidak ada atau tak berurutan, `published` tanpa `verified_on`, pola rahasia (AC-22…24), ID tak ada di kurikulum |
| 4 | Hasilkan konfigurasi MkDocs | langkah 2–3 | `.build/mkdocs.generated.yml` | — |
| 5 | Persiapkan `site/` | — | `site/` lama dipindah ke `.build/site.prev/`; `site/` dibuat kosong | — |
| 6 | Bangun dokumentasi | konfigurasi 4 | `site/materi/**` | `mkdocs build --strict` ≠ 0 |
| 7 | Hasilkan daftar bab terbit | `site/materi/chapter/*/index.html` | `site/materi/chapters.json` | bab `published` tanpa halaman hasil build (I-6, I-7) |
| 8 | Rakit akar | HTML sumber, `public/` | `site/index.html` (salin biner), `.nojekyll`, `404.html` (isi `{{BASE}}`), `favicon.svg` | — |
| 9 | Verifikasi integritas | `site/`, sumber | — | `sha256(site/index.html)` ≠ sumber; manifes sumber berubah (C-09) |
| 10 | Pemeriksa tautan | `site/` | laporan | ada tautan internal atau aset yang tidak ada; tautan `chapters.json` tidak tersedia |
| 11 | Tulis manifes keluaran | `site/` | `.build/output-manifest.json` (SHA-256 terurut) | — |
| 12 | Selesai | — | hapus `.build/site.prev/`; kode 0 | — |

Kegagalan pada langkah 6–11 memicu **pemulihan lokal** (bagian 13.1): `site/` yang gagal dipindah ke `.build/site.failed/` dan `site.prev` dikembalikan.

### 8.3 Determinisme (C-10)

| Sumber ketidakpastian | Kendali |
|---|---|
| Versi alat | `.nvmrc`, `.python-version`, `package-lock.json`, `requirements.txt` dengan hash (`pip install --require-hashes`); versi MkDocs, tema, dan plugin dikunci tepat (NFR-012) |
| Tanda waktu | Tidak ada tanda waktu di keluaran buatan sendiri; plugin berbasis waktu atau git (mis. `git-revision-date`) **dilarang** |
| Urutan | Semua daftar/kunci terurut; sistem berkas dibaca dalam urutan leksikografis |
| Akhir baris dan pengodean | `.gitattributes` `eol=lf`; UTF-8 tanpa BOM |
| Lingkungan | `TZ=UTC`, `LC_ALL=C.UTF-8`, `PYTHONHASHSEED=0` |
| Berkas terkompresi | `sitemap.xml.gz` dari MkDocs memuat waktu pada header gzip; **dikecualikan** dari perbandingan hash dan tidak dipublikasikan bila tidak dibutuhkan **[Verifikasi T-04]** |
| Jaringan | Build tidak mengunduh apa pun saat berjalan (dependensi dipasang sebelum build); font tema dilayani lokal atau tema dikonfigurasi tanpa font eksternal **[Verifikasi T-05]** |
| Konten bergantung URL | `SITE_URL` identik antar dua build yang dibandingkan |

Uji: build dua kali dalam direktori bersih dengan masukan sama, lalu bandingkan `output-manifest.json` (AC-41, usulan; bagian 12.2).

### 8.4 Jaminan "build tidak mengubah sumber" (C-09)

Berlapis:

1. **Desain:** tidak ada langkah yang membuka berkas sumber untuk ditulis; semua keluaran ke `.build/` dan `site/`.
2. **Runtime:** langkah 9 membandingkan manifes SHA-256 sumber (langkah 1) dengan keadaan sesudah build; selisih = build gagal.
3. **CI:** setelah build, `git status --porcelain` harus kosong dan `git diff --exit-code` lulus; jika tidak, pipeline gagal.
4. **Opsional:** CI dapat menjalankan build dengan pohon sumber dipasang sebagai baca-saja.
5. **Uji:** satu uji integrasi menjalankan build pada fixture dan memastikan tidak ada berkas sumber yang berubah (hash, mtime, daftar berkas).

---

## 9. Alur Deployment

### 9.1 GitHub Pages (deployment awal, C-06)

Dua alur kerja GitHub Actions (versi action disematkan pada SHA saat implementasi; SEC-04):

**`ci.yml`:** dijalankan pada pull request ke `main`.

```yaml
name: ci
on: { pull_request: { branches: [main] } }
permissions: { contents: read }
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: actions/setup-node@<sha>        # node-version-file: .nvmrc, cache: npm
      - uses: actions/setup-python@<sha>      # python-version-file: .python-version
      - run: npm ci
      - run: pip install --require-hashes -r requirements.txt
      - run: node tools/build.mjs --check
      - run: SITE_URL=https://example.invalid/repo/ node tools/build.mjs
      - run: node tools/verify.mjs
      - run: npm test                          # unit, integrasi, kontrak, e2e, axe
      - run: git diff --exit-code && test -z "$(git status --porcelain)"
      - uses: actions/upload-artifact@<sha>    # site/ untuk pratinjau PR (DEP-08)
```

**`deploy.yml`:** dijalankan pada push ke `main` dan `workflow_dispatch`.

```yaml
name: deploy
on: { push: { branches: [main] }, workflow_dispatch: {} }
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: false }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: actions/configure-pages@<sha>
        id: pages
      - uses: actions/setup-node@<sha>
      - uses: actions/setup-python@<sha>
      - run: npm ci
      - run: pip install --require-hashes -r requirements.txt
      - run: SITE_URL="${{ steps.pages.outputs.base_url }}/" node tools/build.mjs
      - run: node tools/verify.mjs && npm test
      - run: git diff --exit-code && test -z "$(git status --porcelain)"
      - uses: actions/upload-pages-artifact@<sha>
        with: { path: site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: "${{ steps.d.outputs.page_url }}" }
    steps:
      - id: d
        uses: actions/deploy-pages@<sha>
  smoke:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - run: node tools/smoke.mjs "${{ needs.deploy.outputs.page_url }}"
```

Ketentuan:

- Sumber Pages dikonfigurasi "GitHub Actions" (DEP-02). Cabang `main` dilindungi; PR dan CI hijau wajib (DEP-01, DEP-04).
- Deploy hanya berjalan bila `build` hijau; artefak yang diunggah adalah `site/` penuh. Situs lama tetap utuh selama build/deploy gagal (DEP-05).
- `base_url` dari `configure-pages` dinormalisasi `build.mjs` (akhiran `/`). Belum ada domain kustom (Q-12).
- `smoke.mjs` memeriksa `BASE`, `BASE materi/`, satu bab terbit, `chapters.json`, dan `404.html`; kegagalan menandai alur kerja merah (pemulihan: 13.2).
- Alur kerja ketiga `links.yml` (jadwal bulanan) memeriksa tautan eksternal (MNT-03).

### 9.2 Adaptasi ke Vercel (C-07)

Karena keluaran adalah direktori statis berisi jalur relatif, adaptasi hanya konfigurasi:

```json
{
  "buildCommand": "node tools/build.mjs",
  "outputDirectory": "site",
  "installCommand": "npm ci && pip install --require-hashes -r requirements.txt",
  "trailingSlash": true,
  "headers": [ { "source": "/(.*)", "headers": [
    { "key": "X-Content-Type-Options", "value": "nosniff" },
    { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" } ] } ]
}
```

| Aspek | Penanganan |
|---|---|
| `SITE_URL` | `build.mjs` memakai `SITE_URL` bila ada; bila tidak, mengambil dari `VERCEL_PROJECT_PRODUCTION_URL` (produksi) atau `VERCEL_URL` (pratinjau) **[Verifikasi T-06]** |
| `trailingSlash: true` | Menyamakan perilaku dengan GitHub Pages (`/chapter/CH-…/`) |
| `cleanUrls` | **Tidak dipakai**: tidak diperlukan dan dapat mengubah tautan `.html` |
| Runtime di Vercel | Citra build harus menyediakan Node dan Python. Bila tidak, gunakan jalur cadangan: bangun di GitHub Actions lalu `vercel deploy --prebuilt` atau unggah `site/` **[Verifikasi T-07]** |
| Header keamanan | `X-Content-Type-Options`, `Referrer-Policy`; CSP ditambahkan dengan hash (10.3) |
| 404 | Vercel melayani `404.html` di akar; sudah dibuat build |
| Preview per PR | Bawaan Vercel (DEP-08) |
| Perubahan konten/URL | Tidak ada (NFR-014, AC-38) |

### 9.3 Perbandingan alternatif deployment GitHub Pages

| Opsi | Uraian | Kelebihan | Kekurangan |
|---|---|---|---|
| **G1. Actions + artefak Pages (dipilih)** | `upload-pages-artifact` + `deploy-pages` | Tanpa cabang `gh-pages`; atomik; izin minimal; sesuai DEP-02 | Perlu konfigurasi Pages sekali |
| G2. Dorong `site/` ke cabang `gh-pages` | Cabang berisi keluaran | Mudah diperiksa | Mengotori riwayat dengan artefak build; butuh token tulis; bertentangan NFR-013 (keluaran jangan dikomit) |
| G3. "Deploy from branch" tanpa build | Jekyll/statis dari repo | Paling sederhana | Tidak menjalankan MkDocs; tidak sesuai arsitektur |

**Keputusan: G1.**

---

## 10. Keamanan

### 10.1 Rantai pasok dan CI

- Dependensi Node dan Python dikunci, dipasang dari lockfile/hash, dipantau Dependabot (SEC-03).
- Action disematkan SHA; `permissions:` eksplisit minimum per job (SEC-04). Job `build` tidak memiliki `pages: write`.
- Tidak ada rahasia dipakai oleh build; PR dari fork tidak menerima token tulis.
- Pemindaian pola kunci/token pada materi di langkah 3 (FR-062, AC-24); pemindai rahasia GitHub diaktifkan (SEC-01).

### 10.2 Sandbox ekstraktor

Lihat 4.3. Tidak ada `require`, `process`, `fetch`, atau akses sistem berkas di konteks `vm`; batas waktu eksekusi ketat; hasil divalidasi skema.

### 10.3 CSP (JS-06, A6)

GitHub Pages tidak dapat mengatur header. Di Vercel, `tools/lib/csp.mjs` menghitung hash SHA-256 setiap blok `<script>` inline pada `site/index.html` dan menuliskan `script-src 'self' 'sha256-…'` ke `site/_headers.json` untuk dikonsumsi `vercel.json` pada langkah build. Gaya inline dan atribut `style` yang dibuat skrip memerlukan `style-src 'self' 'unsafe-inline'`. Halaman MkDocs/Material memiliki inline script sendiri yang akan dianalisis pada spike **[Verifikasi T-08]**. Karena `index.html` byte-identik dengan sumber, hash stabil kecuali sumber berubah.

### 10.4 Permukaan serangan

| Risiko | Kontrol |
|---|---|
| Skrip pihak ketiga | Tidak ada (AC-39) |
| XSS dari `CONTENT` mentah | Tidak dipakai di v1 (materi di Markdown); komentar peringatan di dashboard (JS-07) |
| `progress.js` membaca/menulis `localStorage` | Memakai `sanitize` yang setara dengan dashboard (kontrak), tidak memasukkan data ke DOM tanpa escape |
| Impor progres berbahaya | Sanitasi di dashboard (NFR-010) |

---

## 11. Integrasi Progres

### 11.1 Kontrak data (PRG-01, PRG-02)

Kunci `kurikulum-mail-ubuntu-v1`, skema v1 (`{v:1, status:{ID:1..4}, checks:{ID:{p0:true,…}}}`), kunci tema `kmu-theme`. Ekspor `{app:"kurikulum-mail-server-ubuntu", version:1, …}`. Kontrak ini didokumentasikan di `tests/contract/progress-contract.md` dan diwujudkan sebagai fixture.

### 11.2 Perilaku `progress.js` (halaman materi)

1. Membaca `ID` dari `<meta name="chapter-id">`/front matter yang dipancarkan Markdown (atau dari URL), menolak ID di luar pola.
2. Memuat state dengan `sanitize` yang setara dashboard; ID tak dikenal diabaikan dan **dipertahankan** saat menulis ulang (menghindari penghapusan data bila dashboard dan materi punya versi berbeda; **[Pertanyaan Q-07]**).
3. Menampilkan pemilih status dan checklist kelulusan bab; menyimpan hanya perubahan lokal, dengan membaca ulang penyimpanan tepat sebelum menulis (tanpa menimpa tab lain).
4. Mendengarkan event `storage` untuk sinkronisasi.
5. Bila `localStorage` tidak dapat ditulis, menampilkan pesan dan tidak melempar galat.

### 11.3 Alternatif berbagi kode progres

| Opsi | Kelebihan | Kekurangan |
|---|---|---|
| **S1. Dua implementasi + uji kontrak (dipilih v1)** | Dashboard tidak diubah (C-01); jalur kerja sederhana | Duplikasi ±60 baris; risiko menyimpang bila uji lemah |
| S2. Ekstrak modul bersama dan sisipkan ke HTML saat build | Satu kode | Build mengubah isi HTML keluaran (tidak byte-identik); kompleksitas penyisipan |
| S3. Dashboard memuat `progress.js` dari berkas | Satu kode | Mengubah dashboard menjadi dua berkas; di luar C-01 untuk v1 |

**Keputusan: S1** untuk v1, S3 sebagai evolusi bila duplikasi membebani (butuh amandemen A2).

### 11.4 Uji kontrak

Dijalankan terhadap kedua implementasi dengan fixture yang sama: muat state v1 → ubah status → simpan → hasil identik byte-demi-byte (setelah normalisasi JSON); impor berkas ekspor v1 diterima; ID tak dikenal diabaikan/dipertahankan sesuai keputusan Q-07.

### 11.5 Navigasi instan

`navigation.instant` dinonaktifkan pada v1 agar `progress.js` berjalan pada setiap pemuatan halaman tanpa bergantung pada API internal tema (JS-04). Bila diaktifkan kelak, `progress.js` akan berlangganan `document$` bila ada.

---

## 12. Strategi Pengujian

### 12.1 Piramida

| Lapisan | Cakupan | Alat | Dijalankan |
|---|---|---|---|
| Unit | ekstraktor, validator, generator nav, pembuat `chapters.json`, normalisasi `SITE_URL`, pembuat `404` | runner Node bawaan | tiap PR |
| Integrasi build | build penuh pada **fixture** (kurikulum kecil: 2 kategori, 3 bab, 1 terbit, 1 draft, 1 tak ada) dan pada repositori nyata | Node + MkDocs | tiap PR |
| Kontrak | data v1, skema ekspor, rute hash, penanda blok data | fixture + uji | tiap PR |
| Pasca-build | byte-identik, manifes sumber, tautan, struktur URL | `verify.mjs` | tiap build |
| E2E | dashboard dan materi pada chromium/firefox/webkit | Playwright | tiap PR |
| Aksesibilitas/kinerja | axe, Lighthouse CI | | tiap PR (axe), terjadwal/rilis (Lighthouse) |
| Smoke produksi | URL terbit | `smoke.mjs` | setelah deploy |
| Tautan eksternal | dokumentasi resmi | `links.yml` | bulanan |

### 12.2 Uji kunci dan pemetaan ke PRD

| ID uji | Uji | Mencakup |
|---|---|---|
| T-INT-01 | `site/index.html` byte-identik dengan sumber | C-02, C-09 |
| T-INT-02 | Manifes sumber sebelum dan sesudah build identik; `git status` bersih | C-09 |
| T-INT-03 | Dua build berurutan menghasilkan `output-manifest.json` identik (kecuali berkas yang dikecualikan T-04) | C-10 |
| T-INT-04 | Setiap entri `chapters.json` memiliki berkas hasil build; setiap bab `published` ada di `chapters.json` | C-08, I-6, I-7 |
| T-INT-05 | Bab `draft` tidak ada di `site/materi/chapter/` dan tidak ada di `chapters.json` | FR-044, FR-054 |
| T-INT-06 | Build gagal bila: ID ganda, prasyarat rusak, front matter kurang, heading kurang, `verified_on` hilang, pola kunci privat, `id` ≠ nama berkas | AC-20…AC-24 |
| T-INT-07 | Nav hasil generasi cocok dengan urutan `curriculum.json` | IA-02, AC-21 |
| T-INT-08 | Pemeriksa tautan: 0 tautan/aset internal rusak di `/` dan `/repo/` | AC-30, AC-31 |
| T-INT-09 | `SITE_URL` berubah → `canonical`, sitemap, dan `404` mengikuti; tidak ada berkas dikomit berubah | AC-32 |
| T-E2E-01…10 | AC-01…AC-10 pada ketiga browser | NFR-004 |
| T-E2E-11 | Klik tiap tautan "Buka materi" → halaman bab benar, status HTTP 200 | AC-25 |
| T-E2E-12 | Dengan `chapters.json` 404/rusak, semua fungsi dashboard tetap bekerja | FR-055 |
| T-E2E-13 | Perubahan status di materi terlihat di dashboard dan sebaliknya | AC-34 |
| T-NET-01 | Muat dashboard + satu halaman materi: 0 permintaan lintas-origin | AC-39 |
| T-CON-01 | Kontrak progres lulus pada dashboard dan `progress.js` | PRG-01, PRG-02, AC-35 |
| T-SEC-01 | Bahwa workflow memiliki `permissions:` eksplisit dan action tersemat SHA | AC-40 |

Usulan penambahan ke PRD: **AC-41** = T-INT-03 (reproduksi build) dan **AC-42** = T-INT-01/02 (sumber tak berubah dan salinan byte-identik).

### 12.3 Fixture dan data uji

- `tests/fixtures/mini-dashboard.html` berisi blok data kecil dengan penanda yang sama; digunakan agar uji cepat dan stabil.
- `tests/fixtures/materi/` berisi bab terbit, bab draft, dan bab dengan berbagai cacat (untuk T-INT-06).
- Uji pada repositori nyata memverifikasi 16/36/136 (AC-20).

### 12.4 Kriteria lulus per tahap

| Tahap | Lulus bila |
|---|---|
| PR | semua uji unit, integrasi, kontrak, e2e, axe hijau; `git status` bersih setelah build |
| Sebelum deploy | tahap PR + build di `main` hijau |
| Setelah deploy | `smoke.mjs` hijau (5 URL, `chapters.json` valid) |

---

## 13. Pemulihan Ketika Build Gagal

### 13.1 Pemulihan lokal (otomatis oleh `build.mjs`)

1. Sebelum menulis, `site/` yang ada dipindah ke `.build/site.prev/` (langkah 5).
2. Pada kegagalan di langkah mana pun, `build.mjs` memindahkan `site/` setengah jadi ke `.build/site.failed/`, mengembalikan `.build/site.prev/` menjadi `site/`, menulis `.build/report.json` (langkah gagal, pesan, berkas terkait), dan keluar dengan kode ≠ 0.
3. Kegagalan tidak pernah meninggalkan `site/` setengah jadi sebagai keluaran yang tampak valid.
4. Bila proses dihentikan paksa (mis. daya mati), penanda `.build/IN-PROGRESS` tertinggal; build berikutnya memulihkan `site.prev` terlebih dahulu lalu melanjutkan.

### 13.2 Pemulihan di CI/produksi

| Kegagalan | Efek pada produksi | Pemulihan |
|---|---|---|
| Validasi data/materi gagal (langkah 2–3) | Tidak ada; deploy tidak berjalan | Perbaiki sumber sesuai `report.json`; dorong ulang |
| `mkdocs --strict` gagal | Tidak ada | Perbaiki tautan/konfigurasi; jalankan lokal dengan `build.mjs` |
| Verifikasi/pemeriksa tautan gagal | Tidak ada | Perbaiki penyebab; jangan menonaktifkan pemeriksaan |
| Uji e2e/aksesibilitas gagal | Tidak ada | Perbaiki regresi; PR tidak dapat digabung |
| Build hijau tetapi sumber berubah (C-09) | Tidak ada | Perlakukan sebagai galat alat; perbaiki langkah yang menulis |
| Dua build tidak identik (T-INT-03) | Tidak ada | Telusuri berkas berbeda di `manifest`; kunci/larang sumber ketidakpastian (8.3) |
| `deploy-pages` gagal | Situs lama tetap aktif | Jalankan ulang job; Pages mengunggah ulang artefak yang sama |
| Smoke pasca-deploy gagal (situs terbit rusak) | **Situs rusak aktif** | **Rollback:** revert komit pada `main` dan biarkan pipeline berjalan, atau jalankan ulang alur `deploy` dari komit hijau terakhir (`workflow_dispatch` pada ref tersebut); target ≤ 15 menit (AC-37) |
| Gangguan GitHub Pages | Di luar kendali | Tunggu pemulihan; situs lama tetap bila tersedia; Vercel sebagai cadangan setelah milestone M9 |
| Rahasia ditemukan di repo/materi | Potensi bocor | Cabut/rotasi rahasia, hapus dari riwayat sesuai prosedur keamanan, terbitkan ulang; kebijakan SEC-01 |

### 13.3 Panduan diagnosis

`.build/report.json` memuat: langkah, kode galat, pesan, daftar berkas, versi alat. CI mengunggah `.build/` sebagai artefak pada kegagalan. README memuat tabel "gejala → penyebab → perbaikan" (MNT-05).

### 13.4 Rollback bab

Satu bab bermasalah: ubah `status` menjadi `draft` pada PR cepat. Build mengeluarkannya dari `nav` dan `chapters.json`, dashboard otomatis berhenti menaut ke sana (I-5), dan ID tetap di `published-ids.json` sehingga URL lama menampilkan halaman penjelasan (URL-04).

---

## 14. Keputusan Terbuka, Spike, dan Rencana

### 14.1 Spike verifikasi (sebelum implementasi massal)

| ID | Pertanyaan | Hasil yang dibutuhkan |
|---|---|---|
| T-01 | `INHERIT` dengan `docs_dir`/`site_dir` relatif ke `.build/`; `site_url: !ENV [..., null]`; `exclude_docs`; `site_dir: site/materi` bersarang | Konfigurasi minimal yang membangun fixture ke `site/materi/` tanpa peringatan |
| T-02 | Perilaku `--strict` atas tautan ke bab draft yang dikecualikan | Aturan tautan yang aman |
| T-03 | Sandbox `node:vm` dapat mengevaluasi blok data apa adanya (sudah diuji lepas oleh audit dengan `new Function`) | Skrip ekstraktor lulus pada 16/36/136 |
| T-04 | Apa saja berkas MkDocs/Material yang tidak deterministik (mis. `sitemap.xml.gz`) | Daftar pengecualian atau pengaturan agar deterministik |
| T-05 | Apakah tema memuat font/sumber daya eksternal secara bawaan | Konfigurasi tanpa permintaan lintas-origin (AC-39) |
| T-06 | Variabel lingkungan Vercel untuk URL produksi/pratinjau | Aturan turunan `SITE_URL` |
| T-07 | Ketersediaan Python/Node pada citra build Vercel | Pilih build di Vercel atau `--prebuilt` |
| T-08 | Inline script/style bawaan tema untuk CSP berbasis hash | Kebijakan CSP yang bekerja atau keputusan `unsafe-inline` terbatas |
| T-09 | Status dan versi MkDocs Material (A-05) | Keputusan tema dan versi terkunci |

### 14.2 Keputusan produk yang memengaruhi desain

| PRD | Dampak pada TDD |
|---|---|
| Q-03 (tata letak situs) | Desain ini mengasumsikan dashboard di `/` dan materi di `/materi/` (ditegaskan oleh batasan C-02, C-04) |
| Q-02 (`file://`) | Dampak berkurang: data tertanam; hanya tautan materi yang tidak muncul saat `file://` |
| Q-07 (nasib ID dihapus) | Aturan pemeliharaan state di `progress.js` (11.2 butir 2) |
| Q-09 (lisensi), Q-12 (domain kustom) | `SITE_URL` dan berkas lisensi di akar |
| Q-04, Q-13 | Isi materi; tidak memengaruhi arsitektur |

### 14.3 Pemetaan ke milestone PRD (setelah amandemen A1…A6)

| Milestone | Isi menurut TDD |
|---|---|
| M0 | Git, README, lisensi, `.gitignore`, `.gitattributes`, perlindungan cabang |
| M1 | Uji e2e dasar untuk dashboard dan fixture kontrak (tanpa mengubah dashboard kecuali cacat) |
| M2 | Ekstraktor, skema, validator graf; `curriculum.json` turunan (AC-20) |
| M3 | Kontrak progres dan `progress.js` dengan uji kontrak (menggantikan "pisah berkas") |
| M4 | `mkdocs.yml`, generator `nav`, validator materi, `scaffold`, templat 14 bagian |
| M5 | Perakit situs, `chapters.json`, pemeriksa tautan, alur kerja CI/Pages, tautan "Buka materi" di dashboard |
| M6…M9 | Tidak berubah; M9 memuat `vercel.json` dan CSP berbasis hash |

### 14.4 Kriteria kesiapan implementasi

Implementasi dimulai bila: (1) dokumen ini disetujui, (2) amandemen A1…A6 (sudah diterapkan ke PRD v0.2) dikonfirmasi pemilik produk, (3) spike T-01 dan T-09 selesai.

---

## Lampiran A. Matriks Batasan ke Rancangan

| Batasan | Dipenuhi oleh |
|---|---|
| C-01 | Dashboard tetap berkas sumber; build hanya membaca dan menyalin (3, 4.3, 8.2 #8) |
| C-02 | `site/index.html` salinan byte-identik (8.2 #8, T-INT-01) |
| C-03 | `materi/` = `docs_dir` (4.1, 4.4) |
| C-04 | `site_dir: site/materi` (4.4, 5) |
| C-05 | Satu `site/` diunggah sebagai satu artefak (9.1) |
| C-06 | `ci.yml`, `deploy.yml` (9.1) |
| C-07 | Jalur relatif, `SITE_URL`, `vercel.json` (7, 9.2) |
| C-08 | `chapters.json` dibuat dari berkas hasil build; invarian I-1…I-7 (6) |
| C-09 | Tulis hanya ke `.build/` dan `site/`; manifes, `git diff`, uji (8.4) |
| C-10 | Pengendali determinisme dan uji reproduksi (8.3, T-INT-03) |

## Lampiran B. Glosarium

| Istilah | Arti |
|---|---|
| Sumber | Berkas yang dikomit dan ditulis manusia: HTML dashboard, `materi/`, `mkdocs.yml`, `public/`, `tools/`, `tests/` |
| Artefak turunan | Berkas hasil build di `.build/` dan `site/`; tidak dikomit |
| Bab terbit | Bab dengan `status: published` yang halamannya benar-benar ada di `site/materi/chapter/<ID>/` |
| `BASE` | Awalan path situs (`/` atau `/<repo>/`) |
| Byte-identik | Hash SHA-256 salinan sama dengan hash sumber (setelah akhir baris LF terkendali oleh `.gitattributes`) |

---

## 15. Status Implementasi (diperbarui 2026-10-13)

Konfigurasi MkDocs dibangun ulang secara minimal. Bagian 1-14 tetap menjadi rancangan target; tabel berikut mencatat keadaan nyata.

| Komponen | Rancangan | Keadaan nyata |
|---|---|---|
| Konfigurasi MkDocs | `mkdocs.yml` + `.build/mkdocs.generated.yml` (`INHERIT`) | Hanya `mkdocs.yml` dengan `nav` manual (beranda dan level L0–L15 (L15 adalah level terakhir) beserta seluruh chapternya); tautan ke dashboard (`../../../#ID`) ditangani hook `hooks/dashboard_links.py` karena dashboard berada di luar `docs_dir` dan tidak dapat divalidasi MkDocs; navigasi sebelumnya/berikutnya di bawah halaman memakai fitur bawaan Material `navigation.footer` (urutan mengikuti `nav`, tanpa tautan manual di Markdown; label diubah lewat `overrides/partials/languages/id.html` dengan `theme.custom_dir: overrides`, salinan terjemahan `id` Material dengan dua kunci `footer.*` diganti — periksa ulang saat Material dinaikkan versinya); mode terang/gelap memakai `theme.palette` bawaan Material dengan tiga status (otomatis mengikuti sistem, terang, gelap) dan pilihan pengguna disimpan Material di `localStorage`; tanpa CSS/JS kustom, dan dashboard HTML tidak ikut (temanya terpisah); diagram Mermaid memakai `custom_fences` `pymdownx.superfences` (Material memuat pustaka mermaid@11 dari unpkg saat halaman dibuka). `INHERIT` dan generator belum dibuat karena belum ada bab; T-01 sebagian terjawab: `site_dir: site/materi`, `docs_dir: materi`, dan `site_url: !ENV [SITE_URL, null]` bekerja pada MkDocs 1.6.1 |
| Perakitan dashboard | `tools/build.mjs` (Node) | `scripts/copy-dashboard.py` (Python, sudah ada) menyalin dashboard ke `site/index.html`; alat Node belum dibuat |
| Dashboard | Tidak diubah build | Tautan header "Materi" (`href="materi/"`, relatif) dan pemuatan `materi/chapters.json` (opsional, gagal-aman) yang menampilkan tombol "Buka materi" pada bab terbit |
| `chapters.json` | Bagian 6.3 | `scripts/generate-chapters-json.py` memindai front matter dan hasil build; bab terbit: L0 (`CH-01-01-*`), L1 (`CH-02-*`), dan `CH-03-01-01`; ringkasan level `L0`, `L1` |
| Ekstraktor, validator front matter/14 heading, generator `nav` | Bagian 4.3, 4.4.1 | Belum dibuat; `nav` masih manual |
| CI/CD Pages, Vercel, `.gitattributes` | Bagian 9 | Belum dibuat |
| Versi | Dikunci di `requirements.txt` | `mkdocs==1.6.1`, `mkdocs-material==9.7.7`, `pymdown-extensions==11.0.2` (dependensi transitif belum dikunci dengan hash) |

Temuan pendukung T-04 dan A-05: `sitemap.xml.gz` adalah satu-satunya berkas yang berbeda antar build; MkDocs Material 9.7.7 menampilkan peringatan tentang MkDocs 2.0 (tanpa dukungan plugin/tema), sehingga versi MkDocs harus tetap `<2`. Perbedaan penataan folder: `CLAUDE.md` menyebut berkas bab "di bawah kategori yang sesuai" sedangkan bagian 4.1 menetapkan `materi/chapter/CH-NN-NN-NN.md`; keputusan diperlukan sebelum bab pertama.
