"""
API REST simple avec Flask.
"""

import os
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

API_VERSION = "1.0.0"


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "version": API_VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Bienvenue sur l'API CI/CD Demo",
        "version": API_VERSION,
        "endpoints": {
            "GET /": "Cette page",
            "GET /health": "Health check"
        }
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
