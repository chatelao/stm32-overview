import os
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
    result = runner.invoke(cli, ["recommend", "-r", "M33", "-c", "-a"])
    assert result.exit_code == 0
    assert "Board: Nucleo-C542RC (Match Score: 100.0%)" in result.output
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
