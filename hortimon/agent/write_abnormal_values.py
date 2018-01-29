import time
import random
from influxdb import InfluxDBClient


def write():
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "environment": "flower_tent",
            },
            "fields": {
                "value": random.uniform(91, 95)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "flower_tent",
            },
            "fields": {
                "value": random.uniform(78, 85)
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "environment": "veg_tent",
            },
            "fields": {
                "value": random.uniform(91, 95)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "veg_tent",
            },
            "fields": {
                "value": random.uniform(25, 35)
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "environment": "clone_incubator",
            },
            "fields": {
                "value": random.uniform(85, 90)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "clone_incubator",
            },
            "fields": {
                "value": random.uniform(40, 50)
            }
        }
    ]

    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.write_points(json_body)

def main():
    """
    Writes abnormal values for all sensors.
    """
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.create_database('garden')

    while True:
        print "writing abnormal data"
        write()
        time.sleep(10)

if __name__ == "__main__":
    main()    
