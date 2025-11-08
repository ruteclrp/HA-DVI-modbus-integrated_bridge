from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class DviBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Create the config entry with whatever the user typed
            return self.async_create_entry(title="DVI Bridge", data=user_input)

        # Show form with manual port entry
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("port", default="/dev/ttyUSB0"): str,
                vol.Required("slave_id", default=16): int,
                vol.Optional("poll_interval", default=30): int,
            }),
            errors=errors,
        )
