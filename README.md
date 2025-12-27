# Minimal Cloudflare Pages Smoke Test

This repo now only publishes `public/index.html` so we can verify a simple Pages deployment before reintroducing backend logic.

## Local smoke test

```bash
wrangler pages dev public --port 8787
```

Open `http://localhost:8787/` (append `?hello=1` if you want the pure Hello-World variant) to confirm the Worker serves the static file.

## Deploy

```bash
wrangler pages deploy public
```

Cloudflare will upload just `public/index.html` and you can point a browser at the generated URL to ensure the minimal site renders.
