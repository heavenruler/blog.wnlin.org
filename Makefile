.PHONY: help manifest

help:
	@echo "Available targets:"
	@echo "  help     Show this help."
	@echo "  manifest Regenerate public/content/posts/manifest.json from Markdown files."

manifest:
	@python3 scripts/generate_manifest.py
