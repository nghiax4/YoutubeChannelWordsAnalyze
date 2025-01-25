from flask import Flask, request, send_from_directory, jsonify

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