# hortimon mothership

Code for time series database and graphing server.

We run docker containers for influxdb and grafana.

An alternative architecture would use prometheus rather than influxdb. (pull vs push)


## Setup

- Export the following environment variables:
  - `TWILIO_ACCOUNT_SID` twilio credentials
  - `TWILIO_AUTH_TOKEN`
  - `TWILIO_SENDER` twilio number to send messages from, with country code. eg +12104563456
  - `TWILIO_NOTIFY_TO` comma-separated numbers to send notifications to
- Bring up the docker cluster `docker-compose up`
- (Optional) test that the sms notifier service is running:
  ```bash
  $> curl -XGET http://localhost:5000
  sms-notifier running in docker
  ```
- import alert tasks into kapacitor:
  - these alert tasks POST their json events to our notifier microservice.
  ```bash
  $ docker-compose run kapacitor-cli
  root@cafebabe:/# cd /usr/local/tickscripts
  root@cafebabe:/usr/local/tickscripts# ./recreate.sh

    ID                    Type      Status    Executing Databases and Retention Policies
    clone_humidity_alert  stream    enabled   true      ["garden"."autogen"]
    clone_temp_alert      stream    enabled   true      ["garden"."autogen"]
    flower_humidity_alert stream    enabled   true      ["garden"."autogen"]
    flower_temp_alert     stream    enabled   true      ["garden"."autogen"]
    veg_humidity_alert    stream    enabled   true      ["garden"."autogen"]
    veg_temp_alert        stream    enabled   true      ["garden"."autogen"]
  ```
- (Optional) create any other newly desired alerts
  - our template for kapacitor alerts is defined in `tickscripts/generic_mean_alert.tick`
  - create a new json file that provides all required variables.
    see examples in `tickscripts` directory.
  - define new kapacitor tasks and enable them:
    ```bash
    $ docker-compose run kapacitor-cli
    root@cafebabe:/# kapacitor define <alert_name> -template generic_mean_alert -vars /path/to/alert.json  -dbrp garden.autogen
    root@cafebabe:/# kapacitor enable <alert_name>
    ```


TODO
- anomaly detection. this could be interesting since we are dealing with a cyclical period
  
