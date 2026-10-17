"""Tautan dari halaman materi ke dashboard (site/index.html).

Dashboard berada di luar docs_dir sehingga MkDocs tidak dapat memvalidasi tautan relatifnya
(`unrecognized relative link`). Sumber Markdown tetap memakai `../../../#ID`; hook ini mengganti
tautan itu dengan skema sementara `dashboard:` agar tidak divalidasi sebagai berkas dokumentasi,
lalu menuliskan jalur relatif yang benar sesuai kedalaman halaman hasil build (aman untuk
base path GitHub Pages karena tetap relatif).
"""
import re

_SRC = re.compile(r"\]\((?:\.\./)+(#[A-Za-z0-9-]+)?\)")
_OUT = re.compile(r'href="dashboard:(#[A-Za-z0-9-]*)?"')


def on_page_markdown(markdown, page, config, files):
    return _SRC.sub(lambda m: f"](dashboard:{m.group(1) or ''})", markdown)


def on_post_page(output, page, config):
    # site_dir = site/materi, dashboard di site/ -> satu tingkat di atas akar dokumentasi.
    depth = len([s for s in page.url.split("/") if s]) + 1
    prefix = "../" * depth
    return _OUT.sub(lambda m: f'href="{prefix}{m.group(1) or ""}"', output)
