import os
import pytest
import tempfile
import yaml
from src.core.repository import DataRepository
from src.core.registry import RegistryEngine
from src.core.recommendation import Constraints, RecommendationEngine

@pytest.fixture
def sample_registry_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        spec_f446 = {
            "board": "Nucleo-F446RE",
            "mcu": "STM32F446RET6",
            "core": {"architecture": "Cortex-M4", "frequency_mhz": 180, "fpu": True},
            "memory": {"flash_kb": 512, "sram_kb": 128},
            "peripherals": {
                "uarts": 4, "usarts": 2, "i2c": 3, "spi": 4, "can": 2, "adc_channels": 16, "dac_channels": 2, "timers": 10, "opamps": 0, "comps": 0,
                "adc_resolution_bits": 12, "adc_speed_msps": 2.4, "timer_resolution_bits": 32
            },
            "electrical": {"min_voltage": 1.7, "max_voltage": 3.6}
        }
        spec_c031 = {
            "board": "Nucleo-C031C6",
            "mcu": "STM32C031C6T6",
            "core": {"architecture": "Cortex-M0+", "frequency_mhz": 48, "fpu": False},
            "memory": {"flash_kb": 32, "sram_kb": 12},
            "peripherals": {
                "uarts": 1, "usarts": 1, "i2c": 1, "spi": 1, "can": 0, "adc_channels": 5, "dac_channels": 0, "timers": 4, "opamps": 0, "comps": 0,
                "adc_resolution_bits": 12, "adc_speed_msps": 1.25, "timer_resolution_bits": 16
            },
            "electrical": {"min_voltage": 2.0, "max_voltage": 3.6}
        }
        spec_g431 = {
            "board": "Nucleo-G431RB",
            "mcu": "STM32G431RBT6",
            "core": {"architecture": "Cortex-M4", "frequency_mhz": 170, "fpu": True},
            "memory": {"flash_kb": 128, "sram_kb": 32},
            "peripherals": {
                "uarts": 0, "usarts": 3, "i2c": 3, "spi": 3, "can": 1, "adc_channels": 10, "dac_channels": 4, "timers": 8, "opamps": 4, "comps": 3,
                "adc_resolution_bits": 12, "adc_speed_msps": 4.0, "timer_resolution_bits": 32
            },
            "electrical": {"min_voltage": 1.71, "max_voltage": 3.6}
        }

        with open(os.path.join(tmp_dir, "nucleo_f446re.yaml"), "w") as f:
            yaml.dump(spec_f446, f)
        with open(os.path.join(tmp_dir, "nucleo_c031c6.yaml"), "w") as f:
            yaml.dump(spec_c031, f)
        with open(os.path.join(tmp_dir, "nucleo_g431rb.yaml"), "w") as f:
            yaml.dump(spec_g431, f)

        yield tmp_dir

def test_recommendation_empty_constraints(sample_registry_dir):
    repo = DataRepository(sample_registry_dir)
    registry = RegistryEngine(repo)
    engine = RecommendationEngine(registry)

    constraints = Constraints()
    recommendations = engine.evaluate(constraints)

    # With no active constraints, all boards should match 100%, sorted alphabetically
    assert len(recommendations) == 3
    assert [r.board_name for r in recommendations] == ["Nucleo-C031C6", "Nucleo-F446RE", "Nucleo-G431RB"]
    for r in recommendations:
        assert r.match_score == 100.0
        assert r.matched_features == []
        assert r.missing_features == []

