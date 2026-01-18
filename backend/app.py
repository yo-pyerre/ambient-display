"""
Raspberry Pi Art Display - Main Flask Application
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from config_loader import get_config

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend')

# Configure CORS for local development
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running."""
    return jsonify({
        'status': 'healthy',
        'service': 'raspberry-pi-art-display'
    }), 200

# Configuration endpoint
@app.route('/api/config', methods=['GET'])
def get_configuration():
    """Get application configuration."""
    config = get_config()
    return jsonify(config.get()), 200

@app.route('/api/config/reload', methods=['POST'])
def reload_configuration():
    """Reload configuration from file."""
    config = get_config()
    config.reload()
    return jsonify({
        'status': 'reloaded',
        'config': config.get()
    }), 200

# Serve frontend static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files."""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Serve index.html for any unknown routes (SPA routing)
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Run the development server
    app.run(host='0.0.0.0', port=5000, debug=True)
