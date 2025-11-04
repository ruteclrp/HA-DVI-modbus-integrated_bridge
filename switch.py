from homeassistant.components.switch import SwitchEntity

async def async_setup_entry(hass, entry, async_add_entities):
    instrument = hass.data["dvi_bridge"].get("instrument")
    switches = [
        DviSwitch("Heating element", 3, instrument),
        DviSwitch("Circ. pump warm side", 4, instrument),
    ]
    async_add_entities(switches)

class DviSwitch(SwitchEntity):
    def __init__(self, name, coil, instrument):
        self._attr_name = f"DVI {name}"
        self._coil = coil
        self._instrument = instrument
        self._state = False

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(
            self._instrument.write_bit, self._coil, 1
        )
        self._state = True

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(
            self._instrument.write_bit, self._coil, 0
        )
        self._state = False

    async def async_update(self):
        val = await self.hass.async_add_executor_job(
            self._instrument.read_bit, self._coil
        )
        self._state = bool(val)
