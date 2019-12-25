import os
import numpy as np

SAMPLES = 1201
NODATA  = -99999

TILESDIR = "data/tiles"
HGTDIR   = "data/hgt"
RGBDIR   = "data/rgb"

def get_altitude(lon: float, lat: float) -> int:
  hgt_file = get_file_name(lon, lat)
  if hgt_file:
    return read_altitude_from_file(hgt_file, lon, lat)
  return NODATA

def read_altitude_from_file(hgt_file: str, lon: float, lat: float) -> int:
  with open(hgt_file, 'rb') as hgt_data:
    elevations = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))

    lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
    lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))

    return elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)

def get_file_name(lon: float, lat: float):
  if lat >= 0:
    ns = 'N'
  elif lat < 0:
    ns = 'S'

  if lon >= 0:
    ew = 'E'
  elif lon < 0:
    ew = 'W'

  coordinate_structure = {
    'lat': abs(lat), 
    'lon': abs(lon), 
    'ns': ns, 
    'ew': ew
  }

  hgt_file = "%(ns)s%(lat)02d%(ew)s%(lon)03d.hgt" % coordinate_structure
  hgt_file_path = os.path.join(HGTDIR, hgt_file)

  if os.path.isfile(hgt_file_path):
    return hgt_file_path
  else:
    return None