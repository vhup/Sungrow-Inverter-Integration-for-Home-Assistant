# Sungrow Inverter Integration for Home Assistant

This repo contains my custom integration for Home Assistant for a mono-phased SunGrow inverter.

Known limitations: -It only works with mono-phase inverters... but feel free to improve it by extracting the (see https://knowledge-center.solaredge.com/sites/kc/files/se_monitoring_api.pdf for details on API response) -It has been tested only with one inverter... but I suppose that it will work with most mono-phased inverters

To install it, copy the "solardge" folder to <home_assistant_config_folder>/custom_components Then restart Home Assistant (just to be sure) and add the "SolarEdge" integration.
