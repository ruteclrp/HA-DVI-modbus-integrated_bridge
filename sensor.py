from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS

async def async_setup_entry(hass, entry, async_add_entities):
    instrument = hass.data["dvi_bridge"].get("instrument")
    sensors = [
        DviSensor("CV Forward", 0x01, TEMP_CELSIUS, instrument),
        DviSensor("CV Return", 0x02, TEMP_CELSIUS, instrument),
    ]
    async_add_entities(sensors, update_before_add=True)

class DviSensor(SensorEntity):
    def __init__(self, name, register, unit, instrument):
        self._attr_name = f"DVI {name}"
        self._register = register
        self._unit = unit
        self._instrument = instrument
        self._state = None

    @property
    def native_value(self):
        return self._state

    @property
    def native_unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        # Run blocking Modbus call in executor
        val = await self.hass.async_add_executor_job(
            self._instrument.read_register, self._register, 0, 4
        )
        self._state = val * 0.1
