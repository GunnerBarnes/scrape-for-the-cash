from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'streak'
COLLECTION_NAME = 'results'


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/results")
def results():
	connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
	collection = connection[DBS_NAME][COLLECTION_NAME]
	results = collection.find()
	json_results = []
	for result in results:
		json_results.append(result)
	json_results = json.dumps(json_results, default=json_util.default)
	connection.close()
	return json_results

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)