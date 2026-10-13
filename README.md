# Mail Server Ubuntu Learning Portal

Kurikulum interaktif (dashboard) dan materi Markdown untuk membangun dan mengelola mail server dengan Ubuntu Server. Detail produk dan arsitektur: `docs/PRD.md`, `docs/TECHNICAL-DESIGN.md`.

## Struktur

| Jalur | Fungsi |
|---|---|
| `kurikulum-mail-server-ubuntu.html` | Sumber dashboard (diterbitkan sebagai `site/index.html`) |
| `materi/` | Sumber materi Markdown (`docs_dir` MkDocs) |
| `mkdocs.yml`, `requirements.txt` | Konfigurasi dan dependensi MkDocs |
| `scripts/copy-dashboard.py` | Menyalin dashboard ke `site/index.html` setelah MkDocs dibangun |
| `scripts/generate-chapters-json.py` | Membuat `site/materi/chapters.json` (daftar bab dan level terbit) dari hasil build |
| `site/` | Keluaran build (tidak dikomit): dashboard di `/`, dokumentasi di `/materi/` |

## Perintah

```bash
pip install -r requirements.txt
python -m mkdocs serve                 # pratinjau materi saja: http://127.0.0.1:8000/materi/
python -m mkdocs build                 # menulis site/materi/
python scripts/copy-dashboard.py       # menyalin dashboard ke site/index.html
python scripts/generate-chapters-json.py   # membuat site/materi/chapters.json (tautan "Buka materi")
cd site
python -m http.server 8000             # menjalankan server
```

Urutan build wajib: `mkdocs build` dahulu, lalu kedua skrip (MkDocs membersihkan `site/materi/` saat build).

### Variabel lingkungan

Tidak ada variabel lingkungan yang wajib diisi sebelum build. Tanpa variabel apa pun, build lokal tetap berjalan.

| Variabel | Wajib | Fungsi |
|---|---|---|
| `SITE_URL` | Tidak | Mengisi `site_url` di `mkdocs.yml` (`!ENV [SITE_URL, null]`) untuk `canonical` dan sitemap. Isi hanya saat deploy; bila kosong, nilainya null. |

Contoh untuk deploy (isi dengan URL materi, berakhiran `/materi/`):

```bash
SITE_URL=https://pengguna.github.io/repo/materi/ python -m mkdocs build
```

Semua tautan dashboard dan materi relatif, sehingga situs berjalan di akar domain maupun di subpath GitHub Pages.

## Menjalankan dashboard dan materi secara lokal

`mkdocs serve` hanya menyajikan materi. Untuk dashboard dan materi sekaligus, bangun lalu sajikan folder `site/`:

```bash
python -m mkdocs build
python scripts/copy-dashboard.py
python scripts/generate-chapters-json.py
cd site
python -m http.server 8000
```

- Dashboard: `http://localhost:8000/`
- Materi: `http://localhost:8000/materi/`
- Jangan membuka `index.html` lewat `file://`: `chapters.json` tidak dapat dimuat sehingga tombol "Buka materi" tidak muncul.
- Ulangi ketiga perintah build setelah mengubah materi, karena `mkdocs build` menghapus `site/materi/` beserta `chapters.json`.

## Deploy

Semua cara deploy di bawah ini **belum diuji** di repositori ini; sesuaikan dengan penyedia yang Anda pakai. Prinsipnya sama: jalankan urutan build, lalu publikasikan **seluruh folder `site/`** (dashboard di akar, materi di `/materi/`).

Jangan memakai `mkdocs gh-deploy`: perintah itu hanya menerbitkan isi `site/materi/` ke akar branch `gh-pages`, tanpa dashboard dan `chapters.json`, sehingga URL dan tautan kembali ke dashboard salah.

Nilai `SITE_URL` selalu berupa URL materi, berakhiran `/materi/`.

| Penyedia | Biaya | `SITE_URL` |
|---|---|---|
| GitHub Pages | Gratis untuk repo publik; repo privat bergantung paket GitHub | `https://<pengguna>.github.io/<repo>/materi/` |
| Cloudflare Pages, Netlify, Vercel | Ada paket gratis; periksa batasan penyedia | `https://<domain>/materi/` |
| GitLab Pages | Gratis; periksa batasan penyedia | sesuai URL Pages proyek |

### Opsi 1: GitHub Pages dengan GitHub Actions (disarankan di GitHub)

1. Di repositori: *Settings > Pages > Source: GitHub Actions*.
2. Buat `.github/workflows/pages.yml`:

```yaml
name: Deploy Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/configure-pages@v5
        id: pages
      - run: pip install -r requirements.txt
      - run: python -m mkdocs build
        env:
          SITE_URL: ${{ steps.pages.outputs.base_url }}/materi/
      - run: python scripts/copy-dashboard.py
      - run: python scripts/generate-chapters-json.py
      - run: touch site/.nojekyll
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
      - id: deployment
        uses: actions/deploy-pages@v4
```

3. Commit dan push ke `main`. Pastikan `scripts/`, `materi/`, `mkdocs.yml`, dan `requirements.txt` ikut ter-commit (`site/` memang diabaikan git).
4. Hasil: dashboard di `https://<pengguna>.github.io/<repo>/`, materi di `.../<repo>/materi/`.

### Opsi 2: GitHub Pages tanpa Actions (manual)

Bangun di komputer sendiri, lalu dorong isi `site/` ke branch `gh-pages` dengan `ghp-import` (belum ada di `requirements.txt`; pasang dengan `pip install ghp-import`):

```bash
SITE_URL=https://<pengguna>.github.io/<repo>/materi/ python -m mkdocs build
python scripts/copy-dashboard.py
python scripts/generate-chapters-json.py
touch site/.nojekyll
ghp-import -n -p site
```

Lalu atur *Settings > Pages > Source: Deploy from a branch* dengan branch `gh-pages` dan folder `/ (root)`.

### Opsi 3: Vercel, Netlify, atau Cloudflare Pages

Hubungkan repositori dan atur:

- Framework preset: Other / tanpa framework.
- Install command: `pip install -r requirements.txt`
- Build command: `python -m mkdocs build && python scripts/copy-dashboard.py && python scripts/generate-chapters-json.py`
- Output directory: `site`
- Environment variable (di dashboard penyedia, bukan `.env`): `SITE_URL=https://<domain>/materi/`

Pastikan lingkungan build penyedia memiliki Python dan `pip`; periksa versi yang tersedia.

### Opsi 4: GitLab Pages

Buat `.gitlab-ci.yml` yang menjalankan urutan build, lalu menyalin hasilnya ke folder `public` sebagai artifact pada job bernama `pages`. Contoh kerangka (belum diuji):

```yaml
pages:
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - python -m mkdocs build
    - python scripts/copy-dashboard.py
    - python scripts/generate-chapters-json.py
    - mkdir public && cp -r site/. public/
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

Atur `SITE_URL` sebagai CI/CD variable proyek.

### Setelah deploy

- Buka `/` (dashboard), klik **Materi** di header, dan buka satu chapter lewat tombol **Buka materi**.
- Pastikan `/materi/chapters.json` dapat diakses (HTTP 200).
