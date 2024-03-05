"""Support for SunGrow API."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfElectricPotential,UnitOfTemperature,UnitOfTime,UnitOfFrequency,UnitOfElectricCurrent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import CONF_ADDRESS, DOMAIN
from .coordinator import SunGrowDataService
from sungrow_websocket import SungrowWebsocket

@dataclass(frozen=True)
class SunGrowSensorEntityRequiredKeyMixin:
    """Sensor entity description with json_key for SunGrow."""
    json_key: str


@dataclass(frozen=True)
class SunGrowSensorEntityDescription(
    SensorEntityDescription, SunGrowSensorEntityRequiredKeyMixin
):
    """Sensor entity description for SunGrow."""


SENSOR_TYPES = [
    SunGrowSensorEntityDescription(
        key="running_state",
        json_key="running_state",
        icon="mdi:cog-outline",
        translation_key="running_state",
        entity_registry_enabled_default=False,
    ),
    SunGrowSensorEntityDescription(
        key="total_yield",
        json_key="total_yield",
        translation_key="total_yield",
        icon="mdi:solar-power",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SunGrowSensorEntityDescription(
        key="total_active_power",
        json_key="total_active_power",
        translation_key="total_active_power",
        icon="mdi:solar-power",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    SunGrowSensorEntityDescription(
        key="commonua",
        json_key="commonua",
        translation_key="commonua",
        icon="mdi:sine-wave",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SunGrowSensorEntityDescription(
        key="air_tem_inside_machine",
        json_key="air_tem_inside_machine",
        translation_key="air_tem_inside_machine",
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SunGrowSensorEntityDescription(
        key="total_grid_running_time",
        json_key="total_grid_running_time",
        translation_key="total_grid_running_time",
        icon="mdi:timer-cog-outline",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SunGrowSensorEntityDescription(
        key="daily_power_yield",
        json_key="daily_power_yield",
        translation_key="daily_power_yield",
        icon="mdi:solar-power",
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SunGrowSensorEntityDescription(
        key="bus_voltage",
        json_key="bus_voltage",
        translation_key="bus_voltage",
        icon="mdi:flash-triangle-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SunGrowSensorEntityDescription(
        key="square_array_insulation_impedance",
        json_key="square_array_insulation_impedance",
        translation_key="square_array_insulation_impedance",
        icon="mdi:resistor",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SunGrowSensorEntityDescription(
        key="total_dcpower",
        json_key="total_dcpower",
        translation_key="total_dcpower",
        icon="mdi:solar-power",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    SunGrowSensorEntityDescription(   # kvar
        key="total_reactive_power",
        json_key="total_reactive_power",
        translation_key="total_reactive_power",
        icon="mdi:solar-power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.REACTIVE_POWER,
    ),
    SunGrowSensorEntityDescription(   # kVA
        key="total_apparent_power",
        json_key="total_apparent_power",
        translation_key="total_apparent_power",
        icon="mdi:solar-power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.APPARENT_POWER,
    ),
    SunGrowSensorEntityDescription(
        key="total_power_factor",
        json_key="total_power_factor",
        translation_key="total_power_factor",
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER_FACTOR,
    ),
    SunGrowSensorEntityDescription(
        key="grid_frequency",
        json_key="grid_frequency",
        translation_key="grid_frequency",
        icon="mdi:sine-wave",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
    ),
    SunGrowSensorEntityDescription(
        key="fragment_run_type1",
        json_key="fragment_run_type1",
        translation_key="fragment_run_type1",
        icon="mdi:solar-power",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
    ),
    SunGrowSensorEntityDescription(
        key="measuring_point_afd",
        json_key="measuring_point_afd",
        translation_key="measuring_point_afd",
        icon="mdi:note-alert-outline",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SunGrowSensorEntityDescription(
        key="maximum_apparent_power_siwhfgqy",
        json_key="maximum_apparent_power_siwhfgqy",
        translation_key="maximum_apparent_power_siwhfgqy",
        icon="mdi:solar-power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.APPARENT_POWER,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    sensor_factory = SunGrowSensorFactory(hass, entry.data[CONF_ADDRESS])
    for service in sensor_factory.all_services:
        service.async_setup()
        await service.coordinator.async_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        sensor = sensor_factory.create_sensor(sensor_type)
        if sensor is not None:
            entities.append(sensor)
    async_add_entities(entities)


class SunGrowSensorFactory:
    """Factory which creates sensors based on the sensor_key."""

    def __init__(self, hass: HomeAssistant, ip_address: str) -> None:
        """Initialize the factory."""
        inverter = SunGrowDataService(hass, ip_address)
        self.all_services = [inverter]

        self.services: dict[
            str,
            tuple[
                type[SunGrowSensorEntity],
                SunGrowDataService,
            ],
        ] = {}
        for key in ("commonua", "total_active_power", "air_tem_inside_machine", "total_yield", "running_state", 'total_grid_running_time', 'daily_power_yield', 'bus_voltage', 'square_array_insulation_impedance', 'total_dcpower', 'total_reactive_power', 'total_apparent_power', 'total_power_factor', 'grid_frequency', 'fragment_run_type1', 'measuring_point_afd', 'maximum_apparent_power_siwhfgqy'):
            self.services[key] = (SunGrowSensor, inverter)


    def create_sensor(
        self, sensor_type: SunGrowSensorEntityDescription
    ) -> SunGrowSensor:
        """Create and return a sensor based on the sensor_key."""
        sensor_class, service = self.services[sensor_type.key]
        return sensor_class(sensor_type, service)


class SunGrowSensor(
    CoordinatorEntity[DataUpdateCoordinator[None]], SensorEntity
):
    _attr_has_entity_name = True

    entity_description: SunGrowSensorEntityDescription

    def __init__(
        self,
        description: SunGrowSensorEntityDescription,
        data_service: SunGrowDataService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(data_service.coordinator)
        self.entity_description = description
        self.data_service = data_service
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, data_service.ip_address)}, manufacturer="SunGrow"
        )

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        if not self.data_service.ip_address:
            return None
        return f"{self.data_service.ip_address}_{self.entity_description.key}"

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the state attributes."""
        return self.data_service.attributes.get(self.entity_description.json_key)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.data_service.data.get(self.entity_description.json_key)

