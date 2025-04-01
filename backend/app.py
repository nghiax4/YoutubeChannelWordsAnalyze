from flask import Flask, request, send_from_directory, jsonify
import util
import json
import os

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

# Serve the frontend (e.g., React/Vue/Angular app) from the 'dist' folder
@app.route('/')
def serve():
    """
    Serves the main frontend page (index.html) when the root URL is accessed.

    Returns:
    - The `index.html` file from the `dist` folder.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    """
    Endpoint to get statistics of a YouTube channel.

    Returns:
        JSON: A JSON object containing the statistics.
        Example is shown in sample_video_data.json
    """
    request_data = request.get_json()

    ANOTHERROOF_ID = "UCHEnZhUKjZSLYs3jJ0raKZA"
    MRBEAST_ID = 'UCX6OQ3DkcsbYNE6H8uQQuVA'

    if request_data['use_already_calculated']:
        if request_data["channel_id"] == ANOTHERROOF_ID:
            return jsonify(util.calculate_statistics(json.load(open(os.path.join("sample_data", "anotherroof_data.json")))))
        elif request_data["channel_id"] == MRBEAST_ID:
            return jsonify(util.calculate_statistics(json.load(open(os.path.join("sample_data", "mrbeast_data.json")))))
        

    return jsonify(util.calculate_statistics(util.fetch_video_data(request_data['channel_id'])))


# Run the Flask app in debug mode (useful for development)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
