import json

from flask import Flask, make_response, Response, request
from flask_cors import CORS

from constants import ADDR, LOGO
from src.Core.Point import Point
from src.Core.Tile import Tile

from utils import *
# [[[30.51057815551758, 50.422956317144944], [30.571002960205078, 50.422956317144944], [30.571002960205078, 50.46285884285004], [30.51057815551758, 50.46285884285004], [30.51057815551758, 50.422956317144944]]]

app = Flask(__name__)
CORS(app)

print(LOGO)

@app.route("/tiles/<zoom>/<x>/<y>", methods=["GET"])
def tiles(zoom, x, y):
  try:
    point = Tile(zoom, x, y)
    return make_response(point.as_json(), 200)
  except Exception as e:
    print(e)
    return Response(status=404)

@app.route("/height/<lat>/<lon>", methods=["GET"])
def height(lat, lon):
  try:
    alt = { "alt": int(get_elevation(lon, lat)) }
    return make_response(alt, 200)
  except Exception as e:
    print(e)
    return Response(status=404)

@app.route("/height/profile", methods=["POST"])
def profile():
  try:
    body = group(json.loads(request.data))

    interpolated_path = []
    for line in body:
      point1 = list(line[0].values())
      point2 = list(line[1].values())

      interpolated_path.append(interpolate_path(point1, point2))

    result = []
    for line in interpolated_path:
      for point in line:
        alt = int(get_elevation(point[1], point[0]))
        result.append([*point, alt])

    return make_response(json.dumps(remove_duplicates(result)), 200)
  except Exception as e:
    print(e)
    return Response(status=404)

@app.route("/tiles/export", methods=["POST"])
def export():
  try:
    body = group(json.loads(request.data)[0])

    out = []

    for side in body:
      p = interpolate_path(side[0], side[1])
      out.append(p)

    for side in out:
      for n in side:
        idx = side.index(n)
        side[idx] = [*side[idx], int(get_elevation(*side[idx]))]

    return make_response({ "result": out }, 200)
  except Exception as e:
    print(e)
    return Response(status=404)

@app.route("/distance", methods=["POST"])
def distance():
  try:
    body = pairwise(json.loads(request.data))

    for line in body:
      p1 = line[0]
      p2 = line[1]

      out = {
        "distance": haversine_gc(*p1, *p2),
        "bearing": calc_bearing(p1, p2)
      }

    return make_response(out, 200)
  except Exception as e:
    print(e)
    return Response(status=404)

if __name__ == "__main__":
  app.run(*ADDR, True)



  


