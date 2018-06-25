#!/bin/bash

# use this script to recreate all the kapacitor alerts
# docker-compose run kapacitor-cli
# $ cd /usr/local/tickscripts
# $ ./recreate.sh
kapacitor delete tasks clone_chamber_temperature_alert clone_dome_temperature_alert flower_canopy_temperature_alert flower_roots_temperature_alert veg_canopy_temperature_alert
kapacitor delete tasks clone_chamber_humidity_alert clone_dome_humidity_alert flower_canopy_humidity_alert flower_roots_humidity_alert veg_canopy_humidity_alert
kapacitor define-template generic_mean_alert -tick /usr/local/tickscripts/generic_mean_alert.tick -type stream

kapacitor define clone_chamber_temperature_alert -template generic_mean_alert -vars /usr/local/tickscripts/clone_chamber_temperature.json  -dbrp garden.autogen
kapacitor define clone_dome_temperature_alert -template generic_mean_alert -vars /usr/local/tickscripts/clone_dome_temperature.json  -dbrp garden.autogen
kapacitor define flower_canopy_temperature_alert -template generic_mean_alert -vars /usr/local/tickscripts/flower_canopy_temperature.json  -dbrp garden.autogen
kapacitor define flower_roots_temperature_alert -template generic_mean_alert -vars /usr/local/tickscripts/flower_roots_temperature.json  -dbrp garden.autogen
kapacitor define veg_canopy_temperature_alert -template generic_mean_alert -vars /usr/local/tickscripts/veg_canopy_temperature.json  -dbrp garden.autogen

kapacitor define clone_chamber_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/clone_chamber_humidity.json  -dbrp garden.autogen
kapacitor define clone_dome_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/clone_dome_humidity.json  -dbrp garden.autogen
kapacitor define flower_canopy_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/flower_canopy_humidity.json  -dbrp garden.autogen
kapacitor define flower_roots_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/flower_roots_humidity.json  -dbrp garden.autogen
kapacitor define veg_canopy_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/veg_canopy_humidity.json  -dbrp garden.autogen

kapacitor enable clone_chamber_temperature_alert
kapacitor enable clone_dome_temperature_alert
kapacitor enable flower_canopy_temperature_alert
kapacitor enable flower_roots_temperature_alert
kapacitor enable veg_canopy_temperature_alert

kapacitor enable clone_chamber_humidity_alert
kapacitor enable clone_dome_humidity_alert
kapacitor enable flower_canopy_humidity_alert
kapacitor enable flower_roots_humidity_alert
kapacitor enable veg_canopy_humidity_alert

kapacitor list tasks
