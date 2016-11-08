# regrow
python script to convert FC1.0 to FC2.0 recipe format

# usage
python regro.py -f <inputfilename> -d <desciption>

# details

This script will convert this:

~~~~
...
00:00:00:00 SLIN 100000
000:00:00:00 SATM 26
000:00:00:00 SAHU 50.0
000:00:00:00 SACO 1000
000:18:00:00 SLIN 0
000:18:00:00 SATM 23
001:00:00:00 SLIN 100000
001:00:00:00 SATM 26
001:18:00:00 SLIN 0
001:18:00:00 SATM 23
...
~~~~

To this:

~~~~
 "_id": "a074e6b9292a4afd8228c983af48abda",
    "description": "sqroot simple green recipe",
    "operations": [
        [
            0,
            "light_illuminance",
            100000.0
        ],
        [
            0,
            "air_temperature",
            26.0
        ],
        [
            0,
            "air_humidity",
            50.0
        ],
        [
            0,
            "air_carbon_dioxide",
            1000.0
        ],
        [
            64800,
            "light_illuminance",
            0.0
        ],
        [
            64800,
            "air_temperature",
            23.0
        ],
...
~~~~

