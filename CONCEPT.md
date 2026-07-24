# Concept: STM32 Workshop Microcontroller Comparison and Overview

This document outlines the conceptual structure, business cases, use cases, high-level architecture, and strategic architectural decisions for the STM32 Workshop Microcontroller Overview and Comparison project.

---

## 1. Goals & Scope

### 1.1 Goals
The main goal of this project is to provide a comprehensive overview and feature comparison of the STM32 microcontrollers in the workshop:
*   **Nucleo-F446RE** (High-Performance series, Cortex-M4 with FPU, 180 MHz, 512 KB Flash, 128 KB SRAM)
*   **Nucleo-C031C6** (Low-Cost/Entry-level series, Cortex-M0+, 48 MHz, 32 KB Flash, 12 KB SRAM)
*   **Nucleo-G431RB** (Mixed-Signal advanced series, Cortex-M4 with FPU, 170 MHz, 128 KB Flash, 32 KB SRAM)
*   **Nucleo-C542RC** (Advanced or low-power series, featuring specific peripheral layouts)

### 1.2 Scope
*   **Hardware Feature Specification**: Formalizing the hardware specifications, peripheral capabilities, electrical properties, and performance traits of the four targets.
*   **Automated Comparison**: Creating an extensible tool/system that compares these MCU features.
*   **Documentation Artifacts**: Generating rich documentation formats (e.g., Markdown comparison matrix, interactive diagrams, etc.) to assist developers, hardware engineers, and workshop instructors.

---

## 2. Business & Use Cases

### 2.1 Business Cases

*   **BC-1: Optimization of Workshop Material Costs**
    *   *Description*: The workshop hosts need to minimize cost per attendee while delivering appropriate MCU features for experiments.
    *   *Impact*: By comparing the ultra-low-cost `Nucleo-C031C6` with the advanced `Nucleo-F446RE` or `Nucleo-G431RB`, coordinators can assign simpler tasks (like basic UART, I2C, GPIO) to the cheapest board, reserving high-end boards only for DSP or high-speed analog processing.

*   **BC-2: Accelerated Project Prototyping & Hardware Tiering**
    *   *Description*: Engineering teams must decide which production MCU to choose based on prototyping outcomes.
    *   *Impact*: Having a clear, structured mapping of MCU capabilities helps transition projects smoothly from prototype boards to custom production boards of varying tiers without over-specifying hardware.

*   **BC-3: Workshop Curriculum Standardization**
    *   *Description*: Educational instructors need to design laboratory assignments that are compatible across multiple boards.
    *   *Impact*: Standardized feature mapping lets teachers write portable exercise libraries and identify which boards support specific exercises (e.g., DMA, ADC/DAC, PWM, CAN bus).

### 2.2 Use Cases

*   **UC-1: Query Board Specifications**
    *   *Actor*: Embedded Developer / Workshop Attendee
    *   *Flow*: The actor queries the system to retrieve detailed specification sheets for any of the four boards (e.g., Flash size, SRAM, maximum clock speed, and pinout options).

*   **UC-2: Compare Features Across Target MCUs**
    *   *Actor*: Developer / System Architect
    *   *Flow*: The actor selects two or more target boards and triggers a side-by-side comparison matrix. The system highlights differences in critical dimensions (e.g., core type, maximum frequency, floating-point support, analog-to-digital converters, and timers).

*   **UC-3: Recommend Board for Project Requirements**
    *   *Actor*: Embedded Developer / Student
    *   *Flow*: The actor inputs their project constraints (e.g., "Requires at least 64 KB RAM, FPU, and 2x I2C interfaces"). The system evaluates the available workshop boards and suggests the most optimal board that fits the constraints.

*   **UC-4: Export Comparison Reports**
    *   *Actor*: Workshop Instructor
    *   *Flow*: The actor triggers an export of the latest comparison tables to dynamic documentation formats (such as HTML or PDF reports) for embedding in course syllabus pages.

---

## 3. High-Level Architecture

The system follows a modular architectural pattern containing functional modules with distinct business interfaces.

```
+-------------------------------------------------------------+
|                     Business Interfaces                     |
|  [CLI User Interface]           [Documentation Generator]   |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                    Core Application Logic                   |
|                                                             |
|   +-------------------+             +-------------------+   |
|   |                   |             |                   |   |
|   |  Registry Engine  | ----------->| Comparison Engine |   |
|   |                   |             |                   |   |
|   +-------------------+             +-------------------+   |
|             ^                                 |             |
|             |                                 v             |
|   +-------------------+             +-------------------+   |
|   |                   |             |                   |   |
|   |  Data Repository  |             | Recommendation    |   |
|   |                   |             | Engine            |   |
|   +-------------------+             +-------------------+   |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                      Storage & Assets                       |
|   [Spec Datastore (YAML/JSON)]      [Rendered Assets (MD)]  |
+-------------------------------------------------------------+
```

### 3.1 Functional Components

*   **Data Repository**: Loads, parses, and validates the hardware specifications of the Nucleo boards from static definition files.
*   **Registry Engine**: Provides search and query capabilities for individual boards. It acts as the single source of truth for all device metadata.
*   **Comparison Engine**: Processes multiple board specifications, aligns their peripheral counts and memory dimensions, and computes a detailed difference matrix.
*   **Recommendation Engine**: Executes constraint-based matching logic to recommend the ideal MCU based on user inputs.
*   **Business Interfaces**:
    *   *CLI Interface*: Command-line utility for interactive queries, comparison, and recommendation workflows.
    *   *Documentation Generator / Exporter*: Automates outputting comparative tables to Markdown or static HTML files.

