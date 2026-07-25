# Project Roadmap

This document outlines the milestones, goals, and phases for the STM32 Workshop Microcontroller Comparison and Overview project. The roadmap is designed to support parallelized development by specifying interfaces first, followed by functional implementation.

---

## Progress Overview

| Phase | Description | Status |
| :--- | :--- | :--- |
| **Phase 1** | Project Initiation, Conceptualization, and Design | ✅ |
| **Phase 2** | Specification Schemas & MCU Data Repository | ✅ |
| **Phase 3** | Core Engine Interfaces & Implementations | ✅ |
| **Phase 4** | Command-Line Interface (CLI) & Exporter | ✅ |
| **Phase 5** | Continuous Integration, Documentation, & RTD Setup | ✅ |

---

## Goals

*   **Goal 1**: Establish a unified, validated YAML specification schema for workshop microcontrollers. ✅
*   **Goal 2**: Develop a robust core comparison and recommendation engine in Python. ✅
*   **Goal 3**: Build a user-friendly CLI to query, compare, and get board recommendations. ✅
*   **Goal 4**: Automate documentation generation (Markdown) and host it via ReadTheDocs. ✅

---

## Phases

### Phase 1: Project Initiation, Conceptualization, and Design
Focuses on defining goals, specifying system architecture, and drafting the project's conceptual foundation.

*   [x] Define target microcontrollers: Nucleo-F446RE, Nucleo-C031C6, Nucleo-G431RB, Nucleo-C542RC.
*   [x] Formulate high-level use cases and business cases (`CONCEPT.md`).
*   [x] Design technological stack, technical component interfaces, and database entities (`DESIGN.md`).
*   [x] Create and integrate top-level architecture PlantUML diagram.
*   [x] Establish development roadmap and progress metrics (`ROADMAP.md`).

### Phase 2: Specification Schemas & MCU Data Repository
Defines data structures and captures MCU-specific details in static YAML files.

*   [x] Define and implement Pydantic validation schema matching the design specification.
*   [x] Create individual board specification profiles under `/specification/`:
    *   [x] `specification/nucleo_f446re.yaml`
    *   [x] `specification/nucleo_c031c6.yaml`
    *   [x] `specification/nucleo_g431rb.yaml`
    *   [x] `specification/nucleo_c542rc.yaml`
*   [x] Set up local installation scripts (`src/install.sh` and `test/install.sh`).
*   [x] Implement the `DataRepository` interface to load, parse, and validate YAML files.

### Phase 3: Core Engine Interfaces & Implementations
Implements the core business logic. All components must define clean interfaces before implementing internal logic to support parallel development.

*   **Registry & Comparison Engines**
    *   [x] Define the python type-hinted interface for `RegistryEngine`.
    *   [x] Define the python type-hinted interface for `ComparisonEngine`.
    *   [x] Implement `RegistryEngine` to query single sources of truth.
    *   [x] Implement `ComparisonEngine` to compute differences and align optional features.
*   **Recommendation & Generation Engines**
    *   [x] Define the constraint structures and interfaces for `RecommendationEngine`.
    *   [x] Define the exporting interfaces for `DocGenerator`.
    *   [x] Implement `RecommendationEngine` using constraint-matching logic and scoring.
    *   [x] Implement `DocGenerator` to convert comparison results to standard Markdown tables.

### Phase 4: Command-Line Interface (CLI) & Exporter
Builds the user-facing CLI utility allowing direct interaction with the engines.

*   [x] Setup CLI commands structure (`list`, `show`, `compare`, `recommend`, `export`) using the Click framework.
*   [x] Connect CLI argument parser to corresponding core engines (Registry, Comparison, Recommendation).
*   [x] Implement validation logic for user CLI inputs (e.g., verifying board names exist).
*   [x] Integrate markdown exporting to automatically update the project comparison tables.

### Phase 5: Continuous Integration, Documentation, & RTD Setup
Ensures the software is robust, tested, and automatically deployed.

*   [x] Write unit tests for Pydantic validation, core engines, and CLI command outputs. [Completed: 2025-02-18]
*   [x] Setup an empty GitHub Action workflow to automate tests on every branch. [Completed: 2025-02-18]
*   [x] Integrate coverage reporting and caching into the CI/CD pipeline. [Completed: 2025-02-18]
*   [x] Configure `ReadTheDocs` (.readthedocs.yaml) for publishing project documentation compiled from the main branch. [Completed: 2025-02-18]
*   [x] Log outstanding issues and non-critical technical observations in `TECHNICAL_DEBTS.md`. [Completed: 2025-02-18]
