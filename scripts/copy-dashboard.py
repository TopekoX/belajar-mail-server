from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "kurikulum-mail-server-ubuntu.html"
DESTINATION = ROOT / "site" / "index.html"

if not SOURCE.is_file():
    raise FileNotFoundError(f"Dashboard tidak ditemukan: {SOURCE}")

if not (ROOT / "site" / "materi" / "index.html").is_file():
    raise FileNotFoundError(
        "Dokumentasi MkDocs belum dibuat. Jalankan mkdocs build terlebih dahulu."
    )

DESTINATION.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(SOURCE, DESTINATION)

print(f"Dashboard berhasil disalin ke: {DESTINATION}")
