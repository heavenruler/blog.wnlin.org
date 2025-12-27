# Cloudflare Pages + Workers Markdown Demo

This repo shows a minimal Cloudflare Pages site that renders Markdown in the browser using `markdown-it`. The front end now reads metadata from `public/content/posts/manifest.json`, presents the `public/content/posts/default` stream by default, groups the numbered posts into `category1`–`category4`, sorts them by date within each category, and renders five posts per page with category tabs, dual pagination strips, and lazy-loading excerpts while the Pages Function in `functions/api/latest-commit.js` stays available for manual API testing or future integration.

## Structure

```
public/           # Static assets served by Pages
  ├── index.html  # WordPress-style feed that paginates category-based posts (5 per page)
 └── content/
     └── posts/
         ├── default/
         │   ├── 1.md
         │   ├── 10.md
         │   ├── 2.md
         │   ├── 3.md
         │   ├── 4.md
         │   ├── 5.md
         │   ├── 6.md
         │   ├── 7.md
         │   ├── 8.md
         │   ├── 9.md
          ├── category1/
          │   ├── 1.md
          │   ├── 2.md
          │   └── 3.md
          ├── category2/
          │   ├── 4.md
          │   ├── 5.md
          │   └── 6.md
          ├── category4/
          │   ├── 9.md
          │   └── 10.md
          ├── category5/
          │   ├── 7.md
          │   ├── 8.md
          │   ├── 9.md
          │   ├── 10.md
          │   ├── 11.md
          │   └── 12.md
          └── manifest.json  # Metadata used by the frontend to provide the default stream and category grouping
functions/        # Pages Functions run on Cloudflare Workers
  └── api/latest-commit.js  # Endpoint fetching GitHub commits
wrangler.toml     # Wrangler config to deploy both the Pages site and functions
``` 

## Pagination

`public/index.html` reads the `default` collection first so the default stream is shown until a category tab is clicked. Each tab targets a real `category*` directory, sorts by `date`, and renders five posts per page with rounded Previous/Next controls (plus numerical page dots) positioned both above and below the article feed. Category 5 has six entries so the pagination controls surface the second page, and category tabs now read their directory names straight from `manifest.json`, letting renames and URL-driven lookups stay in sync with how your filesystem is arranged. The header title remains a link back to the default feed, and the current page/category pair is persisted in the URL (`?category=category5&page=2`) so you can deep link while navigation updates history during browsing.

## Generating the manifest

`public/content/posts/manifest.json` now comes from `scripts/generate_manifest.py`, so there’s no need to hand-edit the JSON after adding a Markdown file. Drop new posts into `public/content/posts/<category>/` (use `default/` for the homepage stream) and run `make manifest` to regenerate the manifest JSON—the script infers titles from the first heading, dates from front-matter or file modification time, automatically injects a `title/date/excerpt` front matter block if missing, and uses the first ten non-empty lines of the article for the excerpt, then sorts each feed by date for the paginated tabs.

## Excerpts & lazy loading

Each manifest entry now includes an `excerpt` so the feed initially shows trimmed content instead of loading the complete post bodies. A “Read full article” button fetches the Markdown for that post only when clicked, which keeps the default page payload small while still letting readers expand any article they want.

## Running locally

1. Install Wrangler 3 via `npm install -g wrangler` if you haven't already.
2. From the repo root run:

```bash
wrangler pages dev public --local-protocol http --local-port 8787
```

This command hosts the Pages site, automatically wiring `functions/` so `/api/latest-commit` is handled by the function.

## Deploying

1. Create a Cloudflare Pages project in the dashboard, connect this GitHub repo, and set the build command to `npm run build` (if defined) or leave blank for static sites.
2. Set the Environment Variables on Pages for the GitHub token (optional but recommended for higher rate limits):

```
GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXX
```

3. Link `public/` as the deployment directory and enable Functions support by ensuring they are in `functions/`.
4. Optional: run `wrangler publish` against a Pages environment once `wrangler.toml` has your `account_id` and `project` settings filled out.

## API usage

The frontend posts to `/api/latest-commit?repo=owner/name`. Example:

```
fetch('/api/latest-commit?repo=cloudflare/cloudflare-docs')
  .then(res => res.json())
```

The response is JSON with `sha`, `message`, `author`, `date`, and `url` to the commit.

## Next steps

1. Add more Markdown-it plugins (tables, footnotes) in `public/index.html`.
2. Extend the function to cache responses in Durable Objects or KV.
3. Wire CI/CD to automatically deploy when the GitHub repo is updated.
