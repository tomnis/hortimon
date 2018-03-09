# hortimon agent

Python code for reading temperature and humidity values from a raspberry pi.

A single pi zero should be able to pull data from multiple connected sensors
and write that data to the mothership. 

This should have the single responsibility of writing sensor data to the db.
All other analysis should take place elsewhere.

This should be implemented as a python script that doesnt have a while loop.
Invocation of that script will be controlled via cron job.

A nice feature to have would be a notification of a failed cron job. We would
like to be alerted quickly any time data collection fails.

Wired sensors are rated to remain accurate even with wires of ~100 meters.
We should confirm for ourselves, but it should be possible to connect several
wired sensors to a single pi that remains connected to wall power.

An alternative architecture would have multiple pis, each with a single sensor.
We could experiment with battery power and have small physical agents that could
be conveniently placed anywhere in the room.



