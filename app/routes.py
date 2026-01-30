from flask import Blueprint, request, jsonify, render_template
from .services import process_webhook, get_latest_events

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    delivery_id = request.headers.get('X-GitHub-Delivery')
    
    if not event_type or not delivery_id:
        return jsonify({"error": "Missing GitHub headers"}), 400

    payload = request.json
    if not payload:
        return jsonify({"error": "Invalid JSON payload"}), 400

    result = process_webhook(event_type, payload, delivery_id)
    
    # Always return 200 to GitHub to avoid retries on logic ignores
    return jsonify(result), 200

@main_bp.route('/events', methods=['GET'])
def get_events():
    events = get_latest_events()
    return jsonify(events)
