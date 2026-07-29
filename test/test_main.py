import os
from unittest import mock
from click.testing import CliRunner
from src.main import cli

def test_cli_list():
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "Registered STM32 boards:" in result.output
    assert "Nucleo-C031C6" in result.output
    assert "Nucleo-C542RC" in result.output
    assert "Nucleo-F446RE" in result.output
    assert "Nucleo-G431RB" in result.output

def test_cli_show():
    runner = CliRunner()
    result = runner.invoke(cli, ["show", "-b", "Nucleo-C542RC"])
    assert result.exit_code == 0
    assert "board: Nucleo-C542RC" in result.output
    assert "architecture: Cortex-M33" in result.output

def test_cli_show_invalid():
    runner = CliRunner()
    result = runner.invoke(cli, ["show", "-b", "InvalidBoard"])
    assert result.exit_code != 0
    assert "Error" in result.output

def test_cli_compare():
    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "-b", "Nucleo-F446RE", "-b", "Nucleo-C031C6"])
    assert result.exit_code == 0
    assert "Feature" in result.output
    assert "Nucleo-F446RE" in result.output
    assert "Nucleo-C031C6" in result.output

def test_cli_recommend():
    runner = CliRunner()
    result = runner.invoke(cli, ["recommend", "-r", "M33", "-c"])
    assert result.exit_code == 0
    assert "Board: Nucleo-C542RC (Match Score: 100.0%)" in result.output
    assert "Matched Features" in result.output

def test_cli_recommend_dsp():
    runner = CliRunner()
    result = runner.invoke(cli, ["recommend", "-d"])
    assert result.exit_code == 0
    assert "Matched Features" in result.output

def test_cli_export(tmp_path):
    output_file = tmp_path / "test_report.md"
    runner = CliRunner()
    result = runner.invoke(cli, ["export", "-o", str(output_file)])
    assert result.exit_code == 0
    assert f"Successfully exported comparison matrix to '{output_file}'." in result.output
    assert output_file.exists()
    content = output_file.read_text()
    assert "Feature" in content
    assert "Nucleo-C031C6" in content
    assert "Nucleo-C542RC" in content
    assert "Nucleo-F446RE" in content
    assert "Nucleo-G431RB" in content

@mock.patch("src.main.DocGenerator.export_report")
def test_cli_export_default(mock_export):
    runner = CliRunner()
    result = runner.invoke(cli, ["export"])
    assert result.exit_code == 0
    assert "Successfully exported comparison matrix to 'docs/comparison_matrix.md'." in result.output
    mock_export.assert_called_once()
    args, kwargs = mock_export.call_args
    assert args[1] == "docs/comparison_matrix.md"

def test_cli_export_overwrite_confirm_yes():
    temp_filename = "temp_test_root_file.md"
    abs_temp_path = os.path.abspath(temp_filename)
    with open(abs_temp_path, "w") as f:
        f.write("existing content")

    try:
        runner = CliRunner()
        result = runner.invoke(cli, ["export", "-o", temp_filename], input="y\n")
        assert result.exit_code == 0
        assert "Warning: You are about to overwrite a root-level file" in result.output
        assert f"Successfully exported comparison matrix to '{temp_filename}'." in result.output

        with open(abs_temp_path, "r") as f:
            content = f.read()
            assert "Feature" in content
    finally:
        if os.path.exists(abs_temp_path):
            os.remove(abs_temp_path)

def test_cli_export_overwrite_confirm_no():
    temp_filename = "temp_test_root_file_no.md"
    abs_temp_path = os.path.abspath(temp_filename)
    with open(abs_temp_path, "w") as f:
        f.write("existing content")

    try:
        runner = CliRunner()
        result = runner.invoke(cli, ["export", "-o", temp_filename], input="n\n")
        assert result.exit_code == 0
        assert "Warning: You are about to overwrite a root-level file" in result.output
        assert "Export aborted." in result.output

        with open(abs_temp_path, "r") as f:
            content = f.read()
            assert content == "existing content"
    finally:
        if os.path.exists(abs_temp_path):
            os.remove(abs_temp_path)
