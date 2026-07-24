import os
import pytest
import tempfile
import yaml
from src.core.repository import DataRepository
from src.core.registry import RegistryEngine
from src.core.comparison import ComparisonEngine, ComparisonResult

def test_comparison_empty_input():
    repo = DataRepository("specification")
    registry = RegistryEngine(repo)
    engine = ComparisonEngine(registry)

    result = engine.compare([])
    assert result.headers == []
    assert result.features == {}

def test_comparison_valid_boards():
    with tempfile.TemporaryDirectory() as tmp_dir:
        spec_1 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {"architecture": "Cortex-M4", "frequency_mhz": 180, "fpu": True},
            "memory": {"flash_kb": 512, "sram_kb": 128},
            "peripherals": {
                "uarts": 4, "usarts": 2, "i2c": 3, "spi": 4, "can": 2,
                "adc_channels": 16, "dac_channels": 2, "timers": 10,
                "opamps": 0, "comps": 0
            },
            "electrical": {"min_voltage": 1.7, "max_voltage": 3.6}
        }
        spec_2 = {
            "board": "Nucleo-C031C6",
            "mcu": "STM32C031C6T6",
            "core": {"architecture": "Cortex-M0+", "frequency_mhz": 48, "fpu": False},
            "memory": {"flash_kb": 32, "sram_kb": 12},
            "peripherals": {
                "uarts": 1, "usarts": 1, "i2c": 1, "spi": 1, "can": 0,
                "adc_channels": 5, "dac_channels": 0, "timers": 4,
                "opamps": 0, "comps": 0
            },
            "electrical": {"min_voltage": 2.0, "max_voltage": 3.6}
        }

        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(spec_1, f)
        with open(os.path.join(tmp_dir, "nucleo_c031c6.yaml"), "w") as f:
            yaml.dump(spec_2, f)

        repo = DataRepository(tmp_dir)
        registry = RegistryEngine(repo)
        engine = ComparisonEngine(registry)

        result = engine.compare(["Nucleo-F446RE", "Nucleo-C031C6"])

        # Check headers
        assert result.headers == ["Nucleo-F446RE", "Nucleo-C031C6"]

        # Check features map correct alignment
        assert result.features["mcu"] == ["STM32F446RET6", "STM32C031C6T6"]
        assert result.features["architecture"] == ["Cortex-M4", "Cortex-M0+"]
        assert result.features["frequency_mhz"] == [180, 48]
        assert result.features["fpu"] == [True, False]
        assert result.features["flash_kb"] == [512, 32]
        assert result.features["sram_kb"] == [128, 12]
        assert result.features["can"] == [2, 0]
        assert result.features["min_voltage"] == [1.7, 2.0]

def test_comparison_case_insensitivity_and_invalid_board():
    with tempfile.TemporaryDirectory() as tmp_dir:
        spec_1 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {"architecture": "Cortex-M4", "frequency_mhz": 180, "fpu": True},
            "memory": {"flash_kb": 512, "sram_kb": 128},
            "peripherals": {
                "uarts": 4, "usarts": 2, "i2c": 3, "spi": 4, "can": 2,
                "adc_channels": 16, "dac_channels": 2, "timers": 10,
                "opamps": 0, "comps": 0
            },
            "electrical": {"min_voltage": 1.7, "max_voltage": 3.6}
        }
        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(spec_1, f)

        repo = DataRepository(tmp_dir)
        registry = RegistryEngine(repo)
        engine = ComparisonEngine(registry)

        # Case-insensitive check
        result = engine.compare(["nucleo-f446re"])
        assert result.headers == ["Nucleo-F446RE"]
        assert result.features["mcu"] == ["STM32F446RET6"]

        # Non-existent board
        with pytest.raises(ValueError):
            engine.compare(["Invalid-Board"])

def test_comparison_missing_optional_or_nested_fields():
    # Test that missing fields fall back to "N/A"
    with tempfile.TemporaryDirectory() as tmp_dir:
        # A partial spec dictionary (directly bypass repository loading to test the fallback, or let repo load it)
        # Wait, repository's DataRepository loads and validates, but let's test comparison fallback with raw data
        # manually populated or mock RegistryEngine.
        pass

class MockRegistry:
    def get_board_details(self, name: str):
        if name == "Partial":
            return {
                "board": "Partial-Board",
                "mcu": "STM32PARTIAL",
                "core": {
                    "architecture": "Cortex-M3"
                    # frequency_mhz and fpu are missing!
                }
                # memory, peripherals, and electrical are missing!
            }
        raise ValueError("Not found")

def test_comparison_fallback_logic():
    mock_registry = MockRegistry()
    engine = ComparisonEngine(mock_registry)

    result = engine.compare(["Partial"])
    assert result.headers == ["Partial-Board"]
    assert result.features["mcu"] == ["STM32PARTIAL"]
    assert result.features["architecture"] == ["Cortex-M3"]
    assert result.features["frequency_mhz"] == ["N/A"]
    assert result.features["fpu"] == ["N/A"]
    assert result.features["flash_kb"] == ["N/A"]
    assert result.features["can"] == ["N/A"]
