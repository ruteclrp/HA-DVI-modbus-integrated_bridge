from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class DviBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="DVI Bridge", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("port", default="/dev/ttyUSB0"): str,
                vol.Required("slave_id", default=16): int,
                vol.Optional("poll_interval", default=30): int,
            }),
            errors=errors,
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("port", default=self.config_entry.data.get("port", "/dev/ttyUSB0")): str,
                vol.Required("slave_id", default=self.config_entry.data.get("slave_id", 16)): int,
                vol.Optional("poll_interval", default=self.config_entry.data.get("poll_interval", 30)): int,
            }),
        )
