#!/usr/bin/env python3
"""
download_ref_docs.py
A robust helper utility to automate reference documentation downloading,
with support for HEAD validation (dry runs) and fallback handling.
"""

import os
import sys
import time
import urllib.request
import urllib.error

# User-Agent to avoid getting blocked by CDNs
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


def check_url_head(url, timeout=10):
    """
    Performs an HTTP HEAD request to verify url availability.
    Returns (status_code, reason/error_msg)
    """
    req = urllib.request.Request(url, method='HEAD', headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, "OK"
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)
    except urllib.error.URLError as e:
        return None, f"Connection Failed: {e.reason}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def download_file(url, dest, is_fallback=False, dry_run=False, timeout=10):
    """
    Downloads the file from url to dest, or runs HEAD check if dry_run=True.
    In case of failure on a fallback, writes a placeholder text file.
    """
    if dry_run:
        print(f"[DRY-RUN] Verifying URL: {url} -> {dest}")
        status, message = check_url_head(url, timeout=timeout)
        if status == 200:
            print(f" -> Available (HTTP 200)")
            return True
        else:
            print(f" -> Unavailable/Error: {status} ({message})")
            if is_fallback:
                print(" -> Note: This is a fallback/placeholder mapping for the custom/fictional STM32C542RC series.")
            return False

    print(f"Downloading: {url} -> {dest}")
    if is_fallback:
        print(" -> Note: This is a fallback/placeholder mapping for the custom/fictional STM32C542RC series.")

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            with open(dest, 'wb') as out_file:
                out_file.write(content)
        print(" -> Success!")
        return True
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
        return False
    except Exception as e:
        print(f" -> Unexpected Error: {e}")
        if is_fallback:
            txt_dest = dest.replace('.pdf', '_placeholder.txt')
            with open(txt_dest, 'w') as f:
                f.write(f"Placeholder for custom/fictional STM32C542RC device manual.\n")
                f.write(f"Attempted to fetch fallback: {url}\n")
                f.write(f"Result: Unexpected Error - {str(e)}\n")
            print(f" -> Created descriptive placeholder file at {txt_dest}")
        return False


def main(args):
    dry_run = "--dry-run" in args
    print(f"Starting planned reference documentation acquisition process (dry_run={dry_run})...")

    success_count = 0
    total_count = len(DOWNLOAD_TARGETS)

    for target in DOWNLOAD_TARGETS:
        success = download_file(
            target["url"],
            target["dest"],
            is_fallback=target.get("is_fallback", False),
            dry_run=dry_run
        )
        if success:
            success_count += 1

        # Polite rate-limiting delay during real runs or dry runs if network is hit
        if not dry_run or success:
            time.sleep(2)

    print(f"Completed! {success_count}/{total_count} operations succeeded.")
    if success_count < total_count:
         # In non-dry-run mode, fallbacks might fail and create placeholders, which is accepted
         print("Some targets failed or were mapped to placeholders.")


if __name__ == "__main__":
    main(sys.argv[1:])
