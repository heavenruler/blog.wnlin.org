.PHONY: help manifest test push newpost

MESSAGE ?= chore: update

help:
	@echo "Available targets:"
	@echo "  help     Show this help."
	@echo "  manifest Regenerate public/content/posts/manifest.json from Markdown files."
	@echo "  sitemap  Generate public/sitemap.xml for Google Search Console."
	@echo "  test     Run wrangler pages dev to preview the site locally."
	@echo "  push     git add ., git commit -m \"$$MESSAGE\", and git push."
	@echo "  newpost  Create public/content/posts/default/draft.md with a draft template."

manifest:
	@for f in $$(find public/content/posts -type f -name draft.md); do \
		dir=$$(dirname "$$f"); \
		base=$$(date +%Y%m%d%H%M%S); \
		target="$$dir/$${base}.md"; \
		n=1; \
		while [ -e "$$target" ]; do \
			target="$$dir/$${base}_$${n}.md"; \
			n=$$((n+1)); \
		done; \
		mv "$$f" "$$target"; \
		echo "Renamed $$f -> $$target"; \
	done
	@python3 scripts/generate_manifest.py

test:
	@WRANGLER=$$(command -v wrangler || { [ -x node_modules/.bin/wrangler ] && echo node_modules/.bin/wrangler; }); \
	if [ -z "$$WRANGLER" ]; then \
		if ! command -v npm >/dev/null 2>&1; then \
			echo "wrangler not found and npm is missing. Install Node.js (e.g. brew install node) to get npm, then run: npm i -g wrangler"; \
		else \
			echo "wrangler not found. Install it globally with: npm i -g wrangler"; \
		fi; \
		exit 1; \
	fi; \
	"$$WRANGLER" pages dev public --port 8787

push:
	@$(MAKE) manifest
	@git add .
	@git commit -m "$(MESSAGE)"
	@git push

sitemap:
	@python3 scripts/generate_sitemap.py

newpost:
	@dest="public/content/posts/default/draft.md"; \
	today=$$(date +%Y-%m-%d); \
	printf '%s\n' \
	'---' \
	'title: Draft Post' \
	'date: REPLACE_WITH_DATE' \
	'excerpt: |' \
	'  Short summary goes here.' \
	'draft: true' \
	'---' \
	'' \
	'# Draft Title' \
	'' \
	'Start writing your content here.' \
	> "$$dest"; \
	sed -i '' "s/REPLACE_WITH_DATE/$$today/" "$$dest" 2>/dev/null || \
	  sed -i "s/REPLACE_WITH_DATE/$$today/" "$$dest" 2>/dev/null || true; \
	echo "Created $$dest (marked draft: true)."
