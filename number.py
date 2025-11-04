from homeassistant.components.number import NumberEntity
from .modbus_bridge import DviModbusBridge

# Map writable registers to (name, min, max, step, scale)
NUMBER_REGISTERS = {
    0x102: ("CV Curve", 0, 100, 1, 1),       # cvcurve
    0x10B: ("VV Setpoint", 0, 100, 1, 1),     # vvsetpoint
    0x10C: ("VV Schedule", 0, 100, 1, 1),     # optional
    0x03:  ("CV Setpoint", 0, 100, 1, 1),     # cv_setpoint (if writable)
    0x04:  ("Night Setback", 0, 10, 0.5, 1),  # cv_night_setback
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    bridge = DviModbusBridge("/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_COM_Port_48D874673036-if00", 0x10)
    entities = [DviNumber(name, reg, bridge, min_val, max_val, step, scale)
                for reg, (name, min_val, max_val, step, scale) in NUMBER_REGISTERS.items()]
    async_add_entities(entities)

class DviNumber(NumberEntity):
    def __init__(self, name, register, bridge, min_val, max_val, step, scale):
        self._attr_name = name
        self._register = register
        self._bridge = bridge
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._scale = scale
        self._attr_native_value = None

    async def async_update(self):
        val = self._bridge.read_via_fc06(self._register)
        if val is not None:
            self._attr_native_value = round(val / self._scale, 2)

    async def async_set_native_value(self, value: float):
        scaled = int(value * self._scale)
        self._bridge.write_register(self._register, scaled)
        self._attr_native_value = value
