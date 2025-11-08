from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import device_registry as dr
from homeassistant.const import Platform
from .modbus_bridge import DviModbusBridge
from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.NUMBER]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """YAML setup (not used)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DVI Bridge from config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create and store bridge instance
    port = entry.data["port"]
    slave_id = entry.data["slave_id"]
    bridge = DviModbusBridge(port, slave_id)
    hass.data[DOMAIN][entry.entry_id] = bridge

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload DVI Bridge."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def async_get_options_flow(config_entry):
    return OptionsFlowHandler(config_entry)

