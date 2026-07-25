import os
import pytest
import tempfile
import yaml
from src.core.repository import DataRepository
from src.core.registry import RegistryEngine

def test_registry_list_boards():
    with tempfile.TemporaryDirectory() as tmp_dir:
        spec_1 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {
                "architecture": "Cortex-M4", "frequency_mhz": 180, "fpu": True, "cordic": False, "fmac": False,
                "instruction_set": "Armv7E-M", "fpu_type": "FPv4-SP", "dsp": True, "accelerations": ["ART Accelerator"]
            },
            "memory": {"flash_kb": 512, "sram_kb": 128},
            "peripherals": {
                "uarts": 4, "usarts": 2, "i2c": 3, "spi": 4, "can": 2, "adc_channels": 16, "dac_channels": 2, "timers": 10, "opamps": 0, "comps": 0,
                "adc_resolution_bits": 12, "adc_speed_msps": 2.4, "timer_resolution_bits": 32
            },
            "electrical": {"min_voltage": 1.7, "max_voltage": 3.6}
        }
        spec_2 = {
            "board": "Nucleo-C031C6",
            "mcu": "STM32C031C6T6",
            "core": {
                "architecture": "Cortex-M0+", "frequency_mhz": 48, "fpu": False, "cordic": False, "fmac": False,
                "instruction_set": "Armv6-M", "fpu_type": None, "dsp": False, "accelerations": []
            },
            "memory": {"flash_kb": 32, "sram_kb": 12},
            "peripherals": {
                "uarts": 1, "usarts": 1, "i2c": 1, "spi": 1, "can": 0, "adc_channels": 5, "dac_channels": 0, "timers": 4, "opamps": 0, "comps": 0,
                "adc_resolution_bits": 12, "adc_speed_msps": 1.25, "timer_resolution_bits": 16
            },
            "electrical": {"min_voltage": 2.0, "max_voltage": 3.6}
        }

        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(spec_1, f)
        with open(os.path.join(tmp_dir, "nucleo_c031c6.yaml"), "w") as f:
            yaml.dump(spec_2, f)

        repo = DataRepository(tmp_dir)
        registry = RegistryEngine(repo)

        # list_boards should return board names sorted alphabetically
        boards = registry.list_boards()
        assert boards == ["Nucleo-C031C6", "Nucleo-F446RE"]

def test_registry_get_board_details():
    with tempfile.TemporaryDirectory() as tmp_dir:
        spec_1 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {
                "architecture": "Cortex-M4", "frequency_mhz": 180, "fpu": True, "cordic": False, "fmac": False,
                "instruction_set": "Armv7E-M", "fpu_type": "FPv4-SP", "dsp": True, "accelerations": ["ART Accelerator"]
            },
            "memory": {"flash_kb": 512, "sram_kb": 128},
            "peripherals": {
                "uarts": 4, "usarts": 2, "i2c": 3, "spi": 4, "can": 2, "adc_channels": 16, "dac_channels": 2, "timers": 10, "opamps": 0, "comps": 0,
                "adc_resolution_bits": 12, "adc_speed_msps": 2.4, "timer_resolution_bits": 32
            },
            "electrical": {"min_voltage": 1.7, "max_voltage": 3.6}
        }
        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(spec_1, f)

        repo = DataRepository(tmp_dir)
        registry = RegistryEngine(repo)

        # Valid retrieval
        details = registry.get_board_details("Nucleo-F446RE")
        assert details["board"] == "Nucleo-F446RE"
        assert details["mcu"] == "STM32F446RET6"

        # Case-insensitive retrieval
        details_lower = registry.get_board_details("nucleo-f446re")
        assert details_lower["board"] == "Nucleo-F446RE"

        # Non-existent board
        with pytest.raises(ValueError):
            registry.get_board_details("Invalid-Board")
