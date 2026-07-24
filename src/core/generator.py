import os
from typing import Any
from src.core.comparison import ComparisonResult

class DocGenerator:
    @staticmethod
    def to_markdown_table(comparison_result: ComparisonResult) -> str:
        """
        Transforms a ComparisonResult structure into a Markdown-formatted table.
        """
        if not comparison_result.headers or not comparison_result.features:
            return ""

        # Build header row
        headers = ["Feature"] + comparison_result.headers
        header_row = "| " + " | ".join(headers) + " |"

        # Build separator row
        separator_row = "| " + " | ".join([":---"] * len(headers)) + " |"

        # Build feature rows
        feature_rows = []
        for feature_name, values in comparison_result.features.items():
            formatted_values = []
            for val in values:
                if isinstance(val, bool):
                    formatted_values.append("Yes" if val else "No")
                elif val is None:
                    formatted_values.append("N/A")
                else:
                    formatted_values.append(str(val))
            row = f"| {feature_name} | " + " | ".join(formatted_values) + " |"
            feature_rows.append(row)

        return "\n".join([header_row, separator_row] + feature_rows)

    @staticmethod
    def export_report(comparison_result: ComparisonResult, output_path: str) -> None:
        """
        Writes the generated markdown comparison table to the specified output path.
        """
        md_table = DocGenerator.to_markdown_table(comparison_result)

        # Ensure target directory exists
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_table)
