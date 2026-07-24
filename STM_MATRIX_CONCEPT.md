# Concept: STM32 Workshop Microcontroller Comparison (STM_MATRIX)

This document outlines the conceptual structure, business cases, use cases, high-level architecture, and strategic architectural decisions for the STM32 Workshop Microcontroller Overview and Comparison project, also referred to as the STM Matrix.

---

## 1. Goals & Scope

### 1.1 Goals
The main goal of this project is to provide a comprehensive overview and feature comparison of the specific STM32 microcontrollers in our workshop:
*   **Nucleo-F446RE**: High-Performance series (Cortex-M4 with FPU, 180 MHz, 512 KB Flash, 128 KB SRAM)
*   **Nucleo-C031C6**: Low-Cost/Entry-level series (Cortex-M0+, 48 MHz, 32 KB Flash, 12 KB SRAM)
*   **Nucleo-G431RB**: Mixed-Signal advanced series (Cortex-M4 with FPU, 170 MHz, 128 KB Flash, 32 KB SRAM)
*   **Nucleo-C542RC**: Advanced or low-power series featuring specific peripheral layouts

The tool must facilitate clear identification of the target MCUs' capabilities, allowing developers, workshop attendees, and instructors to easily query, compare, and get recommendations based on project constraints.

### 1.2 Scope
*   **Hardware Feature Specification**: Formalizing the hardware specifications, peripheral capabilities, electrical properties, and performance traits of the four target boards.
*   **Automated Comparison**: Creating an extensible comparison engine that processes the specification files to generate structured comparative matrices.
*   **Constraint-Based Recommendation**: Designing a module to map target board features against user requirements (e.g., RAM size, specific peripheral availability, performance constraints).
*   **Documentation Artifacts**: Emitting clean Markdown tables and detailed specification sheets that can be embedded into workshop curriculum portals or viewed directly on Git hosting services.

---

## 2. Business & Use Cases

### 2.1 Business Cases

*   **BC-1: Optimization of Workshop Material Costs**
    *   *Description*: Workshop coordinators must manage budgets while ensuring students have access to hardware with adequate features for course labs.
    *   *Impact*: By providing a direct comparison between low-cost boards (like the `Nucleo-C031C6`) and high-performance options (such as the `Nucleo-F446RE`), instructors can select the minimum viable board for general-purpose tasks, saving high-end hardware for advanced DSP or high-speed analog exercises.

*   **BC-2: Accelerated Project Prototyping and Hardware Selection**
    *   *Description*: Embedded developers must select the right-sized MCU to move from early prototyping to final product design.
    *   *Impact*: A standardized comparison allows quick mapping of prototype firmware requirements to target production-grade chips, avoiding the common pitfall of over-specifying (and over-paying for) unused MCU capabilities.

*   **BC-3: Workshop Curriculum Portability and Standardization**
    *   *Description*: Teachers and lab developers must design portable exercises that run on multiple boards with minimal driver changes.
    *   *Impact*: Standardized peripheral mappings help instructors identify standard API subsets (e.g., standard I2C, SPI, UART, or ADC limits) that are supported across all four models, enabling write-once-run-anywhere code sheets for student labs.

### 2.2 Use Cases

*   **UC-1: Query Board Specifications**
    *   *Actor*: Embedded Developer / Workshop Attendee
    *   *Flow*: The actor queries the registry for a single target (e.g., `Nucleo-G431RB`) to view its specifications, clock speeds, memory, and pin constraints.

*   **UC-2: Side-by-Side Board Comparison**
    *   *Actor*: Embedded Developer / Architect
    *   *Flow*: The actor selects multiple target boards (e.g., `Nucleo-F446RE` vs. `Nucleo-C031C6`) and triggers the comparison tool. The system highlights differing dimensions such as core architecture, DMA channel count, FPU support, and ADC resolution.

*   **UC-3: Project-Driven Board Recommendation**
    *   *Actor*: Student / Developer
    *   *Flow*: The actor inputs desired constraints (e.g., "Requires 64 KB RAM, FPU support, and at least 2 hardware UART ports"). The system evaluates the candidate boards and recommends the most resource-efficient and cost-effective matches.

