import os
import math
import numpy as np

SAMPLES = 1201
NODATA = -32768

TILESDIR = "data/tiles"
HGTDIR = "data/srtm"
RGBDIR = "data/rgb"

def get_altitude(lon: float, lat: float):
	hgt_file = get_file_name(lon, lat)
	if hgt_file:
		return read_altitude_from_file(hgt_file, lon, lat)
	return NODATA

def read_altitude_from_file(hgt_file: str, lon: float, lat: float):
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

def deg2num(lat_deg: float, lon_deg: float, zoom: int) -> tuple:
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = int((lon_deg + 180.0) / 360.0 * n)
	ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
	return xtile, ytile

def get_index(target, iter):
	return iter.index(target)

def get_tail(iter):
	return iter[len(iter) - 1]

def filtered(target, iter):
	return list(filter(lambda x: x == target,iter))

def lerp(v0, v1, i):
	return v0 + i * (v1 - v0)

def interpolate(p1, p2, parts=32):
	return list(reversed([
		(lerp(p1[0], p2[0], 1. / parts * i),
		 lerp(p1[1], p2[1], 1. / parts * i))
		for i in range(parts + 1)
	]))

def split_half(_lon0: float, _lon1: float, _lat0: float, _lat1: float) -> list:
	return list(reversed(((_lat0 + _lat1) / 2, (_lon0 + _lon1) / 2)))

def group(arr):
	a = list(reversed(arr))
	return list(zip(a, a[1:] + a[:1]))

def remove_duplicates(values: list) -> list:
	out = []
	for n in values:
		if n not in out:
			out.append(n)
	return out