"""
Raspberry Pi Art Display - Main Flask Application
"""
from flask import Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
from config_loader import get_config
from image_handler import ImageHandler
from todo_handler import TodoHandler

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

# Image endpoints
@app.route('/api/images', methods=['GET'])
def list_images():
    """Get list of available images."""
    config = get_config()
    images_path = config.get('paths.images')

    try:
        handler = ImageHandler(images_path)
        images = handler.scan_images()
        return jsonify({
            'count': len(images),
            'images': images
        }), 200
    except FileNotFoundError as e:
        return jsonify({
            'error': 'Images directory not found',
            'message': str(e),
            'count': 0,
            'images': []
        }), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to scan images',
            'message': str(e),
            'count': 0,
            'images': []
        }), 500

@app.route('/api/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    """Serve an individual image file."""
    config = get_config()
    images_path = config.get('paths.images')

    try:
        handler = ImageHandler(images_path)
        image_path = handler.get_image_path(filename)
        return send_file(image_path, mimetype='image/jpeg')
    except FileNotFoundError:
        return jsonify({
            'error': 'Image not found',
            'filename': filename
        }), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to serve image',
            'message': str(e)
        }), 500

# TODO endpoints
@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get TODO list."""
    config = get_config()
    todo_path = config.get('paths.todos')

    try:
        handler = TodoHandler(todo_path)
        todos = handler.read_todos()
        return jsonify(todos), 200
    except FileNotFoundError as e:
        return jsonify({
            'error': 'TODO file not found',
            'message': str(e),
            'items': [],
            'count': 0
        }), 404
    except Exception as e:
        return jsonify({
            'error': 'Failed to read TODO file',
            'message': str(e),
            'items': [],
            'count': 0
        }), 500

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
