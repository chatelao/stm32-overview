import os
from typing import Dict, List, Any
import yaml
from pydantic import BaseModel, ValidationError

class CoreSpec(BaseModel):
    architecture: str
    frequency_mhz: int
    fpu: bool
    cordic: bool
    fmac: bool

class MemorySpec(BaseModel):
    flash_kb: int
    sram_kb: int

class PeripheralsSpec(BaseModel):
    uarts: int
    usarts: int
    i2c: int
    spi: int
    can: int
    adc_channels: int
    dac_channels: int
    timers: int
    opamps: int
    comps: int
    adc_resolution_bits: int
    adc_speed_msps: float
    timer_resolution_bits: int

class ElectricalSpec(BaseModel):
    min_voltage: float
    max_voltage: float

class BoardSpecification(BaseModel):
    board: str
    mcu: str
    core: CoreSpec
    memory: MemorySpec
    peripherals: PeripheralsSpec
    electrical: ElectricalSpec

class DataRepository:
    def __init__(self, spec_dir: str):
        self.spec_dir = spec_dir

    def load_all_specs(self) -> List[Dict[str, Any]]:
        """
        Scans spec_dir, parses all yaml files, validates them against the Pydantic schema,
        and returns a list of dictionaries representing valid MCU specifications.
        """
        specs = []
        if not os.path.isdir(self.spec_dir):
            return specs

        for filename in sorted(os.listdir(self.spec_dir)):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(self.spec_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if data:
                        # Validate data against Pydantic schema
                        board_spec = BoardSpecification(**data)
                        specs.append(board_spec.model_dump())
                except (yaml.YAMLError, ValidationError, OSError):
                    # Silently skip or let it propagate? The docstring says:
                    # "returns a list of dictionaries representing valid MCU specifications"
                    # We will only append valid specifications.
                    continue
        return specs

    def get_spec(self, board_name: str) -> Dict[str, Any]:
        """
        Retrieves and validates the specification for a specific board.
        Raises ValueError if the board is not found.
        """
        all_specs = self.load_all_specs()
        for spec in all_specs:
            if spec["board"].lower() == board_name.lower():
                return spec
        raise ValueError(f"Board '{board_name}' not found in specifications.")
