.PHONY: help test commit update manifest

help:
	@echo "Available targets:"
	@echo "  help     Show this help."
	@echo "  test     Start local http server rooted at public/ (python3 -m http.server PORT --directory public, default 80)."
	@echo "  manifest Regenerate public/content/posts/manifest.json from Markdown files."
	@echo "  commit   Git add -A and commit with COMMIT_MSG (default: \"chore: update site\")."
	@echo "  update   Git pull to sync with remote."

PORT ?= 80
COMMIT_MSG ?= "chore: update site"

test:
	@echo "Starting local server on port $(PORT) (Ctrl+C to stop)..."
	@echo "http://localhost:$(PORT)"
	python3 -m http.server $(PORT) --directory public

commit:
	git add -A
	git commit -m $(COMMIT_MSG)

update:
	git pull

manifest:
	@python3 scripts/generate_manifest.py
