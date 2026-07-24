from typing import Dict, List, Any
from pydantic import BaseModel
from src.core.registry import RegistryEngine

class ComparisonResult(BaseModel):
    headers: List[str]                  # List of board names compared
    features: Dict[str, List[Any]]       # Feature name mapped to values in order of headers

class ComparisonEngine:
    def __init__(self, registry: RegistryEngine):
        self.registry = registry

    def compare(self, board_names: List[str]) -> ComparisonResult:
        """
        Compares multiple boards and creates a row-by-row feature matrix.
        Aligns optional features with default values (e.g., None or N/A).
        """
        if not board_names:
            return ComparisonResult(headers=[], features={})

        # Feature paths mapping to extract features from the board specifications
        feature_paths = {
            "mcu": "mcu",
            "architecture": "core.architecture",
            "frequency_mhz": "core.frequency_mhz",
            "fpu": "core.fpu",
            "flash_kb": "memory.flash_kb",
            "sram_kb": "memory.sram_kb",
            "uarts": "peripherals.uarts",
            "usarts": "peripherals.usarts",
            "i2c": "peripherals.i2c",
            "spi": "peripherals.spi",
            "can": "peripherals.can",
            "adc_channels": "peripherals.adc_channels",
            "dac_channels": "peripherals.dac_channels",
            "timers": "peripherals.timers",
            "opamps": "peripherals.opamps",
            "comps": "peripherals.comps",
            "adc_resolution_bits": "peripherals.adc_resolution_bits",
            "adc_speed_msps": "peripherals.adc_speed_msps",
            "timer_resolution_bits": "peripherals.timer_resolution_bits",
            "min_voltage": "electrical.min_voltage",
            "max_voltage": "electrical.max_voltage",
        }

        # Retrieve board details from registry (raises ValueError if board not found)
        boards_details = []
        headers = []
        for name in board_names:
            details = self.registry.get_board_details(name)
            boards_details.append(details)
            headers.append(details["board"])

        def get_nested_val(data: Dict[str, Any], path: str, default: Any = "N/A") -> Any:
            parts = path.split(".")
            curr = data
            for p in parts:
                if isinstance(curr, dict) and p in curr:
                    curr = curr[p]
                else:
                    return default
            return curr

        features: Dict[str, List[Any]] = {}
        for feature_name, path in feature_paths.items():
            features[feature_name] = [
                get_nested_val(detail, path) for detail in boards_details
            ]

        return ComparisonResult(headers=headers, features=features)
