from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import Entity
from .modbus_bridge import DviModbusBridge

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    bridge = DviModbusBridge("/dev/serial/by-id/...", 0x10)

    entities = []

    # FC04 sensors
    fc04_map = {
        0x01: ("CV Forward", "°C"),
        0x02: ("CV Return", "°C"),
        0x03: ("Storage tank VV", "°C"),
        0x05: ("Storage tank CV", "°C"),
        0x06: ("Evaporator", "°C"),
        0x07: ("Outdoor", "°C"),
        0x11: ("Compressor HP", "bar"),
        0x12: ("Compressor LP", "bar")
    }

    for reg, (name, unit) in fc04_map.items():
        entities.append(DviSensor(name, reg, bridge, unit, scale=0.1))

    # Coils
    coil_map = {
        0: "Soft starter Compressor",
        3: "Heating element",
        4: "Circ. pump warm side",
        12: "Circ. pump CV"
    }

    for index, name in coil_map.items():
        entities.append(DviCoil(name, index, bridge))

    async_add_entities(entities)

class DviSensor(SensorEntity):
    def __init__(self, name, register, bridge, unit, scale=1.0):
        self._name = name
        self._register = register
        self._bridge = bridge
        self._unit = unit
        self._scale = scale
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        return self._state

    @property
    def native_unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        raw = self._bridge.read_input(self._register)
        if raw is not None:
            self._state = round(raw * self._scale, 1)

class DviCoil(BinarySensorEntity):
    def __init__(self, name, index, bridge):
        self._name = name
        self._index = index
        self._bridge = bridge
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_update(self):
        bits = self._bridge.read_coils()
        if bits:
            self._state = bits[self._index]

