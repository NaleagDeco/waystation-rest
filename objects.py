# import PIL
# import googlemaps
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date

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
