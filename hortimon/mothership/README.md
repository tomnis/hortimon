# hortimon mothership

Code for time series database and graphing server.

We run docker containers for influxdb and grafana.

An alternative architecture would use prometheus rather than influxdb. (pull vs push)

TODO
- text alerts for thresholds. this can take the form of grafana webhooks, grafana email alerts,
  or possibly a cron job that simply reads the most recent values and uses twilio api
  the particular thresholds should probably be configurable somehow.
- anomaly detection. this could be interesting since we are dealing with a cyclical period
  
