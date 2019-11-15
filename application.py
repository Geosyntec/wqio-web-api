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
    values = request.args.getlist("values", float)
    censored = [bool(x) for x in request.args.getlist("censored", int)]
    imputed = ROS(values, censored)
    return jsonify(imputed)


@app.route("/as_parts", methods=["POST"])
def as_parts():
    uncen = request.args.getlist("uncensored", float)
    cen = request.args.getlist("censored", float)

    values = [*cen, *uncen]
    censored = [*[True for _ in cen], *[False for _ in uncen]]
    imputed = ROS(values, censored)
    return jsonify(imputed)


if __name__ == "__main__":
    app.run()
