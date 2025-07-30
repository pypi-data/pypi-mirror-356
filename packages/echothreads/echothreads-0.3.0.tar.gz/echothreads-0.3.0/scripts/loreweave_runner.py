#!/usr/bin/env python3
"""Simple runner for LoreWeave narrative processing.

This consolidates the usual CLI steps into a single script so developers can
run `python scripts/loreweave_runner.py` from the repository root.
"""
from pathlib import Path
import sys

# Ensure local packages are importable when running from the repo root
repo_root = Path(__file__).resolve().parents[1]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from loreweave.parser import LoreWeaveParser
from loreweave.openapi_specweaver import OpenAPISpecWeaver


def main() -> None:
    config_path = repo_root / "LoreWeave" / "config.yaml"
    parser = LoreWeaveParser(str(repo_root), str(config_path))
    # Load OpenAPI specification for enhanced issue sync
    weaver = OpenAPISpecWeaver()
    if weaver.load_openapi_spec():
        print(f"Loaded OpenAPI spec from {weaver.spec_path}")
    else:
        print("Failed to load OpenAPI spec; proceeding with basic sync")

    parser.run_post_commit()
    parser.run_post_push()
    parser.sync_with_github_issues()
    parser.update_redstone_registry()


if __name__ == "__main__":
    main()
