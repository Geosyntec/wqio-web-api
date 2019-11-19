import json

from flask import Flask
from flask import request
from flask import jsonify

import pandas

from ros import ROS


app = Flask(__name__)


@app.route("/v1/echo", methods=["POST"])
def echo():
    return jsonify(request.json)


@app.route("/v1/as_arrays", methods=["POST"])
def as_arrays():
    data = pandas.read_json(request.get_json()).assign(
        censored=lambda df: df['censored'].astype(bool),
        values=lambda df: df['values'].astype(float)
    )
    imputed = ROS('values', 'censored', df=data)
    return jsonify(imputed)


@app.route("/v1/as_parts", methods=["POST"])
def as_parts():
    data = json.loads(request.get_json())
    values = map(float, [*data['censored'], *data['uncensored']])
    censored = [*[True]*len(data['censored']), *[False]*len(data['uncensored'])]
    imputed = ROS(values, censored)
    return jsonify(imputed)


if __name__ == "__main__":
    app.run()
