import os
import pytest
from src.core.repository import DataRepository
from src.download_ref_docs import DOWNLOAD_TARGETS

def test_yaml_documentation_matches_downloader_targets():
    """
    Ensures that every YAML specification file in specification/ contains accurate URL
    references and destination paths under its 'documentation' block, matching
    the DOWNLOAD_TARGETS defined in src/download_ref_docs.py.
    """
    repo = DataRepository("specification")
    specs = repo.load_all_specs()

    # We expect exactly 7 specifications loaded.
    assert len(specs) == 7, f"Expected 7 specs, but got {len(specs)}"

    # Convert downloader targets list into a lookup dictionary/set of (url, dest)
    downloader_pairs = {(target["url"], target["dest"]) for target in DOWNLOAD_TARGETS}

    for spec in specs:
        board_name = spec["board"]
        docs = spec.get("documentation")

        assert docs is not None, f"Board '{board_name}' is missing documentation block."

        # Verify that each document type exists and matches downloader targets
        for doc_type in ["user_manual", "datasheet", "reference_manual"]:
            doc_item = docs.get(doc_type)
            assert doc_item is not None, f"Board '{board_name}' is missing '{doc_type}' inside documentation."

            url = doc_item["url"]
            dest = doc_item["dest"]

            # Check for exact match in our downloader targets
            assert (url, dest) in downloader_pairs, (
                f"For board '{board_name}', doc type '{doc_type}': "
                f"pair (URL: {url}, Dest: {dest}) was not found in src/download_ref_docs.py DOWNLOAD_TARGETS."
            )
