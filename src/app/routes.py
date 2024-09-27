import os
from flask import Flask, Blueprint, jsonify

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


@main_bp.route('/add', methods=['GET'])
def add():
    return jsonify({"status": "Add page"})


@main_bp.route('/favicon.ico')
def favicon():
    return '', 204


app = Flask(__name__)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_ENV') == 'development')
