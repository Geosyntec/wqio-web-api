from flask import Flask
from flask import request
from flask import jsonify

from ros import ROS


app = Flask(__name__)


@app.route("/echo", methods=["POST"])
def echo():
    return jsonify(request.json)


@app.route("/as_arrays", methods=["POST"])
def as_arrays():
    request.args

    res = request.args.getlist("values", float)
    cen = request.args.getlist("values", bool)
    imputed = ROS(res, cen)
    return jsonify(imputed)


if __name__ == "__main__":
    app.run(debug=True)
