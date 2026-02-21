from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import verify_token

client = TestClient(app)

def test_admin_dashboard_override():
    # Definimos un comportamiento mock para la seguridad
    # ¡Saltamos la validación real!
    def mock_verify_token():
        return True

    # Inyectamos el mock en la app
    app.dependency_overrides[verify_token] = mock_verify_token

    # Hacemos la petición SIN token, y debería pasar (200)
    response = client.get("/admin/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Panel de Control Secreto"}
    
    # Limpiamos el override para no afectar otros tests
    app.dependency_overrides = {}

# 1. Test de un endpoint público
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Modularizada Corriendo"}

# 2. Test de creación de Item (Happy Path)
def test_create_item():
    payload = {"id": 1, "name": "Teclado Mecánico", "price": 150.0}
    response = client.post("/items/", json=payload)
    
    # Validamos respuesta HTTP
    assert response.status_code == 200
    
    # Validamos el contenido del JSON
    data = response.json()
    assert data["name"] == "Teclado Mecánico"
    assert data["price"] == 150.0
    assert "is_offer" in data  # Verificamos que el default se aplicó

# 3. Test de Validación (Edge Case)
def test_create_item_invalid_price():
    # Enviamos precio negativo
    payload = {"id": 2, "name": "Mouse", "price": -50} 
    response = client.post("/items/", json=payload)
    
    assert response.status_code == 422 # Unprocessable Entity