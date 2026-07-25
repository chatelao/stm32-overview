# Roadmap: Reference and User Manual PDF Downloads for STM32 Workshop Boards

This document outlines the strategic roadmap, milestones, and phased execution plan for setting up, validating, and maintaining the automated download pipeline for the STM32 Workshop board reference manuals and datasheets, as conceptualized in `ALL_REF_DOC_CONCEPT.md`.

---

## Progress Overview

| Phase | Description | Status | Target Completion |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Pipeline Conceptualization & Script Preparation | ✅ | Completed |
| **Phase 2** | Directory Schema Setup & Mock Verification | ✅ | Completed |
| **Phase 3** | Automated Testing & Fallback Validation | ⏳ | Q1 |
| **Phase 4** | CLI Integration & CI Workflows | ⏳ | Q2 |
| **Phase 5** | Long-Term Maintenance & Version Audits | ⏳ | Ongoing |

---

## Phase Details

### Phase 1: Pipeline Conceptualization & Script Preparation
Establish the target specification models, mapping strategies, and write a robust acquisition script.

*   [x] **Target Identification**: Identify the exact board models, main MCU chips, and their standard documentation numbers (UM1724, RM0390, etc.) as detailed in `ALL_REF_DOC_CONCEPT.md`.
*   [x] **Acquisition Script Drafting**: Write `download_ref_docs.py` with custom User-Agent headers, polite delays (2-5 seconds) for rate-limiting, and error-handling routines.
*   [x] **Fictional Target Analysis**: Establish fallback logic for the private/fictional `Nucleo-C542RC` device to map its PDFs to STM32U5 Cortex-M33 equivalents or create text-based informational placeholders.

---

### Phase 2: Directory Schema Setup & Local Dry Runs
Prepare the local environment and verify all documentation URLs without triggering full PDF downloads.

*   [x] **Create Directory Hierarchy**: Initialize the structured folders under `specification/`:
    ```bash
    mkdir -p specification/pdfs/boards
    mkdir -p specification/pdfs/mcus
    ```
*   [x] **Dry Run HTTP HEAD Verification**: Write a Python validation test or run a bash script utilizing `curl -I` (or `requests.head()`) to check for HTTP `200 OK` status across all real target URLs.
*   [x] **Validate Fallback Behavior**: Dry-run the script with simulated network errors or missing targets to ensure it gracefully creates `stm32c542rc_placeholder.txt` or maps to the defined Cortex-M33 backup manuals.

---

### Phase 3: Automated Testing & Validation
Incorporate the document presence and mapping into the project's test suite.

*   [x] **Metadata Association Tests**: Write a test in `test/` to check that the YAML specifications (`specification/*.yaml`) contain accurate URL references or document IDs matching the downloaded files.
*   [ ] **PDF Integrity Verification**: (Optional/Post-Download) Implement basic binary checks to ensure downloaded `.pdf` files are not corrupt and are valid PDF files (e.g., matching the `%PDF-` magic header).
*   [ ] **Downloader Mocking**: Test the downloader script using mock URLs (e.g., via `unittest.mock` or a lightweight local HTTP server) to verify full-path downloads, timeouts, and rate-limiting behaviors.

---

### Phase 4: CLI Integration & CI Workflows
Make the download pipeline accessible to workshop participants and CI runners.

*   [ ] **Click CLI Command Integration**: Add a dedicated `--download-docs` command flag to the project's main CLI application to trigger the download sequence interactively.
*   [ ] **Workflow Action Cache**: Setup a GitHub Action or local caching configuration so that the downloaded PDFs (which are large static assets) are cached and not repeatedly re-downloaded on every minor CI build.
*   [ ] **Local Workshop Bundler**: Create a packaging script that zips `specification/pdfs/` into a single archive (`stm32_workshop_docs.zip`) for distribution to workshop attendees.

---

### Phase 5: Long-Term Maintenance & Version Audits
Handle the evolution of STMicroelectronics documentation.

*   [ ] **URL Refresh Script**: Implement a lightweight auditing script to detect broken URLs or newer document revisions (e.g., if UM1724 is upgraded to a newer revision).
*   [ ] **Fictional Board Review**: If a real STM32C5 series is ever officially released by STMicroelectronics, update the `specification/nucleo_c542rc.yaml` file and replace the Cortex-M33 fallbacks with the authentic datasheets and reference manuals.
*   [ ] **User Feedback Loop**: Allow workshop coordinators to log issues in `TECHNICAL_DEBTS.md` if specific chapters or documents are missing or if URLs require manual overrides.
