from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "dvi_bridge"

async def async_setup(hass: HomeAssistant, config: dict):
    """YAML setup (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from UI config flow (not shown here)."""
    hass.data.setdefault(DOMAIN, {})
    # Could initialize your Modbus instrument here and store in hass.data
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload integration."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
