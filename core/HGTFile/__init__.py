import os
import struct

class HGTFile:
  def __init__(self, path):
    self.path = path

    self.lat = 0
    self.lon = 0

    self.parse_name()

  def parse_name(self):
    dir, file_name = os.path.split(self.path)
    stem, suffix = os.path.splitext(file_name)

    try:
      if len(stem) != 7:
        raise ValueError

      lat = int(stem[1:3])
      lon = int(stem[4:7])

      if stem[0] == "N":
        pass
      elif stem[0] == "S":
        lat = -lat
      else:
        raise ValueError

      if stem[3] == "W":
        lon = -lon
      elif stem[3] == "E":
        pass
      else:
        raise ValueError
    except ValueError:
      print("Invalid file name for HGT file: %s" % file_name)

    self.lat = lat
    self.lat = lon

  def read(self):
    f = open(self.path, "rb")
    f.seek(0, 2)

    length = f.tell()
    f.seek(0, 0)

    if length == (1201 * 1201 * 2):
      size = 1201
    elif length == (3601 * 3601 * 2):
      size = 3601
    else:
      print("Invalid size for HGT file '%s'" % self.path)

    format = ">" + ("h" * size)
    d = []
    i = 0

    while i < size:
      values = struct.unpack(format, f.read(size * 2))
      d.append(values)
      i += 1

    f.close()
    return d