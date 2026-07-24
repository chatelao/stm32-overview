import os
import pytest
import yaml
from pydantic import ValidationError
from src.core.schema import BoardSpecification
from src.core.repository import DataRepository

def test_pydantic_schema_valid():
    raw_data = {
        "board": "Test-Board",
        "mcu": "STM32F401",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": 84,
            "fpu": True
        },
        "memory": {
            "flash_kb": 512,
            "sram_kb": 96
        },
        "peripherals": {
            "uarts": 2,
            "usarts": 1,
            "i2c": 3,
            "spi": 4,
            "can": 0,
            "adc_channels": 16,
            "dac_channels": 0,
            "timers": 8
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
        }
    }
    spec = BoardSpecification(**raw_data)
    assert spec.board == "Test-Board"
    assert spec.memory.flash_kb == 512
    assert spec.core.fpu is True

def test_pydantic_schema_invalid():
    raw_data = {
        "board": "Test-Board",
        "mcu": "STM32F401",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": "invalid_int", # Wrong type!
            "fpu": True
        }
    }
    with pytest.raises(ValidationError):
        BoardSpecification(**raw_data)

def test_actual_board_yaml_validation():
    # Load all specs from specification/ directory
    repo = DataRepository("specification")
    specs = repo.load_all_specs()
    assert len(specs) == 4

    # Verify boards are sorted or present
    board_names = [spec["board"] for spec in specs]
    assert "Nucleo-F446RE" in board_names
    assert "Nucleo-C031C6" in board_names
    assert "Nucleo-G431RB" in board_names
    assert "Nucleo-C542RC" in board_names

def test_get_spec_by_name():
    repo = DataRepository("specification")
    spec = repo.get_spec("Nucleo-F446RE")
    assert spec["board"] == "Nucleo-F446RE"
    assert spec["mcu"] == "STM32F446RET6"
    assert spec["core"]["frequency_mhz"] == 180
    assert spec["core"]["fpu"] is True

    with pytest.raises(ValueError, match="not found"):
        repo.get_spec("Non-Existent-Board")

def test_invalid_yaml_file(tmp_path):
    # Setup temporary spec dir with an invalid YAML file
    spec_dir = tmp_path / "specs"
    spec_dir.mkdir()

    invalid_file = spec_dir / "bad_spec.yaml"
    invalid_file.write_text("""
board: "Bad-Board"
mcu: "STM32F103"
core:
  architecture: "Cortex-M3"
  frequency_mhz: "should_be_int"
""")

    repo = DataRepository(str(spec_dir))
    with pytest.raises(ValueError, match="Failed to validate"):
        repo.load_all_specs()

def test_repository_non_existent_directory():
    repo = DataRepository("non_existent_directory_xyz")
    with pytest.raises(ValueError, match="does not exist"):
        repo.load_all_specs()
    with pytest.raises(ValueError, match="does not exist"):
        repo.get_spec("Nucleo-F446RE")
