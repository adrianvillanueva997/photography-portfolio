.PHONY: help clean clean-raw clean-converted clean-all process-collection

# macOS setup - required for pyvips on Apple Silicon
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	export DYLD_LIBRARY_PATH := /opt/homebrew/lib:$(DYLD_LIBRARY_PATH)
endif

help:
	@echo "Image Processing Pipeline - Available Commands"
	@echo ""
	@echo "  make clean-raw                      Remove all files from pipeline_artifacts/raw/"
	@echo "  make clean-converted                Remove all files from pipeline_artifacts/converted/"
	@echo "  make clean-all                      Remove all files from both raw/ and converted/"
	@echo ""
	@echo "  make process-collection COLLECTION=<name>   Process all raw images and add to collection"
	@echo "                                     Example: make process-collection COLLECTION=tokyo"
	@echo ""

clean-raw:
	@echo "🗑️  Cleaning pipeline_artifacts/raw/..."
	@find pipeline_artifacts/raw -type f ! -name '.gitkeep' -delete
	@echo "✓ Done"

clean-converted:
	@echo "🗑️  Cleaning pipeline_artifacts/converted/..."
	@find pipeline_artifacts/converted -type f ! -name '.gitkeep' -delete
	@echo "✓ Done"

clean-all: clean-raw clean-converted
	@echo "✓ All folders cleaned"

process-collection:
	@if [ -z "$(COLLECTION)" ]; then \
		echo "Error: COLLECTION not specified"; \
		echo "Usage: make process-collection COLLECTION=<name>"; \
		echo "Example: make process-collection COLLECTION=tokyo"; \
		exit 1; \
	fi
	@echo "📸 Processing all raw images and adding to collection: $(COLLECTION)"
	@uv run image_processing_pipeline/src/image_processing_pipeline/cli.py add-to-collection --collection $(COLLECTION)
	@echo "✓ Collection updated: $(COLLECTION)"
