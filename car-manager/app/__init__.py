from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Enable CORS for specific origins
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Register blueprints
    from .controllers import bp 
    app.register_blueprint(bp)

    return app