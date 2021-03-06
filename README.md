waystation-rest
===============

REST API for Waystation #spaceapps TO Hackathon project

Usage
-----

To add a Sighting:
`/sightings` (POST)
Parameters:
* lat
* lng
* timestamp
* name
* country
* stateprov
* city
* photo (optional, URL of associated photo)

Returns HTTP Code 201, Location: header contains URL for new sighting.

To view a particular sighting:
`/sightings/<id>` (GET)

To view 50 recent sightings:
`/sightings` (GET)

To view 50 recent sightings in your area:
`/sightings/<country>/<stateprov>/<city>` (GET)

To get a KML of all sighting points thus far:
`/sightings/kml` (GET)

Get a json set of the next few rise/set timestamps of the ISS for your location
`/iss/<timestamp>/<latitude>/<longitude>` (GET)
Returns an JSON array of "tuples", containing pairs of the following format:
`[<rise_timestamp>, <set_timestamp>]`

Installation
------------

1. Check out code
2. (Optional) create a python virtualenv w/ `virtualenv .env`
3. (Optional) active virtualenv w/ `source ./env/bin/activate`
4. Install dependencies with `pip install -r requirements.txt`
5. Run webserver with `python ./waystation-rest.py`

Default listener is on 0.0.0.0:3000
This software is Heroku-friendly.
