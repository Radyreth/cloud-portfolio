"""
Tests unitaires pour l'API Flask.
Chaque route est testee avec des cas normaux ET des cas d'erreur.
"""

import pytest
from app.app import app


@pytest.fixture
def client():
    """Cree un client de test Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# =============================================================================
# Tests de la route GET /
# =============================================================================
class TestHome:
    def test_home_returns_200(self, client):
        """La page d'accueil doit retourner un status 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_welcome_message(self, client):
        """La reponse doit contenir un message de bienvenue."""
        response = client.get("/")
        data = response.get_json()
        assert "message" in data
        assert "Bienvenue" in data["message"]

    def test_home_lists_endpoints(self, client):
        """La reponse doit lister les endpoints disponibles."""
        response = client.get("/")
        data = response.get_json()
        assert "endpoints" in data
        assert len(data["endpoints"]) > 0


# =============================================================================
# Tests de la route GET /health
# =============================================================================
class TestHealth:
    def test_health_returns_200(self, client):
        """Le health check doit retourner 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_is_healthy(self, client):
        """Le status doit etre 'healthy'."""
        response = client.get("/health")
        data = response.get_json()
        assert data["status"] == "healthy"

    def test_health_contains_version(self, client):
        """La reponse doit contenir la version de l'API."""
        response = client.get("/health")
        data = response.get_json()
        assert "version" in data

    def test_health_contains_timestamp(self, client):
        """La reponse doit contenir un timestamp."""
        response = client.get("/health")
        data = response.get_json()
        assert "timestamp" in data


# =============================================================================
# Tests de la route POST /calculate
# =============================================================================
class TestCalculate:
    def test_addition(self, client):
        """10 + 5 = 15"""
        response = client.post("/calculate", json={
            "a": 10, "b": 5, "operation": "add"
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 15

    def test_subtraction(self, client):
        """10 - 3 = 7"""
        response = client.post("/calculate", json={
            "a": 10, "b": 3, "operation": "subtract"
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 7

    def test_multiplication(self, client):
        """4 * 3 = 12"""
        response = client.post("/calculate", json={
            "a": 4, "b": 3, "operation": "multiply"
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 12

    def test_division(self, client):
        """10 / 2 = 5"""
        response = client.post("/calculate", json={
            "a": 10, "b": 2, "operation": "divide"
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 5.0

    def test_division_by_zero(self, client):
        """La division par zero doit retourner une erreur 400."""
        response = client.post("/calculate", json={
            "a": 10, "b": 0, "operation": "divide"
        })
        assert response.status_code == 400
        assert "zero" in response.get_json()["error"].lower()

    def test_invalid_operation(self, client):
        """Une operation inconnue doit retourner une erreur 400."""
        response = client.post("/calculate", json={
            "a": 10, "b": 5, "operation": "modulo"
        })
        assert response.status_code == 400
        assert "inconnue" in response.get_json()["error"].lower()

    def test_missing_fields(self, client):
        """Des champs manquants doivent retourner une erreur 400."""
        response = client.post("/calculate", json={
            "a": 10
        })
        assert response.status_code == 400

    def test_no_json_body(self, client):
        """Un appel sans body JSON doit retourner une erreur 400."""
        response = client.post("/calculate")
        assert response.status_code == 400

    def test_non_numeric_values(self, client):
        """Des valeurs non numeriques doivent retourner une erreur 400."""
        response = client.post("/calculate", json={
            "a": "abc", "b": 5, "operation": "add"
        })
        assert response.status_code == 400

    def test_float_calculation(self, client):
        """Les nombres a virgule doivent fonctionner."""
        response = client.post("/calculate", json={
            "a": 1.5, "b": 2.5, "operation": "add"
        })
        assert response.status_code == 200
        assert response.get_json()["result"] == 4.0


# =============================================================================
# Tests de la route GET /info
# =============================================================================
class TestInfo:
    def test_info_returns_200(self, client):
        """La route info doit retourner 200."""
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_contains_api_version(self, client):
        """La reponse doit contenir la version de l'API."""
        response = client.get("/info")
        data = response.get_json()
        assert "api_version" in data

    def test_info_contains_python_version(self, client):
        """La reponse doit contenir la version Python."""
        response = client.get("/info")
        data = response.get_json()
        assert "python_version" in data
