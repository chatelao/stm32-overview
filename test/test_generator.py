import os
import tempfile
from src.core.comparison import ComparisonResult
from src.core.generator import DocGenerator

def test_doc_generator_empty_result():
    # Empty headers/features should return an empty string
    empty_result = ComparisonResult(headers=[], features={})
    assert DocGenerator.to_markdown_table(empty_result) == ""

def test_doc_generator_standard_result():
    comparison_result = ComparisonResult(
        headers=["Nucleo-F446RE", "Nucleo-C031C6"],
        features={
            "mcu": ["STM32F446RET6", "STM32C031C6T6"],
            "frequency_mhz": [180, 48],
            "fpu": [True, False],
            "optional_field": [None, "Present"]
        }
    )

    expected_table = (
        "| Feature | Nucleo-F446RE | Nucleo-C031C6 |\n"
        "| :--- | :--- | :--- |\n"
        "| mcu | STM32F446RET6 | STM32C031C6T6 |\n"
        "| frequency_mhz | 180 | 48 |\n"
        "| fpu | Yes | No |\n"
        "| optional_field | N/A | Present |"
    )

    actual_table = DocGenerator.to_markdown_table(comparison_result)
    assert actual_table == expected_table

def test_doc_generator_export_report():
    comparison_result = ComparisonResult(
        headers=["Nucleo-G431RB"],
        features={
            "mcu": ["STM32G431RBT6"],
            "frequency_mhz": [170]
        }
    )

    expected_table = (
        "| Feature | Nucleo-G431RB |\n"
        "| :--- | :--- |\n"
        "| mcu | STM32G431RBT6 |\n"
        "| frequency_mhz | 170 |"
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "subdir", "report.md")
        DocGenerator.export_report(comparison_result, output_file)

        # Verify the file is created and contains correct table
        assert os.path.isfile(output_file)
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == expected_table
