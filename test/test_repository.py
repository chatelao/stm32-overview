import os
import pytest
import tempfile
import yaml
from pydantic import ValidationError
from src.core.repository import BoardSpecification, DataRepository

def test_valid_board_specification():
    valid_data = {
        "board": "Nucleo-F446RE",
        "mcu": "STM32F446RET6",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": 180,
            "fpu": True,
            "cordic": False,
            "fmac": False
        },
        "memory": {
            "flash_kb": 512,
            "sram_kb": 128
        },
        "peripherals": {
            "uarts": 4,
            "usarts": 2,
            "i2c": 3,
            "spi": 4,
            "can": 2,
            "adc_channels": 16,
            "dac_channels": 2,
            "timers": 10,
            "opamps": 0,
            "comps": 0,
            "adc_resolution_bits": 12,
            "adc_speed_msps": 2.4,
            "timer_resolution_bits": 32
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
        },
        "documentation": {
            "user_manual": {"url": "http://um.pdf", "dest": "pdf/um.pdf"},
            "datasheet": {"url": "http://ds.pdf", "dest": "pdf/ds.pdf"},
            "reference_manual": {"url": "http://rm.pdf", "dest": "pdf/rm.pdf"}
        }
    }
    board_spec = BoardSpecification(**valid_data)
    assert board_spec.board == "Nucleo-F446RE"
    assert board_spec.mcu == "STM32F446RET6"
    assert board_spec.core.architecture == "Cortex-M4"
    assert board_spec.core.frequency_mhz == 180
    assert board_spec.core.fpu is True
    assert board_spec.core.cordic is False
    assert board_spec.core.fmac is False
    assert board_spec.memory.flash_kb == 512
    assert board_spec.memory.sram_kb == 128
    assert board_spec.peripherals.uarts == 4
    assert board_spec.peripherals.opamps == 0
    assert board_spec.peripherals.comps == 0
    assert board_spec.peripherals.adc_resolution_bits == 12
    assert board_spec.peripherals.adc_speed_msps == 2.4
    assert board_spec.peripherals.timer_resolution_bits == 32
    assert board_spec.electrical.min_voltage == 1.7
    assert board_spec.electrical.max_voltage == 3.6

def test_invalid_board_specification_missing_field():
    invalid_data = {
        "board": "Nucleo-F446RE",
        "mcu": "STM32F446RET6",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": 180,
            "cordic": False,
            "fmac": False
            # fpu is missing
        },
        "memory": {
            "flash_kb": 512,
            "sram_kb": 128
        },
        "peripherals": {
            "uarts": 4,
            "usarts": 2,
            "i2c": 3,
            "spi": 4,
            "can": 2,
            "adc_channels": 16,
            "dac_channels": 2,
            "timers": 10,
            "opamps": 0,
            "comps": 0,
            "adc_resolution_bits": 12,
            "adc_speed_msps": 2.4,
            "timer_resolution_bits": 32
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
        },
        "documentation": {
            "user_manual": {"url": "http://um.pdf", "dest": "pdf/um.pdf"},
            "datasheet": {"url": "http://ds.pdf", "dest": "pdf/ds.pdf"},
            "reference_manual": {"url": "http://rm.pdf", "dest": "pdf/rm.pdf"}
        }
    }
    with pytest.raises(ValidationError):
        BoardSpecification(**invalid_data)

def test_invalid_board_specification_wrong_type():
    invalid_data = {
        "board": "Nucleo-F446RE",
        "mcu": "STM32F446RET6",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": "one hundred and eighty",  # should be int
            "fpu": True,
            "cordic": False,
            "fmac": False
        },
        "memory": {
            "flash_kb": 512,
            "sram_kb": 128
        },
        "peripherals": {
            "uarts": 4,
            "usarts": 2,
            "i2c": 3,
            "spi": 4,
            "can": 2,
            "adc_channels": 16,
            "dac_channels": 2,
            "timers": 10,
            "opamps": 0,
            "comps": 0,
            "adc_resolution_bits": 12,
            "adc_speed_msps": 2.4,
            "timer_resolution_bits": 32
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
        },
        "documentation": {
            "user_manual": {"url": "http://um.pdf", "dest": "pdf/um.pdf"},
            "datasheet": {"url": "http://ds.pdf", "dest": "pdf/ds.pdf"},
            "reference_manual": {"url": "http://rm.pdf", "dest": "pdf/rm.pdf"}
        }
    }
    with pytest.raises(ValidationError):
        BoardSpecification(**invalid_data)

