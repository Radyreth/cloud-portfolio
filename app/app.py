"""
API REST simple avec Flask.
3 routes pour demontrer une application realiste.
"""

import os
import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Version de l'API - utile pour le health check et le monitoring
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
            "GET /health": "Health check",
            "POST /calculate": "Calculatrice (envoyer JSON avec a, b, operation)",
            "GET /info": "Informations sur l'environnement",
            "GET /version": "Build metadata (git SHA, build date)"
        }
    }), 200


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Corps JSON requis"}), 400

    a = data.get("a")
    b = data.get("b")
    operation = data.get("operation")

    if a is None or b is None or operation is None:
        return jsonify({"error": "Champs requis : a, b, operation"}), 400

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return jsonify({"error": "a et b doivent etre des nombres"}), 400

    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }

    if operation not in operations:
        return jsonify({
            "error": f"Operation inconnue : {operation}",
            "operations_disponibles": list(operations.keys())
        }), 400

    result = operations[operation](a, b)

    if result is None:
        return jsonify({"error": "Division par zero impossible"}), 400

    return jsonify({
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }), 200


@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "environment": os.getenv("FLASK_ENV", "production"),
        "python_version": os.sys.version,
        "api_version": API_VERSION,
        "deployed_at": datetime.datetime.utcnow().isoformat()
    }), 200


@app.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": API_VERSION,
        "git_sha": os.getenv("GIT_SHA", "unknown"),
        "build_date": os.getenv("BUILD_DATE", "unknown"),
        "environment": os.getenv("FLASK_ENV", "production")
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
