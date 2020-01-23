import math
from utils import get_elevation
from constants import NODATA

class Point(object):
  def __init__(self, x, y):
    self.x = float(x)
    self.y = float(y)
    self.a = int(get_elevation(self.y, self.x))

  def __add__(self, p):
    """
      Point(x1+x2, y1+y2)
    """
    return Point(self.x + p.x, self.y + p.y)

  def __sub__(self, p):
    """
      Point(x1-x2, y1-y2)
    """
    return Point(self.x - p.x, self.y - p.y)

  def __mul__(self, scalar):
    """
      Point(x1*x2, y1*y2)
    """
    return Point(self.x * scalar, self.y * scalar)

  def __div__(self, scalar):
    """
      Point(x1/x2, y1/y2)
    """
    return Point(self.x / scalar, self.y / scalar)

  def length(self):
    return math.sqrt(self.x ** 2 + self.y ** 2)

  def distance_to(self, p):
    """
      Calculate the distance between two points
    """
    return (self - p).length()

  def as_tuple(self):
    return (self.x, self.y, self.a)

  def as_json(self):
    return self.__dict__