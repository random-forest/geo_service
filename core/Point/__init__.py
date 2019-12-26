import json
from utils import get_altitude, NODATA

class Point:
  def __init__(self, lat, lon):
    self.lat = float(lat)
    self.lon = float(lon)
    self.alt = int(get_altitude(self.lon, self.lat))

  def json(self):
    return self.__dict__