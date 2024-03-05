"""The SolarEdge integration."""
from __future__ import annotations

import socket

from requests.exceptions import ConnectTimeout, HTTPError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
import homeassistant.helpers.config_validation as cv

from sungrow_websocket import SungrowWebsocket
from .const import CONF_ADDRESS, DOMAIN, LOGGER

CONFIG_SCHEMA = cv.removed(DOMAIN, raise_if_present=False)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SunGrow from a config entry."""
#    try:
#        sg = SungrowWebsocket(entry.data[CONF_ADDRESS], locale="en_US")
#        data = sg.get_data()
#    except Exception as ex:
#        LOGGER.error("Could not retrieve details from SunGrow inverter")
#        raise ConfigEntryNotReady from ex
#
#    if "commonua" not in data:
#        LOGGER.error("Missing details data in SunGrow response")
#        raise ConfigEntryNotReady

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload SunGrow config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN][entry.entry_id]
    return unload_ok
