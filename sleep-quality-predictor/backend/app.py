from flask import Flask, request, jsonify
from flask_cors import CORS   # ADD THIS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)   # ADD THIS

model = pickle.load(open('sleep_model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    input_data = np.array([[
        float(data['sleep_duration']),
        float(data['stress']),
        float(data['exercise'])
    ]])

    prediction = model.predict(input_data)[0]

    return jsonify({"prediction": str(prediction)})

if __name__ == '__main__':
    app.run(debug=True)