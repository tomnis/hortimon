# tickscripts

- We use kapacitator tickscripts to define our alerting thresholds.
- https://docs.influxdata.com/kapacitor/v1.4/nodes/alert_node/

- We define a generic thresholding template in `generic_mean_alert.tick`
- https://docs.influxdata.com/kapacitor/v1.4/working/template_tasks/
- Particular values for instantiating this template are defined in the assorted json files
- To recreate all the kapacitator tasks:
  ```
  docker-compose run kapacitor-cli
  $ > cd /usr/local/tickscripts/
  $ > cd ./recreate.sh
  ```

- All alerts will write their notifications to /var/log/alerts (mounted in data/alerts on the host)
- We use `stateChangesOnly()` on our alert definitions.
  Notifications wil be sent only when the state changes, even if abnormal readings are observed
  for a long period of time.
