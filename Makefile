.PHONY: help manifest test push

MESSAGE ?= chore: update

help:
	@echo "Available targets:"
	@echo "  help     Show this help."
	@echo "  manifest Regenerate public/content/posts/manifest.json from Markdown files."
	@echo "  test     Run wrangler pages dev to preview the site locally."
	@echo "  push     git add ., git commit -m \"$$MESSAGE\", and git push."

manifest:
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
	@git add .
	@git commit -m "$(MESSAGE)"
	@git push
