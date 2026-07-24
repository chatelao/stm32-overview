# Technical Debts

This document logs outstanding issues, non-critical technical observations, and design trade-offs made during development, as specified in the project guidelines.

---

## 1. CLI Exception Handling & Test Coverage
*   **Observation**: The Click CLI commands in `src/main.py` contain catch-all `except Exception as e` blocks that exit the program with code `1`.
*   **Impact**: These branches are currently not hit during unit tests (which contributes to the remaining uncovered lines in `src/main.py`), because simulating unexpected system-level or dependency failures requires extensive mocking and patching of core modules.
*   **Actionable Recommendation**: Refactor CLI error handling to bubble specific exceptions to a centralized Click exception handler, or add specialized test fixtures to mock failures in the `RegistryEngine` or `ComparisonEngine`.

## 2. ReadTheDocs Setup & Missing Documentation Config
*   **Observation**: We have configured `.readthedocs.yaml` to point to `mkdocs.yml` for rendering documentation. However, the `mkdocs.yml` configuration and the corresponding `docs/` source directory have not been fully initialized.
*   **Impact**: When ReadTheDocs attempts to build the project, it will fail due to the missing `mkdocs.yml` configuration.
*   **Actionable Recommendation**: Create a standard `mkdocs.yml` file and standard markdown pages under a new `docs/` folder, importing `CONCEPT.md`, `DESIGN.md`, and any exported comparison matrices.

## 3. Simplistic Hardware Accelerator Modeling
*   **Observation**: Hardware accelerators (`cordic` and `fmac`) are currently modeled as simple boolean flags in both specifications and recommendations.
*   **Impact**: It does not allow for specifying version numbers, performance characteristics, or memory allocation details.
*   **Actionable Recommendation**: Extend the `CoreSpec` model to allow optional objects/sub-schemas for hardware accelerators to support more granular hardware capabilities if they become relevant in future workshop iterations.

## 4. Default Export File Safety
*   **Observation**: The `export` command defaults to writing to `README.md`.
*   **Impact**: An accidental execution of `python3 src/main.py export` without specifying `-o` will overwrite the repository's root `README.md` (if it existed or was customized).
*   **Actionable Recommendation**: Change the default output of the `export` command to a safe path (such as `docs/comparison_matrix.md`) or prompt the user for confirmation if they are about to overwrite an existing root-level file.
