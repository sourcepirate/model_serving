import argparse
import joblib
from flask import Flask, jsonify
from flask import request

app = Flask("model_serving")


@app.post("/")
def index_route():

    data = request.json
    columns = app.config["columns"]
    model = app.config["model"]
    values = []

    for key in columns:
        try:
            values.append(data[key])
        except KeyError:
            return jsonify({
                "error": f"{key} missing"
            }), 500

    prediction = model.predict([values])

    return jsonify({"result": prediction.tolist()}), 200


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str)
    parser.add_argument("-c", "--columns", required=True, type=str)

    args = parser.parse_args()
    columns = args.columns.split(",")
    model = args.model

    app.config.update({"model": joblib.load(model), "columns": columns})

    app.run(host="0.0.0.0", port="4000", debug=False)
