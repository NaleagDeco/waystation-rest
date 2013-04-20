import os
import bottle
from bottle import template, abort, request, run
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base

#from objects import Sighting

app = bottle.Bottle()
database_url = os.environ.get("DATABASE_URL", "sqlite:///:memory:")

NUM_SIGHTINGS = 50

# Set up SQLAlchemy
Base = declarative_base()


class Sighting(Base):
    __tablename__ = 'sightings'

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    name = Column(String)
    timestamp = Column(Integer)
    country = Column(String)
    stateprov = Column(String)
    city = Column(String)

    def to_dict(self):
        return dict(lat=self.lat,
                    lng=self.lng,
                    name=self.name,
                    date=self.timestamp,
                    country=self.country,
                    stateprov=self.stateprov,
                    city=self.city,
                    )
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
@app.route('/sightings', method='POST')
def create_sighting(db):
    form_params = dict(
        lat=request.forms.get('lat'),
        lng=request.forms.get('lng'),
        name=request.forms.get('name'),
        country=request.forms.get('country'),
        stateprov=request.forms.get('stateprov'),
        city=request.forms.get('city'),
        timestamp=request.forms.get('timestamp'),
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


run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
