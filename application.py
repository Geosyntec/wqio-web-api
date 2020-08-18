from flask import Flask
from flask import request
from flask import jsonify

import pandas

from ros import ROS


app = Flask(__name__)


@app.route("/echo", methods=["GET"])
def echo():
    return jsonify(request.json)


@app.route("/v1/as_arrays", methods=["POST"])
def as_arrays():
    data = pandas.DataFrame(request.get_json()).assign(
        censored=lambda df: df['censored'].astype(bool),
        values=lambda df: df['values'].astype(float)
    )
    imputed = ROS('values', 'censored', df=data)
    return jsonify(imputed)


@app.route("/v1/as_parts", methods=["POST"])
def as_parts():
    data = request.get_json()
    values = map(float, [*data['censored'], *data['uncensored']])
    censored = [*[True]*len(data['censored']), *[False]*len(data['uncensored'])]
    imputed = ROS(values, censored)
    return jsonify(imputed)


@app.route('/v1/add', methods=['POST'])
def add():
    data = request.get_json()
    return jsonify({
        'sum': data['a'] + data['b'],
        'a': data['a'],
        'b': data['b']
    })


if __name__ == "__main__":
    app.run()
