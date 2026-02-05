"""
Raspberry Pi Art Display - Main Flask Application
"""
from flask import Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
from config_loader import get_config
from image_handler import ImageHandler
from todo_handler import TodoHandler
from time_service import TimeService
from presence_detector import PresenceDetector
from weather_service import WeatherService

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend')

# Configure CORS for local development
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize presence detector
config = get_config()
presence_detector = PresenceDetector(
    device_ip=config.get('device_ip'),
    scan_interval=config.get('presence.scan_interval'),
    scan_method=config.get('presence.scan_method')
)
# Start monitoring in background
presence_detector.start_monitoring()

# Initialize weather service singleton
_weather_service = None

def _get_weather_service():
    global _weather_service
    config = get_config()
    latitude = config.get('location.latitude')
    longitude = config.get('location.longitude')
    if latitude is None or longitude is None:
        return None
    temperature_unit = config.get('temperature_unit') or 'fahrenheit'
    if _weather_service is None or _weather_service.latitude != latitude or _weather_service.longitude != longitude or _weather_service.temperature_unit != temperature_unit:
        _weather_service = WeatherService(latitude, longitude, temperature_unit)
    return _weather_service

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check to verify server is running."""
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
    global _weather_service
    config = get_config()
    config.reload()
    _weather_service = None
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

# Time period endpoints
@app.route('/api/time-period', methods=['GET'])
def get_time_period():
    """Get current time period (day/night)."""
    config = get_config()
    day_start = config.get('time_periods.day_start')
    night_start = config.get('time_periods.night_start')

    try:
        service = TimeService(day_start, night_start)
        period_info = service.get_period_info()
        return jsonify(period_info), 200
    except ValueError as e:
        return jsonify({
            'error': 'Invalid time configuration',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Failed to determine time period',
            'message': str(e)
        }), 500

# Weather endpoint
@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get full weather data: current conditions, forecast, moon phase."""
    ws = _get_weather_service()
    if ws is None:
        return jsonify({
            'error': 'Location not configured',
            'message': 'Please set location.latitude and location.longitude in config'
        }), 400

    try:
        weather = ws.get_weather()
        return jsonify(weather), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch weather',
            'message': str(e)
        }), 500

# Morning info endpoint
@app.route('/api/morning-info', methods=['GET'])
def get_morning_info():
    """Get combined morning display information."""
    config = get_config()
    day_start = config.get('time_periods.day_start')
    night_start = config.get('time_periods.night_start')
    duration_minutes = config.get('morning_display.duration_minutes')
    morning_enabled = config.get('morning_display.enabled')

    try:
        from datetime import datetime
        service = TimeService(day_start, night_start)
        is_morning = morning_enabled and service.is_morning_hour(duration_minutes=duration_minutes)

        result = {
            'is_morning_hour': is_morning,
            'current_time': datetime.now().strftime('%H:%M'),
            'morning_enabled': morning_enabled
        }

        # Include weather if it's morning time
        if is_morning:
            ws = _get_weather_service()
            if ws is not None:
                result['weather'] = ws.get_weather()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to get morning info',
            'message': str(e)
        }), 500

# Presence detection endpoints
@app.route('/api/presence', methods=['GET'])
def get_presence():
    """Get device presence status."""
    try:
        status = presence_detector.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to get presence status',
            'message': str(e)
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
    # use_reloader with extra_files helps detect changes on WSL
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
