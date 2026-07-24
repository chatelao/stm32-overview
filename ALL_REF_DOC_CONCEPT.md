# Concept: Reference and User Manual PDF Downloads for STM32 Workshop Boards

This document outlines the concept, directory structure, identification of targets, and a systematic download plan for fetching all relevant reference and user manual PDFs for each board and its main MCU.

---

## 1. Objectives

* **Offline Capability**: Provide workshop attendees and developers with offline-accessible documentation.
* **Organized Repository**: Store the documents in a structured schema under `specification/pdfs/` to easily map them to specification YAML files.
* **Automated & Safe Acquisition**: Ensure the downloading process uses robust scripting featuring rate-limiting, retries, proper user-agent headers, and error handling for missing/fictional targets.
* **No Immediate Execution**: Plan and structure the downloads without running them now.

---

## 2. Directory Structure

All downloaded assets will reside within `specification/pdfs/`, organized logically to distinguish between Board-level User Manuals and MCU-level Technical Documents (Datasheets & Reference Manuals):

```
specification/
├── pdfs/
│   ├── boards/
│   │   ├── nucleo_f446re_user_manual.pdf
│   │   ├── nucleo_c031c6_user_manual.pdf
│   │   ├── nucleo_g431rb_user_manual.pdf
│   │   └── nucleo_c542rc_user_manual.pdf (Placeholder / Fallback)
│   └── mcus/
│       ├── stm32f446re_datasheet.pdf
│       ├── stm32f446re_reference_manual.pdf
│       ├── stm32c031c6_datasheet.pdf
│       ├── stm32c031c6_reference_manual.pdf
│       ├── stm32g431rb_datasheet.pdf
│       ├── stm32g431rb_reference_manual.pdf
│       ├── stm32c542rc_datasheet.pdf (Placeholder / Fallback)
│       └── stm32c542rc_reference_manual.pdf (Placeholder / Fallback)
```

---

## 3. Document Identification & Target URLs

### 3.1 Nucleo-F446RE (MCU: STM32F446RET6)
* **Board User Manual**: UM1724 (*STM32 Nucleo-64 boards (MB1136)*)
  * Target URL: `https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf`
* **MCU Datasheet**: *STM32F446xC/E datasheet*
  * Target URL: `https://www.st.com/resource/en/datasheet/stm32f446re.pdf`
* **MCU Reference Manual**: RM0390 (*STM32F446xx advanced Arm®-based 32-bit MCUs*)
  * Target URL: `https://www.st.com/resource/en/reference_manual/rm0390-stm32f446xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf`

### 3.2 Nucleo-C031C6 (MCU: STM32C031C6T6)
* **Board User Manual**: UM2953 (*STM32 Nucleo-64 board (MB1717)*)
  * Target URL: `https://www.st.com/resource/en/user_manual/um2953-stm32-nucleo64-board-mb1717-stmicroelectronics.pdf`
* **MCU Datasheet**: *STM32C031x4/x6 datasheet*
  * Target URL: `https://www.st.com/resource/en/datasheet/stm32c031c6.pdf`
* **MCU Reference Manual**: RM0490 (*STM32C0x1 advanced Arm®-based 32-bit MCUs*)
  * Target URL: `https://www.st.com/resource/en/reference_manual/rm0490-stm32c0x1-advanced-armbased-32bit-mcus-stmicroelectronics.pdf`

### 3.3 Nucleo-G431RB (MCU: STM32G431RBT6)
* **Board User Manual**: UM2505 (*STM32 Nucleo-64 board (MB1367)*)
  * Target URL: `https://www.st.com/resource/en/user_manual/um2505-stm32-nucleo64-board-mb1367-stmicroelectronics.pdf`
* **MCU Datasheet**: *STM32G431xx datasheet*
  * Target URL: `https://www.st.com/resource/en/datasheet/stm32g431rb.pdf`
* **MCU Reference Manual**: RM0440 (*STM32G4 Series advanced Arm®-based 32-bit MCUs*)
  * Target URL: `https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf`

### 3.4 Nucleo-C542RC (MCU: STM32C542RC)
* **Fictional / Private Target Analysis**:
  * The `STM32C5` or `STM32C542RC` does not exist in standard STMicroelectronics catalog databases. It likely represents a fictional design, a highly customized private specification, or a typo of another line (e.g., STM32U542 or STM32H542).
  * **Fallback Handling Plan**:
    1. During the automated download phase, the script will attempt to probe official and mirror sources for any matching custom datasheet/manual.
    2. If unavailable (as expected), the script will map the downloads to fallback placeholder documents (such as general STM32 Cortex-M33 reference documents like RM0456 for STM32U5 series, or place a descriptive placeholder text file `stm32c542rc_placeholder.txt` detailing the fictional nature of this board).
    3. Suggested Mapping Fallbacks:
       * *Cortex-M33 Board User Manual*: UM2861 (*STM32 Nucleo-144 board MB1363 for STM32U5 series*)
         * URL: `https://www.st.com/resource/en/user_manual/um2861-stm32-nucleo144-board-mb1363-stmicroelectronics.pdf`
       * *Cortex-M33 MCU Datasheet (STM32U542)*:
         * URL: `https://www.st.com/resource/en/datasheet/stm32u542xx.pdf`
       * *Cortex-M33 MCU Reference Manual (RM0456)*:
         * URL: `https://www.st.com/resource/en/reference_manual/rm0456-stm32u5-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf`

---

## 4. Execution Steps for the Download

To execute the download in a stable, predictable fashion when requested:

