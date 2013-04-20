waystation-rest
===============

REST API for Waystation #spaceapps TO Hackathon project

To add a Sighting:
/sightings (POST)
Parameters:
* lat
* lng
* timestamp
* name
* country
* stateprov
* city
Returns HTTP Code 201, Location: header contains URL for new sighting.

To view a particular sighting:
/sightings/<id> (GET)

To view 50 recent sightings:
/sightings (GET)

To view 50 recent sightings in your area:
/sightings/<country>/<stateprov>/<city> (GET)
