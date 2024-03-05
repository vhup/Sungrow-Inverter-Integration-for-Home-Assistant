"""Constants for the SunGrow Inverter"""
from datetime import timedelta
import logging

# domain needs to be the same as the one in manifest.json.
# it also need to be the same as the folder name, otherwise the strings.json will not be found
# it has also to be the same as the folder name of brand (to be able to fetch the logo)
DOMAIN = "sungrow"

LOGGER = logging.getLogger(__package__)

# Config for sungrow inverter
CONF_ADDRESS = "ip_address"
DEFAULT_NAME = "SunGrow Inverter"

INVERTER_UPDATE_DELAY = timedelta(seconds=15)

