from flask import Flask, request, send_from_directory, jsonify
import util
import json

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Endpoint to get statistics of a YouTube channel.

    Returns:
        JSON: A JSON object containing the statistics.
        Example is shown in sample_video_data.json
    """

    # loads sample data
    with open(r'sample_video_data.json', 'r') as file:
        data = json.load(file)
    
    # return sample data
    return jsonify(util.calculate_statistics(data))


# Run the Flask app in debug mode (useful for development)
if __name__ == '__main__':
    app.run(debug=True)
