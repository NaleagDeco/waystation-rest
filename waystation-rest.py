import os
import datetime
import json

import bottle
from bottle import template, abort, request, run
from bottle.ext import sqlalchemy
import ephem
import simplekml
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base

#from objects import Sighting

app = bottle.Bottle()
database_url = os.environ.get("DATABASE_URL", "sqlite:///:memory:")

NUM_SIGHTINGS = 50
UNIX_EPOCH = datetime.datetime(1970, 1, 1)

# Set up SQLAlchemy
Base = declarative_base()

name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   13111.17031100  .00008766  00000-0  14819-3 0  6495"
line2 = "2 25544  51.6472  31.2384 0010423 164.2523 280.5029 15.52398960825853"
iss = ephem.readtle(name, line1, line2)


class Sighting(Base):
    __tablename__ = 'sightings'

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    name = Column(String)
    timestamp = Column(Float)
    country = Column(String)
    stateprov = Column(String)
    city = Column(String)

    def to_dict(self):
        return dict(lat=self.lat,
                    lng=self.lng,
                    name=self.name,
                    timestamp=self.timestamp,
                    country=self.country,
                    stateprov=self.stateprov,
                    city=self.city,
                    )

    @property
    def coords(self):
        return (self.lat, self.lng)

    @property
    def location(self):
        return ", ".join([self.city, self.stateprov, self.country])

engine = create_engine(database_url, echo=True)

plugin = sqlalchemy.Plugin(
    # SQLAlchemy engine created with create_engine function.
    engine,
    # SQLAlchemy metadata, required only if create=True.
    Base.metadata,
    # Keyword used to inject session database in a route (default 'db')
    keyword='db',
    # If it is true, execute `metadata.create_all(engine)` when plugin is
    # applied (default False)
    create=True,
    # If it is true, plugin commit changes after route is executed
    # (default True)
    commit=True,
    # If it is true and keyword is not defined,
    # plugin uses **kwargs argument to inject session database (default False)
    use_kwargs=False,
)
app.install(plugin)


## Routes
@app.route('/', method='GET')
def hello():
    return "waystation-rest is running w/ DATABASE_URL = " + database_url


@app.route('/sightings', method='POST')
def create_sighting(db):
    form_params = dict(
        lat=float(request.forms.get('lat')),
        lng=float(request.forms.get('lng')),
        name=request.forms.get('name'),
        country=request.forms.get('country'),
        stateprov=request.forms.get('stateprov'),
        city=request.forms.get('city'),
        timestamp=float(request.forms.get('timestamp')),
    )
    sighting = Sighting(**form_params)
    db.add(sighting)
    db.commit()

    return bottle.HTTPResponse(
        status=201,
        Location='/sightings/' + str(sighting.id)
    )


@app.route('/sightings/<id>', method='GET')
def get_sighting(id, db):
    sighting = db.query(Sighting).filter(Sighting.id == id).first()

    if sighting:
        return template('sighting', **sighting.to_dict())
    else:
        abort(404, 'Sighting not found')


@app.route('/sightings/<country>/<stateprov>/<city>', method='GET')
def get_local_sightings(country, stateprov, city, db):
    sightings = db.query(Sighting).filter_by(country=country)
    sightings = sightings.filter_by(stateprov=stateprov)
    sightings = sightings.filter_by(city=city).order_by(Sighting.timestamp)

    return template('sightings', sightings=sightings[0:NUM_SIGHTINGS])


@app.route('/sightings', method='GET')
def get_latest_sightings(db):
    sightings = db.query(Sighting).order_by(Sighting.timestamp)

    return template('sightings', sightings=sightings[0:NUM_SIGHTINGS])


@app.route('/sightings/kml', method='GET')
def generate_kml(db):
    sightings = db.query(Sighting).order_by(Sighting.timestamp)

    kml = simplekml.Kml()
    for sighting in sightings:
        kml.newpoint(
            name=sighting.name,
            description=sighting.location,
            coords=[sighting.coords]
        )
    return kml.kml()


def deweird_date(x):
    # WTF are Ephemeral dates
    dt = x.datetime() - UNIX_EPOCH
    return dt.total_seconds()


@app.route('/iss/<timestamp:float>/<lat:float>/<lng:float>', method='GET')
def get_next_iss_pass(timestamp, lat, lng, db):

    passes = []

    location = ephem.Observer()
    location.lat = lat
    location.lon = lng
    location.date = ephem.Date(datetime.datetime.fromtimestamp(timestamp))
    passes.append(location.next_pass(iss))

    for _ in range(9):
        # 5th element in tuple is set time
        # We will add 1/2 hour to set time to predict the next pass
        location.date = passes[-1][4] + ephem.minute * 30
        mypass = location.next_pass(iss)
        if not mypass:
            # It looks like next_pass returns none if we've advanced
            # past a moment in time in which a prediction can be made.
            break
        passes.append(mypass)

    result = map(lambda x: (deweird_date(x[0]), deweird_date(x[4])), passes)
    return json.dumps(result)


run(app, host="0.0.0.0", port=os.environ.get("PORT", 3000))