def test_recommendation_all_match(sample_registry_dir):
    repo = DataRepository(sample_registry_dir)
    registry = RegistryEngine(repo)
    engine = RecommendationEngine(registry)

    # Constraints that only Nucleo-F446RE should fully match, others partially
    constraints = Constraints(
        min_flash_kb=256,
        min_sram_kb=64,
        min_freq_mhz=100,
        requires_fpu=True,
        peripherals=["can"]
    )
    recommendations = engine.evaluate(constraints)

    assert len(recommendations) == 3

    # Best match must be Nucleo-F446RE (100% score)
    best = recommendations[0]
    assert best.board_name == "Nucleo-F446RE"
    assert best.match_score == 100.0
    assert set(best.matched_features) == {"flash_kb", "sram_kb", "frequency_mhz", "fpu", "can"}
    assert best.missing_features == []

    # Nucleo-G431RB matches some (FPU, CAN, FREQ) but missing flash (128 < 256) and sram (32 < 64)
    # Active constraints count: 5. Matches: 3 (FPU, CAN, frequency). Score: 3/5 * 100 = 60%
    g431 = [r for r in recommendations if r.board_name == "Nucleo-G431RB"][0]
    assert g431.match_score == 60.0
    assert set(g431.matched_features) == {"frequency_mhz", "fpu", "can"}
    assert set(g431.missing_features) == {"flash_kb", "sram_kb"}

    # Nucleo-C031C6 matches none of them. Score: 0/5 * 100 = 0%
    c031 = [r for r in recommendations if r.board_name == "Nucleo-C031C6"][0]
    assert c031.match_score == 0.0
    assert c031.matched_features == []
    assert set(c031.missing_features) == {"flash_kb", "sram_kb", "frequency_mhz", "fpu", "can"}

def test_recommendation_fpu_only(sample_registry_dir):
    repo = DataRepository(sample_registry_dir)
    registry = RegistryEngine(repo)
    engine = RecommendationEngine(registry)

    constraints = Constraints(requires_fpu=True)
    recommendations = engine.evaluate(constraints)

    # 1 active constraint (FPU).
    # Nucleo-F446RE and Nucleo-G431RB should have FPU (100%), Nucleo-C031C6 does not (0%).
    # Sorted by score desc, then board name asc:
    # 1. Nucleo-F446RE (100%)
    # 2. Nucleo-G431RB (100%)
    # 3. Nucleo-C031C6 (0%)
    assert [r.board_name for r in recommendations] == ["Nucleo-F446RE", "Nucleo-G431RB", "Nucleo-C031C6"]

    assert recommendations[0].match_score == 100.0
    assert recommendations[0].matched_features == ["fpu"]
    assert recommendations[0].missing_features == []

    assert recommendations[1].match_score == 100.0
    assert recommendations[1].matched_features == ["fpu"]
    assert recommendations[1].missing_features == []

    assert recommendations[2].match_score == 0.0
    assert recommendations[2].matched_features == []
    assert recommendations[2].missing_features == ["fpu"]

def test_recommendation_peripherals(sample_registry_dir):
    repo = DataRepository(sample_registry_dir)
    registry = RegistryEngine(repo)
    engine = RecommendationEngine(registry)

    constraints = Constraints(peripherals=["opamps", "can"])
    recommendations = engine.evaluate(constraints)

    # Constraints: opamps, can (2 active constraints)
    # F446: opamps=0 (no), can=2 (yes) -> 50%
    # G431: opamps=4 (yes), can=1 (yes) -> 100%
    # C031: opamps=0 (no), can=0 (no) -> 0%
    # Sorted:
    # 1. Nucleo-G431RB (100%)
    # 2. Nucleo-F446RE (50%)
    # 3. Nucleo-C031C6 (0%)
    assert [r.board_name for r in recommendations] == ["Nucleo-G431RB", "Nucleo-F446RE", "Nucleo-C031C6"]

    g431 = recommendations[0]
    assert g431.match_score == 100.0
    assert set(g431.matched_features) == {"opamps", "can"}
    assert g431.missing_features == []

    f446 = recommendations[1]
    assert f446.match_score == 50.0
    assert f446.matched_features == ["can"]
    assert f446.missing_features == ["opamps"]

    c031 = recommendations[2]
    assert c031.match_score == 0.0
    assert c031.matched_features == []
    assert set(c031.missing_features) == {"opamps", "can"}

def test_recommendation_no_boards():
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = DataRepository(tmp_dir)
        registry = RegistryEngine(repo)
        engine = RecommendationEngine(registry)

        constraints = Constraints(min_flash_kb=64)
        recommendations = engine.evaluate(constraints)
        assert recommendations == []
