import os
import math
import time
import numpy as np

from constants import DATA, SRTM, SAMPLES, NODATA, R

def get_elevation(lon, lat):
  hgt_file = get_file_name(float(lon), float(lat))
  if hgt_file:
    return read_elevation_from_file(hgt_file, float(lon), float(lat))
  return NODATA

def read_elevation_from_file(hgt_file, lon, lat):
  with open(hgt_file, 'rb') as hgt_data:
    #HGT is 16bit signed integer(i2) - big endian(>)
    elevations = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES * SAMPLES).reshape((SAMPLES, SAMPLES))

    lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
    lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))

    return elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)

def get_file_name(lon, lat):
  if lat >= 0:
    ns = 'N'
  elif lat < 0:
    ns = 'S'

  # HGT is 16bit signed integer(i2) - big endian(>)

  if lon >= 0:
    ew = 'E'
  elif lon < 0:
    ew = 'W'

  hgt_file = "%(ns)s%(lat)02d%(ew)s%(lon)03d.hgt" % {'lat': abs(lat), 'lon': abs(lon), 'ns': ns, 'ew': ew}
  hgt_file_path = os.path.join(f'{DATA}/{SRTM}/', hgt_file)

  if os.path.isfile(hgt_file_path):
    return hgt_file_path
  else:
    return None

def lerp(v0, v1, i):
  return v0 + i * (v1 - v0)

def interpolate_path(p1, p2, parts=16):
  return list(
    reversed([
      (lerp(p1[0], p2[0], 1. / parts * i),
       lerp(p1[1], p2[1], 1. / parts * i))
      for i in range(parts + 1)
    ])
  )

def group(arr):
  a = list(reversed(arr))
  return list(zip(a, a[1:] + a[:1]))

def pairwise(seq):
  """
  Pair an iterable (1, 2, 3, 4) -> ((1, 2), (2, 3), (3, 4))
  """
  for i in range(0, len(seq) - 1):
    yield [seq[i], seq[i + 1]]

def remove_duplicates(values):
  out = []
  for n in values:
    if n not in out:
      out.append(n)
  return out

def get_unix_timestamp():
  return int(time.time())

def haversine_gc(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points
  on the earth (specified in decimal degrees)

  All args must be of equal length.
  """
  lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2

  c = 2 * np.arcsin(np.sqrt(a))
  km = R * c

  return km

def haversine_est(lon1, lat1, lon2, lat2):
  """
  Estimation with equirectangular distance approximation.
  Since the distance is relatively small, you can use the equirectangular distance approximation.
  This approximation is faster than using the Haversine formula.
  So, to get the distance from your reference point (lat1/lon1) to the point your are testing (lat2/lon2),
  use the formula below.
  Important Note: you need to convert all lat/lon points to radians:
  """
  lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

  x = (lon2 - lon1) * np.cos(0.5 * (lat2 + lat1))
  y = lat2 - lat1

  km = R * np.sqrt(x * x + y * y)

  return km

def calc_bearing(p1, p2):
  lat1 = math.radians(p1[1])
  lat2 = math.radians(p2[1])

  difflon = math.radians(p2[0] - p1[0])

  x = math.sin(difflon) * math.cos(lat2)
  y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(difflon))

  bearing = math.atan2(x, y)
  bearing = math.degrees(bearing)

  return (bearing + 360) % 360
