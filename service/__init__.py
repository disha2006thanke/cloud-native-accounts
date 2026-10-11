
import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "development-only-change-me"
    )

    CORS(app)

    Talisman(
        app,
        force_https=os.environ.get("FORCE_HTTPS", "false").lower() == "true",
        content_security_policy=None,
    )

    from service.routes import accounts_bp
    app.register_blueprint(accounts_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app
