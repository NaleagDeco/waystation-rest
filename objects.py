# import PIL
# import googlemaps


def Sighting(Object):
    def __init__(self, lat, long, user, photo, timestamp, country, stateprov):
        self.lat = lat
        self.long = long
        self.user = user
        self.picture = photo
        self.timestamp = timestamp
        self.country = country
        self.stateprov = stateprov

    def lat():
        doc = "The lat property."
        def fget(self):
            return self._lat
        def fset(self, value):
            self._lat = value
        def fdel(self):
            del self._lat
        return locals()
    lat = property(**lat())


    def long():
        doc = "The long property."
        def fget(self):
            return self._long
        def fset(self, value):
            self._long = value
        def fdel(self):
            del self._long
        return locals()
    long = property(**long())

    def user():
        doc = "The user property."
        def fget(self):
            return self._user
        def fset(self, value):
            self._user = value
        def fdel(self):
            del self._user
        return locals()
    user = property(**user())

    def photo():
        doc = "The photo property."
        def fget(self):
            return self._photo
        def fset(self, value):
            self._photo = value
        def fdel(self):
            del self._photo
        return locals()
    photo = property(**photo())

    def timestamp():
        doc = "The timestamp property."
        def fget(self):
            return self._timestamp
        def fset(self, value):
            self._timestamp = value
        def fdel(self):
            del self._timestamp
        return locals()
    timestamp = property(**timestamp())

    def country():
        doc = "The country property."
        def fget(self):
            return self._country
        def fset(self, value):
            self._country = value
        def fdel(self):
            del self._country
        return locals()
    country = property(**country())

    def stateprov():
        doc = "The stateprov property."
        def fget(self):
            return self._stateprov
        def fset(self, value):
            self._stateprov = value
        def fdel(self):
            del self._stateprov
        return locals()
    stateprov = property(**stateprov())
