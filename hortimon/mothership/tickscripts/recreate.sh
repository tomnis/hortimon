#!/bin/bash

kapacitor delete tasks clone_temp_alert flower_temp_alert veg_temp_alert
kapacitor delete tasks clone_humidity_alert flower_humidity_alert veg_humidity_alert
kapacitor define-template generic_mean_alert -tick /usr/local/tickscripts/generic_mean_alert.tick -type stream
kapacitor define clone_temp_alert -template generic_mean_alert -vars /usr/local/tickscripts/clone_temperature.json  -dbrp garden.autogen
kapacitor define flower_temp_alert -template generic_mean_alert -vars /usr/local/tickscripts/flower_temperature.json  -dbrp garden.autogen
kapacitor define veg_temp_alert -template generic_mean_alert -vars /usr/local/tickscripts/veg_temperature.json  -dbrp garden.autogen
kapacitor define clone_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/clone_temperature.json  -dbrp garden.autogen
kapacitor define flower_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/flower_temperature.json  -dbrp garden.autogen
kapacitor define veg_humidity_alert -template generic_mean_alert -vars /usr/local/tickscripts/veg_humidity.json  -dbrp garden.autogen
kapacitor enable clone_temp_alert
kapacitor enable veg_temp_alert
kapacitor enable flower_temp_alert
kapacitor enable clone_humidity_alert
kapacitor enable veg_humidity_alert
kapacitor enable flower_humidity_alert
kapacitor list tasks
