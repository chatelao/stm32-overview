# STM32 Workshop Microcontroller Overview and Comparison

This repository provides a comprehensive overview and feature comparison of specific STM32 microcontrollers used in our workshop:
- **Nucleo-F446RE**
- **Nucleo-C031C6**
- **Nucleo-G431RB**
- **Nucleo-C542RC**

The goal is to support decision-making, hardware tiering, workshop curricula standardization, and constraint-based board recommendations.

## Documentation

The full documentation is published and hosted on ReadTheDocs:
👉 **[STM32 Workshop Comparison Documentation (ReadTheDocs)](https://stm32-overview.readthedocs.io/)**

## Directory Structure

- `/docs/` - Source markdown files for the documentation site.
- `/specification/` - YAML specification configurations representing each board's hardware limits, memories, electrical specs, and documentation metadata paths.
- `/src/` - The CLI application source code (built with Pydantic and Click).
- `/test/` - Unit tests for verifying schemas, downloader utility, comparison/recommendation engine correctness, and metadata association.

## Quick Start / Usage

To set up the environment and run the CLI:

1. **Install dependencies**:
   ```bash
   bash src/install.sh
   bash test/install.sh
   ```

2. **Run the CLI**:
   ```bash
   # List all registered boards
   python3 src/main.py list

   # Show detailed info for a board
   python3 src/main.py show --board Nucleo-F446RE

   # Compare boards
   python3 src/main.py compare -b Nucleo-F446RE -b Nucleo-C031C6

   # Get a recommendation based on criteria
   python3 src/main.py recommend --flash 64 --sram 16 --fpu
   ```

3. **Run unit tests**:
   ```bash
   python3 -m pytest
   ```
