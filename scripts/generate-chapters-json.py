"""Membuat site/materi/chapters.json dari hasil build MkDocs (TECHNICAL-DESIGN 6.3).

Hanya bab berstatus published yang halaman hasil build-nya benar-benar ada yang dimasukkan.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "materi" / "chapter"
LEVEL_SOURCE = ROOT / "materi" / "level"
OUTPUT_DIR = ROOT / "site" / "materi"
ID_PATTERN = re.compile(r"^CH-\d{2}-\d{2}-\d{2}$")
LEVEL_ID_PATTERN = re.compile(r"^CAT-\d{2}$")
LEVEL_FILE_PATTERN = re.compile(r"^L\d{1,2}$")

if not (OUTPUT_DIR / "index.html").is_file():
    raise FileNotFoundError("Dokumentasi MkDocs belum dibuat. Jalankan mkdocs build terlebih dahulu.")


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        raise ValueError(f"Front matter tidak ditemukan: {path}")
    data = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "-")):
            data[key.strip()] = value.strip()
    return data


chapters = {}
for md in sorted(SOURCE.glob("*.md")):
    meta = front_matter(md)
    chapter_id = meta.get("id", "")
    if not ID_PATTERN.match(chapter_id) or chapter_id != md.stem:
        raise ValueError(f"ID front matter harus sama dengan nama berkas: {md.name}")
    if meta.get("status") != "published":
        continue
    if not (OUTPUT_DIR / "chapter" / chapter_id / "index.html").is_file():
        raise FileNotFoundError(f"Halaman hasil build tidak ada untuk {chapter_id}")
    chapters[chapter_id] = {"path": f"chapter/{chapter_id}/", "title": meta["title"]}

levels = {}
for md in sorted(LEVEL_SOURCE.glob("*.md")):
    meta = front_matter(md)
    level_id = meta.get("id", "")
    if not LEVEL_ID_PATTERN.match(level_id) or not LEVEL_FILE_PATTERN.match(md.stem):
        raise ValueError(f"Berkas level tidak valid: {md.name}")
    if meta.get("status") != "published":
        continue
    if not (OUTPUT_DIR / "level" / md.stem / "index.html").is_file():
        raise FileNotFoundError(f"Halaman hasil build tidak ada untuk {md.stem}")
    levels[level_id] = {"path": f"level/{md.stem}/", "title": meta["title"].strip('"')}

target = OUTPUT_DIR / "chapters.json"
target.write_text(
    json.dumps({"schema": 1, "chapters": chapters, "levels": levels}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(f"{len(chapters)} bab dan {len(levels)} level dicatat di: {target}")
