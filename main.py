import json

from flask import Flask, Response, make_response, send_file, request
from flask_cors import CORS

from constants import host, port
from core.Point import Point
from utils import get_altitude, interpolate, group

app = Flask(__name__)
CORS(app)

@app.route("/tiles/<z>/<x>/<y>", methods=["GET"])
def tiles(z, x, y):
  try:
    path = f'data/tiles/{z}/{x}/{y}.png'
    return send_file(path)
  except:
    return Response(status=404)

@app.route("/height/<lat>/<lon>", methods=["GET"])
def height(lat, lon):
  try:
    point = Point(lat, lon)
    return make_response(point.json(), 200)
  except:
    return Response(status=404)

@app.route("/height/raster/<z>/<x>/<y>", methods=["GET"])
def raster(z, x, y):
  try:
    path = f'data/rgb/{z}/{x}/{y}.png'
    return send_file(path)
  except:
    return Response(status=404)

@app.route("/height/profile", methods=["POST"])
def profile():
  try:
    body = group(json.loads(request.data))

    interpolated_path = []
    for line in body:
      interpolated_path.append(interpolate(line[0], line[1]))

    result = []
    for line in interpolated_path:
      for point in line:
        alt = int(get_altitude(point[1], point[0]))
        result.append([*point, alt])

    print(result)
    return make_response(json.dumps(result), 200)
  except:
    return Response(status=404)


if __name__ == '__main__':
  app.run(
    host=host,
    port=port,
    debug=True
  )


