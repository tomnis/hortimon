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
                "value": random.uniform(60, 80)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "flower_tent",
            },
            "fields": {
                "value": random.uniform(25, 80)
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "environment": "veg_tent",
            },
            "fields": {
                "value": random.uniform(61, 80)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "veg_tent",
            },
            "fields": {
                "value": random.uniform(25, 80)
            }
        },
        {
            "measurement": "temperature",
            "tags": {
                "environment": "clone_incubator",
            },
            "fields": {
                "value": random.uniform(70,80)
            }
        },
        {
            "measurement": "relative_humidity",
            "tags": {
                "environment": "clone_incubator",
            },
            "fields": {
                "value": random.uniform(70,99)
            }
        }
    ]

    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.write_points(json_body)

def main():
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.create_database('garden')

    while True:
        print "writing data"
        write()
        time.sleep(10)

if __name__ == "__main__":
    main()    
