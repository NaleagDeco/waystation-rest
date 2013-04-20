import bottle
from bottle import route, run, template, abort
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from objects import Sighting

# Set up SQLAlchemy
Base = declarative_base()
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
def create_sighting():
    sighting = Sighting()


@route('/sightings/<id>', method='GET')
def get_sighting(id, db):
    sighting = db.query(Sighting).filter(Sighting.id == id)

    if sighting:
        return template('sighting', kwargs=sighting.to_dict())
    else:
        abort('404')


@route('/sightings/<lat>/<long>', method='GET')
def get_local_sightings():
    pass


@route('/sightings', method='GET')
def get_latest_sightings():
    pass


run(host='localhost', port=8080, debug=True)
