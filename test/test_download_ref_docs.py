import os
import tempfile
import urllib.request
import urllib.error
from unittest import mock
import pytest

from src.download_ref_docs import check_url_head, download_file, main, DOWNLOAD_TARGETS, is_valid_pdf


def test_is_valid_pdf_non_existent():
    assert is_valid_pdf("non_existent_file.pdf") is False


def test_is_valid_pdf_valid_magic_header():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"%PDF-1.4\nsome content")
        filepath = f.name
    try:
        assert is_valid_pdf(filepath) is True
    finally:
        os.remove(filepath)


def test_is_valid_pdf_invalid_magic_header():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"NOT_A_PDF\nsome content")
        filepath = f.name
    try:
        assert is_valid_pdf(filepath) is False
    finally:
        os.remove(filepath)


def test_is_valid_pdf_exception_handling():
    # Attempting to read a directory as a file raises an exception in is_valid_pdf which is caught
    with tempfile.TemporaryDirectory() as tmpdir:
        assert is_valid_pdf(tmpdir) is False


def test_check_url_head_success():
    with mock.patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = mock.MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        status, reason = check_url_head("https://example.com/test.pdf")
        assert status == 200
        assert reason == "OK"


def test_check_url_head_http_error():
    with mock.patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.com/test.pdf", 404, "Not Found", None, None
        )

        status, reason = check_url_head("https://example.com/test.pdf")
        assert status == 404
        assert "Not Found" in reason


def test_check_url_head_url_error():
    with mock.patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("reason_string")

        status, reason = check_url_head("https://example.com/test.pdf")
        assert status is None
        assert "Connection Failed" in reason


def test_check_url_head_unexpected_exception():
    with mock.patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = ValueError("unexpected")

        status, reason = check_url_head("https://example.com/test.pdf")
        assert status is None
        assert "unexpected" in reason


def test_download_file_dry_run_success():
    with mock.patch("src.download_ref_docs.check_url_head") as mock_head:
        mock_head.return_value = (200, "OK")
        success = download_file("https://example.com/test.pdf", "dest.pdf", dry_run=True)
        assert success is True
        mock_head.assert_called_once_with("https://example.com/test.pdf", timeout=10)


def test_download_file_dry_run_failure():
    with mock.patch("src.download_ref_docs.check_url_head") as mock_head:
        mock_head.return_value = (404, "Not Found")
        success = download_file("https://example.com/test.pdf", "dest.pdf", dry_run=True)
        assert success is False


def test_download_file_real_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = os.path.join(tmp_dir, "test.pdf")
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = mock.MagicMock()
            mock_response.read.return_value = b"%PDF-1.4 mock content"
            mock_urlopen.return_value.__enter__.return_value = mock_response

            success = download_file("https://example.com/test.pdf", dest_path)
            assert success is True
            assert os.path.exists(dest_path)
            with open(dest_path, "rb") as f:
                assert f.read() == b"%PDF-1.4 mock content"


def test_download_file_invalid_pdf_content():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = os.path.join(tmp_dir, "test.pdf")
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = mock.MagicMock()
            mock_response.read.return_value = b"NOT_A_PDF_CONTENT"
            mock_urlopen.return_value.__enter__.return_value = mock_response

            success = download_file("https://example.com/test.pdf", dest_path, is_fallback=False)
            assert success is False
            assert not os.path.exists(dest_path)


def test_download_file_real_failure_no_fallback():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = os.path.join(tmp_dir, "test.pdf")
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.HTTPError(
                "https://example.com/test.pdf", 404, "Not Found", None, None
            )

            success = download_file("https://example.com/test.pdf", dest_path, is_fallback=False)
            assert success is False
            assert not os.path.exists(dest_path)


def test_download_file_real_failure_no_fallback_generic_exception():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = os.path.join(tmp_dir, "test.pdf")
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = RuntimeError("network timeout")

            success = download_file("https://example.com/test.pdf", dest_path, is_fallback=False)
            assert success is False
            assert not os.path.exists(dest_path)


def test_download_file_real_failure_with_fallback_http_error():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = os.path.join(tmp_dir, "test.pdf")
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.HTTPError(
                "https://example.com/test.pdf", 404, "Not Found", None, None
            )

            success = download_file("https://example.com/test.pdf", dest_path, is_fallback=True)
            assert success is False
            assert not os.path.exists(dest_path)

            # Should create a placeholder text file
            txt_path = dest_path.replace(".pdf", "_placeholder.txt")
            assert os.path.exists(txt_path)
            with open(txt_path, "r") as f:
                content = f.read()
                assert "Placeholder for custom/fictional STM32C542RC device manual" in content
                assert "HTTP Error 404" in content


def test_download_file_real_failure_with_fallback_generic_exception():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dest_path = os.path.join(tmp_dir, "test.pdf")
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = RuntimeError("network timeout")

            success = download_file("https://example.com/test.pdf", dest_path, is_fallback=True)
            assert success is False
            assert not os.path.exists(dest_path)

            # Should create a placeholder text file
            txt_path = dest_path.replace(".pdf", "_placeholder.txt")
            assert os.path.exists(txt_path)
            with open(txt_path, "r") as f:
                content = f.read()
                assert "network timeout" in content


def test_main_dry_run():
    with mock.patch("src.download_ref_docs.download_file") as mock_download, \
         mock.patch("time.sleep") as mock_sleep:
        mock_download.return_value = True

        main(["--dry-run"])

        # Verify download_file was called for each target with dry_run=True
        assert mock_download.call_count == len(DOWNLOAD_TARGETS)
        for call_args in mock_download.call_args_list:
            assert call_args[1]["dry_run"] is True


def test_main_real():
    with mock.patch("src.download_ref_docs.download_file") as mock_download, \
         mock.patch("time.sleep") as mock_sleep:
        mock_download.return_value = True

        main([])

        # Verify download_file was called for each target with dry_run=False
        assert mock_download.call_count == len(DOWNLOAD_TARGETS)
        for call_args in mock_download.call_args_list:
            assert call_args[1]["dry_run"] is False


def test_main_verify_all_valid():
    with mock.patch("os.path.exists", return_value=True), \
         mock.patch("src.download_ref_docs.is_valid_pdf", return_value=True):
        res = main(["--verify"])
        assert res is True


def test_main_verify_missing():
    with mock.patch("os.path.exists", return_value=False):
        res = main(["--verify"])
        assert res is False


def test_main_verify_with_placeholder():
    # If the target is a fallback and does not exist as PDF, but a placeholder text exists, it's valid
    def side_effect_exists(path):
        if path.endswith(".pdf"):
            return False
        if path.endswith("_placeholder.txt"):
            return True
        return False

    with mock.patch("os.path.exists", side_effect=side_effect_exists):
        # Let's mock DOWNLOAD_TARGETS to only have fallbacks
        mock_targets = [
            {"dest": "specification/pdfs/mcus/stm32c542rc_datasheet.pdf", "is_fallback": True}
        ]
        with mock.patch("src.download_ref_docs.DOWNLOAD_TARGETS", mock_targets):
            res = main(["--verify"])
            assert res is True


def test_main_verify_invalid_pdf():
    # File exists but is_valid_pdf returns False
    with mock.patch("os.path.exists", return_value=True), \
         mock.patch("src.download_ref_docs.is_valid_pdf", return_value=False):
        res = main(["--verify"])
        assert res is False
