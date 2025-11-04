from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .modbus_bridge import DviModbusBridge
from .const import DOMAIN

FC04_SENSORS = {
    0x01: ("CV Forward", "°C", 0.1),
    0x02: ("CV Return", "°C", 0.1),
    0x03: ("Storage tank VV", "°C", 0.1),
    0x05: ("Storage tank CV", "°C", 0.1),
    0x06: ("Evaporator", "°C", 0.1),
    0x07: ("Outdoor", "°C", 0.1),
    0x11: ("Compressor HP", "bar", 0.1),
    0x12: ("Compressor LP", "bar", 0.1)
}

COIL_SENSORS = {
    0: "Soft starter Compressor",
    3: "Heating element",
    4: "Circ. pump warm side",
    12: "Circ. pump CV"
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    port = entry.data["port"]
    slave_id = entry.data["slave_id"]

    # Create and store bridge instance
    bridge = DviModbusBridge(port, slave_id)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = bridge

    entities = []

    for reg, (name, unit, scale) in FC04_SENSORS.items():
        entities.append(DviSensor(name, reg, bridge, unit, scale))

    for index, name in COIL_SENSORS.items():
        entities.append(DviCoil(name, index, bridge))

    async_add_entities(entities)

class DviSensor(SensorEntity):
    def __init__(self, name, register, bridge, unit, scale=1.0):
        self._attr_name = name
        self._register = register
        self._bridge = bridge
        self._attr_native_unit_of_measurement = unit
        self._scale = scale
        self._attr_native_value = None

    async def async_update(self):
        raw = self._bridge.read_input(self._register)
        if raw is not None:
            self._attr_native_value = round(raw * self._scale, 1)

class DviCoil(BinarySensorEntity):
    def __init__(self, name, index, bridge):
        self._attr_name = name
        self._index = index
        self._bridge = bridge
        self._attr_is_on = None

    async def async_update(self):
        bits = self._bridge.read_coils()
        if bits and self._index < len(bits):
            self._attr_is_on = bool(bits[self._index])
