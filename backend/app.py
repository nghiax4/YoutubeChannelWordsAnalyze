from flask import Flask, request, send_from_directory, jsonify
import util

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Endpoint to get statistics of a YouTube channel.

    Returns:
        JSON: A JSON object containing the statistics.
        Example:
        {
            "numDifferentWords": 1000,
            "totalWordsSpoken": 50000,
            "wpmOverYear": [{"year": 2020, "wpm": 120}, {"year": 2021, "wpm": 130}],
            "wpmVsViews": [{"year": 2020, "wpm": 120, "views": 1000}, {"year": 2021, "wpm": 130, "views": 1500}],
            "sentimentOverYear": [{"year": 2020, "sentiment": 0.5}, {"year": 2021, "sentiment": 0.6}]
        }
    """
    channel_id = request.args.get('channel_id')
    if not channel_id:
        return jsonify({"error": "channel_id is required"}), 400

    transcripts_with_years = util.fetch_random_video_transcripts_with_years(channel_id)
    statistics = util.calculate_statistics(transcripts_with_years)
    return jsonify(statistics)

# Run the Flask app in debug mode (useful for development)
if __name__ == '__main__':
    app.run(debug=True)
