from flask import Flask, render_template, request, jsonify
from ml_model import predict_delivery_time, simulate_maps_distance
 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/distance', methods=['POST'])
def get_distance():
    data        = request.get_json(force=True)
    origin      = data.get('origin', '').strip()
    destination = data.get('destination', '').strip()
 
    if not origin or not destination:
        return jsonify({"success": False,
                        "error": "Both addresses are required."}), 400
 
    result = simulate_maps_distance(origin, destination)
    result["success"] = True
    return jsonify(result)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    result = predict_delivery_time(
        distance_km   = float(data.get('distance_km', 5.0)),
        prep_time_min = int(data.get('prep_time', 15)),
        traffic       = str(data.get('traffic', 'moderate')),
        weather       = str(data.get('weather', 'clear')),
        vehicle       = str(data.get('vehicle', 'bike')),
        time_of_day   = str(data.get('time_of_day', 'afternoon')),
    )
    result["success"] = True
    return jsonify(result)
 
if __name__ == '__main__':
    app.run(debug=True, port=8000)
