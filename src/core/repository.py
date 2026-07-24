import os
import yaml
from typing import Dict, List, Any
from src.core.schema import BoardSpecification

class DataRepository:
    def __init__(self, spec_dir: str):
        self.spec_dir = spec_dir

    def _load_and_validate(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Validate against the Pydantic schema
        spec = BoardSpecification(**data)

        # Support both Pydantic v1 (dict()) and Pydantic v2 (model_dump())
        if hasattr(spec, "model_dump"):
            return spec.model_dump()
        else:
            return spec.dict()

    def load_all_specs(self) -> List[Dict[str, Any]]:
        """
        Scans spec_dir, parses all yaml files, validates them against the Pydantic schema,
        and returns a list of dictionaries representing valid MCU specifications.
        """
        specs = []
        if not os.path.isdir(self.spec_dir):
            raise ValueError(f"Specification directory '{self.spec_dir}' does not exist.")

        for filename in sorted(os.listdir(self.spec_dir)):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(self.spec_dir, filename)
                try:
                    spec_dict = self._load_and_validate(filepath)
                    specs.append(spec_dict)
                except Exception as e:
                    # In a real app we might log or re-raise; for safety, let's let validation errors propagate
                    raise ValueError(f"Failed to validate '{filename}': {e}") from e
        return specs

    def get_spec(self, board_name: str) -> Dict[str, Any]:
        """
        Retrieves and validates the specification for a specific board.
        Raises ValueError if the board is not found.
        """
        if not os.path.isdir(self.spec_dir):
            raise ValueError(f"Specification directory '{self.spec_dir}' does not exist.")

        for filename in os.listdir(self.spec_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(self.spec_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if data and data.get("board") == board_name:
                        # Validate and return
                        return self._load_and_validate(filepath)
                except Exception:
                    # If this file has error, we keep searching or raise
                    pass

        raise ValueError(f"Board '{board_name}' specification not found in '{self.spec_dir}'.")
