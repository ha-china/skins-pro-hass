"""Config flow for Skins Pro."""
from __future__ import annotations

from homeassistant import config_entries

DOMAIN = "skins_pro"


class SkinsProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Skins Pro."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Skins Pro", data={})

        return self.async_show_form(step_id="user")
