from influxdb import InfluxDBClient
import time
import random
import sys

"""
We monitor 4 environment types:
    flower_tent
    veg_tent
    clone_chamber
    clone_dome

Use this script to generate fake data as needed
"""

# upper and lower bounds for fake data
if "--abnormal" in sys.argv:
    bounds = {
        "clone_dome": {
            "temperature": [80, 90],
            "relative_humidity": [35, 55]
        },
        "clone_chamber": {
            "temperature": [55, 70],
            "relative_humidity": [85, 90]
        },
        "veg_tent": {
            "temperature": [85, 90],
            "relative_humidity": [35, 50]
        },
        "flower_tent": {
            "temperature": [80, 90],
            "relative_humidity": [60, 80]
        }
    }
else:
    bounds = {
        "clone_dome": {
            "temperature": [73, 77],
            "relative_humidity": [73, 85]
        },
        "clone_chamber": {
            "temperature": [64, 78],
            "relative_humidity": [48, 74]
        },
        "veg_tent": {
            "temperature": [65, 78],
            "relative_humidity": [48, 75]
        },
        "flower_tent": {
            "temperature": [59, 75],
            "relative_humidity": [25, 45]
        }
    }

def generate_fake_point(measurement, environment):
    """
    Generates a single fake point to write into influx
    """
    (lower_bound, upper_bound) = bounds[environment][measurement] 
    return {
        "measurement": measurement,
        "tags": {
            "environment": environment,
            "is_generated": True,
        },
        "fields": {
            "value": random.uniform(lower_bound, upper_bound)
        }
    }


def generate_data():
    """
    Generates the fake data we'll write. Creates 1 point for each measurement for each specified environment type.
    """
    measurements = ["temperature", "relative_humidity"]
    json_body = [ ]

    if "--flower" in sys.argv:
        for measurement in measurements:
            json_body.append(generate_fake_point(measurement, "flower_tent"))
    if "--veg" in sys.argv:
        for measurement in measurements:
            json_body.append(generate_fake_point(measurement, "veg_tent"))
    if "--clone" in sys.argv:
        for measurement in measurements:
            json_body.append(generate_fake_point(measurement, "clone_chamber"))
            json_body.append(generate_fake_point(measurement, "clone_dome"))

    return json_body

def main():
    """
    Usage: run with arguments of the environments to generate fake data for eg "--clone --abnormal"
    """
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')
    client.create_database('garden')

    while True:
        data = generate_data()
        print("writing data: " + str(data))
        client.write_points(data)
        time.sleep(10)

if __name__ == "__main__":
    main()    