---

## 4. Architectural Alternatives & Decisions

### 4.1 Decision 1: Feature Comparison Strategy
How should the comparison matrix and data alignment be managed?

*   **Alternative A: Static Markdown/Table Matrix**
    *   *Description*: Manually maintain a comprehensive comparison table in a markdown document.
    *   *Pros*: Zero development overhead, easily readable by humans directly on GitHub.
    *   *Cons*: Prone to human error when updating features, lacks flexibility to filter or programmatically query.
*   **Alternative B: Schema-Driven Specification Comparison (Selected)**
    *   *Description*: Maintain structured specification files (e.g., YAML/JSON) per MCU model, and write a light-weight Comparison Engine that processes them to dynamically generate tables.
    *   *Pros*: High flexibility, single source of truth per board, easily extensible when adding new boards, programmatically queryable.
    *   *Cons*: Requires upfront design of the metadata schema and an implementation of a generator.
*   **Alternative C: Relational SQL Database Comparison**
    *   *Description*: Store all board parameters in relational database tables (e.g., PostgreSQL/SQLite) and perform SQL joins or queries to build comparisons.
    *   *Pros*: Scalable to thousands of boards, supports complex relational queries.
    *   *Cons*: Overkill for a local workshop of 4 boards; adds unnecessary database setup and maintenance overhead.

### 4.2 Decision 2: Hardware Specification Metadata Format
What format should be used to model the metadata of the MCU boards?

*   **Alternative A: Hardcoded Software Objects**
    *   *Description*: Define hardware capabilities directly inside the source code (e.g., Python dictionaries or Rust structures).
    *   *Pros*: Simple compilation/packaging; no external file parsing required.
    *   *Cons*: Highly coupled; changes to board specifications require modifying code and rebuilding the application.
*   **Alternative B: YAML Specification Schema (Selected)**
    *   *Description*: Store each board's specification in a separate YAML file matching a standardized, validated schema.
    *   *Pros*: Easily readable and editable by non-programmers, widely used in the embedded community (similar to SVD or device tree syntax).
    *   *Cons*: Requires a parser and schema validator to prevent typos.
*   **Alternative C: XML Schema (e.g., SVD files)**
    *   *Description*: Directly parse System View Description (SVD) files from STMicroelectronics.
    *   *Pros*: Extremely detailed, standardized industry format.
    *   *Cons*: SVDs are designed for register-level debugging and are highly verbose, making high-level feature comparison (like board pins or physical costs) difficult to extract.

### 4.3 Decision 3: High-Level Application Architecture
What is the best medium to deliver this comparison tool to the workshop users?

*   **Alternative A: Command-Line Interface (CLI) & Build Artifact (Selected)**
    *   *Description*: Build a lightweight CLI application that can run locally or during automated CI/CD workflows to output the Markdown tables.
    *   *Pros*: Fast, easily integrates with GitHub Actions, works offline, no server hosting costs.
    *   *Cons*: Lacks graphical interactivity out-of-the-box.
*   **Alternative B: Interactive Single-Page Web Application (SPA)**
    *   *Description*: Build a React or Vue web application where users can interactively check boxes to compare MCU boards.
    *   *Pros*: Best user experience, visually engaging.
    *   *Cons*: Requires hosting, increases tech stack complexity, longer development cycles.
*   **Alternative C: Serverless Static Site (e.g., GitHub Pages)**
    *   *Description*: Compile the comparison data into static HTML files during CI and host them directly on GitHub Pages.
    *   *Pros*: Combines the ease of a web interface with zero-cost hosting and low maintenance.
    *   *Cons*: Requires configuring CI actions and dealing with deployment lag.

---

## 5. Summary of Alternatives and Discarded Options

### 5.1 Chosen Technologies and Paradigms
*   **Specification Format**: YAML files (`/specification/*.yaml`) matching a strictly enforced schema.
*   **Core Application**: Command-Line Interface (CLI) utility written in Python or Node.js to read specifications, validate them, and perform dynamic comparison or recommendations.
*   **Output Channels**: Automated generation of static comparison tables in Markdown format, embedded within documentation pages, ensuring simple viewing directly in git repositories or static page viewers.

### 5.2 Discarded Alternatives

| Decision Dimension | Discarded Alternative | Reason for Rejection |
| :--- | :--- | :--- |
| **Feature Comparison Strategy** | Static Markdown Matrix | Too rigid; hard to extend dynamically or query automatically for constraints. |
| **Feature Comparison Strategy** | Relational SQL DB | High operational complexity for a small, specialized dataset. |
| **Hardware Metadata Format** | Hardcoded Software Objects | Strongly couples data to code, limiting community contributions. |
| **Hardware Metadata Format** | XML/SVD Schema | Overly verbose, register-level focus rather than high-level overview. |
| **Application Architecture** | Dedicated Web SPA | Adds unnecessary hosting costs, deployment overhead, and tech stack complexity. |
| **Application Architecture** | Static manual site | Lacks interactive query features for recommendations. |