*   **UC-4: Export Generated Documentation Reports**
    *   *Actor*: Workshop Instructor
    *   *Flow*: The instructor runs the documentation generation utility to output updated markdown tables into the project docs folder or website hosting pipeline, guaranteeing that the public documentation is always synchronized with the underlying specifications.

---

## 3. High-Level Architecture

The system is structured as a decoupled architecture consisting of core logic modules and multi-channel business interfaces, operating on structured specification schemas.

```
+-----------------------------------------------------------------+
|                      Business Interfaces                        |
|   +--------------------------+     +------------------------+   |
|   |  CLI User Interface      |     |  Docs Generator Engine |   |
|   +--------------------------+     +------------------------+   |
+-----------------------------------------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                     Core Application Logic                      |
|                                                                 |
|   +--------------------------+     +------------------------+   |
|   |  Registry Engine         | --> |  Comparison Engine     |   |
|   |  (Loads & Index Specs)   |     |  (Builds Diff Matrix)  |   |
|   +--------------------------+     +------------------------+   |
|                 ^                               |               |
|                 |                               v               |
|   +--------------------------+     +------------------------+   |
|   |  Data Repository         |     |  Recommendation Engine |   |
|   |  (Validates Schema)      |     |  (Evaluates Filters)   |   |
|   +--------------------------+     +------------------------+   |
+-----------------------------------------------------------------+
                                 |
                                 v
+-----------------------------------------------------------------+
|                       Storage & Assets                          |
|   [Spec Datastore (YAML files)]     [Rendered Markdown Assets]  |
+-----------------------------------------------------------------+
```

### 3.1 Functional Components

*   **Data Repository**: Loads the MCU board specification definitions from local storage and ensures they adhere to the strictly defined, validated schema structure.
*   **Registry Engine**: Provides indexing and search operations. It exposes APIs to retrieve board-specific capability maps by identifier.
*   **Comparison Engine**: Processes specified lists of board definitions, aligns physical and virtual parameters (such as clock speeds, peripheral counts, memory structures), and produces a synchronized matrix.
*   **Recommendation Engine**: Implements matching algorithms to filter the registered boards against technical constraints, ordering candidates by cost/resource-efficiency.
*   **Business Interfaces**:
    *   *CLI Interface*: Provides developers and students with a command-line portal to interactively query specifications, run comparisons, and obtain recommendation choices.
    *   *Documentation Generator / Exporter*: Automates compiling specification files into highly-readable static Markdown tables to keep project documentation automatically up-to-date.

---

## 4. Architectural Alternatives & Decisions

To establish a solid, maintainable foundation, three major architectural decisions were evaluated, comparing three distinct alternatives for each choice.

### 4.1 Decision 1: Feature Comparison Strategy
How should board capability comparisons be maintained and aligned?

*   **Alternative A: Manual Static Markdown Tables**
    *   *Description*: Maintain the feature matrix manually within documentation files using GitHub-Flavored Markdown tables.
    *   *Pros*: Zero development overhead; easy to read directly in GitHub out-of-the-box.
    *   *Cons*: Extremely error-prone, hard to keep synchronized across different files, and lacks capability for dynamic query filtering or automated recommendation.
*   **Alternative B: Schema-Driven Dynamic Comparison (Selected)**
    *   *Description*: Define structured metadata files (YAML format) for each board, and implement a lightweight engine to dynamically compile comparative matrices.
    *   *Pros*: Single source of truth per board, easily extensible with new boards, programmatically queryable, supports automated document compilation.
    *   *Cons*: Requires initial development of a comparison compiler and metadata schema.
*   **Alternative C: Relational SQL Database Storage**
    *   *Description*: Import board parameters into localized SQL databases (such as SQLite) and use relational queries to align and compare models.
    *   *Pros*: Highly scalable to thousands of boards, robust querying options.
    *   *Cons*: Overkill for a local workshop containing four target boards; introduces unnecessary hosting, drivers, and runtime dependencies.

