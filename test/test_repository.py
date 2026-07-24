import pytest
from pydantic import ValidationError
from src.core.repository import BoardSpecification

def test_valid_board_specification():
    valid_data = {
        "board": "Nucleo-F446RE",
        "mcu": "STM32F446RET6",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": 180,
            "fpu": True
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
            "timers": 10
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
        }
    }
    board_spec = BoardSpecification(**valid_data)
    assert board_spec.board == "Nucleo-F446RE"
    assert board_spec.mcu == "STM32F446RET6"
    assert board_spec.core.architecture == "Cortex-M4"
    assert board_spec.core.frequency_mhz == 180
    assert board_spec.core.fpu is True
    assert board_spec.memory.flash_kb == 512
    assert board_spec.memory.sram_kb == 128
    assert board_spec.peripherals.uarts == 4
    assert board_spec.electrical.min_voltage == 1.7
    assert board_spec.electrical.max_voltage == 3.6

def test_invalid_board_specification_missing_field():
    invalid_data = {
        "board": "Nucleo-F446RE",
        "mcu": "STM32F446RET6",
        "core": {
            "architecture": "Cortex-M4",
            "frequency_mhz": 180,
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
            "timers": 10
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
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
            "fpu": True
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
            "timers": 10
        },
        "electrical": {
            "min_voltage": 1.7,
            "max_voltage": 3.6
        }
    }
    with pytest.raises(ValidationError):
        BoardSpecification(**invalid_data)
