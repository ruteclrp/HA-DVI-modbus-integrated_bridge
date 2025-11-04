from homeassistant.components.switch import SwitchEntity
from .modbus_bridge import DviModbusBridge

# Map your writable Modbus registers to switch names
SWITCHES = {
    0x10A: "VV State",
    0x101: "CV State",
    0x102: "CV Curve",
    0x10B: "VV Setpoint",
    0x10F: "TV State"
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    bridge = DviModbusBridge("/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_COM_Port_48D874673036-if00", 0x10)
    switches = [DviSwitch(name, reg, bridge) for reg, name in SWITCHES.items()]
    async_add_entities(switches)

class DviSwitch(SwitchEntity):
    def __init__(self, name, register, bridge):
        self._name = name
        self._register = register
        self._bridge = bridge
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        self._bridge.write_register(self._register, 1)
        self._state = True

    async def async_turn_off(self, **kwargs):
        self._bridge.write_register(self._register, 0)
        self._state = False

    async def async_update(self):
        val = self._bridge.read_via_fc06(self._register)
        self._state = bool(val)
