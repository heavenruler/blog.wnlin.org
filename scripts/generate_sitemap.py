#!/usr/bin/env python3
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from generate_manifest import ROOT as POSTS_ROOT, parse_front_matter, is_draft

PUBLIC_ROOT = Path("public")
DEFAULT_BASE = "https://blog.wnlin.org"
SITEMAP_PATH = PUBLIC_ROOT / "sitemap.xml"


def get_base_url() -> str:
    return os.environ.get("SITE_BASE", DEFAULT_BASE).rstrip("/")


def build_url_entries() -> List[Dict[str, str]]:
    base = get_base_url()
    urls: List[Dict[str, str]] = []

    index_path = PUBLIC_ROOT / "index.html"
    if index_path.exists():
        urls.append(
            {
                "loc": f"{base}/",
                "lastmod": datetime.fromtimestamp(index_path.stat().st_mtime).date().isoformat(),
            }
        )

    for path in sorted(POSTS_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, _, _ = parse_front_matter(text)
        if is_draft(meta, path):
            continue
        urls.append(
            {
                "loc": f'{base}/{path.relative_to(PUBLIC_ROOT).as_posix()}',
                "lastmod": datetime.fromtimestamp(path.stat().st_mtime).date().isoformat(),
            }
        )
    return urls


def render_xml(urls: List[Dict[str, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in urls:
        lines.append("  <url>")
        lines.append(f'    <loc>{entry["loc"]}</loc>')
        if entry.get("lastmod"):
            lines.append(f'    <lastmod>{entry["lastmod"]}</lastmod>')
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    urls = build_url_entries()
    if not urls:
        raise SystemExit("No URLs found for sitemap. Add posts or check paths.")
    SITEMAP_PATH.write_text(render_xml(urls), encoding="utf-8")
    print(f"Wrote sitemap with {len(urls)} entries to {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
