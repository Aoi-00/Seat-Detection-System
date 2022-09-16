from flask import Flask,jsonify
from flask_cors import CORS
import json
app = Flask(__name__)
# Allow CORS on specific route (/* for this case), and specific domain (localhost:3000 in this case)
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

@app.route("/")
def get_result():
    f = open('data.json')
    data = json.load(f)
    return jsonify({'seats': data['occupancy'], 'coord': data['coord']})


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True,)
# Choices: Redis (cache database), or multiprocessing (requires Semaphore, unnecessarily complicated)