1. **Step 1: Setup Directories**
   * Create the parent and child directories:
     `mkdir -p specification/pdfs/boards specification/pdfs/mcus`
2. **Step 2: Dry Run & URL Verification**
   * Verify all listed URLs via standard HTTP HEAD requests using `curl -I` or Python's `requests.head()` to check availability.
3. **Step 3: Execute Downloading with Rate-Limiting and User-Agents**
   * STMicroelectronics websites may block automated scrapers using basic `wget` user-agents.
   * Downloads must include custom headers (e.g., `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)`) and introduce a polite delay of 2-5 seconds between downloads.
4. **Step 4: Handle Missing/Unsupported Documents (e.g., Nucleo-C542RC)**
   * Detect HTTP 404 errors.
   * If a document is missing, apply the mapping fallback described in Section 3.4 or write a clear informational text/JSON document at the target path indicating the status.

---

## 5. Download Automation Script (Ready-to-Run)

Below is a complete Python-based download automation utility. This script is fully prepared to run but **should not be executed yet** (as per current instructions).

```python
#!/usr/bin/env python3
"""
download_ref_docs.py
A robust helper utility to automate reference documentation downloading.
"""

import os
import time
import urllib.request
import urllib.error

# User-Agent to avoid getting blocked by STMicroelectronics CDNs
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

DOWNLOAD_TARGETS = [
    # Nucleo-F446RE
    {
        "url": "https://www.st.com/resource/en/user_manual/um1724-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf",
        "dest": "specification/pdfs/boards/nucleo_f446re_user_manual.pdf"
    },
    {
        "url": "https://www.st.com/resource/en/datasheet/stm32f446re.pdf",
        "dest": "specification/pdfs/mcus/stm32f446re_datasheet.pdf"
    },
    {
        "url": "https://www.st.com/resource/en/reference_manual/rm0390-stm32f446xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf",
        "dest": "specification/pdfs/mcus/stm32f446re_reference_manual.pdf"
    },
    # Nucleo-C031C6
    {
        "url": "https://www.st.com/resource/en/user_manual/um2953-stm32-nucleo64-board-mb1717-stmicroelectronics.pdf",
        "dest": "specification/pdfs/boards/nucleo_c031c6_user_manual.pdf"
    },
    {
        "url": "https://www.st.com/resource/en/datasheet/stm32c031c6.pdf",
        "dest": "specification/pdfs/mcus/stm32c031c6_datasheet.pdf"
    },
    {
        "url": "https://www.st.com/resource/en/reference_manual/rm0490-stm32c0x1-advanced-armbased-32bit-mcus-stmicroelectronics.pdf",
        "dest": "specification/pdfs/mcus/stm32c031c6_reference_manual.pdf"
    },
    # Nucleo-G431RB
    {
        "url": "https://www.st.com/resource/en/user_manual/um2505-stm32-nucleo64-board-mb1367-stmicroelectronics.pdf",
        "dest": "specification/pdfs/boards/nucleo_g431rb_user_manual.pdf"
    },
    {
        "url": "https://www.st.com/resource/en/datasheet/stm32g431rb.pdf",
        "dest": "specification/pdfs/mcus/stm32g431rb_datasheet.pdf"
    },
    {
        "url": "https://www.st.com/resource/en/reference_manual/rm0440-stm32g4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf",
        "dest": "specification/pdfs/mcus/stm32g431rb_reference_manual.pdf"
    },
    # Nucleo-C542RC (Hypothetical / Fictional - Mapped to U5 / Cortex-M33 equivalent placeholders)
    {
        "url": "https://www.st.com/resource/en/user_manual/um2861-stm32-nucleo144-board-mb1363-stmicroelectronics.pdf",
        "dest": "specification/pdfs/boards/nucleo_c542rc_user_manual.pdf",
        "is_fallback": True
    },
    {
        "url": "https://www.st.com/resource/en/datasheet/stm32u542xx.pdf",
        "dest": "specification/pdfs/mcus/stm32c542rc_datasheet.pdf",
        "is_fallback": True
    },
    {
        "url": "https://www.st.com/resource/en/reference_manual/rm0456-stm32u5-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf",
        "dest": "specification/pdfs/mcus/stm32c542rc_reference_manual.pdf",
        "is_fallback": True
    }
]

def download_file(url, dest, is_fallback=False):
    print(f"Downloading: {url} -> {dest}")
    if is_fallback:
        print(" -> Note: This is a fallback/placeholder mapping for the custom/fictional STM32C542RC series.")

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
            out_file.write(response.read())
        print(" -> Success!")
    except urllib.error.HTTPError as e:
        print(f" -> Failed (HTTP {e.code}): {e.reason}")
        if is_fallback:
            # Create a localized placeholder info file instead
            txt_dest = dest.replace('.pdf', '_placeholder.txt')
            with open(txt_dest, 'w') as f:
                f.write(f"Placeholder for custom/fictional STM32C542RC device manual.\n")
                f.write(f"Attempted to fetch fallback: {url}\n")
                f.write(f"Result: HTTP Error {e.code} - {e.reason}\n")
            print(f" -> Created descriptive placeholder file at {txt_dest}")
    except Exception as e:
        print(f" -> Unexpected Error: {e}")

def main():
    print("Starting planned reference documentation acquisition process...")
    for target in DOWNLOAD_TARGETS:
        download_file(target["url"], target["dest"], target.get("is_fallback", False))
        # Polite rate-limiting delay
        time.sleep(3)

if __name__ == "__main__":
    # To run this script when explicitly requested, uncomment the line below or run via command line
    # main()
    print("Plan only mode: Script has been compiled but execution is not triggered yet.")
```
