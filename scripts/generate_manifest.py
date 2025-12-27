#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path('public/content/posts')
DEFAULT_DIR = ROOT / 'default'
MANIFEST_PATH = ROOT / 'manifest.json'


def parse_front_matter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return {}, text, False
    data = {}
    for index, line in enumerate(lines[1:], 1):
        stripped = line.strip()
        if stripped == '---':
            body = '\n'.join(lines[index + 1 :])
            return data, body, True
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data, '\n'.join(lines), False


def extract_title(body: str):
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith('#'):
            return stripped.lstrip('#').strip()
    return ''


def extract_excerpt(body: str, line_count: int = 10):
    excerpt_lines = []
    for line in body.splitlines():
        text = line.strip()
        if not text:
            continue
        excerpt_lines.append(line.rstrip())
        if len(excerpt_lines) >= line_count:
            break
    return '\n'.join(excerpt_lines)


def guess_date(path: Path, meta: dict):
    raw = meta.get('date')
    if raw:
        return raw
    mtime = path.stat().st_mtime
    return datetime.fromtimestamp(mtime).date().isoformat()


def format_excerpt_block(excerpt: str):
    if not excerpt:
        return "excerpt: ''"
    lines = excerpt.splitlines()
    block_lines = ['excerpt: |']
    for line in lines:
        block_lines.append(f'  {line}')
    return '\n'.join(block_lines)


def write_front_matter(path: Path, title: str, date: str, excerpt: str, body: str):
    block = '\n'.join([
        '---',
        f'title: {title}',
        f'date: {date}',
        format_excerpt_block(excerpt),
        '---',
        '',
    ])
    path.write_text(f'{block}{body}', encoding='utf-8')


def build_post(path: Path):
    text = path.read_text(encoding='utf-8')
    meta, body, has_meta = parse_front_matter(text)
    title = meta.get('title') or extract_title(body) or path.stem
    excerpt = extract_excerpt(body)
    date = guess_date(path, meta)
    if not has_meta:
        write_front_matter(path, title, date, excerpt, text)
    return {
        'file': path.relative_to(ROOT).as_posix(),
        'title': title,
        'date': date,
        'excerpt': excerpt,
    }


def gather_posts(directory: Path):
    posts = []
    for path in sorted(directory.glob('*.md')):
        posts.append(build_post(path))
    return sorted(posts, key=lambda e: e['date'], reverse=True)


def build_manifest():
    if not ROOT.exists():
        raise SystemExit('Posts directory not found')

    manifest = {'default': {'label': 'Default', 'posts': []}, 'categories': []}
    if DEFAULT_DIR.exists():
        manifest['default']['posts'] = gather_posts(DEFAULT_DIR)

    for subdir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name != 'default'):
        posts = gather_posts(subdir)
        if posts:
            manifest['categories'].append(
                {
                    'slug': subdir.name,
                    'directory': subdir.name,
                    'label': subdir.name,
                    'posts': posts,
                }
            )
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated manifest at {MANIFEST_PATH}')


if __name__ == '__main__':
    build_manifest()
