from typing import Dict, List, Any
from pydantic import BaseModel, Field

class CoreSpec(BaseModel):
    architecture: str
    frequency_mhz: int
    fpu: bool

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
        pass

    def get_spec(self, board_name: str) -> Dict[str, Any]:
        """
        Retrieves and validates the specification for a specific board.
        Raises ValueError if the board is not found.
        """
        pass
