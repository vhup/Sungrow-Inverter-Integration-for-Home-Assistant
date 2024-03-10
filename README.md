# Sungrow Inverter Integration for Home Assistant

This repo contains my custom integration for Home Assistant for a mono-phased SunGrow inverter.
It is based on "sungrow_websocket" (https://github.com/wallento/sungrow-websocket)

It brings the following sensors:
* Active power
* Array insulation resistance
* Bus voltage
* Daily power yield
* Grid frequency
* Inverter mode
* Lifetime energy
* Maximum apparent power
* Number of AFCI faults
* Phase A current
*Temperature
* Total apparent power
* Total DC power
* Total power factor
* Total reactive power
* Total running time
* Voltage AC
  
## Installation
To install it, copy the "sungrow" folder to <home_assistant_config_folder>/custom_components Then restart Home Assistant (just to be sure) and add the "SunGrow" integration.

## Known limitations:
* It only works with mono-phase inverters... but feel free to improve it by extracting the (see https://knowledge-center.solaredge.com/sites/kc/files/se_monitoring_api.pdf for details on API response) 
* It has been tested only with one inverter... but I suppose that it will work with most mono-phased inverters

