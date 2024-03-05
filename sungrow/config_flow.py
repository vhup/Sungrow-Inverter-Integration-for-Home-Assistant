"""Config flow for the SunGrow platform."""
from __future__ import annotations

from typing import Any

from requests.exceptions import ConnectTimeout, HTTPError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.util import slugify

from sungrow_websocket import SungrowWebsocket
from .const import CONF_ADDRESS, DEFAULT_NAME, DOMAIN


class SunGrowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._errors: dict[str, str] = {}

    @callback
    def _async_current_ip_address(self) -> set[str]:
        """Return the site_ids for the domain."""
        return {
            entry.data[CONF_ADDRESS]
            for entry in self._async_current_entries(include_ignore=False)
            if CONF_ADDRESS in entry.data
        }

    def _ip_address_in_configuration_exists(self, ip_address: str) -> bool:
        """Return True if site_id exists in configuration."""
        return ip_address in self._async_current_ip_address()

    def _check_ip_address(self, ip_address: str) -> bool:
        """Check if we can connect to the sunfrow inverter."""
        try:
            sg = SungrowWebsocket(ip_address, locale="en_US")
            data = sg.get_data()
            if 'commonua' not in data:
                self._errors[CONF_ADDRESS] = "unexpected_data"
                return False
        except:
            self._errors[CONF_ADDRESS] = "could_not_connect"
            return False
        return True

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step when user initializes a integration."""
        self._errors = {}
        if user_input is not None:
            #name = slugify(user_input.get(CONF_NAME, DEFAULT_NAME))
            name = user_input.get(CONF_NAME, DEFAULT_NAME)
            if self._ip_address_in_configuration_exists(user_input[CONF_ADDRESS]):
                self._errors[CONF_ADDRESS] = "already_configured"
            else:
                ip_address = user_input[CONF_ADDRESS]
                can_connect = await self.hass.async_add_executor_job(
                    self._check_ip_address, ip_address
                )
                if can_connect:
                    return self.async_create_entry(
                        title=name, data={CONF_ADDRESS: ip_address}
                    )
        else:
            user_input = {CONF_NAME: DEFAULT_NAME, CONF_ADDRESS: ""}
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=user_input.get(CONF_NAME, DEFAULT_NAME)
                    ): str,
                    vol.Required(CONF_ADDRESS, default=user_input[CONF_ADDRESS]): str,
                }
            ),
            errors=self._errors,
        )
