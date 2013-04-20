import bottle
from bottle import route, run, template, abort, request
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base

#from objects import Sighting

# Set up SQLAlchemy
Base = declarative_base()


class Sighting(Base):
    __tablename__ = 'sightings'

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    user = Column(String)
    timestamp = Column(Integer)
    country = Column(String)
    stateprov = Column(String)

    def to_dict(self):
        return dict(lat=self.lat,
                    lng=self.lng,
                    user=self.user,
                    date=self.timestamp,
                    country=self.country,
                    stateprov=self.stateprov,
                    )
engine = create_engine('sqlite:///:memory:', echo=True)

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
bottle.install(plugin)


## Routes
@route('/sightings', method='POST')
def create_sighting(db):
    form_params = dict(
        lat=request.forms.get('lat'),
        lng=request.forms.get('lng'),
        user=request.forms.get('user'),
        country=request.forms.get('country'),
        stateprov=request.forms.get('stateprov'),
        timestamp=request.forms.get('timestamp'),
    )
    sighting = Sighting(**form_params)
    db.add(sighting)
    db.commit()

    return bottle.HTTPResponse(
        status=201,
        Location='/sightings/' + str(sighting.id)
    )


@route('/sightings/<id>', method='GET')
def get_sighting(id, db):
    sighting = db.query(Sighting).filter(Sighting.id == id).first()

    if sighting:
        return template('sighting', **sighting.to_dict())
    else:
        abort(404, 'Sighting not found')


@route('/sightings/<lat>/<long>', method='GET')
def get_local_sightings():
    pass


@route('/sightings', method='GET')
def get_latest_sightings():
    pass


run(host='localhost', port=8080, debug=True)
