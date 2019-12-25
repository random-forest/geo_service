from flask import Flask, Response, make_response
from flask_cors import CORS
from constants import *

app = Flask(__name__)
CORS(app)

@app.route("/tiles/<z>/<x>/<y>", methods=["GET"])
def tiles(z, x, y):
  try:
    path = f'data/tiles/{z}/{x}/{y}.png'
    return make_response({}, 200)
  except:
    return Response(status=404)

@app.route("/height/<lat>/<lon>")
def height(lat, lon):
  try:
    path = f'data/hgt/{lat}/{lon}.png'
    return make_response({}, 200)
  except:
    return Response(status=404)

@app.route("/height/raster/<z>/<x>/<y>")
def raster(z, x, y):
  try:
    path = f'data/rgb/{z}/{x}/{y}.png'
  except:
    return Response(status=404)

if __name__ == '__main__':
  app.run(host=host, port=port, debug=True)


