import argparse
import joblib
import os
from flask import Flask, jsonify
from flask import request
from boto3 import session

app = Flask("model_serving")


ACCESS_ID = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
BUCKET_NAME = os.environ.get("BUCKET")
ENDPOINT = os.environ.get("ENDPOINT")

DATA_DIR = "/data"

# Initiate session
session = session.Session()
client = session.client(
    "s3",
    region_name="sgp1",
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key=SECRET_KEY,
)


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
            return jsonify({"error": f"{key} missing"}), 500

    prediction = model.predict([values])

    return jsonify({"result": prediction.tolist()}), 200


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str)
    parser.add_argument("-c", "--columns", required=True, type=str)
    

    args = parser.parse_args()
    columns = args.columns.split(",")
    model = args.model
    
    model_path = f"_models/{args.model}"
    data_path = f"{DATA_DIR}/{args.model}"
    

    client.download_file(BUCKET_NAME, model_path, data_path)

    app.config.update({"model": joblib.load(data_path), "columns": columns})

    app.run(host="0.0.0.0", port="4000", debug=False)
