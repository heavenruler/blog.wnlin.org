# Markdown-it Posts Feed

This repo now renders Markdown posts from `public/content/posts/` via a manifest. Each category folder maps to a tab in the UI, and the default feed is served until you click a tab.

## Setup

Install Python 3 if you don't already have it, then regenerate the manifest after adding or editing Markdown files:

```bash
make manifest
```

The generator infers `title`, `date`, and an excerpt (the first ten non-empty lines) from each `.md` file and writes `manifest.json`, which the frontend fetches at runtime.

## Local preview

```bash
wrangler pages dev public --port 8787
```

Visit `http://localhost:8787/` to browse the default feed, and click the tabs to switch categories.

## Deploy

```bash
wrangler pages deploy public
```

Cloudflare Pages will upload `public/index.html` alongside `public/content/posts/manifest.json`, and the site will serve the rendered Markdown feed.