def test_data_repository_load_all_specs():
    # Setup temporary directory with valid and invalid specs
    with tempfile.TemporaryDirectory() as tmp_dir:
        valid_spec_1 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {
                "architecture": "Cortex-M4",
                "frequency_mhz": 180,
                "fpu": True,
                "cordic": False,
                "fmac": False
            },
            "memory": {
                "flash_kb": 512,
                "sram_kb": 128
            },
            "peripherals": {
                "uarts": 4,
                "usarts": 2,
                "i2c": 3,
                "spi": 4,
                "can": 2,
                "adc_channels": 16,
                "dac_channels": 2,
                "timers": 10,
                "opamps": 0,
                "comps": 0,
                "adc_resolution_bits": 12,
                "adc_speed_msps": 2.4,
                "timer_resolution_bits": 32
            },
            "electrical": {
                "min_voltage": 1.7,
                "max_voltage": 3.6
            },
            "documentation": {
                "user_manual": {"url": "http://um.pdf", "dest": "pdf/um.pdf"},
                "datasheet": {"url": "http://ds.pdf", "dest": "pdf/ds.pdf"},
                "reference_manual": {"url": "http://rm.pdf", "dest": "pdf/rm.pdf"}
            }
        }

        valid_spec_2 = {
            "board": "Nucleo-C031C6",
            "mcu": "STM32C031C6T6",
            "core": {
                "architecture": "Cortex-M0+",
                "frequency_mhz": 48,
                "fpu": False,
                "cordic": False,
                "fmac": False
            },
            "memory": {
                "flash_kb": 32,
                "sram_kb": 12
            },
            "peripherals": {
                "uarts": 1,
                "usarts": 1,
                "i2c": 1,
                "spi": 1,
                "can": 0,
                "adc_channels": 5,
                "dac_channels": 0,
                "timers": 4,
                "opamps": 0,
                "comps": 0,
                "adc_resolution_bits": 12,
                "adc_speed_msps": 1.25,
                "timer_resolution_bits": 16
            },
            "electrical": {
                "min_voltage": 2.0,
                "max_voltage": 3.6
            },
            "documentation": {
                "user_manual": {"url": "http://um.pdf", "dest": "pdf/um.pdf"},
                "datasheet": {"url": "http://ds.pdf", "dest": "pdf/ds.pdf"},
                "reference_manual": {"url": "http://rm.pdf", "dest": "pdf/rm.pdf"}
            }
        }

        invalid_spec = {
            "board": "Invalid-Board",
            # Missing MCU and other fields
        }

        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(valid_spec_1, f)
        with open(os.path.join(tmp_dir, "nucleo_c031c6.yaml"), "w") as f:
            yaml.dump(valid_spec_2, f)
        with open(os.path.join(tmp_dir, "invalid.yaml"), "w") as f:
            yaml.dump(invalid_spec, f)
        with open(os.path.join(tmp_dir, "ignored.txt"), "w") as f:
            f.write("should be ignored")

        repo = DataRepository(tmp_dir)
        specs = repo.load_all_specs()

        # Should only load valid yaml files, and they should be sorted by filename (nucleo_c031c6.yaml, then nucleo_f446re.yaml)
        assert len(specs) == 2
        assert specs[0]["board"] == "Nucleo-C031C6"
        assert specs[1]["board"] == "Nucleo-F446RE"

def test_data_repository_get_spec():
    with tempfile.TemporaryDirectory() as tmp_dir:
        valid_spec_1 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {
                "architecture": "Cortex-M4",
                "frequency_mhz": 180,
                "fpu": True,
                "cordic": False,
                "fmac": False
            },
            "memory": {
                "flash_kb": 512,
                "sram_kb": 128
            },
            "peripherals": {
                "uarts": 4,
                "usarts": 2,
                "i2c": 3,
                "spi": 4,
                "can": 2,
                "adc_channels": 16,
                "dac_channels": 2,
                "timers": 10,
                "opamps": 0,
                "comps": 0,
                "adc_resolution_bits": 12,
                "adc_speed_msps": 2.4,
                "timer_resolution_bits": 32
            },
            "electrical": {
                "min_voltage": 1.7,
                "max_voltage": 3.6
            },
            "documentation": {
                "user_manual": {"url": "http://um.pdf", "dest": "pdf/um.pdf"},
                "datasheet": {"url": "http://ds.pdf", "dest": "pdf/ds.pdf"},
                "reference_manual": {"url": "http://rm.pdf", "dest": "pdf/rm.pdf"}
            }
        }
        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(valid_spec_1, f)

        repo = DataRepository(tmp_dir)

        # Valid retrieval (case-insensitive)
        spec = repo.get_spec("nucleo-f446re")
        assert spec["board"] == "Nucleo-F446RE"
        assert spec["mcu"] == "STM32F446RET6"

        # Invalid retrieval
        with pytest.raises(ValueError) as excinfo:
            repo.get_spec("Non-Existent-Board")
        assert "not found in specifications" in str(excinfo.value)

def test_data_repository_empty_or_missing_dir():
    repo = DataRepository("non_existent_directory_abc")
    assert repo.load_all_specs() == []

def test_actual_repository_files():
    repo = DataRepository("specification")
    specs = repo.load_all_specs()
    # There are exactly 4 YAML files in specification/
    assert len(specs) == 4

    # Check that they have the new fields and validated correctly
    for spec in specs:
        assert "opamps" in spec["peripherals"]
        assert "comps" in spec["peripherals"]
