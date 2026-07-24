from pydantic import BaseModel

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