### 4.2 Decision 2: Hardware Metadata Format
What structural format should be chosen for storing target board feature metrics?

*   **Alternative A: Hardcoded Software Variables**
    *   *Description*: Directly hardcode all board specifications as native code objects (e.g., Python dictionaries or Rust structures).
    *   *Pros*: Simplified packaging; no external parser or file system reads required at runtime.
    *   *Cons*: Data is tightly coupled with executable code. Non-developers cannot easily suggest fixes or add new specifications without rebuilding and redeploying the CLI utility.
*   **Alternative B: YAML Specification Schema (Selected)**
    *   *Description*: Store individual board definitions as standalone YAML files under a dedicated folder, verified by a JSON/YAML schema.
    *   *Pros*: Highly readable and editable by hardware engineers and students, native support for nested configurations (e.g., specific pin/peripheral counts), widely used in embedded build toolchains.
    *   *Cons*: Requires a parsing and validation library at runtime to protect against formatting mistakes.
*   **Alternative C: XML Schema (SVD / System View Description)**
    *   *Description*: Parse System View Description (SVD) files directly supplied by STMicroelectronics.
    *   *Pros*: Extremely fine-grained specification of register layouts and peripheral architectures.
    *   *Cons*: SVD files are highly verbose and focus on low-level registers rather than high-level comparison metrics (e.g., pinout availability, cost, user-facing physical features).

### 4.3 Decision 3: Application Architecture and Delivery Medium
What is the best delivery mechanism for making these comparison tools available to developers and learners?

*   **Alternative A: Command-Line Interface (CLI) & Build Artifact (Selected)**
    *   *Description*: Package the registry, comparison, and validation core into a lightweight CLI executable.
    *   *Pros*: Highly performant, runs locally without network dependencies, easily integrates into CI/CD build scripts to compile documentation.
    *   *Cons*: Lacks graphical styling and real-time interactive UI controls.
*   **Alternative B: Interactive Single-Page Application (SPA)**
    *   *Description*: Build a front-end framework application (e.g., React or Vue) to compare boards interactively.
    *   *Pros*: Elegant user experience with interactive slider filters and graphical board layouts.
    *   *Cons*: Substantially higher complexity, long-term maintenance overhead, and hosting infrastructure requirements.
*   **Alternative C: Serverless static website (e.g., GitHub Pages)**
    *   *Description*: Host compiled static HTML tables and comparison charts, generated during GitHub Action CI workflows.
    *   *Pros*: No hosting costs, minimal server maintenance, accessible from any web browser.
    *   *Cons*: No support for real-time local interactive querying without loading complex clients, and updates suffer deployment latency.

---

## 5. Summary of Alternatives and Discarded Options

### 5.1 Chosen Technologies and Paradigms
*   **Specification Format**: Standardized YAML definitions stored under `/specification/*.yaml`.
*   **Application Core**: Extensible CLI engine that handles board registry, schema validation, comparison matching, and recommendation calculations.
*   **Output Channels**: Markdown comparison pages dynamically compiled and stored within the repository docs directory for direct consumption, combined with CLI console outputs.

### 5.2 Discarded Alternatives

| Decision Dimension | Discarded Alternative | Reason for Rejection |
| :--- | :--- | :--- |
| **Feature Comparison Strategy** | Static Markdown Matrix | High manual editing error rate; fails to provide interactive search or dynamic recommendation. |
| **Feature Comparison Strategy** | Relational SQL DB | Unjustified architectural complexity and setup overhead for small datasets. |
| **Hardware Metadata Format** | Hardcoded Software Objects | Strongly couples hardware specifications with codebase, restricting documentation updates by non-programmers. |
| **Hardware Metadata Format** | XML/SVD Schema | Overly granular focus on hardware registers rather than high-level physical board features. |
| **Application Architecture** | Dedicated Web SPA | Unnecessary deployment overhead, web design effort, and hosting infrastructure maintenance. |
| **Application Architecture** | Serverless static site | High latency to update, complex pipeline required, lack of offline CLI usage for developers. |
