"""Provides the data update coordinators for SunGrow."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from typing import Any

from stringcase import snakecase

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from sungrow_websocket import SungrowWebsocket, InverterItem

from .const import (
    LOGGER,
    INVERTER_UPDATE_DELAY
)


class SunGrowDataService(ABC):
    """Get and update the latest data."""

    coordinator: DataUpdateCoordinator[None]

    def __init__(self, hass: HomeAssistant, ip_address: str ) -> None:
        """Initialize the data object."""
        self.ip_address = ip_address
        self.data: dict[str, Any] = {}
        self.attributes: dict[str, Any] = {}
        self.hass = hass

    @callback
    def async_setup(self) -> None:
        """Coordinator creation."""
        self.coordinator = DataUpdateCoordinator(
            self.hass,
            LOGGER,
            name=str(self),
            update_method=self.async_update_data,
            update_interval=self.update_interval,
        )

    @property
    def update_interval(self) -> timedelta:
        """Update interval."""
        return INVERTER_UPDATE_DELAY

    def update(self) -> None:
        """Update the data from the SunGrow inverter."""
        try:
            #now = datetime.now()
            sg = SungrowWebsocket(self.ip_address, locale="en_US")
            dataFromSunGrow = sg.get_data()
            LOGGER.info(dataFromSunGrow)
        except KeyError as ex:
            raise UpdateFailed("Missing inverter data, skipping update") from ex
        self.data = {}
        self.attributes = {}
        try:
            if "commonua" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["commonua"]
                self.data["commonua"] = item.value
            if "total_yield" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_yield"]
                self.data["total_yield"] = item.value
            if "running_state" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["running_state"]
                self.data["running_state"] = item.value
            if "total_active_power" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_active_power"]
                self.data["total_active_power"] = item.value
            if "air_tem_inside_machine" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["air_tem_inside_machine"]
                self.data["air_tem_inside_machine"] = item.value
            if "total_grid_running_time" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_grid_running_time"]
                self.data["total_grid_running_time"] = item.value
            if "daily_power_yield" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["daily_power_yield"]
                self.data["daily_power_yield"] = item.value
            if "bus_voltage" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["bus_voltage"]
                self.data["bus_voltage"] = item.value
            if "square_array_insulation_impedance" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["square_array_insulation_impedance"]
                self.data["square_array_insulation_impedance"] = item.value
            if "total_dcpower" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_dcpower"]
                self.data["total_dcpower"] = item.value
            if "total_reactive_power" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_reactive_power"]
                self.data["total_reactive_power"] = item.value
            if "total_apparent_power" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_apparent_power"]
                self.data["total_apparent_power"] = item.value
            if "total_power_factor" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["total_power_factor"]
                self.data["total_power_factor"] = item.value
            if "grid_frequency" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["grid_frequency"]
                self.data["grid_frequency"] = item.value
            if "fragment_run_type1" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["fragment_run_type1"]
                self.data["fragment_run_type1"] = item.value
            if "measuring_point_afd" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["measuring_point_afd"]
                self.data["measuring_point_afd"] = item.value
            if "maximum_apparent_power_siwhfgqy" in dataFromSunGrow:
                item: InverterItem = dataFromSunGrow["maximum_apparent_power_siwhfgqy"]
                self.data["maximum_apparent_power_siwhfgqy"] = item.value
        except Exception as ex:
            raise UpdateFailed("Not able to extract data, skipping update") from ex
        LOGGER.debug("Updated SunGrow inverter details: %s, %s", self.data, self.attributes)

    async def async_update_data(self) -> None:
        """Update data."""
        await self.hass.async_add_executor_job(self.update)





