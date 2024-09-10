from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello, World!"})


@main_bp.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "App is running smoothly"})


@main_bp.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({"status": "App is monitoring by Prometheus"})
