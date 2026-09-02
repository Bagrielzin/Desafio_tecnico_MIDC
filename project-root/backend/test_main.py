import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# Atualize a criação do engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_record_success():
    response = client.post("/records", json={
        "employee_name": "Carlos Silva",
        "department": "Logística",
        "reference_date": "2026-09-02",
        "deliveries": 15,
        "note": "Entregas prioritárias"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["name"] == "Carlos Silva"
    assert data["deliveries"] == 15

def test_create_record_negative_deliveries():
    response = client.post("/records", json={
        "employee_name": "Ana",
        "department": "Vendas",
        "reference_date": "2026-09-02",
        "deliveries": -5 
    })
    assert response.status_code == 422

def test_get_records():
    response = client.get("/records")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_summary():
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "total_deliveries" in data
    assert "chart_data" in data