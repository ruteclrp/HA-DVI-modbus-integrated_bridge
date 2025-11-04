from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .modbus_bridge import DviModbusBridge
from .const import DOMAIN

SWITCHES = {
    0x10A: "VV State",
    0x101: "CV State",
    0x102: "CV Curve",
    0x10B: "VV Setpoint",
    0x10F: "TV State"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    bridge = hass.data[DOMAIN][entry.entry_id]
    entities = [DviSwitch(name, reg, bridge) for reg, name in SWITCHES.items()]
    async_add_entities(entities)

class DviSwitch(SwitchEntity):
    def __init__(self, name, register, bridge):
        self._attr_name = name
        self._register = register
        self._bridge = bridge
        self._attr_is_on = None

    async def async_turn_on(self, **kwargs):
        self._bridge.write_register(self._register, 1)
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        self._bridge.write_register(self._register, 0)
        self._attr_is_on = False

    async def async_update(self):
        val = self._bridge.read_via_fc06(self._register)
        self._attr_is_on = bool(val)
